


################################################################
#######################    IMPORTS    ##########################
################################################################

from dataclasses import dataclass
from openai import OpenAI
from tqdm import tqdm

import subprocess
import threading
import time
import os

################################################################
#######################   VARIABLES   ##########################
################################################################

# tests = [1, 2, 10, 100, 1000, 10000]
# solutions = [0, 2, 17, 1060, 76127, 5736396]

reference_test = 1000000
reference_solution = 37550402023

fortran_files_path = f"fortran_runs"


prompt = """
Generate a complete Fortran 90 program that:
1. Reads an integer N from the user.
2. Finds all prime numbers from 1 to N.
3. Computes the sum of those prime numbers.
4. Do not print any output.
5. The fortran code should return only the sum as an integer and nothing else.

Return ONLY the Fortran code.
"""

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = f"https://api.openai.com/v1"

@dataclass
class ExecutionResult: # an object per execution to store the input, output, and execution time
    index: int
    input: str
    execution_time: float
    output: str

results = [] # where we will store the results of each execution



################################################################
#######################   FUNCTIONS   ##########################
################################################################



def init_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_base_url = f"https://api.openai.com/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url,
    )
    return client

def prompt_openai_client(client, prompt):
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )
    return response.output_text


def compile_fortran_code(fortran_code, index):
    source_file = os.path.join(fortran_files_path, f"prime_sum_{index}.f90")
    executable = os.path.join(fortran_files_path, f"prime_sum_{index}")

    with open(source_file, "w") as f:
        f.write(fortran_code)

    try:
        subprocess.run(
            ["gfortran", source_file, "-o", executable],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Compiled Fortran code saved to: {executable}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Compilation failed for index {index}")
        print(e.stderr)
        return False


def run_fortran_code(input_value, index):
    try:
        executable = os.path.join(fortran_files_path, f"prime_sum_{index}")
        start = time.perf_counter()
        result = subprocess.run(
            [executable],
            input=f"{input_value}\n",
            text=True,
            capture_output=True,
            check=True
        )

        elapsed = time.perf_counter() - start
        return result.stdout.strip(), elapsed
    except Exception as e:
        print(f"Error while executing Fortran code: {e}")
        return "Execution failed", 0.0



def print_results(_results):
    print(f"{'Index':<15}{'Input':<15}{'Time (s)':<15}{'Output'}")
    print("-" * 70)

    for r in _results:
        print(
            f"{r.index:<15}"
            f"{r.input:<15}"
            f"{r.execution_time:<15.4f}"
            f"{r.output}"
        )
    print("-" * 70)


################################################################
#########################   MAIN   #############################
################################################################


def main():

    for index in tqdm(range(1, 11), desc="Executions"):  # Change the range to run multiple executions
        print(f"----------------------------------------------------")
        print(f"Execution {index}")
        client = init_openai_client()
        fortran_code = prompt_openai_client(client, prompt)
        compiled = compile_fortran_code(fortran_code, index)


        if not compiled:
            execution_result = ExecutionResult(
                index=index,
                input=str(reference_test),
                execution_time=0.0,
                output="Compilation failed"
            )
            results.append(execution_result)
        else:
            output, elapsed = run_fortran_code(reference_test, index)
            execution_result = ExecutionResult(
                index=index,
                input=str(reference_test),
                execution_time=elapsed,
                output=output
            )
            results.append(execution_result)

    print(f"***************************************************")
    print(f"Reference input: {reference_test}")
    print(f"Reference output: {reference_solution}") 
    print(f"***************************************************")
    print(f"************   Methods evaluation   ***************")
    print(f"***************************************************")

    sorted_results = sorted(
        results,
        key=lambda r: (
            r.output != str(reference_solution),  # False comes before True
            float("inf") if r.execution_time == 0.0 else r.execution_time
        )
    )

    print_results(sorted_results)
    print(f"End of the process.")


    


if __name__ == "__main__":
    main()
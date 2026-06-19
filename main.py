


################################################################
#######################    IMPORTS    ##########################
################################################################

import time

from openai import OpenAI
import subprocess
import os

################################################################
#######################   VARIABLES   ##########################
################################################################

tests = [1, 2, 10, 100, 1000, 10000]
solutions = [0, 2, 17, 1060, 76127, 5736396]

reference_test = 1000000
reference_solution = 37550402023

fortran_files_path = f"fortran_runs"


prompt = """
Generate a complete Fortran 90 program that:
1. Reads an integer N from the user.
2. Finds all prime numbers from 1 to N.
3. Computes the sum of those prime numbers.
4. Prints the result.

Return ONLY the Fortran code.
"""

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = f"https://api.openai.com/v1"



################################################################
#######################   FUNCTIONS   ##########################
################################################################



def build_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_base_url = f"https://api.openai.com/v1"

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url,
    )
    return client

def use_openai_client(client, prompt):
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

    subprocess.run(
        ["gfortran", source_file, "-o", executable],
        check=True
    )
    print(f"Compiled Fortran code saved to: {executable}")


def run_fortran_code(input_value, index):
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

    print(f"Execution #{index}")
    print(f"Input: {input_value}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Runtime: {elapsed:.6f} seconds")

    return result.stdout.strip(), elapsed
################################################################
#########################   MAIN   #############################
################################################################


def main():
    client = build_openai_client()
    fortran_code = use_openai_client(client, prompt)
    compile_fortran_code(fortran_code, 1)
    run_fortran_code(reference_test, 1)
    # print("Generated Fortran code:")
    # print(fortran_code)


if __name__ == "__main__":
    main()
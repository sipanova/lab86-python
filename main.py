from openai import OpenAI
import os

tests = [1, 2, 10, 100, 1000, 10000]
solutions = [0, 2, 17, 1060, 76127, 5736396]

reference_test = 1000000
reference_solution = 37550402023


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

def main():
    client = build_openai_client()
    fortran_code = use_openai_client(client, prompt)
    print("Generated Fortran code:")
    print(fortran_code)


def compile_fortran_code(fortran_code, index):
    with open(f"prime_sum_{index}.f90", "w") as f:
        f.write(fortran_code)
    os.system(f"gfortran -o prime_sum_{index} prime_sum_{index}.f90")

def run_fortran_code(index):
    os.system(f"./prime_sum_{index}")

if __name__ == "__main__":
    main()
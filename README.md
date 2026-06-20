# Fortran Prime Sum Benchmark
For Lab86.

This project evaluates multiple AI-generated Fortran 90 implementations for calculating the sum of all prime numbers from `1` to `N`.

For each execution:

1. A Fortran program is generated using the OpenAI API.
2. The generated code is compiled with `gfortran`.
3. The executable is run using a reference input.
4. Execution time and output are recorded.
5. Results are ranked by correctness and performance.

## Requirements

- Docker
- OpenAI API Key

## Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Build

```bash
make build
```

## Run

```bash
make run
```

Or build and run in a single command:

```bash
make build-run
```

## Project Structure

```text
.
├── main.py
├── Dockerfile
├── Makefile
├── requirements.txt
├── .env
└── README.md
```

## Output

The program generates multiple Fortran solutions, compiles them, executes them with a fixed test value, and displays a ranked table containing:

- Execution index
- Input value
- Execution time
- Program output

Solutions producing the correct result are ranked before incorrect ones.
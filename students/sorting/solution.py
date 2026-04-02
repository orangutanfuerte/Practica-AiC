import argparse
import bz2
import json
import sys
from pathlib import Path
import math


def merge(A, m):
    n = len(A)
    B = [0] * n
    
    i = 0
    j = m+1
    # recorrem el array
    for k in range(n):
        if j >= n: # si j està fora de la mida de l'array
            B[k] = A[i]
            i += 1
        elif i > m:
            B[k] = A[j]
            j += 1
        elif A[i] < A[j]:
            B[k] = A[i]
            i += 1
        else:
            B[k] = A[j]
            j += 1
    return B


def mergesort(A, start, end):
    if start < end:
        m = math.floor((start+end)/2)
        mergesort(A, start, m)
        mergesort(A, m+1, end)
        A[start:end+1] = merge(A[start:end+1], m-start)
        #print(A, start, end, m)


def my_sort(arr):
    mergesort(arr, 0, len(arr)-1)
    return arr



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=Path,
        help="Path to input .bz2 file containing JSON array of integers",
    )
    args = parser.parse_args()

    # Load instance
    try:
        with bz2.open(args.input, "rb") as f:
            data = json.load(f)
    except Exception as e:
        sys.exit(f"Error loading instance: {e}")

    if not isinstance(data, list):
        sys.exit("Invalid instance format: expected a JSON list")

    sorted_arr = my_sort(data)

    # Print result to standard output (space-separated)
    print(*(sorted_arr))


if __name__ == "__main__":
    main()

import argparse
import bz2
import json
import sys
from pathlib import Path
import math

###
### MERGESORT
###

def merge(A, m):
    n = len(A)
    B = [0] * n
    
    i = 0
    j = m+1
    # recorrem l'array
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
    if start < end: # si és només 1, ho deixem igual
        m = math.floor((start+end)/2)
        if end-start > 1: # si és només 2, no cal
            mergesort(A, start, m)
            mergesort(A, m+1, end)
        A[start:end+1] = merge(A[start:end+1], m-start)


###
### INSERTIONSORT
###

def insertionsort(A):
    for i in range (1, len(A)):
        key = A[i]
        j = i - 1

        while j >= 0 and A[j] > key:
            A[j+1] = A[j]
            j -= 1

        A[j+1] = key


###
### PORTFOLIO
###

def mergeTwoArrays(A, B):
    i = j = 0
    result = []

    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1

    result.extend(A[i:])
    result.extend(B[j:])
    return result

ANALYSIS_LENGTH = 1000
CHCECK_STEP = 400

def my_sort(arr):

    # Primer analitzem a grans trets com és l'array
    if len(arr) > ANALYSIS_LENGTH:
        sortedScore = 0
        for i in range (1, len(arr)//CHCECK_STEP):
            if arr[i*CHCECK_STEP] >= arr[(i-1)*CHCECK_STEP]:
                sortedScore += 1
            else:
                sortedScore -= 1
        sortedScore /= (len(arr)//CHCECK_STEP-1)
        
        # Si està bastant ordenat o ivnersament ordenat
        if sortedScore >= 0.6:
            insertionsort(arr)
            return arr
        elif sortedScore <= -0.6:
            arr.reverse()
            insertionsort(arr)
            return arr

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

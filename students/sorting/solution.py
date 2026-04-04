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
### QUICKSORT
###
INSERTION_THRESHOLD = 32

def quicksort(A, low, high):

    while low < high:

        # arrays petits → insertion sort
        if high - low < INSERTION_THRESHOLD:
            insertion_sort(A, low, high)
            return

        pivot_index = choose_pivot(A, low, high)
        A[pivot_index], A[high] = A[high], A[pivot_index]

        p = partition(A, low, high)

        # recursió només al costat més petit
        if p - low < high - p:
            quicksort(A, low, p - 1)
            low = p + 1
        else:
            quicksort(A, p + 1, high)
            high = p - 1


def partition(A, low, high):
    pivot = A[high]
    i = low - 1

    for j in range(low, high):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]

    A[i+1], A[high] = A[high], A[i+1]
    return i + 1


def choose_pivot(A, low, high):
    mid = (low + high) // 2

    if A[low] > A[mid]:
        A[low], A[mid] = A[mid], A[low]

    if A[mid] > A[high]:
        A[mid], A[high] = A[high], A[mid]

    if A[low] > A[mid]:
        A[low], A[mid] = A[mid], A[low]

    return mid


def insertion_sort(A, low, high):
    for i in range(low + 1, high + 1):
        key = A[i]
        j = i - 1
        while j >= low and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key


###
### PORTFOLIO
###


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

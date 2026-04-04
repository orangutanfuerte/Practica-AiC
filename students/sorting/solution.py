import argparse
import bz2
import json
import sys
from pathlib import Path
import math

###
### MERGESORT
###

INSERTION_THRESHOLD = 32


def insertion_sort(A, left, right):
    for i in range(left + 1, right + 1):
        key = A[i]
        j = i - 1

        while j >= left and A[j] > key:
            A[j + 1] = A[j]
            j -= 1

        A[j + 1] = key


def merge(A, temp, left, mid, right):

    i = left
    j = mid + 1
    k = left

    while i <= mid and j <= right:
        if A[i] <= A[j]:
            temp[k] = A[i]
            i += 1
        else:
            temp[k] = A[j]
            j += 1
        k += 1

    while i <= mid:
        temp[k] = A[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = A[j]
        j += 1
        k += 1

    for i in range(left, right + 1):
        A[i] = temp[i]


def mergesort(A, temp, left, right):

    if right - left < INSERTION_THRESHOLD:
        insertion_sort(A, left, right)
        return

    mid = (left + right) // 2

    mergesort(A, temp, left, mid)
    mergesort(A, temp, mid + 1, right)

    # si ja està ordenat, evitem merge
    if A[mid] <= A[mid + 1]:
        return

    merge(A, temp, left, mid, right)


def merge_sort(A):
    temp = [0] * len(A)
    mergesort(A, temp, 0, len(A) - 1)

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

    merge_sort(arr)
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

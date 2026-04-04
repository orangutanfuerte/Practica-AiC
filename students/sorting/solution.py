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
### QUICKSORT
###

def choose_pivot(A, low, high):
    mid = (low + high) // 2

    if A[low] > A[mid]:
        A[low], A[mid] = A[mid], A[low]

    if A[mid] > A[high]:
        A[mid], A[high] = A[high], A[mid]

    if A[low] > A[mid]:
        A[low], A[mid] = A[mid], A[low]

    return mid

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


INSERTION_THRESHOLD = 24

def quicksort_iterative(arr, low, high):
    stack = [(low, high)]
    
    while stack:
        low, high = stack.pop()
        
        if high - low < INSERTION_THRESHOLD:
            for i in range(low + 1, high + 1):
                key = arr[i]
                j = i - 1
                while j >= low and arr[j] > key:
                    arr[j+1] = arr[j]
                    j -= 1
                arr[j+1] = key
            continue
        
        # choose_pivot inlinat
        mid = (low + high) // 2
        a, b, c = arr[low], arr[mid], arr[high]
        if a <= b <= c or c <= b <= a:
            pivot_idx = mid
        elif b <= a <= c or c <= a <= b:
            pivot_idx = low
        else:
            pivot_idx = high
        
        # partition inlinat
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        p = i + 1
        
        if p - low < high - p:
            stack.append((p + 1, high))
            stack.append((low, p - 1))
        else:
            stack.append((low, p - 1))
            stack.append((p + 1, high))

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


def insertionsort_reversed(A):
    for i in range(len(A)-2, -1, -1):
        key = A[i]
        j = i + 1

        while j < len(A) and A[j] < key:
            A[j-1] = A[j]
            j += 1

        A[j-1] = key

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

sliceLength = 5000000
analysisLength = 1000
checkStep = 400

def my_sort(arr):

    # Pas 2, analitzem a grans trets com és l'array
    # Cada 5? Cada 4? No sé, depèn de la mida del array?
    if len(arr) > analysisLength:
        sortedScore = 0
        for i in range (1, len(arr)//checkStep):
            # podem fer operador ternari
            # podem fer QUANT canvia un nombre
            if arr[i*checkStep] >= arr[(i-1)*checkStep]:
                sortedScore += 1
            else:
                sortedScore -= 1
        sortedScore /= (len(arr)//checkStep-1)
        
        if sortedScore >= 0.6: # un valor bastant alt, ja que l'InsertionSort pot ser molt ineficient
            insertionsort(arr)
            return arr
        elif sortedScore <= -0.6:
            arr.reverse()
            insertionsort(arr)
            #insertionsort_reversed(arr)
            return arr

                # Quicksort amb el pivot així més mitjà que troebm

        # Mergesort? CAL? Val la pena en algun cas? Potser si té menys de X mida
            # Segur que ha posat algun que té el pivot completament sense sentit
           #  Pitjor cas O(n²) — si els tests tenen arrays quasi-ordenats o amb molts duplicats, el quicksort es dispara tot i el pivot medià de tres. El mergesort sempre garanteix O(n log n).
        # Algun altre algoritme de sort? Em penso que en princpi no

    
    #quicksort(arr, 0, len(arr)-1)
    # 

    # Altres:
        # En iteratius gasten més espai però triguen menys en CPU (diria!) o sigui que ens interessa
            # Val la pena???? Preguntali al compa
        # Optimitzar al màxim els algoritmes (comprovacions abans de cridar)
            # Es pot???

    quicksort_iterative(arr, 0, len(arr)-1)
    # CAL?
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

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
    trio = [(A[low], low), (A[mid], mid), (A[high], high)]
    # Ordena per valor i agafa el del mig
    trio.sort(key=lambda x: x[0])
    return trio[1][1]  # retorna l'índex del pivot


def quicksort(A, low, high):
    if low < high:
        pivot_index = choose_pivot(A, low, high)
        # Mou el pivot a l'última posició abans de particionar
        A[pivot_index], A[high] = A[high], A[pivot_index]

        p = partition(A, low, high)
        quicksort(A, low, p-1)
        quicksort(A, p+1, high)


def partition(A, low, high):
    pivot = A[high]
    i = low - 1

    for j in range(low, high):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]

    A[i+1], A[high] = A[high], A[i+1]
    return i + 1


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

###
### PORTFOLIO
###

def my_sort(arr):
    # Pas 1, si es prou gran, dividir en dos o quatre

    # Pas 2, analitzem a grans trets com és l'array
    # Cada 5? Cada 4? No sé, depèn de la mida del array?
    if len(arr) > 1000:
        sortedScore = 0
        for i in range (1, len(arr)//5):
            # podem fer operador ternari
            # podem fer QUANT canvia un nombre
            if arr[i*5] >= arr[(i-1)*5]:
                sortedScore += 1
            else:
                sortedScore -= 1
        sortedScore /= len(arr)//5
        
        if sortedScore >= 0.8: # un valor bastant alt, ja que l'InsertionSort pot ser molt ineficient
            return insertionsort(arr)
        elif sortedScore <= -0.8:
            return insertionsort_reversed(arr)

                # Quicksort amb el pivot així més mitjà que troebm

        # Mergesort? CAL? Val la pena en algun cas? Potser si té menys de X mida
            # Segur que ha posat algun que té el pivot completament sense sentit
        # Algun altre algoritme de sort? Em penso que en princpi no

    
    # quicksort(arr, 0, len(arr)-1)
    # 

    # Altres:
        # En iteratius gasten més espai però triguen menys en CPU (diria!) o sigui que ens interessa
        # Optimitzar al màxim els algoritmes (comprovacions abans de cridar)
        # Partir l'algoritme en trossos perquè cadascun trobi el més adequat?

    #mergesort(arr, 0, len(arr)-1)
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

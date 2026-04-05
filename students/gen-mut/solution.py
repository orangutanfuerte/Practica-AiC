import argparse
import bz2
import sys
import math
from pathlib import Path


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def my_gen_mut_algorithm(points):
    indexed_points = list(enumerate(points))  # [(0, p0), (1, p1), (2, p2), ...]
    ordered_points_by_x = sorted(indexed_points, key=lambda ip: ip[1][0])
    ordered_points_by_y = sorted(indexed_points, key=lambda ip: ip[1][1])

    min_dist = dist(ordered_points_by_x[0][1], ordered_points_by_x[1][1])
    result_point0_index = ordered_points_by_x[0][0]
    result_point1_index = ordered_points_by_x[1][0]
    for i in range (0, len(ordered_points_by_x)-1):
        # Mirem els que estan en y més petita que distancia (binarysearch) i ho ordenem per x
        valor_y = ordered_points_by_x[i][1][1]
        primer = binary_search_lower(ordered_points_by_y, valor_y - min_dist)
        darrer = binary_search_upper(ordered_points_by_y, valor_y + min_dist)

        new_arr = ordered_points_by_y[primer:darrer+1]
        new_arr.sort(key=lambda ip: ip[1][0])
        # els ja vistitats (x menor que ordered_points_by_x[i] sen van fora directament, és a dir comencem per tal)
        # llegim el set en ordre de X
        # un cop superem la x, fora

        pos_i = binary_search_x(new_arr, ordered_points_by_x[i][1][0])
        for j in range(pos_i + 1, len(new_arr)):
            # Només cal comparar-lo amb els punts que tant en la x com la y estan dins la dist
            if new_arr[j][1][0] - ordered_points_by_x[i][1][0] > min_dist:
                break

            new_dist = dist(ordered_points_by_x[i][1], new_arr[j][1])
            if  new_dist < min_dist:
                min_dist=new_dist
                result_point0_index = ordered_points_by_x[i][0]
                result_point1_index = new_arr[j][0]
    
    return min_dist, [points[result_point0_index], points[result_point1_index]]


def binary_search_lower(arr, value):
    # Retorna el primer índex on arr[index][1][1] >= value
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid][1][1] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def binary_search_upper(arr, value):
    # Retorna el primer índex on arr[index][1][1] > value
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if arr[mid][1][1] > value:
            hi = mid - 1
        else:
            lo = mid
    return lo


def binary_search_x(arr, value):
    # Retorna el primer índex on arr[index][1][0] >= value
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid][1][0] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Input .bz2 file")
    args = parser.parse_args()

    try:
        with bz2.open(args.input, "rb") as f:
            content = f.read().decode("utf-8")
    except Exception as e:
        sys.exit(f"Error loading instance: {e}")

    points = []
    for line in content.splitlines():
        if line.strip():
            points.append(list(map(float, line.split())))

    if len(points) < 2:
        print(0.0)
    else:
        d, pair = my_gen_mut_algorithm(points)
        print(d)
        print(f"{pair[0][0]} {pair[0][1]}")
        print(f"{pair[1][0]} {pair[1][1]}")


if __name__ == "__main__":
    main()
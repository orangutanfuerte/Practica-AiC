import argparse
import bz2
import sys
import math
from pathlib import Path


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def my_gen_mut_algorithm(points):
    raise NotImplementedError("Implement Me!")


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

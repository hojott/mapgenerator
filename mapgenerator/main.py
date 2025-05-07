""" mapgenerator.main """

import sys

from .algorithms.fortunes.fortunes import FortunesAlgorithm
from .algorithms.fortunes.base_structs import Point

def load_points() -> list[Point]:
    """ Load points from sys arguments """
    points = []
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue

        if arg in ["-h", "--help"]:
            print_help()

        if not ',' in arg:
            print_help("Point coordinates must be split by \",\"")
        raw_point = arg.split(",")
        
        try:
            point = Point(
                int(raw_point[0]),
                int(raw_point[1])
            )
        except ValueError:
            print_help("Point coordinates must be integers!")
        
        points.append(point)

    if not points:
        print_help("No points added!")

    return points

def print_help(message: str = None):
    """ Print help message """
    if message is not None:
        print("mapgenerator: " + message)
    print("Usage: python -m mapgenerator [X,Y]...")
    print()
    print("Example: python -m mapgenerator 100,155 300,54")

    exit()

def main():

    points = load_points()

    fortunes = FortunesAlgorithm(size=(10,10), points=points)

    edges = fortunes.get_areas()

    print(edges)

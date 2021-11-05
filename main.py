#! /usr/bin/python

from graph import Graph, from_file
from argparse import ArgumentParser, Namespace
import matplotlib.pyplot as plt
import numpy as np

def main(args : Namespace):
    graph : Graph = from_file(args.filename)
    graph.vertices()

if __name__ == "__main__":
    parser : ArgumentParser = ArgumentParser()

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Shows extra information about the program running'
    )

    parser.add_argument(
        '-i', '--iterations',
        type=int,
        help='Amount of iterations to perform (default is 50)',
        default=50
    )

    parser.add_argument(
        '-t', '--temperature',
        type=float,
        help='Initial temperature (default is 100.0)',
        default=100.0
    )

    parser.add_argument(
        'filename',
        help='Source file to read the graph information from'
    )

    args : Namespace = parser.parse_args()
    main(args)

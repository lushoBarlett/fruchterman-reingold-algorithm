#! /usr/bin/python

from graph import Graph, Vertex, from_file
from argparse import ArgumentParser, Namespace
from geometry import PointSet, initialize_point_set
from render import render_graph
from fruchterman_reingold import force

def main(args : Namespace):
    graph : Graph = from_file(args.filename)

    vertices : set[Vertex] = graph.vertices()
    edges : list[tuple[Vertex, Vertex]] = graph.edges()

    point_set : PointSet = initialize_point_set(vertices)

    while args.iterations:

        render_graph(point_set, edges)

        for v in vertices:
            f = force(v, point_set, edges)
            print(v, f)

        args.iterations -= 1
    
    input()


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

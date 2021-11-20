#! /usr/bin/python

from graph import Graph, Vertex, from_file
from argparse import ArgumentParser, Namespace
from geometry import PointSet, initialize_point_set
from parameters import DELTA_TIME, TEMPERATURE_DESCENT
from render import render_graph
from fruchterman_reingold import force
from vector import Vector2D

def main(args : Namespace):
    graph : Graph = from_file(args.filename)

    vertices : set[Vertex] = graph.vertices()
    edges : list[tuple[Vertex, Vertex]] = graph.edges()

    point_set : PointSet = initialize_point_set(vertices)

    while args.iterations:

        render_graph(point_set, edges)

        for v in vertices:
            net_force : Vector2D = force(v, point_set, edges)

            if abs(net_force) > args.temperature:
                net_force = net_force.normalized() * args.temperature

            point_set.apply_force(v, net_force)

        point_set.update(DELTA_TIME)
        args.temperature *= TEMPERATURE_DESCENT
        args.iterations -= 1


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

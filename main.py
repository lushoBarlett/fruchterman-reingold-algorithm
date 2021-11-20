#! /usr/bin/python

from graph import Graph, Vertex, from_file
from argparse import ArgumentParser, Namespace
from geometry import PointSet, initialize_point_set
from render import render_graph
from fruchterman_reingold import force
from vector import Vector2D

# TODO: inline algorithm in main and implement it by phase
# in orden to have the verbose option make sense
# and to be more arquitecturaly accurate
# as the algorithm is the main concern of our program
def main(args : Namespace):
    graph : Graph = from_file(args.filename)

    vertices : set[Vertex] = graph.vertices()
    edges : list[tuple[Vertex, Vertex]] = graph.edges()

    point_set : PointSet = initialize_point_set(vertices)

    while args.iterations:

        render_graph(point_set, edges, 1 / args.refresh_rate)

        for v in vertices:
            net_force : Vector2D = force(v, point_set, edges, args.scatter, args.gforce)

            if abs(net_force) > args.temperature:
                net_force = net_force.normalized() * args.temperature

            point_set.apply_force(v, net_force)

        point_set.update(1 / args.refresh_rate)
        args.temperature *= args.damping
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
        help='Amount of iterations to perform (default is 100)',
        default=100
    )

    parser.add_argument(
        '-r', '--refresh-rate',
        type=int,
        help='Frames per second (default is 60)',
        default=60
    )

    parser.add_argument(
        '-t', '--temperature',
        type=float,
        help='Initial temperature (default is 100.0)',
        default=100.0
    )

    parser.add_argument(
        '-s', '--scatter',
        type=float,
        help='Scatter factor, how much the nodes repel (default is 0.5)',
        default=0.5
    )

    parser.add_argument(
        '-g', '--gforce',
        type=float,
        help='Global pull factor toward the center (default is 2.0)',
        default=2.0
    )

    parser.add_argument(
        '-d', '--damping',
        type=float,
        help='Percentage of temperature remaining through each iteration (default is 0.95)',
        default=0.95
    )

    parser.add_argument(
        'filename',
        help='Source file to read the graph information from'
    )

    args : Namespace = parser.parse_args()
    main(args)

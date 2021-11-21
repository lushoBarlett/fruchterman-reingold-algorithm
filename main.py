#! /usr/bin/python

from graph import Edge, Graph, Vertex, from_file
from argparse import ArgumentParser, Namespace
from geometry import PointSet, initialize_point_set
from render import render_graph
from math import sqrt
from parameters import BOTTOM_BOUND, DELTA_DISTANCE, LEFT_BOUND, RIGHT_BOUND, TOP_BOUND
from vector import Vector2D


def scattering(scatter : float, nodes : int) -> float:
    layout_area : float = (RIGHT_BOUND - LEFT_BOUND) * (TOP_BOUND - BOTTOM_BOUND)
    return scatter * sqrt(layout_area / nodes)


def attraction(pos1 : Vector2D, pos2 : Vector2D, k : float) -> Vector2D:
    diff = pos2 - pos1
    return diff.normalized() * abs(diff)**2 / k


def repulsion(pos1 : Vector2D, pos2 : Vector2D, k : float) -> Vector2D:
    diff = -(pos2 - pos1)

    if abs(diff) < DELTA_DISTANCE:
        return Vector2D.random()

    return diff.normalized() * k**2 / abs(diff)


def gravity(pos : Vector2D, gforce : float) -> Vector2D:
    middle : Vector2D = Vector2D((RIGHT_BOUND + LEFT_BOUND) / 2, (TOP_BOUND + BOTTOM_BOUND) / 2)
    diff = middle - pos
    return diff.normalized() * abs(diff)**2 * gforce


def main(args : Namespace):
    graph : Graph = from_file(args.filename)

    vertices : set[Vertex] = graph.vertices()
    edges : list[tuple[Vertex, Vertex]] = graph.edges()

    point_set : PointSet = initialize_point_set(vertices)

    k : float = scattering(args.scatter, len(vertices))

    delta_time : float = 1 / args.refresh_rate

    while args.iterations:

        render_graph(point_set, edges, delta_time)

        for v in vertices:
            net_force : Vector2D = Vector2D.zero()
            vpos = point_set.get_coord(v)

            outward : list[Edge] = [(a, b) for (a, b) in edges if a == v]
            for (_, w) in outward:
                wpos = point_set.get_coord(w)
                net_force += attraction(vpos, wpos, k)

            non_v : list[Vertex] = [x for x in point_set.labels if x != v]
            for w in non_v:
                wpos = point_set.get_coord(w)
                net_force += repulsion(vpos, wpos, k)

            net_force += gravity(vpos, args.gforce)

            if abs(net_force) > args.temperature:
                net_force = net_force.normalized() * args.temperature

            point_set.apply_force(v, net_force)

        point_set.update(delta_time)
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

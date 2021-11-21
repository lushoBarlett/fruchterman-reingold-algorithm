#! /usr/bin/python

from graph import Edge, Graph, Vertex, from_file
from argparse import ArgumentParser, Namespace
from geometry import PointSet, initialize_point_set
from math import sqrt
from parameters import BOTTOM_BOUND, DELTA_DISTANCE, LEFT_BOUND, RIGHT_BOUND, TOP_BOUND
from vector import Vector2D
import matplotlib.pyplot as pyplot


ForceTable : type = dict[Vertex, Vector2D]


active_verbose : bool = False


def onverbose(message):
    def decorator(function):
        def final(*args, **kwargs):
            if active_verbose:
                print(message)
            return function(*args, **kwargs)
        return final
    return decorator


@onverbose("*** Rendering new frame ***")
def render_graph(point_set : PointSet, biedges : list[Edge], delta_time : float) -> None:
    pyplot.clf()
    pyplot.xlim(LEFT_BOUND, RIGHT_BOUND)
    pyplot.ylim(BOTTOM_BOUND, TOP_BOUND)

    for (a, b) in biedges:
        va = point_set.get_coord(a)
        vb = point_set.get_coord(b)
        pyplot.plot([va.x, vb.x], [va.y, vb.y], color='brown')

    pyplot.scatter(point_set.xcoords(), point_set.ycoords())

    pyplot.show(block = False)
    pyplot.pause(delta_time)


@onverbose("@ Initializing force vectors")
def force_init(point_set : PointSet) -> ForceTable:
    forces : ForceTable = {}

    for v in point_set.labels:
        forces[v] = Vector2D.zero()

    return forces


@onverbose("@ Calculating attraction forces between adjacent nodes")
def attraction(point_set : PointSet, biedges : list[Edge], forces : ForceTable, k : float) -> None:

    def attraction_force(pos1 : Vector2D, pos2 : Vector2D) -> Vector2D:
        diff = pos2 - pos1
        return diff.normalized() * abs(diff)**2 / k

    for (a, b) in biedges:
        va = point_set.get_coord(a)
        vb = point_set.get_coord(b)

        forces[a] += attraction_force(va, vb)
        forces[b] += attraction_force(vb, va)


@onverbose("@ Calculating repulsion forces between all nodes")
def repulsion(point_set : PointSet, forces : ForceTable, k : float) -> None:

    def repulsion_force(pos1 : Vector2D, pos2 : Vector2D) -> Vector2D:
        diff = -(pos2 - pos1)

        if abs(diff) < DELTA_DISTANCE:
            return Vector2D.random()

        return diff.normalized() * k**2 / abs(diff)

    for a in point_set.labels:
        for b in point_set.labels:
            if a != b:
                va = point_set.get_coord(a)
                vb = point_set.get_coord(b)

                forces[a] += repulsion_force(va, vb)
                forces[b] += repulsion_force(vb, va)


@onverbose("@ Calculating gravity toward the center")
def gravity(point_set : PointSet, forces : ForceTable, gforce : float) -> None:

    def gravity(pos : Vector2D) -> Vector2D:
        middle : Vector2D = Vector2D((RIGHT_BOUND + LEFT_BOUND) / 2, (TOP_BOUND + BOTTOM_BOUND) / 2)
        diff = middle - pos
        return diff.normalized() * abs(diff)**2 * gforce

    for w in point_set.labels:
        vw = point_set.get_coord(w)
        forces[w] += gravity(vw)


@onverbose("@ Damping forces according to current temperature and updating temperature")
def damping(point_set : PointSet, forces : ForceTable, temperature : float, damping : float) -> float:
    for v in point_set.labels:
        if abs(forces[v]) > args.temperature:
            forces[v] = forces[v].normalized() * args.temperature

    return temperature * damping


@onverbose("@ Applying forces to all nodes")
def apply_forces(point_set : PointSet, forces : ForceTable, delta_time : float) -> None:
    for v in point_set.labels:
        point_set.apply_force(v, forces[v])

    point_set.update(delta_time)


def scattering(scatter : float, nodes : int) -> float:
    layout_area : float = (RIGHT_BOUND - LEFT_BOUND) * (TOP_BOUND - BOTTOM_BOUND)
    return scatter * sqrt(layout_area / nodes)


def main(args : Namespace):
    graph : Graph = from_file(args.filename)

    vertices : set[Vertex] = graph.vertices()
    biedges : list[Edge] = graph.biedges()

    point_set : PointSet = initialize_point_set(vertices)

    k : float = scattering(args.scatter, len(vertices))

    delta_time : float = 1 / args.refresh_rate

    global active_verbose
    active_verbose = args.verbose

    while args.iterations:

        render_graph(point_set, biedges, delta_time)

        net_forces : ForceTable = force_init(point_set)

        attraction(point_set, biedges, net_forces, k)
        repulsion(point_set, net_forces, k)
        gravity(point_set, net_forces, args.gforce)
        args.temperature = damping(point_set, net_forces, args.temperature, args.damping)

        apply_forces(point_set, net_forces, delta_time)

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

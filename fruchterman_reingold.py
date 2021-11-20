from math import sqrt
from geometry import PointSet
from graph import Edge, Vertex
from parameters import BOTTOM_BOUND, DELTA_DISTANCE, G_FORCE, LEFT_BOUND, RIGHT_BOUND, TOP_BOUND, SCATTER_FACTOR
from vector import Vector2D


def scattering(nodes : int) -> float:
    layout_area : float = (RIGHT_BOUND - LEFT_BOUND) * (TOP_BOUND - BOTTOM_BOUND)
    return SCATTER_FACTOR * sqrt(layout_area / nodes)


def attraction(pos1 : Vector2D, pos2 : Vector2D, k : float) -> Vector2D:
    diff = pos2 - pos1
    return diff.normalized() * abs(diff)**2 / k


def repulsion(pos1 : Vector2D, pos2 : Vector2D, k : float) -> Vector2D:
    diff = -(pos2 - pos1)

    if abs(diff) < DELTA_DISTANCE:
        return Vector2D.random()

    return diff.normalized() * k**2 / abs(diff)


def gravity(pos : Vector2D) -> Vector2D:
    middle : Vector2D = Vector2D((RIGHT_BOUND + LEFT_BOUND) / 2, (TOP_BOUND + BOTTOM_BOUND) / 2)
    diff = middle - pos
    return diff.normalized() * abs(diff)**2 * G_FORCE


def force(v : Vertex, point_set : PointSet, edges : list[Edge]) -> Vector2D:
    force = Vector2D.zero()
    vpos = point_set.get_coord(v)

    k : float = scattering(len(point_set.labels))

    outward : list[Edge] = [(a, b) for (a, b) in edges if a == v]
    for (_, w) in outward:
        wpos = point_set.get_coord(w)
        force += attraction(vpos, wpos, k)

    non_v : list[Vertex] = [x for x in point_set.labels if x != v]
    for w in non_v:
        wpos = point_set.get_coord(w)
        force += repulsion(vpos, wpos, k)

    force += gravity(vpos)

    return force

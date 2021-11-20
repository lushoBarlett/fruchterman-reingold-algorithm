from geometry import PointSet
from graph import Edge, Vertex
from vector import Vector2D


def attraction(pos1 : Vector2D, pos2 : Vector2D) -> float:
    return pos2 - pos1


def repulsion(pos1 : Vector2D, pos2 : Vector2D) -> float:
    return -(pos2 - pos1)


def force(v : Vertex, point_set : PointSet, edges : list[Edge]) -> Vector2D:
    force = Vector2D.zero()
    vpos = point_set.get_coord(v)

    outward = [(a, b) for (a, b) in edges if a == v]
    for (_, w) in outward:
        wpos = point_set.get_coord(w)
        force += attraction(vpos, wpos)

    non_v = [x for x in point_set.labels if x != v]
    for w in non_v:
        wpos = point_set.get_coord(w)
        force += repulsion(vpos, wpos)

    return force

from geometry import PointSet
from graph import Vertex
import matplotlib.pyplot as pyplot


def render_graph(point_set : PointSet, edges : tuple[Vertex, Vertex]) -> None:
    pyplot.clf()

    for (a, b) in edges:
        (ax, ay) = point_set.get_coord(a)
        (bx, by) = point_set.get_coord(b)
        pyplot.plot([ax, bx], [ay, by], color='brown')

    pyplot.scatter(point_set.xcoords(), point_set.ycoords())

    pyplot.show(block = False)
    pyplot.pause(0.001)

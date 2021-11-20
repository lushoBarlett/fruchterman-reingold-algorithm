from geometry import PointSet
from graph import Vertex
import matplotlib.pyplot as pyplot


def render_graph(point_set : PointSet, edges : tuple[Vertex, Vertex]) -> None:
    pyplot.clf()

    # ? FIXME: each edge gets painted twice
    for (a, b) in edges:
        va = point_set.get_coord(a)
        vb = point_set.get_coord(b)
        pyplot.plot([va.x, vb.x], [va.y, vb.y], color='brown')

    pyplot.scatter(point_set.xcoords(), point_set.ycoords())

    pyplot.show(block = False)
    pyplot.pause(0.001)

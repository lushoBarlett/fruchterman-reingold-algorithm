from geometry import PointSet
from graph import Vertex
import matplotlib.pyplot as pyplot

from parameters import BOTTOM_BOUND, LEFT_BOUND, RIGHT_BOUND, TOP_BOUND

def render_graph(point_set : PointSet, edges : tuple[Vertex, Vertex], delta_time : float) -> None:
    pyplot.clf()
    pyplot.xlim(LEFT_BOUND, RIGHT_BOUND)
    pyplot.ylim(BOTTOM_BOUND, TOP_BOUND)

    # ? FIXME: each edge gets painted twice
    for (a, b) in edges:
        va = point_set.get_coord(a)
        vb = point_set.get_coord(b)
        pyplot.plot([va.x, vb.x], [va.y, vb.y], color='brown')

    pyplot.scatter(point_set.xcoords(), point_set.ycoords())

    pyplot.show(block = False)
    pyplot.pause(delta_time)

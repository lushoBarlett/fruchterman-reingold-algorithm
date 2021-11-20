from random import random
from vector import Vector2D


class PointSet:
    def __init__(self, labels : set) -> None:
        self.labels : set = labels
        self.points : dict[any, Vector2D] = dict.fromkeys(labels, (0, 0))
    
    def set_coord(self, label : any, coordinates : Vector2D) -> None:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        self.points[label] = coordinates

    def get_coord(self, label : any) -> Vector2D:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        return self.points[label]

    def xcoords(self) -> list[float]:
        coords : list[Vector2D] = []
        for vector in self.points.values():
            coords.append(vector.x)
        return coords

    def ycoords(self) -> list[float]:
        coords : list[Vector2D] = []
        for vector in self.points.values():
            coords.append(vector.y)
        return coords


def initialize_point_set(labels : set) -> PointSet:
    point_set : PointSet = PointSet(labels)

    for label in labels:
        point_set.set_coord(label, Vector2D(random(), random()))

    return point_set

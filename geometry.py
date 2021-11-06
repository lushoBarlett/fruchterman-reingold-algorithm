from random import random


Coord : type = tuple[float, float]


class PointSet:
    def __init__(self, labels : set) -> None:
        self.points : dict[any, Coord] = dict.fromkeys(labels, (0, 0))
    
    def set_coord(self, label : any, coordinates : Coord) -> None:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        self.points[label] = coordinates

    def get_coord(self, label : any) -> Coord:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        return self.points[label]

    def xcoords(self) -> list[float]:
        coords : list[Coord] = []
        for (x, _) in self.points.values():
            coords.append(x)
        return coords

    def ycoords(self) -> list[float]:
        coords : list[Coord] = []
        for (_, y) in self.points.values():
            coords.append(y)
        return coords


def initialize_point_set(labels : set) -> PointSet:
    point_set : PointSet = PointSet(labels)

    for label in labels:
        point_set.set_coord(label, (random(), random()))

    return point_set

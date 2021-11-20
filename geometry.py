from vector import Vector2D


class Transform:
    def zero():
        return Transform(Vector2D.zero(), Vector2D.zero(), Vector2D.zero())

    def __init__(self, position : Vector2D, velocity : Vector2D, acceleration : Vector2D) -> None:
        self.position : Vector2D = position
        self.velocity : Vector2D = velocity
        self.acceleration : Vector2D = acceleration

    def update(self, delta_time : float) -> None:
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time


class PointSet:
    def __init__(self, labels : set) -> None:
        self.labels : set = labels
        self.points : dict[any, Transform] = {}
        for label in labels:
            self.points[label] = Transform.zero()
    
    def set_coord(self, label : any, coordinates : Vector2D) -> None:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        self.points[label].position = coordinates

    def get_coord(self, label : any) -> Vector2D:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        return self.points[label].position

    def apply_force(self, label: any, force: Vector2D) -> None:
        if label not in self.points:
            raise ValueError(f"Point '{label}' doesn't exist")

        self.points[label].acceleration = force

    def update(self, delta_time : float) -> None:
        for state in self.points.values():
            state.update(delta_time)

    def xcoords(self) -> list[float]:
        coords : list[Vector2D] = []
        for state in self.points.values():
            coords.append(state.position.x)
        return coords

    def ycoords(self) -> list[float]:
        coords : list[Vector2D] = []
        for state in self.points.values():
            coords.append(state.position.y)
        return coords


def initialize_point_set(labels : set) -> PointSet:
    point_set : PointSet = PointSet(labels)

    for label in labels:
        point_set.set_coord(label, Vector2D.random())

    return point_set

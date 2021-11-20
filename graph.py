Vertex : type = str
Edge : type = tuple[Vertex, Vertex]
AdjacencyList : type = dict[Vertex, set[Vertex]]


class Graph:
    def __init__(self) -> None:
        self.adjacency_list : AdjacencyList = {}
    
    def define_vertex(self, name : str) -> None:
        if name in self.adjacency_list:
            raise ValueError(f"Vertex '{name}' is already defined")

        self.adjacency_list[name] = []

    def define_edge(self, a : Vertex, b : Vertex):
        if a not in self.adjacency_list:
            raise ValueError(f"Vertex '{a}' is not defined")

        if b not in self.adjacency_list:
            raise ValueError(f"Vertex '{b}' is not defined")

        self.adjacency_list[a].append(b);
        self.adjacency_list[b].append(a);
    
    def vertices(self) -> set[Vertex]:
        return set(self.adjacency_list.keys())

    def edges(self) -> list[Edge]:
        edges : list[Edge] = []
        for a in self.adjacency_list:
            for b in self.adjacency_list[a]:
                edges.append((a, b))
        return edges


def from_file(filename : str) -> Graph:
    graph : Graph = Graph()
    
    with open(filename, "r") as file:
        vertices : int = int(file.readline().strip())
        while vertices:
            graph.define_vertex(file.readline().strip())
            vertices -= 1
        
        line : str = file.readline().strip()
        while line != "":
            (v1, _, v2) = line.partition(" ")
            graph.define_edge(v1, v2)
            line = file.readline().strip()
    
    return graph

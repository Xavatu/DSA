from collections import deque


class Vertex:
    def __init__(self, val: int):
        self.Value = val
        self.Hit = False

    def __repr__(self):
        return f"Vertex({self.Value}, {self.Hit})"


class SimpleGraph:
    def __init__(self, size: int):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex: list[Vertex | None] = [None] * size
        self._size = 0

    def AddVertex(self, v: int):
        if self._size == self.max_vertex:
            raise ValueError("Graph is full")
        empty_slot_index = self.vertex.index(None)
        self.vertex[empty_slot_index] = Vertex(v)
        self._size += 1

    def RemoveVertex(self, v: int):
        if not 0 <= v < self.max_vertex:
            raise IndexError("Index out of bounds")
        self.vertex[v] = None
        for i in range(self.max_vertex):
            self.m_adjacency[i][v] = 0
        self.m_adjacency[v] = [0 for _ in range(self.max_vertex)]

    def IsEdge(self, v1: int, v2: int) -> bool:
        if not 0 <= v1 < self.max_vertex:
            raise IndexError("Index out of bounds")
        if not 0 <= v2 < self.max_vertex:
            raise IndexError("Index out of bounds")
        return bool(self.m_adjacency[v1][v2] and self.m_adjacency[v2][v1])

    def AddEdge(self, v1: int, v2: int):
        if not 0 <= v1 < self.max_vertex:
            raise IndexError("Index out of bounds")
        if not 0 <= v2 < self.max_vertex:
            raise IndexError("Index out of bounds")
        if self.vertex[v1] is None:
            raise IndexError(f"No vertex with index {v1}")
        if self.vertex[v2] is None:
            raise IndexError(f"No vertex with index {v2}")
        self.m_adjacency[v1][v2] = 1
        self.m_adjacency[v2][v1] = 1

    def RemoveEdge(self, v1: int, v2: int):
        if not 0 <= v1 < self.max_vertex:
            raise IndexError("Index out of bounds")
        if not 0 <= v2 < self.max_vertex:
            raise IndexError("Index out of bounds")
        self.m_adjacency[v1][v2] = 0
        self.m_adjacency[v2][v1] = 0

    def _dfs(
        self,
        current: int,
        to: int,
        dq: deque,
        result: list[Vertex],
        append: bool,
    ) -> list[Vertex]:
        self.vertex[current].Hit = True
        if append:
            result.append(self.vertex[current])
            dq.append(current)
        if self.m_adjacency[current][to]:
            return result
        neighbours = [
            i for i in range(self.max_vertex) if self.m_adjacency[current][i]
        ]
        for neighbour in neighbours:
            if self.m_adjacency[neighbour][to]:
                self.vertex[neighbour].Hit = True
                result.append(self.vertex[neighbour])
                return result
        for neighbour in neighbours:
            if not self.vertex[neighbour].Hit:
                self._dfs(neighbour, to, dq, result, True)
        if not dq:
            return []
        current = dq.pop()
        self._dfs(current, to, dq, result, False)

    def DepthFirstSearch(self, VFrom: int, VTo: int) -> list[Vertex]:
        if self.vertex[VFrom] is None or self.vertex[VTo] is None:
            return []
        dq = deque()
        for el in self.vertex:
            if not el:
                continue
            el.Hit = False
        return self._dfs(VFrom, VTo, dq, [], True)

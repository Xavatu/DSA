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

    def _depth_first_search(self, vfrom: int, vto: int) -> deque[int]:
        cur = vfrom
        dq = deque((vfrom,))
        while dq:
            self.vertex[cur].Hit = True
            if self.m_adjacency[cur][vto]:
                self.vertex[vto].Hit = True
                dq.append(vto)
                return dq
            unvisited = False
            for i in range(self.max_vertex):
                if self.m_adjacency[cur][i] and not self.vertex[i].Hit:
                    cur = i
                    dq.append(i)
                    unvisited = True
                    break
            if not unvisited:
                dq.pop()
                cur = dq[-1] if dq else None
        return dq

    def DepthFirstSearch(self, VFrom: int, VTo: int) -> list[Vertex]:
        if self.vertex[VFrom] is None or self.vertex[VTo] is None:
            return []
        for el in self.vertex:
            if not el:
                continue
            el.Hit = False
        return [self.vertex[i] for i in self._depth_first_search(VFrom, VTo)]

    def _breadth_first_search(self, vfrom: int, vto: int) -> deque[int]:
        cur = vfrom
        dq = deque((vfrom,))
        prev = [-1] * self.max_vertex
        while True:
            self.vertex[cur].Hit = True
            if cur == vto:
                break
            unvisited = False
            for i in range(self.max_vertex):
                if self.m_adjacency[cur][i] and not self.vertex[i].Hit:
                    dq.append(i)
                    prev[i] = cur
                    self.vertex[i].Hit = True
                    unvisited = True
                    break
            if not dq:
                return dq
            if not unvisited:
                cur = dq.popleft()
        dq.clear()
        cur = vto
        while prev[cur] != -1:
            dq.appendleft(cur)
            cur = prev[cur]
        dq.appendleft(vfrom)
        return dq

    def BreadthFirstSearch(self, VFrom: int, VTo: int) -> list[Vertex]:
        if self.vertex[VFrom] is None or self.vertex[VTo] is None:
            return []
        for el in self.vertex:
            if not el:
                continue
            el.Hit = False
        return [self.vertex[i] for i in self._breadth_first_search(VFrom, VTo)]

    def _triangle_cycle_dfs(self, start: int):
        cur = start
        dq = deque((start,))
        while dq:
            self.vertex[cur].Hit = True
            if len(dq) == 3 and self.m_adjacency[cur][start]:
                return dq
            if len(dq) == 3:
                dq.pop()
                cur = dq[-1]
            unvisited = False
            for i in range(self.max_vertex):
                if not self.m_adjacency[cur][i]:
                    continue
                if not self.vertex[i].Hit:
                    cur = i
                    dq.append(i)
                    unvisited = True
                    break
            if unvisited:
                continue
            dq.pop()
            if not dq:
                continue
            cur = dq.pop()
        return dq

    def WeakVertices(self) -> list[Vertex]:
        sorted_vertices = sorted(
            [i for i in range(self.max_vertex)],
            key=lambda i: sum(self.m_adjacency[i]),
        )
        good_vertices = set()
        for i in range(self.max_vertex):
            v = sorted_vertices[i]
            if v in good_vertices:
                continue
            if sum(self.m_adjacency[v]) < 2:
                continue
            cycle = self._triangle_cycle_dfs(v)
            for el in cycle:
                good_vertices.add(el)
            for el in self.vertex:
                if not el:
                    continue
                el.Hit = False
        weak_vertices = set((i for i in range(self.max_vertex))) ^ good_vertices
        return [self.vertex[i] for i in weak_vertices if self.vertex[i]]

import pytest

from graph.simple_graph import Vertex, SimpleGraph


@pytest.fixture()
def get_empty_graph():
    return SimpleGraph(size=10)


#     6 — — — *
#     |       |
#     0 — 1 — 3
#     |   |   |
#     |   8   |
#     |   |   |
#     |   9 — 2
#     |       |
#     * — — — *


@pytest.fixture()
def get_graph():
    graph = SimpleGraph(size=10)
    graph.vertex = [
        Vertex(0),
        Vertex(1),
        Vertex(2),
        Vertex(3),
        None,
        None,
        Vertex(6),
        None,
        Vertex(8),
        Vertex(9),
    ]
    graph.m_adjacency = [
        [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    ]
    return graph


def test_add_vertex(get_empty_graph, get_graph):
    empty_graph = get_empty_graph
    empty_graph.AddVertex(0)
    assert empty_graph.vertex[0] is not None
    assert empty_graph.m_adjacency[0] == [0 for _ in range(10)]
    assert [empty_graph.m_adjacency[0][i] for i in range(10)] == [
        0 for _ in range(10)
    ]
    graph = get_graph
    graph.AddVertex(4)
    assert graph.vertex[4] is not None
    assert graph.m_adjacency[4] == [0 for _ in range(10)]
    assert [graph.m_adjacency[4][i] for i in range(10)] == [
        0 for _ in range(10)
    ]
    graph.AddVertex(5)
    graph.AddVertex(7)
    try:
        graph.AddVertex(8)
    except ValueError:
        assert True


def test_remove_vertex(get_graph):
    graph = get_graph
    graph.RemoveVertex(0)
    assert graph.vertex[0] is None
    assert graph.IsEdge(0, 1) is False
    assert graph.IsEdge(1, 0) is False
    assert graph.IsEdge(0, 2) is False
    assert graph.IsEdge(2, 0) is False
    assert graph.IsEdge(0, 6) is False
    assert graph.IsEdge(6, 0) is False


def test_is_edge(get_graph):
    graph = get_graph
    assert graph.IsEdge(0, 1) is True
    assert graph.IsEdge(1, 2) is False
    assert graph.IsEdge(2, 9) is True
    assert graph.IsEdge(9, 2) is True


def test_add_edge(get_graph):
    graph = get_graph
    assert graph.IsEdge(0, 8) is False
    graph.AddEdge(0, 8)
    assert graph.IsEdge(0, 8) is True


def test_remove_edge(get_graph):
    graph = get_graph
    assert graph.IsEdge(0, 1) is True
    graph.RemoveEdge(0, 1)
    assert graph.IsEdge(0, 1) is False
    assert graph.IsEdge(1, 0) is False
    assert graph.IsEdge(2, 9) is True
    graph.RemoveEdge(9, 2)
    assert graph.IsEdge(9, 2) is False
    assert graph.IsEdge(2, 9) is False


def test_dfs(get_graph):
    graph = get_graph
    assert [el.Value for el in graph.DepthFirstSearch(0, 1)] == [0]
    assert [el.Value for el in graph.DepthFirstSearch(0, 8)] == [0, 1]
    graph.AddVertex(4)
    assert [el.Value for el in graph.DepthFirstSearch(0, 4)] == []

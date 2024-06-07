from collections import deque


def _gen_bbst_tree_recursive(array, queue, max_depth):
    if not queue:
        return
    node_index, left, right, depth = queue.popleft()
    if node_index is not None:
        yield array[node_index]
        if left <= node_index - 1:
            queue.append(
                (
                    left + (node_index - left) // 2,
                    left,
                    node_index - 1,
                    depth + 1,
                )
            )
            max_depth = depth + 1
        elif depth < max_depth:
            queue.append((None,) * 4)
        if node_index + 1 <= right:
            queue.append(
                (
                    node_index + (right - node_index) // 2 + 1,
                    node_index + 1,
                    right,
                    depth + 1,
                )
            )
            max_depth = depth + 1
        elif depth < max_depth:
            queue.append((None,) * 4)
    else:
        yield None
    yield from _gen_bbst_tree_recursive(array, queue, max_depth)


def _gen_bbst_tree(array, queue):
    result = []
    max_depth = 0
    while queue:
        node_index, left, right, depth = queue.popleft()
        if node_index is None:
            result.append(None)
            continue
        result.append(array[node_index])
        if left <= node_index - 1:
            max_depth = depth + 1
            queue.append(
                (
                    left + (node_index - left) // 2,
                    left,
                    node_index - 1,
                    max_depth,
                )
            )
        elif depth < max_depth:
            queue.append((None,) * 4)
        if node_index + 1 <= right:
            max_depth = depth + 1
            queue.append(
                (
                    node_index + (right - node_index) // 2 + 1,
                    node_index + 1,
                    right,
                    max_depth,
                )
            )
        elif depth < max_depth:
            queue.append((None,) * 4)
    return result


def GenerateBBSTArray(a: list[int]) -> list[int]:
    sorted_a = sorted(a)
    queue = deque()
    queue.append((len(sorted_a) // 2, 0, len(sorted_a) - 1, 0))
    return [el for el in _gen_bbst_tree(sorted_a, queue) if el is not None]

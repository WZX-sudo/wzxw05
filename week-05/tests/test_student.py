"""可修改的小测试示例：另选输入，保留自己的预期与解释。

测试通过参数接收课程 fixture，--impl 才能切换候选实现。
不要直接 from operations import pop_last 绕过这个开关。
"""

import numpy as np

from challenges.work import apply_changes, compare_measurements, summarize_values


def test_my_pop_example(pop_last):
    items = [7, 4]

    result = pop_last(items)

    assert result == 4
    assert items == [7]


def test_my_four_item_pop_example(pop_last):
    items = [1, 2, 3, 4]

    result = pop_last(items)

    assert result == 4
    assert items == [1, 2, 3]


def test_my_positive_squares_example(positive_squares):
    values = [-3, 6, 7, 9]

    result = positive_squares(values)

    assert result == [36, 49, 81]
    assert values == [-3, 6, 7, 9]


def test_my_positive_square_map_without_positive_values(positive_square_map):
    record = {"a": -1, "b": -2, "c": -2, "d": -1}

    result = positive_square_map(record)

    assert result == {}
    assert record == {"a": -1, "b": -2, "c": -2, "d": -1}


def test_my_summarize_values_example():
    values = [2, 1, 3, 0, -1, 1, 3]

    result = summarize_values(values)

    assert result["unique"] == [2, 1, 3, 0, -1]
    assert result["counts"] == {2: 1, 3: 2, 1: 2, 0: 1, -1: 1}
    assert result["repeated"] == {1, 3}
    assert values == [2, 1, 3, 0, -1, 1, 3]


def test_my_apply_changes_example():
    original = {"a": 2, "b": 2, "c": 3}
    updates = [("b", 20), ("d", 4), ("b", 22)]
    removals = ["c", "missing"]

    result = apply_changes(original, updates, removals)

    assert result == {
        "record": {"a": 2, "b": 22, "d": 4},
        "changed": {"b", "c", "d"},
    }
    assert original == {"a": 2, "b": 2, "c": 3}
    assert updates == [("b", 20), ("d", 4), ("b", 22)]
    assert removals == ["c", "missing"]


def test_my_compare_measurements_example():
    ids = ["a", "b", "c", "d"]
    baseline = np.array([8, 20, 30, 40])
    current = np.array([11, 18, 30, 45])

    result = compare_measurements(ids, baseline, current, threshold=2)

    np.testing.assert_array_equal(result["delta"], [3, -2, 0, 5])
    assert result["alerts"] == ["a", "d"]
    assert result["normal"] == {"b": 18, "c": 30}
    assert ids == ["a", "b", "c", "d"]
    np.testing.assert_array_equal(baseline, [8, 20, 30, 40])
    np.testing.assert_array_equal(current, [11, 18, 30, 45])

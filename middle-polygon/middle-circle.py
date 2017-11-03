#!/usr/bin/env python3

import numpy as np
from numpy import pi, arctan
import matplotlib.pyplot as plt
import itertools


def get_rad(x, y):
    if y == 0:
        return 1/2 * pi if x >= 0 else 3/2 * pi
    elif y < 0:
        return pi + arctan(x / y)
    else:
        return arctan(x / y) if x > 0 else 2 * pi + arctan(x / y)


def split_polygon(polygon, num):
    result = {}
    rad_unit = 2 * pi / num
    for (x, y) in polygon:
        rad_index = get_rad(x, y) // rad_unit
        result[rad_index] = result.get(rad_index, [])
        result[rad_index].append((x, y))
    return result


def middle_point(point_list_1, point_list_2):
    min_distance = None
    result = None
    for (p1, p2) in itertools.product(point_list_1, point_list_2):
        x1, y1 = p1
        x2, y2 = p2
        distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        if min_distance is None or distance < min_distance:
            min_distance = distance
            result = (x1 + x2) / 2, (y1 + y2) / 2
    return result


def center_point(ploygon):
    (x, y) = zip(*ploygon)
    return 1.0 * sum(x) / len(x), 1.0 * sum(y) / len(y)


def shift(polygon, point):
    return [(p[0] + point[0], p[1] + point[1]) for p in polygon]

def shift_back(polygon, point):
    assert type(polygon) is list
    assert type(point) is tuple
    return [(p[0] - point[0], p[1] - point[1]) for p in polygon]


def get_middle_polygon(polygon_1, polygon_2, center=None, num=30):
    """
    Get middle polygon of two polygons.
    @param polygon_1: polygon 1 of type [(x1, y1), (x2, y2), ...]
    @param polygon_2: polygon 1 of type [(x1, y1), (x2, y2), ...]
    @param center: center of polygon
    @param num: split circle partitions
    """
    assert center is None or type(center) is tuple, "param center error"
    if center is None:
        center = center_point(polygon_1)
    polygon_1 = shift_back(polygon_1, center)
    polygon_2 = shift_back(polygon_2, center)
    sp1 = split_polygon(polygon_1, num)
    sp2 = split_polygon(polygon_2, num)
    results = []
    for i in range(num):
        s1, s2 = sp1.get(i), sp2.get(i)
        if s1 is None or s2 is None:
            pass
        else:
            results.append(middle_point(s1, s2))
    return shift(results, center)


def get_polygon(num, radius, diff_x, diff_y):
    """
    Generate a random polygon.
    """
    rad = np.random.rand(num) * 2 * np.pi
    points = zip(np.cos(rad) * radius, np.sin(rad) * radius)
    diff = zip((np.random.rand(num) - 0.5) * 2 * diff_x, (np.random.rand(num) - 0.5) * 2 * diff_y)
    points = [ (x + dx, y + dy) for (x, y), (dx, dy) in zip(points, diff)]
    points.sort(key=lambda x: get_rad(x[0], x[1]))
    return points


def plot_polygon(polygon, *args, **kwargs):
    polygon.append(polygon[0])
    x, y = zip(*polygon)
    plt.plot(x, y, *args, **kwargs)


if __name__ == '__main__':
    p1 = get_polygon(30, 20, 5, 15)
    p2 = get_polygon(20, 10, 3, 5)
    p3 = get_middle_polygon(p1, p2, num=30)

    plot_polygon(p1, 'b')
    plot_polygon(p2, 'r')
    plot_polygon(p3, 'g')
    plt.show()


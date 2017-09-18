from timeit import Timer
from functools import partial
import numpy as np

def match(c1, c2):
    return 0 if c1 == c2 else 1

def insert(c):
    return 1

def delete(c):
    return 1

def edit_distance(x, i, y, j):
    if i < 0 and j < 0: return 0
    if i < 0: return edit_distance(x, i, y, j-1) + delete(y[j])
    if j < 0: return edit_distance(x, i-1, y, j) + insert(x[i])
    match_cost = edit_distance(x, i-1, y, j-1) + match(x[i], y[j])
    insert_cost = edit_distance(x, i-1, y, j) + insert(x[i])
    delete_cost = edit_distance(x, i, y, j-1) + delete(y[j])

    return min(match_cost, insert_cost, delete_cost)

def edit_distance_memoize(x, i, y, j, cache={}):
    if (i, j) in cache: return cache[(i, j)]

    if i == -1 and j == -1: return 0
    if i == -1: return edit_distance_memoize(x, i, y, j-1) + delete(y[j])
    if j == -1: return edit_distance_memoize(x, i-1, y, j) + insert(x[i])
    match_cost = edit_distance_memoize(x, i-1, y, j-1) + match(x[i], y[j])
    insert_cost = edit_distance_memoize(x, i-1, y, j) + insert(x[i])
    delete_cost = edit_distance_memoize(x, i, y, j-1) + delete(y[j])

    value = min(match_cost, insert_cost, delete_cost)
    cache[(i, j)] = value
    # print i, j, cache[(i, j)]
    return value

def edit_distance_table(x, y):
    cost = np.zeros((len(x)+1, len(y)+1), dtype=np.uint32)

    # set up boundary conditions
    cost[0, 0] = 0

    for i in range(1, len(x)+1):
        cost[i, 0] = cost[i-1, 0] + delete(' ')

    for j in range(1, len(y)+1):
        cost[0, j] = cost[0, j-1] + insert(' ')

    # create table
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            match_cost = cost[i-1, j-1] + match(x[i-1], y[j-1])
            insert_cost = cost[i, j-1] + insert(y[i-1])
            delete_cost = cost[i-1, j] + delete(x[j-1])
            cost[i, j] = min(match_cost, insert_cost, delete_cost)

    return cost[-1, -1]

def edit_distance_table_reconstruct(x, y):
    cost = np.zeros((len(x)+1, len(y)+1), dtype=np.uint32)
    parent = np.zeros((len(x)+1, len(y)+1), dtype=np.int32)

    # set up boundary conditions
    cost[0, 0] = 0
    parent[0, 0] = -1

    for i in range(1, len(x)+1):
        cost[i, 0] = cost[i-1, 0] + delete(' ')
        parent[i, 0] = 2

    for j in range(1, len(y)+1):
        cost[0, j] = cost[0, j-1] + insert(' ')
        parent[0, j] = 1

    # create table
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            match_cost = cost[i-1, j-1] + match(x[i-1], y[j-1])
            insert_cost = cost[i, j-1] + insert(y[i-1])
            delete_cost = cost[i-1, j] + delete(x[j-1])
            choices = [match_cost, insert_cost, delete_cost]
            lowest = np.argmin(choices)
            cost[i, j] = choices[lowest]
            parent[i, j] = lowest

    print parent
    return cost[-1, -1]


def main():
    s2 = "you should not"
    s1 = "thou shalt not"

    # print edit_distance(s1, len(s1)-1, s2, len(s2)-1)
    # print edit_distance_memoize(s1, len(s1)-1, s2, len(s2)-1)
    # print edit_distance_table(s1, s2)
    print edit_distance_table_reconstruct(s1, s2)

    # print Timer(partial(edit_distance, s1, len(s1)-1, s2, len(s2)-1)).timeit(number=1)
    # print Timer(partial(edit_distance_memoize, s1, len(s1)-1, s2, len(s2)-1)).timeit(number=100)
    # print Timer(partial(edit_distance_table, s1, s2)).timeit(number=100)


if __name__ == "__main__":
    main()

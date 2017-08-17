import numpy as np

from IPython.display import clear_output
from ipywidgets import *

from pjdiagram import *
from step import StepExample

def parent(i): return (i-1)/2
def left(i): return 2*i+1
def right(i): return 2*i+2

def percolate_up(heap, startpos, pos):
    ppos = parent(pos)
    while pos > startpos and heap[ppos] < heap[pos]:
        # percolate value up by swapping current position with parent position
        heap[pos], heap[ppos] = heap[ppos], heap[pos]

        # move up one node
        pos = ppos
        ppos = parent(pos)

def heap_insert(heap, value):
    # add value to end
    heap.append(value)

    # move value up heap until the nodes below it are smaller
    percolate_up(heap, 0, len(heap)-1)

def percolate_down(heap, i, size):
    l = left(i)
    r = right(i)
    if l < size and heap[l] > heap[i]:
        max = l
    else:
        max = i

    if r < size and heap[r] > heap[l]:
        max = r

    # if left or right is greater than current index
    if max != i:
        # swap values
        heap[i], heap[max] = heap[max], heap[i]

        # continue downward
        percolate_down(heap, max, size)

def heap_pop(heap):
    # swap root with last value
    heap[0], heap[-1] = heap[-1], heap[0]

    # remove last value
    result = heap.pop()

    # restore heap properties
    for i in range(len(heap)):
        percolate_down(heap, 0, len(heap))

    return result

class InsertItemToHeapExample(StepExample):
    """
    Demonstrates inserting a new item into heap
    """
    def __init__(self, data):
        super(InsertItemToHeapExample, self).__init__()

        self.data = data
        self.index = len(self.data) - 1
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []

    def percoluate_up(self, lst, i, size):
        if i <= 0: return None
        p = parent(i)
        if lst[i] > lst[p]:
            lst[i], lst[p] = lst[p], lst[i]
            return (p, i)
        return None

    def drawCanvas(self, tree, highlight={}):
        with Canvas(400, 155) as ctx:
            draw_binary_tree(ctx, (200, 20), tree, highlight=highlight)

    def on_reset(self, b):
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []
        self.index = len(self.tree) - 1

        clear_output(wait=True)
        self.drawCanvas(self.tree, {self.index:True})

    def on_next(self, b):
        clear_output(wait=True)

        prev_tree = list(self.tree)
        indices = self.percoluate_up(self.tree, self.index, len(self.tree))
        if indices != None:
            next_index, swap_index = indices
            self.prev_trees.append(list(prev_tree))
            self.prev_indices.append(self.index)
            self.index = next_index
            highlight={next_index:True, swap_index:True}
        else:
            highlight = {self.index:True}

        self.drawCanvas(self.tree, highlight)

    def on_prev(self, b):
        clear_output(wait=True)

        swap_index = self.index
        if len(self.prev_trees) > 0:
            self.tree = self.prev_trees.pop()
            self.index = self.prev_indices.pop()
            highlight = {self.index:True, swap_index:True}
        else:
            highlight = {self.index:True}

        self.drawCanvas(self.tree, highlight)

    def __call__(self):
        self.drawCanvas(self.tree, {self.index:True})

        self.next_button.on_click(self.on_next)
        self.prev_button.on_click(self.on_prev)
        self.reset_button.on_click(self.on_reset)

        controls = HBox([self.prev_button, self.next_button, self.reset_button])
        display(controls)

class PercolateDownExample(StepExample):
    """
    Demonstrates percolating values down.
    """
    def __init__(self, data):
        super(PercolateDownExample, self).__init__()

        self.data = data
        self.tree = list(self.data)
        self.mode = 0
        self.current_node, self.next_node = self.select_swap(self.tree, 0)

    def select_swap(self, heap, i):
        l = left(i)
        r = right(i)
        if l < len(heap) and heap[l] > heap[i]:
            max = l
        else:
            max = i

        if r < len(heap) and heap[r] > heap[l]:
            max = r

        # if left or right is greater than current index
        if max != i:
            return (i, max)

        return (None, None)

    def drawCanvas(self, tree, highlight={}):
        with Canvas(400, 155) as ctx:
            draw_binary_tree(ctx, (200, 20), tree, highlight=highlight)

    def on_reset(self, b):
        self.tree = list(self.data)
        self.current_node, self.next_node = self.select_swap(self.tree, 0)
        self.mode = 0

        clear_output(wait=True)
        self.drawCanvas(self.tree, {self.current_node:True, self.next_node:True})

    def on_next(self, b):
        clear_output(wait=True)

        if self.mode % 2 == 0:
            prev_tree = list(self.tree)
            if self.current_node != None and self.next_node != None and \
                self.current_node != self.next_node:
                self.tree[self.current_node], self.tree[self.next_node] = \
                    self.tree[self.next_node], self.tree[self.current_node]
        else:
            if self.current_node != None and self.next_node != None:
                self.current_node = self.next_node
                self.current_node, self.next_node = \
                    self.select_swap(self.tree, self.current_node)

        self.mode += 1
        highlight={self.current_node:True, self.next_node:True}
        self.drawCanvas(self.tree, highlight)

    def __call__(self):
        self.drawCanvas(self.tree, {self.current_node:True, self.next_node:True})

        self.next_button.on_click(self.on_next)
        self.reset_button.on_click(self.on_reset)

        controls = HBox([self.next_button, self.reset_button])
        display(controls)

def binary_heap_allocation_example():
    def f(size):
        with Canvas(650, 250) as ctx:
            array_contents = list(contents[:size]) + [0 for i in range(len(contents) - size)]
            draw_array(ctx, (1, 1), array_contents)
            draw_binary_tree(ctx, (325, 50), contents[:size], xdistance=20)

    contents = np.random.randint(100, size=31)
    interact(f, size=(1, len(contents)))

def insert_item_to_heap_example(data):
    InsertItemToHeapExample(data)()

def percolate_down_example(data):
    PercolateDownExample(data)()

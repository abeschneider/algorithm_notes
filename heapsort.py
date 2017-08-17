import numpy as np

from IPython.display import clear_output
from ipywidgets import *

from pjdiagram import *
from step import StepExample

from heap import parent, left, right, percolate_down

def build_heap(lst):
    # start at bottom non-leaf nodes and work up for each node
    nonleaf_nodes = len(lst)/2
    for i in range(nonleaf_nodes-1, -1, -1):
        percolate_down(lst, i, len(lst))

class BuildHeapExample(StepExample):
    def __init__(self):
        super(BuildHeapExample, self).__init__()

        self.data = np.random.randint(100, size=15)
        self.tree = list(self.data)
        self.nonleaf_nodes = len(self.tree)/2
        self.index = self.nonleaf_nodes-1
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []

    def drawCanvas(self, highlight):
        with Canvas(400, 155) as ctx:
            draw_binary_tree(ctx, (200, 20), self.tree, highlight=highlight)

    def on_reset(self, b):
        self.tree = np.random.randint(100, size=15)
        self.prev_trees = []
        self.prev_indices = []
        self.index = self.nonleaf_nodes-1

        clear_output(wait=True)
        highlight={self.index:True}
        self.drawCanvas(highlight)

    def on_next(self, b):
        clear_output(wait=True)

        highlight={self.index:True}
        if self.index >= 0:
            prev_tree = list(self.tree)
            self.prev_trees.append(list(prev_tree))
            self.prev_indices.append(self.index)
            percolate_down(self.tree, self.index, len(self.tree))
            self.index -= 1

        self.drawCanvas(highlight)

    def on_prev(self, b):
        clear_output(wait=True)

        if len(self.prev_trees) > 0:
            self.tree = self.prev_trees.pop()
            self.index = self.prev_indices.pop()

        self.drawCanvas({self.index:True})

    def __call__(self):
        self.drawCanvas({self.index:True})

        self.next_button.on_click(self.on_next)
        self.prev_button.on_click(self.on_prev)
        self.reset_button.on_click(self.on_reset)

        controls = HBox([self.prev_button, self.next_button, self.reset_button])
        display(controls)

class HeapSortExample(StepExample):
    def __init__(self):
        super(HeapSortExample, self).__init__()

        self.data = np.random.randint(100, size=15)
        build_heap(self.data)

        self.tree = list(self.data)
        self.index = len(self.tree) - 1
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []

    def drawCanvas(self, highlight):
        with Canvas(400, 200) as ctx:
            draw_array(ctx, (1, 1), self.tree)
            draw_binary_tree(ctx, (200, 50), self.tree, highlight=highlight)

    def on_reset(self, b):
        self.tree = np.random.randint(100, size=15)
        self.prev_trees = []
        self.prev_indices = []
        self.index = len(self.tree)-1

        clear_output(wait=True)
        self.drawCanvas({self.index:True})

    def on_next(self, b):
        clear_output(wait=True)

        highlight={self.index:True}
        if self.index >= 0:
            prev_tree = list(self.tree)
            self.prev_trees.append(list(prev_tree))
            self.prev_indices.append(self.index)

            self.tree[0], self.tree[self.index] = self.tree[self.index], self.tree[0]
            percolate_down(self.tree, 0, self.index)
            self.index -= 1

        self.drawCanvas(highlight)

    def on_prev(self, b):
        clear_output(wait=True)

        if len(self.prev_trees) > 0:
            self.tree = self.prev_trees.pop()
            self.index = self.prev_indices.pop()

        self.drawCanvas({self.index:True})

    def __call__(self):
        self.drawCanvas({self.index:True})

        self.next_button.on_click(self.on_next)
        self.prev_button.on_click(self.on_prev)
        self.reset_button.on_click(self.on_reset)

        controls = HBox([self.prev_button, self.next_button, self.reset_button])
        display(controls)

def build_heap_example():
    BuildHeapExample()()

def heap_sort_example():
    HeapSortExample()()

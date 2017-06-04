import numpy as np

from IPython.display import clear_output
from pjdiagram import *
from ipywidgets import *

def parent(i): return i/2
def left(i): return 2*i+1
def right(i): return 2*i+2

def heapify(lst, i, size):
    """
    precondition: left and right subtrees are heaps
    postcondition: makes tree at $i$ a heap
    """
    l = left(i)
    r = right(i)

    # if the left child is larger than parent, set largest to left
    if l < size and lst[l] > lst[i]:
        largest = l
    else:
        largest = i

    # if the right child is greater than the current largest, set largest
    # to right
    if r < size and lst[r] > lst[largest]:
        largest = r

    # if the parent isn't the largest, make it the largest, and
    # call heapify on the the child node that was altered
    if largest != i:
        lst[i], lst[largest] = lst[largest], lst[i]
        heapify(lst, largest, size)

def build_heap(lst):
    # start at bottom non-leaf nodes and work up for each node
    nonleaf_nodes = len(lst)/2
    for i in range(nonleaf_nodes-1, -1, -1):
        heapify(lst, i, len(lst))

def example1():
    def f(size):
        with Canvas(650, 250) as ctx:
            array_contents = list(contents[:size]) + [0 for i in range(len(contents) - size)]
            draw_array(ctx, (1, 1), array_contents)
            draw_binary_tree(ctx, (325, 50), contents[:size], xdistance=20)

    contents = np.random.randint(100, size=31)
    interact(f, size=(1, len(contents)))

class StepExample(object):
    def __init__(self):
        self.reset_button = widgets.Button(
            description='',
            disabled=False,
            button_style='',
            tooltip='reset',
            layout=Layout(width='80px', height='40px'),
            icon='fa-refresh'
        )

        self.prev_button = widgets.Button(
            description='',
            disabled=False,
            button_style='',
            tooltip='go backward',
            layout=Layout(width='80px', height='40px'),
            icon='fa-chevron-left'
        )

        self.next_button = widgets.Button(
            description='',
            disabled=False,
            button_style='',
            tooltip='go forward',
            layout=Layout(width='80px', height='40px'),
            icon='fa-chevron-right'
        )

class Example2(StepExample):
    def __init__(self):
        super(Example2, self).__init__()

        self.data = [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]
        self.index = 1
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []

    def heapify(self, lst, i, size):
        """
        Modified version of heapify that can be used interactively.
        """
        l = left(i)
        r = right(i)

        # if the left child is larger than parent, set largest to left
        if l < size and lst[l] > lst[i]:
            largest = l
        else:
            largest = i

        # if the right child is greater than the current largest, set largest
        # to right
        if r < size and lst[r] > lst[largest]:
            largest = r

        # if the parent isn't the largest, make it the largest, and
        # call heapify on the the child node that was altered
        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            prev_index = i
            i = largest
            return (i, prev_index)
        else:
            return None

    def drawCanvas(self, tree, highlight={}):
        with Canvas(400, 155) as ctx:
            draw_binary_tree(ctx, (200, 20), tree, highlight=highlight)

    def on_reset(self, b):
        self.tree = list(self.data)
        self.prev_trees = []
        self.prev_indices = []
        self.index = 1

        clear_output(wait=True)
        self.drawCanvas(self.tree, {self.index:True})

    def on_next(self, b):
        clear_output(wait=True)

        prev_tree = list(self.tree)
        indices = self.heapify(self.tree, self.index, len(self.tree))
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

class Example3(StepExample):
    def __init__(self):
        super(Example3, self).__init__()

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
        self.drawCanvas({index:True})

    def on_next(self, b):
        clear_output(wait=True)

        highlight={self.index:True}
        if self.index >= 0:
            prev_tree = list(self.tree)
            self.prev_trees.append(list(prev_tree))
            self.prev_indices.append(self.index)
            heapify(self.tree, self.index, len(self.tree))
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

class Example4(StepExample):
    def __init__(self):
        super(Example4, self).__init__()

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
            heapify(self.tree, 0, self.index)
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


def example2():
    Example2()()

def example3():
    Example3()()

def example4():
    Example4()()

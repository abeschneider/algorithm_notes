import numpy as np

from IPython.display import clear_output
from pjdiagram import *
from ipywidgets import *

def merge(left, right):
    i = j = 0

    result = []
    while i < len(left) or j < len(right):
        if i >= len(left):
            result.append(right[j])
            j += 1
        elif j >= len(right):
            result.append(left[i])
            i += 1
        elif left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    return result

def mergesort(lst):
    """
    Iterative version of `mergesort` for demo purposes.
    """
    result = []
    i = 0
    while i < len(lst):
        left = lst[i] if isinstance(lst[i], list) else [lst[i]]
        i += 1
        right = lst[i] if isinstance(lst[i], list) else [lst[i]]
        i += 1
        if i+1 == len(lst):
            right.extend(lst[i] if isinstance(lst[i], list) else [lst[i]])
            i += 1

        result.append(merge(left, right))
    return result

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

def flatten(lst):
    if isinstance(lst[0], list):
        return [item for sublst in lst for item in sublst]
    return lst

class Example1(StepExample):
    def __init__(self, lst):
        super(Example1, self).__init__()

        # self.data = [5, 2, 1, 20, 10, 3, 4, 80]
        self.original = lst
        self.data = list(self.original)
        self.prev_data = []

    def drawCanvas(self, highlight={}):
        sizes = [len(item) if isinstance(item, list) else 1 for item in self.data]
        indices = [0] + list(np.cumsum(sizes))
        indices.pop(-1)

        data = flatten(self.data)
        cell_width = 20
        cell_height = 20
        with Canvas(200, 55) as ctx:
            draw_array(ctx, (1, 1), data)
            for j, i in enumerate(indices):
                ctx.rectangle(1 + i*cell_width, 1, sizes[j]*cell_width, cell_height)

            ctx.set_source_rgb(1, 0, 0)
            ctx.set_line_width(4.0)
            ctx.stroke()

    def on_reset(self, b):
        self.data = list(self.original)
        self.prev_data = []

        clear_output(wait=True)
        self.drawCanvas()

    def on_next(self, b):
        clear_output(wait=True)

        self.prev_data.append(list(self.data))
        self.data = mergesort(self.data)
        self.drawCanvas()

    def on_prev(self, b):
        if len(self.prev_data) > 0:
            clear_output(wait=True)
            self.data = self.prev_data.pop()
            self.drawCanvas()

    def __call__(self):
        self.drawCanvas()

        self.next_button.on_click(self.on_next)
        self.prev_button.on_click(self.on_prev)
        self.reset_button.on_click(self.on_reset)

        controls = HBox([self.prev_button, self.next_button, self.reset_button])
        display(controls)

def example1(lst):
    Example1(lst)()

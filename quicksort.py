import numpy as np

from IPython.display import clear_output
from ipywidgets import *

from step import StepExample
from pjdiagram import *

import math

def drawArrowHead(ctx, x, y, x2, y2, arrow_length, arrow_degrees):
    dx = x2 - x
    dy = y2 - y
    angle = math.atan2(dy, dx)

    hx = x2 - arrow_length * math.cos(angle - arrow_degrees)
    hy = y2 - arrow_length * math.sin(angle - arrow_degrees)
    hx2 = x2 - arrow_length * math.cos(angle + arrow_degrees)
    hy2 = y2 - arrow_length * math.sin(angle + arrow_degrees)

    ctx.move_to(x2, y2)
    ctx.line_to(hx, hy)
    ctx.line_to(hx2, hy2)
    ctx.close_path()
    ctx.stroke_preserve()
    ctx.fill()

    sx = x2 - arrow_length * math.cos(angle)
    sy = y2 - arrow_length * math.sin(angle)
    ctx.move_to(sx, sy)
    ctx.line_to(x, y)
    ctx.stroke()

def draw_partition(ctx, pos, contents, pivot, swapA, swapB, cell_width=20, cell_height=20):
    draw_array(ctx, pos, contents, highlight={swapA:True, swapB:True})

    ax = cell_width*pivot + cell_width/2.0 + pos[0]
    ay = cell_height + pos[1] + 5
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(1.0)
    drawArrowHead(ctx, ax, ay + 15, ax, ay, 10, math.radians(25))

def partition(lst, start, end):
    pivot = lst[start]
    first = start + 1
    last = end
    while first <= last:
        # find the next element that is less than pivot
        while first <= last and lst[first] <= pivot:
            first += 1

        # find the next element that is greater than pivot
        while last >= first and lst[last] > pivot:
            last -= 1

        # and swap their values
        if first < last:
            lst[first], lst[last] = lst[last], lst[first]

    lst[start], lst[last] = lst[last], lst[start]
    return last

class PartitionExample(StepExample):
    def __init__(self, lst, pivotIndex):
        super(PartitionExample, self).__init__()

        self.original = lst
        self.data = list(self.original)
        self.pivot = lst[pivotIndex]
        self.first = 0
        self.last = len(self.data) - 1
        self.mode = 0

    def drawCanvas(self, left=-1, right=-1):
        with Canvas(600, 80) as ctx:
            pivotIndex = self.data.index(self.pivot)
            draw_partition(ctx, (1, 1), self.data, pivotIndex, left, right)

    def on_reset(self, b):
        self.data = list(self.original)
        self.mode = 0
        self.first = 0
        self.last = len(self.data) - 1

        clear_output(wait=True)
        self.drawCanvas()

    def on_next(self, b):
        clear_output(wait=True)

        if self.mode % 2 == 0:
            while self.first < len(self.data)-1 and self.data[self.first] < self.pivot:
                self.first += 1

            # find the next element that is greater than pivot
            while self.last > 0 and self.data[self.last] > self.pivot:
                self.last -= 1
        else:
            self.data[self.first], self.data[self.last] = self.data[self.last], self.data[self.first]

        self.drawCanvas(self.first, self.last)
        self.mode += 1

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

def partition_example(lst, pivotIndex):
    return PartitionExample(lst, pivotIndex)()

class QuicksortExample(StepExample):
    def __init__(self, lst):
        super(QuicksortExample, self).__init__()

        self.original = lst
        self.data = list(self.original)

        self.stack = []
        self.stack.append((0, len(self.data)-1))


    def drawCanvas(self, left=-1, right=-1, partition=-1):
        with Canvas(600, 80) as ctx:
            draw_partition(ctx, (1, 1), self.data, partition, left, right)

    def on_reset(self, b):
        self.data = list(self.original)
        self.mode = 0
        self.first = 0
        self.last = len(self.data) - 1

        clear_output(wait=True)
        self.drawCanvas()

    def on_next(self, b):
        clear_output(wait=True)

        # p = partition(lst, first, last)
        first, last = self.stack.pop(0)
        p = partition(self.data, first, last)

        print(self.data)
        print(p, first, last)
        if (p - 1) - first > 1:
            self.stack.append((first, p-1))

        if last - (p+1) > 1:
            self.stack.append((p+1, last))

        self.drawCanvas(first, last, p)

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

def quicksort_example(lst):
    return QuicksortExample(lst)()

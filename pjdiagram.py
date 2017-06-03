from __future__ import print_function

from IPython.display import SVG, display
import cairocffi
from StringIO import StringIO
import math

def parent(i): return i/2
def left(i): return 2*i+1
def right(i): return 2*i+2

class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __enter__(self):
        self.memory = StringIO()
        self.surface = cairocffi.SVGSurface(self.memory, self.width, self.height)
        return cairocffi.Context(self.surface)

    def __exit__(self, *args):
        self.surface.flush()
        self.surface.finish()
        display(SVG(self.memory.getvalue()))


def draw(cr, width, height):
    cr.scale(width, height)
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(0.01)

    cr.rectangle(0.25, 0.25, 0.5, 0.5)
    cr.stroke()

def draw_array(ctx, pos, contents, cell_width=20, cell_height=20):
    ctx.set_line_width(1)

    for i, value in enumerate(contents):
        ctx.rectangle(pos[0] + i*cell_width, pos[1], cell_width, cell_height)

    ctx.set_source_rgb(0.8, 0.8, 0.8)
    ctx.fill_preserve()
    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.stroke()

    for i, value in enumerate(contents):
        x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = ctx.text_extents(str(value))
        ctx.move_to(pos[0] + i*cell_width + cell_width/2.0 - text_width/2.0, pos[1] + cell_height/2.0 + text_height/2.0)
        ctx.text_path(str(value))

    ctx.fill()

def draw_binary_tree(ctx, pos, contents, ply=1, index=0, radius=10, total_distance=None, xdistance=20, ydistance=40, highlight={}):
    if total_distance == None:
        height = int(math.log(len(contents), 2))
        total_distance = xdistance*(2**height)

    ctx.set_line_width(0.75)


    # draw left child
    left_pos = (pos[0] - total_distance/2.0, pos[1] + ydistance)
    left_index = left(index)
    if left_index < len(contents) and contents[left_index] != None:
        ctx.move_to(pos[0], pos[1])
        ctx.line_to(left_pos[0], left_pos[1])
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1.0)        
        ctx.stroke()

        draw_binary_tree(ctx, left_pos, contents, ply=ply+1,
                         index=left_index, total_distance=total_distance/2.0,
                         xdistance=xdistance, ydistance=ydistance, highlight=highlight)


    # draw right child
    right_pos = (pos[0] + total_distance/2.0, pos[1] + ydistance)
    right_index = right(index)
    if right_index < len(contents) and contents[right_index] != None:
        ctx.move_to(pos[0], pos[1])
        ctx.line_to(right_pos[0], right_pos[1])
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1.0)
        ctx.stroke()

        draw_binary_tree(ctx, right_pos, contents, ply=ply+1,
                         index=right_index, total_distance=total_distance/2.0,
                         xdistance=xdistance, ydistance=ydistance, highlight=highlight)

    # draw node
    ctx.arc(pos[0], pos[1], radius, 0, 2*math.pi)
    if index in highlight:
        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(4.0)
    else:
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1.0)
    ctx.stroke_preserve()
    ctx.set_source_rgb(0.8, 0.8, 0.8)
    ctx.fill()

    # draw text
    value = contents[index]
    x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = ctx.text_extents(str(value))
    ctx.move_to(pos[0] - text_width/2.0, pos[1] + text_height/2.0)
    ctx.text_path(str(value))
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill()

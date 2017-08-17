from ipywidgets import *

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

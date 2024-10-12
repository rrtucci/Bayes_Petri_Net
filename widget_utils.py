import ipywidgets as widgets
from IPython.display import display, clear_output


def create_step_button(refresh, inner_step, **kwargs):
    step_button = widgets.Button(description="Step")
    output = widgets.Output()
    global step_num

    def step():
        global step_num
        with output:
            if refresh:
                clear_output(wait=True)  # Clear the output if refresh is True
            inner_step(**kwargs)

    def on_step_click(b):
        step()

    # Link the buttons to their respective callback functions
    step_button.on_click(on_step_click)
    display(step_button, output)
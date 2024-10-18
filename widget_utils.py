import ipywidgets as widgets
from IPython.display import display, clear_output


def create_step_button(refresh, inner_step, **kwargs):
    """
    This function creates a button labelled "step" in a jupyter notebook.
    Clicking on the button advances executes the code contained in the
    function `inner_state`. The `inner_state` function is one of the input
    parameters. `refresh=True` erases the output cell between steps, whereas
    `refresh=False` appends any new output to the output already existing in
    the output cell.

    Parameters
    ----------
    refresh: bool
    inner_step: function
    kwargs: dict

    Returns
    -------
    None

    """
    step_button = widgets.Button(description="Step")
    step_button.style.button_color = 'limegreen'
    output = widgets.Output()
    global step_num

    def step():
        global step_num
        with output:
            if refresh:
                # Clear the output if refresh is True
                clear_output(wait=True)
            inner_step(**kwargs)

    def on_step_click(b):
        step()

    # Link the buttons to their respective callback functions
    step_button.on_click(on_step_click)
    display(step_button, output)

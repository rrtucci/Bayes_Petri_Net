import re

import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image
import matplotlib.pyplot as plt
import pydotplus as pdp
import os

def get_gray_tone(num_grays, i):
    if i < 0 or i >= num_grays:
        raise ValueError("i should be in the range [0, num_grays]")
    tone_value = int((num_grays - i - 1) * 255 / (num_grays - 1))
    hex_value = f"{tone_value:02x}"  # Convert to 2-digit hex
    return f"#{hex_value}{hex_value}{hex_value}"  # Return the gray color

def get_label_value(str0):
    match = re.search(r'label=(\d+)', str0)
    if match:
        return int(match.group(1))
    else:
        return None

def draw(dot_file_path, jupyter=True):
    """
    This method uses graphviz to draw the dot file located at
    dot_file_path. It creates a temporary file called tempo.png with a
    png of the dot file. If jupyter=True, it embeds the png in a jupyter
    notebook. If jupyter=False, it opens a window showing the png.

    Parameters
    ----------
    dot_file_path : str
    jupyter : bool


    Returns
    -------
    None

    """
    s = gv.Source.from_file(dot_file_path)

    # using display(s) will draw the graph but will not embed it
    # permanently in the notebook. To embed it permanently,
    # must generate temporary image file and use Image().
    # display(s)

    x = s.render("tempo123", format='png', view=False)
    os.remove("tempo123")
    if jupyter:
        display(Image(x))
    else:
        open_image("tempo123.png").show()

if __name__ == "__main__":
    def main():
        num_grays = 10
        print("gray_tones=",
            [get_gray_tone(num_grays, i) for i in range(num_grays)])
        str0 = "my name label=56is bob"
        print(get_label_value(str0))

    main()


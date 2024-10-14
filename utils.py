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
    match = re.search(r'label=(-?\d+)', str0)
    if match:
        return int(match.group(1))
    else:
        return None


def draw_dot_file(dot_file_path, jupyter=True):
    """
    This method uses graphviz to draw_dot_file the dot file located at
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

    # using display(s) will draw_dot_file the graph but will not embed it
    # permanently in the notebook. To embed it permanently,
    # must generate temporary image file and use Image().
    # display(s)

    x = s.render("tempo123", format='png', view=False)
    os.remove("tempo123")
    if jupyter:
        display(Image(x))
    else:
        open_image("tempo123.png").show()


def get_descendants(parent_to_children):
    # Dictionary to store the result: parent -> descendants
    parent_to_descendants = {}

    # Helper function for depth-first search (DFS)
    def dfs(node):
        # If the node has no children, return an empty set
        if node not in parent_to_children:
            return set()

        # If we already computed the descendants for this node,
        # return it
        if node in parent_to_descendants:
            return parent_to_descendants[node]

        # Get the direct children of the current node
        descendants = set(parent_to_children.get(node, []))

        # Recursively add the descendants of each child
        for child in parent_to_children.get(node, []):
            descendants.update(dfs(child))

        # Cache the result for the current node
        parent_to_descendants[node] = list(descendants)
        return descendants

    # Run DFS for each parent in the DAG
    for parent in parent_to_children:
        dfs(parent)

    return parent_to_descendants

def complete_dict(dictio, all_keys, default_val):
    if not dictio:
        dictio = {}
        for key in all_keys:
            dictio[key] = default_val
    else:
        for key in all_keys:
            if key not in dictio:
                dictio[key] = default_val
    return dictio

def reverse_pair(x):
    x1, x2 = x
    x1, x2 = x2, x1
    return (x1, x2)


if __name__ == "__main__":
    def main1():
        num_grays = 10
        print("gray_tones=",
              [get_gray_tone(num_grays, i) for i in range(num_grays)])
        str0 = "my name label=-56is bob"
        print(get_label_value(str0))


    def main2():
        # Example usage
        parent_to_children = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D']
        }

        parent_to_descendants = get_descendants(parent_to_children)
        print(parent_to_descendants)


    main1()
    main2()

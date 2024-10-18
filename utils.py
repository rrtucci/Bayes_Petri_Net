import re
import graphviz as gv
from IPython.display import display, Image
from PIL.Image import open as open_image
import matplotlib.pyplot as plt
import pydotplus as pdp
import os


def get_gray_tone(i, num_grays=10):
    """
    This method returns a str of a hex number for a tone of gray.

    Parameters
    ----------
    num_grays: int
        number of gray tones. It defaults to 10. `num_grays` will be
        increased if more than 10 numbers are required to cover the full
        range of the contents of the place nodes.
    i: int
        some int in the range {0, 1, ..., num_grays-1}. i=0 is for white and
        i=num_grays-1 is for black.

    Returns
    -------
    str
        A string of a hex number like '#ffffff' (white) or '#000000' (black)

    """
    if i < 0 or i >= num_grays:
        raise ValueError("i should be in the range [0, num_grays]")
    tone_value = int((num_grays - i - 1) * 255 / (num_grays - 1))
    hex_value = f"{tone_value:02x}"  # Convert to 2-digit hex
    return f"#{hex_value}{hex_value}{hex_value}"


def get_label_value(str0):
    """
    This method finds a substring of the form `label=-58` (or some other int
    besides -58), within the string `str0` and returns the integer `-58`.

    Parameters
    ----------
    str0: str
        string which contains substring `label=-58`

    Returns
    -------
    int|None

    """
    match = re.search(r'label=(-?\d+)', str0)
    if match:
        return int(match.group(1))
    else:
        return None


def draw_dot_file(dot_file_path, jupyter=True):
    """
    This method uses graphviz to draw the dot file located at
    `dot_file_path`. It creates a temporary file called `tempo.png` with a
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


def get_pa_to_descendants(pa_to_children):
    """
    This method returns a dictionary `pa_to_descendants` that maps each
    parent node to a list of all its descendant nodes, given as input a
    dictionary `pa_to_children` which maps each parent node to a list of all
    its children nodes. Every node is specified by the str which is its name.

    Parameters
    ----------
    pa_to_children: dict[str, list[str]]

    Returns
    -------
    dict[str, list[str]]
    """
    # Dictionary to store the result: parent -> descendants
    pa_to_descendants = {}

    # Helper function for depth-first search (DFS)
    def dfs(node):
        # If the node has no children, return an empty set
        if node not in pa_to_children:
            return set()

        # If we already computed the descendants for this node,
        # return it
        if node in pa_to_descendants:
            return pa_to_descendants[node]

        # Get the direct children of the current node
        descendants = set(pa_to_children.get(node, []))

        # Recursively add the descendants of each child
        for child in pa_to_children.get(node, []):
            descendants.update(dfs(child))

        # Cache the result for the current node
        pa_to_descendants[node] = list(descendants)
        return descendants

    # Run DFS for each parent in the DAG
    for parent in pa_to_children:
        dfs(parent)

    return pa_to_descendants


def complete_dict(dictio, new_keys, default_val):
    """
    This method takes in a dictionary `dictio` and adds to it new keys
    `new_keys` with the value `default_val`. The new dictionary is returned.
    If some of the new_keys are already present in dictio, it replaces their
    values by the default value.

    Parameters
    ----------
    dictio: dict[str, list[int]]
    new_keys: list[str]
    default_val: int

    Returns
    -------
    dict[str, list[int]]

    """
    if not dictio:
        dictio = {}
        for key in new_keys:
            dictio[key] = default_val
    else:
        for key in new_keys:
            if key not in dictio:
                dictio[key] = default_val
    return dictio


def reverse_pair(x):
    """
    This function takes an input like x=("a", "b) and returns its reverse (
    "b", "a").

    Parameters
    ----------
    x: tuple(str, str)

    Returns
    -------
    tuple(str, str)

    """
    x1, x2 = x
    x1, x2 = x2, x1
    return (x1, x2)


if __name__ == "__main__":
    def main1():
        num_grays = 10
        print("gray_tones=",
              [get_gray_tone(i, num_grays) for i in range(num_grays)])
        str0 = "my name label=-56is bob"
        print(get_label_value(str0))


    def main2():
        # Example usage
        parent_to_children = {
            'A': ['B', 'C'],
            'B': ['C', 'D'],
            'C': ['D']
        }

        parent_to_descendants = get_pa_to_descendants(parent_to_children)
        print(parent_to_descendants)


    main1()
    main2()

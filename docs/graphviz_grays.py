from graphviz import Digraph

# Define the color palette
grayscale_palette = [
    "#F0F0F0", "#D9D9D9", "#C0C0C0", "#A8A8A8", "#909090",
    "#787878", "#606060", "#484848", "#303030", "#101010"
]

# Function to generate a graph with the palette
def create_graph(filename):
    dot = Digraph()

    for i, color in enumerate(grayscale_palette, start=1):
        dot.node(f'node{i}', label=str(i), style='filled', fillcolor=color, fontcolor='white')

    # Add edges or customize further
    dot.edge('node1', 'node2')
    dot.edge('node2', 'node3')
    # Save the graph
    dot.render(filename, format='png')

# Create multiple graphs with the same palette
create_graph('graph1')
create_graph('graph2')

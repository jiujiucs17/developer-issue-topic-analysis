import pkgutil
import torch.nn
from pyvis.network import Network
from openpyxl import Workbook, load_workbook

# Counters for packages and modules
package_count = 1  # Start with 1 to include torch.nn
module_count = 0

def add_edges(graph, package, parent=None, ws=None):
    global package_count
    global module_count
    for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{parent}.{name}" if parent else name
        # Add nodes and edge
        graph.add_node(full_name, color='pink' if is_pkg else 'lightblue')
        if parent:
            graph.add_edge(parent, full_name, arrows='to')
        if is_pkg:
            package_count += 1
            add_edges(graph, __import__(f"{package.__name__}.{name}", fromlist=['']), full_name, ws)
        else:
            module_count += 1
        # Write the node name to the Excel file
        ws.append([full_name])

# Create a new Network instance with height of 1000px
G = Network(height='1300px')

# Add torch.nn as a parent node
G.add_node('torch.nn', color='lightcoral')

# Create a new Excel workbook and get the active worksheet
wb = Workbook()
ws = wb.active
ws.append(['Node Name'])  # Add column name

add_edges(G, torch.nn, 'torch.nn', ws)

# Save the interactive graph to the specified path
G.save_graph('/Users/zhangmengqi/Desktop/tmp_network/torch_nn.html')

# Save the Excel file
wb.save('/Users/zhangmengqi/Desktop/tmp_network/list_sub_modules.xlsx')

# Print the counts
print(f"Number of packages: {package_count}")
print(f"Number of modules: {module_count}")

# Load the workbook and get the active worksheet
wb = load_workbook(filename='/Users/zhangmengqi/Desktop/tmp_network/import_relation.xlsx')
ws = wb.active

import networkx as nx

# Convert the PyVis graph to a NetworkX graph
G_nx = nx.DiGraph(G.get_adj_list())

# Iterate over the rows in the worksheet and add edges to the graph
for row in ws.iter_rows(min_row=2, values_only=True):  # Skip the header row
    importing_file, imported_file = row
    # Check if importing_file is a parent package of imported_file
    if not imported_file.startswith(importing_file + '.'):
        # Check if importing_file and imported_file are the same
        if importing_file != imported_file:
            if not G_nx.has_edge(importing_file, imported_file):
                G.add_edge(importing_file, imported_file, color='green', arrows='to', length=500)
# Save the updated graph
G.save_graph('/Users/zhangmengqi/Desktop/tmp_network/torch_nn_relationships.html')
# from pyvis.network import Network
# import networkx as nx
# from networkx.drawing.nx_pydot import read_dot

# # create visualization using .dot file created by code2graph
# file_path_torch = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/c2g-project.dot"
# file_path_torch_nn = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/nn/c2g-project.dot"

# visualization_path = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/call_graph.html"

# # create visualization using .dot file created by code2graph
# file_path_torch = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/c2g-project.dot"
# file_path_torch_nn = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/nn/c2g-project.dot"

# visualization_path = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/call_graph.html"

# dot_file = file_path_torch_nn

# # Read the .dot file using networkx
# G_nx = read_dot(dot_file)

# # Create a new Network instance with height of 1000px
# G = Network(height='1300px')

# # Add nodes
# max_node_number = 500
# num_of_nodes = 0
# for node in G_nx.nodes():
#     G.add_node(node)
#     num_of_nodes += 1
#     if num_of_nodes == max_node_number:
#         break

# # Add edges with arrows
# num_of_edges = 0
# max_edge_number = 9999999999
# for edge in G_nx.edges():
#     try:
#         G.add_edge(edge[0], edge[1], arrows=True)
#     except:
#         continue

#     # print the name of the node here
#     print("(", edge[0], ") ---> (", edge[1], ")")
#     num_of_edges += 1
#     if num_of_edges == max_edge_number:
#         break

# print(f"Number of nodes: {max_node_number}")
# print(f"Number of edges: {num_of_edges}")


# # Save the interactive graph to the specified path
# G.save_graph(visualization_path)
# # The visualization is saved to the specified path
# print(f"Visualization saved to {visualization_path}")




# from pyvis.network import Network
# import networkx as nx
# from networkx.drawing.nx_pydot import read_dot

# create visualization using .dot file created by code2graph
file_path_torch = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/c2g-project.dot"
file_path_torch_nn = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/Call_Graph/pytorch/torch/nn/c2g-project.dot"

# visualization_path = "/Users/zhangmengqi/Documents/PhD/Working Documents/Deliverable 2/call_graph.html"

# dot_file = file_path_torch_nn

# # Read the .dot file using networkx
# G_nx = read_dot(dot_file)

# # Create a new Network instance with height of 1000px
# G = Network(height='1300px')

# # Convert the networkx graph to a pyvis network
# G.from_nx(G_nx)

# # Save the interactive graph to the specified path
# G.save_graph(visualization_path)
# # The visualization is saved to the specified path
# print(f"Visualization saved to {visualization_path}")





# # trying to get the call relationships between modules from the .dot file which provides the call relationships between functions
# import networkx as nx
# from networkx.drawing.nx_pydot import read_dot

# def get_module(node):
#     # This is a placeholder function. You'll need to implement it based on how your nodes are named.
#     return node.split('.')[0]

# # Load the .dot file
# graph = read_dot(file_path_torch_nn)

# # Initialize an empty set to store the call relationships
# module_calls = set()

# # Process each edge in the graph
# for edge in graph.edges():
#     # Get the nodes connected by the edge
#     source_node, target_node = edge

#     # Determine the modules of the source and target nodes
#     source_module = get_module(source_node)
#     target_module = get_module(target_node)

#     # Add the call relationship between the modules
#     module_calls.add((source_module, target_module))

# # Print the call relationships between modules
# for source_module, target_module in module_calls:
#     print(f'{source_module} -> {target_module}')



# get the call relationships between modules by using the importing relationship

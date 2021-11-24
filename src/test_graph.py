import random
import networkx as nx
import pickle as pkl
import math

# The following code has been inspired from the networkx documentation: https://networkx.org/documentation/stable/auto_examples/drawing/plot_directed.html
def make_small_graph():
  random.seed(15)
  graph = nx.generators.directed.random_uniform_k_out_graph(25, 5, seed=5)
  positions = nx.layout.spring_layout(graph, seed=15) 
  duplicates = set()
  marked = {}

  for node in graph.nodes:
    incoming = {}
    outgoing = {}
    graph.nodes[node]["x"] = positions[node][0]
    graph.nodes[node]["y"] = positions[node][1]
    graph.nodes[node]["elevation"] = random.randint(20, 200)
    for path in graph.in_edges(node):
      if path not in incoming:
        incoming[path] = True
      else:
        duplicates.add(path)

    for path in graph.out_edges(node):
      if path not in outgoing:
        outgoing[path] = True
      else:
        duplicates.add(path)

  for path in graph.edges():
    first_node = graph.nodes[path[0]]
    second_node = graph.nodes[path[1]]
    graph.edges[path[0], path[1], 0]["length"] = math.dist([first_node["x"], first_node["y"]], [second_node["x"], second_node["y"]])

  for node in graph.nodes:
      marked[node] = node

  for path in duplicates:
    graph.remove_edge(path[0], path[1])

  filename = "../cached_maps/test_small_graph.pkl"
  pkl.dump(graph, open(filename, "wb"))

def make_medium_graph():
  random.seed(15)
  graph = nx.generators.directed.random_uniform_k_out_graph(50, 10, seed=5)
  positions = nx.layout.spring_layout(graph, seed=15) 
  duplicates = set()
  marked = {}

  for node in graph.nodes:
    incoming = {}
    outgoing = {}
    graph.nodes[node]["x"] = positions[node][0] * 100 # TODO: remove this 100?
    graph.nodes[node]["y"] = positions[node][1] * 100 # TODO: remove this 100?
    graph.nodes[node]["elevation"] = random.randint(20, 200)
    for path in graph.in_edges(node):
      if path not in incoming:
        incoming[path] = True
      else:
        duplicates.add(path)

    for path in graph.out_edges(node):
      if path not in outgoing:
        outgoing[path] = True
      else:
        duplicates.add(path)

  for path in graph.edges():
    first_node = graph.nodes[path[0]]
    second_node = graph.nodes[path[1]]
    graph.edges[path[0], path[1], 0]["length"] = math.dist([first_node["x"], first_node["y"]], [second_node["x"], second_node["y"]])

  for node in graph.nodes:
    marked[node] = node

  for path in duplicates:
    graph.remove_edge(path[0], path[1])

  filename = "../cached_maps/test_medium_graph.pkl"
  pkl.dump(graph, open(filename, "wb"))

if __name__ == "__main__":
    make_small_graph()
    make_medium_graph()

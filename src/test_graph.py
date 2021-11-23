import random
import networkx as nx
import pickle as pkl

def make_small_graph():
  random.seed(15)
  graph = nx.generators.directed.random_uniform_k_out_graph(25, 5, seed=5)
  positions = nx.layout.kamada_kawai_layout(graph) 
  duplicates = set()

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

  for path in duplicates:
    graph.remove_edge(path[0], path[1])

  marked = {}
  for node in graph.nodes:
      marked[node] = node

  filename = "../cached_maps/test_small_graph.pkl"
  pkl.dump(graph, open(filename, "wb"))

def make_medium_graph():
  random.seed(15)
  graph = nx.generators.directed.random_uniform_k_out_graph(50, 10, seed=5)
  positions = nx.layout.kamada_kawai_layout(graph) 
  duplicates = set()

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

  for path in duplicates:
    graph.remove_edge(path[0], path[1])

  marked = {}
  for node in graph.nodes:
      marked[node] = node

  filename = "../cached_maps/test_medium_graph.pkl"
  pkl.dump(graph, open(filename, "wb"))

if __name__ == "__main__":
    make_small_graph()
    make_medium_graph()
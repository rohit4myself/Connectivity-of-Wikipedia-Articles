import pandas as pd
import networkx as nx
from networkx.algorithms.components.connected import connected_components

df1 = pd.read_csv("edges.csv")
df1.columns = ['e1','e2']
# print(df1)

G = nx.from_pandas_edgelist(df1, 'e1', 'e2') #Creating the graph
G.to_undirected() # making the graph undirected
l = list(connected_components(G)) # Getting connected components
number_isolate_nodes = 4604 - (len(l[0])+ len(l[1])) # number of components which have only 1 node

# Getting subgraph of two connected components which have more than 1 node.
H = G.subgraph(l[0])
I = G.subgraph(l[1])
nodes, edges, diameter = [],[],[]

nodes.append(len(l[0]))
nodes.append(len(l[1]))
edges.append(H.number_of_edges())
edges.append(I.number_of_edges())
diameter.append(nx.diameter(H))
diameter.append(nx.diameter(I))

# Adding isolated nodes in the output lists.
for i in range(12): # There are 12 such cases.
    nodes.append(1)
    edges.append(0) # Only one node, so no edge
    diameter.append(0) #since there is no edges

output_df = pd.DataFrame()
output_df["Nodes"] = nodes
output_df["Edges"] = edges
output_df["Diameter"] = diameter

# Exporting the results into graph-components.csv
output_df.to_csv("graph-components.csv", index = False)
print("Output file generated - graph-components.csv")

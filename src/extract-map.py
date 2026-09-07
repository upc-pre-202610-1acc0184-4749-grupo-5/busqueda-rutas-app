import osmnx as ox
import pandas as pd
import os

place = "Barcelona, Spain"
graph = ox.graph_from_place(place, network_type='drive')

qNodes = len(graph.nodes)

print(f"Number of nodes in the graph: {qNodes}")

if qNodes < 1500 :
    print("The graph has less than 1500 nodes. Please choose a larger area.")
else :
    print("The graph has more than 1500 nodes. Proceeding with extraction.")

os.makedirs("dataset", exist_ok=True)

nodesGdf, edgesGdf = ox.graph_to_gdfs(graph)

nodesGdf.to_csv("dataset/intersections.csv")
edgesGdf.to_csv("dataset/streets.csv")
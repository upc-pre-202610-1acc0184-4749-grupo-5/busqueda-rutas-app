import osmnx as ox

place = "Barcelona, Spain"
print(f"Obteniendo el mapa de {place} para dibujarlo...")

graph = ox.graph_from_place(place, network_type='drive')

print("Generando la imagen (esto puede tardar unos segundos)...")
fig, ax = ox.plot_graph(
    graph,
    node_size=0,
    edge_linewidth=0.3,
    edge_color="#1f77b4",
    bgcolor="white",
    show=False,
    save=True,
    filepath="./report/assets/barcelona_map.png"
)

print("Saved image")
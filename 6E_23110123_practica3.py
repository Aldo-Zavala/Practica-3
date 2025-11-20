import heapq
import matplotlib.pyplot as plt
import networkx as nx
import time

# --------------------------
#   Dijkstra con animación
# --------------------------

def dibujar_grafo(G, dist, actual=None, actualizado=None, visitados=set()):
    colors = []
    for nodo in G.nodes():
        if nodo == actual:
            colors.append("red")         # nodo siendo procesado
        elif nodo in visitados:
            colors.append("lightgray")  # nodo ya visitado
        elif nodo == actualizado:
            colors.append("yellow")     # nodo cuya distancia se acaba de actualizar
        else:
            colors.append("skyblue")    # nodo normal

    pos = nx.spring_layout(G, seed=42)  # posición fija

    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=12)
    
    # Dibujar pesos
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    # Dibujar distancias encima
    dist_labels = {nodo: (dist[nodo] if dist[nodo] != float('inf') else "∞") for nodo in G.nodes()}
    y_offset = 0.08
    for nodo, (x, y) in pos.items():
        plt.text(x, y + y_offset, f"dist={dist_labels[nodo]}", 
                 horizontalalignment='center', fontsize=9, color='black')

    plt.pause(1.0)  # pausa para ver cada actualización


def dijkstra_animado(G, inicio):
    dist = {n: float("inf") for n in G.nodes()}
    dist[inicio] = 0
    prev = {n: None for n in G.nodes()}
    visitados = set()

    pq = [(0, inicio)]

    plt.ion()
    fig = plt.figure(figsize=(8, 6))

    print("\nEstado inicial del grafo:")
    dibujar_grafo(G, dist)

    while pq:
        d_actual, nodo = heapq.heappop(pq)

        if nodo in visitados:
            continue

        print(f"\nProcesando nodo: {nodo}")
        visitados.add(nodo)
        dibujar_grafo(G, dist, actual=nodo, visitados=visitados)

        for vecino in G[nodo]:
            peso = G[nodo][vecino]["weight"]
            nueva = dist[nodo] + peso

            print(f"  Revisa {nodo} -> {vecino} (peso {peso})")
            print(f"    Distancia actual a {vecino}: {dist[vecino]}")
            print(f"    Nueva posible: {nueva}")

            if nueva < dist[vecino]:
                print(f"    ✔ Se actualiza {vecino}: {dist[vecino]} → {nueva}")
                dist[vecino] = nueva
                prev[vecino] = nodo
                heapq.heappush(pq, (nueva, vecino))

                dibujar_grafo(G, dist, actualizado=vecino, visitados=visitados)
            else:
                print(f"    ✘ No hay actualización.")

    print("\nDistancias finales:")
    for nodo in dist:
        print(f"  {nodo}: {dist[nodo]}")

    plt.ioff()
    plt.show()

    return dist, prev


# --------------------------
#   EJEMPLO DE USO
# --------------------------

if __name__ == "__main__":
    G = nx.DiGraph()

    # Agregar nodos y aristas con pesos
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 3),
        ("B", "D", 2),
        ("B", "E", 3),
        ("C", "B", 1),
        ("C", "D", 4),
        ("C", "E", 5),
        ("D", "E", 1)
    ]

    G.add_weighted_edges_from(edges)

    origen = "A"
    dist, prev = dijkstra_animado(G, origen)


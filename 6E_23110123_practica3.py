import heapq

def dijkstra(grafo, inicio):
    dist = {nodo: float('inf') for nodo in grafo}
    dist[inicio] = 0
    cola = [(0, inicio)]

    while cola:
        distancia_actual, nodo = heapq.heappop(cola)

        if distancia_actual > dist[nodo]:
            continue

        for vecino, peso in grafo[nodo]:
            nueva = distancia_actual + peso
            if nueva < dist[vecino]:
                dist[vecino] = nueva
                heapq.heappush(cola, (nueva, vecino))

    return dist


# Ejemplo de uso:
grafo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 3), ('D', 2), ('E', 3)],
    'C': [('B', 1), ('D', 4), ('E', 5)],
    'D': [('E', 1)],
    'E': []
}

print(dijkstra(grafo, 'A'))

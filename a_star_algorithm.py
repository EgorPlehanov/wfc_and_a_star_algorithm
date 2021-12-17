import heapq as hp


# Возвращает список кортяжей соседних клеток с ценой перехода в них и их координатами
def get_neighbours(x, y, grid):
    check_neighbour = lambda x, y: True if 0 <= x < len(grid[0]) and 0 <= y < len(grid) else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]#, [-1, -1], [1, -1], [1, 1], [-1, 1]    # Диагональные пути
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]

# Строит граф по переданной ему карте местности
def build_graph(grid):
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y, grid)
    return graph

# Эвристическая функция для черырех направлений (манхеттенское расстояние)
def heuristic_manchen(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

# # Эвристическая функция для четырех направлений и диагоналей (расстояние Чебышева)
# def heuristic_сhebyshev(a, b):
#    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

# Поиск кратчайшего пути (алгоритм Дейкстры)
def dijkstra(start, goal, graph):
    queue = []
    hp.heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_node = hp.heappop(queue)[1]
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic_manchen(neigh_node, goal)
                hp.heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited
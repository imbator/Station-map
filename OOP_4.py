from math import inf


class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links


class Link:
    def __init__(self, v1: Vertex, v2: Vertex):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, val):
        self._dist = val

    def __eq__(self, other):
        return (self.v1 == other.v1 and self.v2 == other.v2) or \
               (self.v2 == other.v1 and self.v1 == other.v2)

    def __hash__(self):
        print("In hash")
        return hash((self.v1, self.v2))


class LinkedGraph:
    infn = str(inf)

    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v) -> None:
        """Добавление новой вершины в граф"""
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link) -> None:
        """для добавления новой связи link в список _links
        (если объект link с указанными вершинами в списке отсутствует)"""
        # print(f"Перед проверкой: Поступающая связь: {link}, Текущий список: {self._links}")
        if link not in self._links:
            self._links.append(link)
            # Развернем link в соответствии с вершиной
            link.v1.links.append(LinkMetro(link.v1, link.v2, link.dist))
            link.v2.links.append(LinkMetro(link.v2, link.v1, link.dist))
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)

    def algorithm_state_info(self, lengths, separators):
        """ Печать в консоль текущего состояния алгоритма поиска
            кратчайшего расстояния
        """
        stations = [station.name for station in self._vertex]
        output_shift = 0
        for i in lengths.values():
            is_end_line = output_shift != len(lengths.values()) - 1
            curr_len_sep = separators[output_shift]
            border = ' ' * curr_len_sep + ' | ' if is_end_line else ' ' * curr_len_sep
            print(str(i) + border[len(str(i))::], end='')
            output_shift += 1
        print('\n')

    def find_path(self, start_v: Vertex, stop_v: Vertex) -> None:
        """Функция для поиска кратчайшего маршрута из вершины start_v в вершину stop_v
        ([вершины кратчайшего пути], [связи между вершинами]).
        Реализован при помощи алгоритма дейкстры."""

        print(f"Суммарное число вершин алгоритма: {len(self._vertex)}")
        stations = [station.name for station in self._vertex]
        separators = [len(station) for station in stations]
        minimum_paths = {}

        to_vertex_path_lengths = {}
        vertex_output = {}  # Отдельный словарь для печати

        # Формат хранения в словаре search_threads: key: номер потока, value: (Массив вершин, суммарная длина)
        search_threads = []  # Исследуемые в ходе работе алгоритма цепи
        algorithm_path = []

        vertex_path = []  # Путь по вершинам
        links_path = []  # Путь по связям

        current_vertex = start_v

        for i in start_v.links:
            print(f"Start vertex link found: {i}")
        for i in self._vertex:
            if i == start_v:
                vertex_output[i] = 0
                search_threads.append(([i], 0))
                minimum_paths[i] = 0
            else:
                to_vertex_path_lengths[i] = inf
                vertex_output[i] = inf

        # Выводим начало таблички на экран
        print(*stations, sep=' | ')
        self.algorithm_state_info(vertex_output, separators)  # Выводим информацию на экран

        # Удалим 0 из стека для печати:
        shortest_distance_vertex = min(vertex_output, key=vertex_output.get)
        vertex_output[shortest_distance_vertex] = ''

        stage = 0

        # start_pos = 0

        while stage != 1:
            # Основные процедуры
            for link_vertex in current_vertex.links:
                input_vertex = (link_vertex.v1, link_vertex.v2)
                route_vertex = list(filter(lambda x: x != current_vertex, input_vertex))[0]
                # print(route_vertex)  # Достали вершину, за которой будем вести учет
                current_distance = to_vertex_path_lengths[route_vertex]

                if current_distance == inf or current_distance > link_vertex.dist:
                    to_vertex_path_lengths[route_vertex] = link_vertex.dist
                    vertex_output[route_vertex] = link_vertex.dist

            self.algorithm_state_info(vertex_output, separators)  # Посмотрели обновленную информацию

            # Найти ближайшую цепочку - > Перейти к ней - > Сменить опорную вершину

            shortest_distance_vertex = min(to_vertex_path_lengths, key=to_vertex_path_lengths.get)
            shortest_path = to_vertex_path_lengths[shortest_distance_vertex]
            print(f"Shortest distance vertex: {shortest_distance_vertex}")

            vertex_output[shortest_distance_vertex] = ''  # Больше на экран выводиться эта вершина не будет
            shortest_path = to_vertex_path_lengths[shortest_distance_vertex]

            # Необходимо присоединить вершину к потоку. Логика присоединения:
            # Если пути, фиксируемые в потоках, больше, чем путь на данной итерации - > Создаем новый поток.
            # Новый поток формируется от базовой вершины (start_v).
            # В противном случае - присоединяем вершину к имеющемуся минимальному потоку.
            # start_pos = to_vertex_path_lengths[shortest_distance_vertex]
            # if shortest_path >
            # for i in search_threads:
            #     print(i)
            #
            # stage += 1


class Station(Vertex):
    """ Класс для описания станций метро"""
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        """Печать информации о станции на экран"""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Печать информации о станции на экран"""
        return f"{self.name}"


class LinkMetro(Link):
    """Класс для описания связей между станциями метро"""
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self.dist = dist

    def __repr__(self):
        return f"{self.v1, self.v2}"


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))  # Проверить, что в v3 линк развернут в нужную сторону

print(v1.__dict__)
print(v3.__dict__)
# map_metro.add_link(LinkMetro(v4, v5, 1))
# map_metro.add_link(LinkMetro(v6, v7, 1))
#
# map_metro.add_link(LinkMetro(v2, v7, 5))
# map_metro.add_link(LinkMetro(v3, v4, 3))
# map_metro.add_link(LinkMetro(v5, v6, 3))

# print(len(map_metro._links))
# print(len(map_metro._vertex))

# path = map_metro.find_path(v1, v6)



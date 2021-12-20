import random
import math
from typing import List


# Класс паттерна
class Pattern:
    def __init__(self, pixels):
        self.pixels = pixels
    def __len__(self):
        return 1

# Класс паттерна с набором всех возможных его соседних паттернов
class Index:
    def __init__(self, patterns: List[Pattern], directions):
        self.data = {}
        for pattern in patterns:
            self.data[pattern] = {}
            for d in directions:
                self.data[pattern][d] = []
    
    # Записывает паттерн который можно присоединить к текущему (self), массив возможных паттернов
    def add_rule(self, pattern: Pattern, relative_position: tuple, next_pattern: Pattern):
        self.data[pattern][relative_position].append(next_pattern)
    
    # Проверка возможности соседства двух паттернов в заданном направлении относительно патерна self
    def check_possibility(self, pattern: Pattern, check_pattern: Pattern, relative_pos: tuple):
        if not pattern: return None
        if isinstance(pattern, list):
            pattern = pattern[0]
            
        return check_pattern in self.data[pattern][relative_pos]

# Поворот шаблона на 90, 180 и 270 градусов
def get_all_rotations(pixelMatrix):
    pixelMatrix_rotated_90 = [[pixelMatrix[j][i] for j in range(len(pixelMatrix))] for i in range(len(pixelMatrix[0])-1,-1,-1)]
    pixelMatrix_rotated_180 = [[pixelMatrix_rotated_90[j][i] for j in range(len(pixelMatrix_rotated_90))] for i in range(len(pixelMatrix_rotated_90[0])-1,-1,-1)]
    pixelMatrix_rotated_270 = [[pixelMatrix_rotated_180[j][i] for j in range(len(pixelMatrix_rotated_180))] for i in range(len(pixelMatrix_rotated_180[0])-1,-1,-1)]
    return tuple(tuple(row) for row in pixelMatrix), \
            tuple(tuple(row) for row in pixelMatrix_rotated_90), \
            tuple(tuple(row) for row in pixelMatrix_rotated_180), \
            tuple(tuple(row) for row in pixelMatrix_rotated_270)

# Разделяет пример на патерны
def parse_patterns(input_size, pixels, weights, patterns, N):
    for y in range(input_size[0]-(N-1)): # row 
        for x in range(input_size[1]-(N-1)): # column        
            pattern = []
            for k in pixels[y:y+N]:
                pattern.append([int(i) for i in k[x:x+N]]) 
            for rotation in get_all_rotations(pattern):
                if rotation not in weights:
                    weights[rotation] = 1
                    patterns.append(rotation)
                else:
                    weights[rotation] += 1

# Добавляет массив направлений valid_directions
def dirs(valid_directions, directions, list_dirs):
    valid_directions.extend([directions[d] for d in list_dirs])

# Возвращает напрасления в 
def valid_dirs(pos, output_size):
    x, y = pos
    
    valid_directions = []

    if x == 0:
        valid_directions.extend([(1, 0)])
        if y == 0:
            valid_directions.extend([(0, 1), (1, 1)])
        elif y == output_size[1]-1:
            valid_directions.extend([(0, -1), (1, -1)])
        else:
            valid_directions.extend([(0, 1), (1, 1), (0, -1), (1, -1)])
    elif x == output_size[0]-1:
        valid_directions.extend([(-1, 0)])
        if y == 0:
            valid_directions.extend([(0, 1), (-1, 1)])
        elif y == output_size[1]-1:
            valid_directions.extend([(0, -1), (-1, -1)])
        else:
            valid_directions.extend([(0, 1), (-1, 1), (0, -1), (-1, -1)])
    else:
        valid_directions.extend([(-1, 0), (1, 0)])
        if y == 0:
            valid_directions.extend([(0, 1), (-1, 1), (1, 1)])
        elif y == output_size[1]-1:
            valid_directions.extend([(0, -1), (-1, -1), (1, -1)])
        else: 
            valid_directions.extend([(0, -1), (-1, -1), (1, -1), (0, 1), (-1, 1), (1, 1)])
    
    return valid_directions

# Возвращает элементы паттерна, каторые нужно проверить на возможность прикрепления к ней другого паттерна
def get_offset_tiles(pattern: Pattern, offset: tuple):
    if offset == (0, 0):
        return pattern.pixels
    if offset == (-1, -1):
        return tuple([pattern.pixels[1][1]])
    if offset == (0, -1):
        return tuple(pattern.pixels[1][:])
    if offset == (1, -1):
        return tuple([pattern.pixels[1][0]])
    if offset == (-1, 0):
        return tuple([pattern.pixels[0][1], pattern.pixels[1][1]])
    if offset == (1, 0):
        return tuple([pattern.pixels[0][0], pattern.pixels[1][0]])
    if offset == (-1, 1):
        return tuple([pattern.pixels[0][1]])
    if offset == (0, 1):
        return tuple(pattern.pixels[0][:])
    if offset == (1, 1):
        return tuple([pattern.pixels[0][0]])

# Генерируем привила для каждого патерна и записываем их в Index
def rule_generator(patterns, directions, index):
    for pattern in patterns:
        for d in directions:
            for pattern_next in patterns:
                # here's checking all offsets
                overlap = get_offset_tiles(pattern_next, d) # Получаем элементы одного патерна
                og_dir = tuple([d[0]*-1, d[1]*-1])  # Инвертируем направление чтобы получить направление с которогобудет крепиться второй паттерн
                part_of_og_pattern = get_offset_tiles(pattern, og_dir)  # Получаем элементы второго патерна
                if (overlap) == (part_of_og_pattern):   # Проверяем возможность присоединения, при совпаденеии записываем в 
                    index.add_rule(pattern, d, pattern_next)

# Записывает в каждую клетку будующей карты местности все возможные паттерны из каторых потом будут выбираться подходящие
def initialize_wave_function(size, patterns):
    coefficients = []
    for col in range(size[0]):
        row = []
        for r in range(size[1]):
            row.append(patterns)
        coefficients.append(row)
    return coefficients

# Проверяет все ли клетки матрицы мастрости сколлапсировали (приняли только одно значение)
def is_fully_collapsed(coefficients):
    for col in coefficients:
        for entry in col:
            if(len(entry)>1):
                return False
    return True

# Возвращает список паттернов, которые можно присоеденить к переданному (position)
def get_possible_patterns_at_position(position, coefficients):
    x, y = position
    possible_patterns = coefficients[x][y]
    return possible_patterns

# Возвращает значение энтропии Шеннона
def get_shannon_entropy(position, coefficients, probability):
    x, y = position
    entropy = 0
    
    # Если ячейка имеет только один допустимый паттерн то ее энтрапия равно 0
    if len(coefficients[x][y]) == 1:
        return 0
    
    for pattern in coefficients[x][y]:  # Формула вычисления энтропии Шеннона
        entropy += probability[pattern] * math.log(probability[pattern], 2) 
    entropy *= -1
    
    # Добавляем шума чтобы получить меннее повторояющийся результат
    entropy -= random.uniform(0, 0.1)
    return entropy

# Возвращает координаты позиции с наименьшей энтропией
def get_min_entropy_pos(coefficients, probability):
    minEntropy = None
    minEntropyPos = None
    
    for x, col in enumerate(coefficients):
        for y, row in enumerate(col):
            entropy = get_shannon_entropy((x, y), coefficients, probability)
            
            if entropy == 0:
                continue
            
            if minEntropy is None or entropy < minEntropy:
                minEntropy = entropy
                minEntropyPos = (x, y)
    return minEntropyPos

# Алгоритм коллапса волновой функции
def observe(probability, coefficients):
    # Ищем позицию с наименьшей энтропией (наименьшим количеством возможных паттернов)
    min_entropy_pos = get_min_entropy_pos(coefficients, probability)

    if min_entropy_pos == None:
        print("All tiles have 0 entropy")
        return    
    
    semi_random_pattern = random.choice(get_possible_patterns_at_position(min_entropy_pos, coefficients))
    
    # Записываем выбранный вариант в элемент массива
    coefficients[min_entropy_pos[0]][min_entropy_pos[1]] = semi_random_pattern
    
    return min_entropy_pos

# Обновляем списки доступных паттернов соседних с выбранным паттерном
def propagate(min_entropy_pos, coefficients, output_size, index):
    stack = [min_entropy_pos]
    
    while len(stack) > 0:
        pos = stack.pop()
        
        possible_patterns = get_possible_patterns_at_position(pos, coefficients)
        
        # Перебирать каждое местоположение, непосредственно примыкающее к текущему местоположению (pos)
        for d in valid_dirs(pos, output_size):
            adjacent_pos = (pos[0] + d[0], pos[1] + d[1])
            possible_patterns_at_adjacent = get_possible_patterns_at_position(adjacent_pos, coefficients)
            
            # Iterate over all still available patterns in adjacent tile and check if pattern is still possible in this location
            if not isinstance(possible_patterns_at_adjacent, list):
                possible_patterns_at_adjacent = [possible_patterns_at_adjacent]
            for possible_pattern_at_adjacent in possible_patterns_at_adjacent:

                if len(possible_patterns) > 1:
                    is_possible = any([index.check_possibility(pattern, possible_pattern_at_adjacent, d) for pattern in possible_patterns])
                else:
                    is_possible = index.check_possibility(possible_patterns, possible_pattern_at_adjacent, d)

                if is_possible is None:
                    return None

                if not is_possible:
                    x, y = adjacent_pos
                    coefficients[x][y] = [patt for patt in coefficients[x][y] if patt.pixels != possible_pattern_at_adjacent.pixels]
                        
                    if adjacent_pos not in stack:
                        stack.append(adjacent_pos)
    return 1

# Создает массив карты местности
def final_pixels_map(coefficients):
    final_pixels = []
    for i in coefficients:
        row = []
        for j in i:
            if isinstance(j, list):
                first_pixel = j[0].pixels[0][0]
            else:
                first_pixel = j.pixels[0][0]
            row.append(first_pixel)
        final_pixels.append(row)
    return final_pixels

def wfc(example, output_cols, output_rows):
    input_size = (len(example), len(example[0]))
    output_size = (output_rows, output_cols)

    N = 2           # Размер паnтерна
    patterns = []   # Хранит паттерны размера N*N
    weights = {}    # Словарь количества появлений каждого паттерна в примере {паттерн: кол-во в примере}
    parse_patterns(input_size, example, weights, patterns, N)   # Разделяем пример на уникальные паттерны (patterns) и находим сколько раз встречается каждый паттерн в примере (weights)

    sum_of_weights = sum(weights.values())  
    patterns = [Pattern(p) for p in patterns]
    weights = {pattern : weights[pattern.pixels] for pattern in patterns} # Кол-во
    probability = {pattern : weights[pattern] / sum_of_weights for pattern in patterns} # Вероятность появлении паттерна в выходном массиве карты местности

    directions = [(0, -1), (-1, 0), (0, 1), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    index = Index(patterns, directions) # Записываем паттерны и направления возможных пресоендинений других паттернов для каждого паттерна

    rule_generator(patterns, directions, index) # Записываем в index для каждого паттерна по каждому направлению набор паттернов которые можно к нему присоединить

    coefficients = initialize_wave_function(output_size, patterns)
    attempt_count = 0
    while not is_fully_collapsed(coefficients):
        min_entropy_pos = observe(probability, coefficients)
        failed_generation = propagate(min_entropy_pos, coefficients, output_size, index)
        if failed_generation == None:
            print('Неудачная генерация( Пробуем снова')
            attempt_count += 1
            if attempt_count > 5: return [[example[0][0] for x in range(output_cols)]for y in range(output_rows)]
            coefficients = initialize_wave_function(output_size, patterns)
    return final_pixels_map(coefficients)

import random
import math

class Solver_8_queens:
    def __init__(self, pop_size=1000, maxChilds=500, cross_prob=0.9, 
                mut_prob=0.1, board_size=64):
        #инициализация переменных
        self.pop_size = pop_size
        self.mut_prob = mut_prob
        self.cross_prob = cross_prob
        self.maxChilds = maxChilds
        self.size = round(math.sqrt(board_size))
        self.epoch_num = 0
        self.maxRoulette = 0
        self.done = False
        self.visualization = ""
        self.sol = []
        self.population = []
        self.coordinates = []
        self.conflicts = []
        self.fitness = []
        self.parents = []

    def generate(self):
        for i in range(self.pop_size):
            self.population.append([])
            for j in range(self.size):
                self.population[i].append([])
                for c in range(self.size):
                    #генерируем доску 8*8 полностью состоящую из нулей
                    self.population[i][j].append(0)
                #рэндомно вставляем единицу в каждую строку
                queen = random.randint(0, 7)
                self.population[i][j][queen] = 1

    def get_coord(self):
        self.coordinates = []
        for i in range(len(self.population)):
            self.coordinates.append([])
            for j in range(self.size):
                for c in range(self.size):
                    #получаем координаты каждого ферзя
                    if self.population[i][j][c] == 1:
                        self.coordinates[i].append([j, c])

    def get_collisions(self):
        self.conflicts = []
        for i in range(len(self.population)):
            self.conflicts.append([])
            for j in range(self.size):
                for m in range(self.size):
                    point = self.coordinates[i]
                    #находим пересечения по вертикалям
                    if point[j][1] == point[m][1] and j != m:
                        #добавляем конфликтные строки в массив
                        self.conflicts[i].extend([j, m])
                    #по диагоналям
                    if ((point[j][0]-point[m][0]) + (point[j][1]-point[m][1]) == 0 and j != m or
                        (point[j][0]-point[m][0]) - (point[j][1]-point[m][1]) == 0 and j != m):
                        #добавляем конфликтные строки в массив
                        self.conflicts[i].extend([m, j])
            #получаем массив без повторяющихся строк
            self.conflicts[i] = set(self.conflicts[i])

    def set_fitness(self):
        self.fitness = []
        for i in range(len(self.population)):
            #находим fitness-значение каждой особи
            self.fitness.append((math.fabs(len(self.conflicts[i])-8)/10)+0.2)
            #верное решение
            if self.fitness[i] > self.min_fitness:
                self.done = True
                return

    def get_visualization(self):
        for c in range(len(self.sol)):
            for j in range(len(self.sol[c])):
                if self.sol[c][j] == 0:
                    self.visualization += "+ "
                else:
                    self.visualization += "Q "
                if j == self.size - 1:
                    self.visualization += "\n"

    def mutate_column(self):
        for i in range(len(self.population)):
            rand = random.randrange(0, 99)
            if rand <= self.mut_prob * 100:
                #изменяем положение ферзя в конкретной строке
                row = random.randrange(0, 8)
                column = random.randrange(0, 8)
                for c in range(8):
                    if self.population[i][row][c] == 1:
                        self.population[i][row][c] = 0
                self.population[i][row][column] = 1

    def crossover(self):
        cross_point = random.randrange(0, 7)
        for i in range(len(self.parents)):
            if random.randrange(0, 99) <= self.cross_prob * 100:
                #получаем двух потомков
                child1 = self.population[self.parents[i][0]]
                child2 = self.population[self.parents[i][1]]
                #реализуем одноточечное скрещивание
                for b in range(cross_point, self.size):
                    child1[b] = self.population[self.parents[i][1]][b]
                    child2[b] = self.population[self.parents[i][0]][b]
                #добавляем особи в популяцию
                self.population.extend([child1, child2])

    def selection(self):
        self.parents = []
        self.maxRoulette = 0
        new_population = []
        current = 0
        #реализация отбора с помощью колеса рулетки
        for i in range(len(self.fitness)):
            self.maxRoulette += self.fitness[i]
        while len(new_population) < self.pop_size:
            pick = random.uniform(0, self.maxRoulette)
            for i in range(len(self.fitness)):
                current += self.fitness[i]
                if current > pick:
                    #отбираем особи в новое потомство
                    new_population.append(self.population[i])
        self.population = []
        self.population = new_population

    def find_pair(self):
        parents = []
        parentA, parentB = 0, 0
        while len(self.parents) < self.maxChilds:
            #отбираем родительские особи
            pick = random.uniform(0, len(self.population)-1)
            self.parents.append(round(pick))
        for i in range(self.maxChilds//2):
            #случайным образом получаем родительские пары
            while parentA == parentB:
                parentA = self.parents[random.randrange(0, len(self.parents))]
                parentB = self.parents[random.randrange(0, len(self.parents))]
            parents.append([parentA, parentB])
        self.parents = None
        self.parents = parents

    def count_epoch(self):
        self.epoch_num+=1
        print(self.epoch_num)

    def solve(self, min_fitness=0.9, maxEpochs=200):  
        self.min_fitness = min_fitness       
        self.generate()
        while self.done == False and self.epoch_num < maxEpochs:
            self.count_epoch()
            self.get_coord()
            self.get_collisions()
            self.set_fitness()
            if self.done == True or self.epoch_num == maxEpochs:
                #получаем наиболее приспособленную особь
                self.sol = self.population[self.fitness.index(max(self.fitness))]
                #подготавливаем визуализацию
                self.get_visualization()
                return max(self.fitness), self.epoch_num, self.visualization     
            self.find_pair()
            self.crossover()
            self.mutate_column()
            self.selection()
        return max(self.fitness), self.epoch_num, self.visualization 
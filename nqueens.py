import random
import math

class Solver_8_queens:
    maxChilds = 500
    maxEpochs = 200
    maxRows = 8
    maxColumns = 8
    epoch_num = 0
    maxRoulette = 0
    done = False
    visualization = ""
    sol = []
    population = []
    coordinates = []
    conflicts = []
    ftness = []
    parents = []


    def __init__ (self, pop_size=1000, cross_prob=0.9, mut_prob=0.1):
        self.pop_size = pop_size
        self.mut_prob = mut_prob
        self.cross_prob = cross_prob

    def generate (self):
        self.population = []

        for i in range(self.pop_size):
            self.population.append([])
            self.ftness.append([])
            self.conflicts.append([])

            for j in range(self.maxRows):
                self.population[i].append([])

                for c in range(self.maxColumns):
                    self.population[i][j].append(0)

                queen = random.randint(0, 7)
                done = False
                self.population[i][j][queen] = 1

    def get_coord (self):
        self.coordinates = []

        for i in range(len(self.population)):
            self.coordinates.append([])
            for j in range(self.maxRows):
                for c in range(self.maxColumns):
                    if self.population[i][j][c] == 1:
                        self.coordinates[i].append([j, c])

    def get_collisions (self):
        self.conflicts = []

        for i in range(len(self.population)):
            self.conflicts.append([])
            for j in range(self.maxColumns):
                for m in range(self.maxRows):

                    point = self.coordinates[i]

                    if point[j][1] == point[m][1] and j != m:
                        if all(num != j for num in self.conflicts[i]):
                            self.conflicts[i].append(j)
                        if all(num != m for num in self.conflicts[i]):
                            self.conflicts[i].append(m)

                    if (point[j][0] - point[m][0]) + (point[j][1] - point[m][1]) == 0 and j != m or (point[j][0] - point[m][0]) - (point[j][1] - point[m][1]) == 0 and j != m:
                        if all(num != m for num in self.conflicts[i]):
                            self.conflicts[i].append(m)
                        if all(num != j for num in self.conflicts[i]):
                            self.conflicts[i].append(j)

    def fitness (self):
        self.ftness = []
        # self.sol = []
        for i in range(len(self.population)):
            self.ftness.append([])
            self.ftness[i].append(math.fabs(len(self.conflicts[i])-8))

            if self.ftness[i][0] == 8:
                self.done = True
                # self.sol = []
                self.sol = self.population[i]
                print(self.sol)
                for c in range(len(self.sol)):
                    for j in range(len(self.sol[c])):

                        if self.sol[c][j] == 0:
                            self.visualization+="+"
                        else:
                            self.visualization+="Q"
                        if j == 7:
                            self.visualization+="\n"
                return
                # for cb in range(8):
                #     print(self.population[i][cb])

    def mutation (self):
        for i in range(len(self.population)):
            rand = random.randrange(0, 99)

            if rand <= self.mut_prob * 100:
                if random.randrange(0, 1) == 1:
                        row1 = random.randrange(0, 8)
                        row2 = random.randrange(0, 8)
                        x = self.population[i][row1]
                        y = self.population[i][row2]
                        if x != y:
                            self.population[i][row1] = y
                            self.population[i][row2] = x
                else:
                    row = random.randrange(0, 8)
                    column = random.randrange(0, 8)
                    for c in range(8):
                        if self.population[i][row][c] == 1:
                            self.population[i][row][c] == 0
                    self.population[i][row][column] == 1

    def crossover (self):
        crossPoint1 = random.randrange(0, 8)
        crossPoint2 = random.randrange(0, 8)

        if crossPoint2 < crossPoint1:
            j = crossPoint1
            crossPoint1 = crossPoint2
            crossPoint2 = j

        for i in range(len(self.parents)):
            if random.randrange(0, 99) <= self.cross_prob * 100:
                child1 = self.population[self.parents[i][0]]
                child2 = self.population[self.parents[i][1]]
                pos1 = 0
                pos2 = 0

                for j in range(crossPoint1, crossPoint2 + 1):
                    item1 = child1[j]
                    item2 = child2[j]

                    for c in range(self.maxRows):
                        if child1[j] == item1:
                            pos1 = j
                        elif child1[j] == item2:
                            pos2 = j

                    if item1 != item2:
                        child1[pos1] = item2
                        child1[pos2] = item1 

                    for c in range(self.maxRows):
                        if child2[j] == item2:
                            pos1 = j
                        elif child2[j] == item1:
                            pos2 = j

                    if item1 != item2:
                        child2[pos1] = item1
                        child2[pos2] = item2 

                self.population.append(child1)
                self.population.append(child2)

    def selection (self):
        self.parents = []
        self.maxRoulette = 0
        new_population = []
        current = 0

        for i in range(len(self.ftness)):
            self.maxRoulette+=self.ftness[i][0]
        # print(self.maxRoulette)

        while len(new_population) < self.pop_size:
            pick = random.uniform(0, self.maxRoulette)
            for i in range(len(self.ftness)):
                current += self.ftness[i][0]
                if current > pick:
                    new_population.append(self.population[i])

        self.population = []
        self.population = new_population

    def find_pair (self):
        current = 0
        parents = []

        for i in range(len(self.ftness)):
            self.maxRoulette+=self.ftness[i][0]

        while len(self.parents) < self.maxChilds:
            pick = random.uniform(0, self.maxRoulette)
            for i in range(len(self.population)):
                current += self.ftness[i][0]
                if current > pick:
                    self.parents.append(i)

        for i in range(self.maxChilds//2):
            parentA = self.parents[random.randrange(0, len(self.parents))]
            parentB = self.parents[random.randrange(0, len(self.parents))]
            if parentA == parentB:
                parentA = self.parents[random.randrange(0, len(self.parents))]
                parentB = self.parents[random.randrange(0, len(self.parents))]
            parents.append([parentA, parentB])

        self.parents = None
        self.parents = parents

    def epoch (self):
        self.epoch_num+=1
        print(self.epoch_num)

    def solve (self):         
        self.generate()
        while self.done == False and self.epoch_num < self.maxEpochs:
            self.epoch()
            self.get_coord()
            self.get_collisions()
            self.fitness()
            if self.done == True:
                return max(self.ftness)[0], self.epoch_num, self.visualization     
            self.find_pair()
            self.crossover()
            if random.randrange(0, 99) <= self.mut_prob * 100:
                self.mutation()
            self.selection()
        return max(self.ftness)[0], self.epoch_num, self.visualization 
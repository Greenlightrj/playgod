import random


class Animal:

    """a single animal that has attributes depending on a genome"""

    def __init__(self):
        """
        genes = [[likely to get food], [resists predators], [likely to breed]]
        """
        self.genes = [['', ''], ['', ''], ['', '']]

    def genomize(self):
        """creates a random genome for Animal"""
        for i in range(3):
            self.genes[i] = [random.randint(0, 2), random.randint(0, 2)]

    def getGene(self, genetype):
        """gets a random one of the Animal's genes"""
        if random.random() < 0.5:
            return self.genes[genetype][0]
        else:
            return self.genes[genetype][1]

    def mutate(self):
        """has a 1/3 chance of mutating one of the Animal's genes"""
        if random.random() < 0.5:
            self.genes[random.randint(0, 2)][
                random.randint(0, 1)] = random.randint(0, 2)
            print self.genes


def breed(animal1, animal2):
    """mixes the genomes of two Animal and outputs a new Animal object"""
    newAnimal = Animal()
    for i in range(3):
        newAnimal.genes[i] = [animal1.getGene(i), animal2.getGene(i)]

    return newAnimal


class World:

    """the environment the Animals are in, with stats like predator density, difficulty of getting food"""

    def __init__(self, animals, pred, food):
        """creates a World and sets predator density and food difficulty from 0 to 2; takes a list of Animals that live there"""
        self.pred = pred
        self.food = food
        self.animals = animals

    def kill(self):
        """kills Animals living in the World depending on their fitness. Animals with a matching stat have 0.95 to survive, with a stat one away have 0.85 to survive, with a stat 2 away have 0.6 to survive"""
        for animal in self.animals:
            kill = 0
            foodFitness = abs(
                min(self.food - animal.genes[0][0], self.food - animal.genes[0][1]))
            predFitness = abs(
                min(self.pred - animal.genes[1][0], self.pred - animal.genes[1][1]))

            if foodFitness == 0:
                if random.random() > 0.95:
                    kill = 1
            elif foodFitness == 1:
                if random.random() > 0.85:
                    kill = 1
            elif foodFitness == 2:
                if random.random() > 0.6:
                    kill = 1

            if predFitness == 0:
                if random.random() > 0.95:
                    kill = 1
            elif predFitness == 1:
                if random.random() > 0.85:
                    kill = 1
            elif predFitness == 2:
                if random.random() > 0.6:
                    kill = 1

            if kill:
                self.animals.remove(animal)

    def mate(self):
        """chooses Animals based on their likelihood to mate and runs the breed function on them, then adds the babies to the population"""
        mateList = []

        for animal in self.animals:
            mateFitness = max(animal.genes[2])
            if mateFitness == 0:
                if random.random() > 0.5:
                    mateList.append(animal)
            elif mateFitness == 1:
                if random.random() > 0.65:
                    mateList.append(animal)
            elif mateFitness == 2:
                if random.random() > 0.8:
                    mateList.append(animal)

        for i in range(len(mateList) / 2):
            newAnimal = breed(random.choice(mateList), random.choice(mateList))
            self.animals.append(newAnimal)


animalList = []
for i in range(100):
    animalList.append(Animal())
    animalList[i].genomize()

environment = World(animalList, 2, 1)
print len(environment.animals)

for i in range(50):
    environment.kill()
    print len(environment.animals)
    environment.mate()
    print len(environment.animals)

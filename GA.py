import numpy as np
import pygame
import time
import operator        

class Bot(object):
    
    def __init__(self, dnaSize):
        self.dnaSize = dnaSize
        self.dna = list()
        self.distance = 0.
        self.posx = 0
        self.posy = 0
        self.colour = (255,0,0)             #default colour of bot
        for i in range(self.dnaSize):
            self.dna.append(np.random.randint(0,4))
    
    def move(self, speedx, speedy):
        self.posx += speedx
        self.posy += speedy

class Environment(object):
    
    def __init__(self):
        self.width = 500                    #width in pixels of the game screen
        self.height = 500                   #height in pixels of the game screen
        self.nRows = 30                     #number of rows in our maze
        self.nColumns = 30                  #number of columns in our maze
        self.populationSize = 50            #size of the population of bots that try and solve the maze
        self.dnaSize = 200                  #dna length for bots, every gene is responsible for each move
        self.bestCopied = 10                #how many best bots we take from our previous generation and mix them
        self.mutationRate = 0.2             #chances that new bot will be completely mutated
        self.offspringMutationRate = 0.15   #chances that a single gene will be mutated
        self.waitTime = 0.1                 #wait time in seconds between moves
        self.slowdownRateOfChange = 0.025   #by how much we change wait time (click s to increase and f to decrease)
        self.wallRatio = 0.3                #walls to all cells ratio in our maze
        
        self.population = list()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.maze = np.zeros((self.nRows, self.nColumns))
        
        if self.bestCopied > self.populationSize:
            self.bestCopied = self.populationSize

        # 1 is for Wall and 0 is for empty square.
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if np.random.rand() < self.wallRatio:
                    self.maze[i][j] = 1
                else:
                    self.maze[i][j] = 0
                
        for i in range(min(3, self.nRows)):
            for j in range(min(3, self.nColumns)):
                self.maze[i][j] = 0
                
        for i in range(self.populationSize):
            bot = Bot(self.dnaSize)
            self.population.append(bot)
        
        
    def drawMaze(self):
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
        self.screen.fill((0,0,0))
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (j*cellWidth, i*cellHeight, cellWidth, cellHeight))
                    
        for i in range(self.populationSize):
            bot = self.population[i]
            pygame.draw.rect(self.screen, bot.colour, (bot.posx * cellWidth, bot.posy*cellHeight, cellWidth, cellHeight))
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.waitTime -= self.slowdownRateOfChange
                    if self.waitTime < 0:
                        self.waitTime = 0
                    print('Wait time lowered to {:.3f}'.format(self.waitTime))
                elif event.key == pygame.K_s:
                    self.waitTime += self.slowdownRateOfChange
                    print('Wait time increased to {:.3f}'.format(self.waitTime))
        
    
    def step(self, nAction):
        for bot in self.population:
            if bot.dna[nAction] == 0:				# Move Left
                if bot.posy > 0:
                    if self.maze[bot.posy - 1][bot.posx] == 0:
                        bot.move(0, -1)
            elif bot.dna[nAction] == 1:				# Move Right
                if bot.posy < self.nRows - 1:
                    if self.maze[bot.posy + 1][bot.posx] == 0:
                        bot.move(0, 1)
            elif bot.dna[nAction] == 2:				# Move Down
                if bot.posx < self.nColumns - 1:
                    if self.maze[bot.posy][bot.posx + 1] == 0:
                        bot.move(1, 0)
            elif bot.dna[nAction] == 3:				# Move Up
                if bot.posx > 0:
                    if self.maze[bot.posy][bot.posx - 1] == 0:
                        bot.move(-1, 0)
            bot.distance = pow(pow(bot.posx,2) + pow(bot.posy, 2), 0.5)          
            
        
        self.drawMaze()
        time.sleep(self.waitTime)
        
    
    def mix(self, dna1, dna2):
        offspring = Bot(self.dnaSize)
        for i in range(self.dnaSize):
            if np.random.rand() > self.offspringMutationRate:
                if np.random.randint(0,2) == 0:
                    offspring.dna[i] = dna1[i]
                else:
                    offspring.dna[i] = dna2[i]
            else:
                offspring.dna[i] = np.random.randint(0,4)
                    
        return offspring
    
    def createNewPopulation(self, gen):
        
        sortedPopulation = sorted(self.population, key = operator.attrgetter('distance'), reverse = True)
        self.population.clear()
        
        bestResult = sortedPopulation[0].distance
        available = self.populationSize - self.bestCopied
        
        for i in range(self.bestCopied):
            best = sortedPopulation[i]
            best.posx = 0
            best.posy = 0
            best.distance = 0.
            best.colour = (255, 255, 0)
            self.population.append(best)
        
        for i in range(available):
            new = Bot(self.dnaSize)
            if np.random.rand() > self.mutationRate:
                p1rnd = np.random.randint(0, self.bestCopied)
                parent1 = sortedPopulation[p1rnd]
                
                p2rnd = np.random.randint(0, self.bestCopied)
                while p2rnd == p1rnd:
                    p2rnd = np.random.randint(0, self.bestCopied)
                parent2 = sortedPopulation[p2rnd]
                
                dna1 = parent1.dna
                dna2 = parent2.dna
            
                new = self.mix(dna1, dna2)
                new.colour = (0,0,255)
                
            self.population.append(new)
            
        print('Generation: ' + str(gen) + ' Population Size: ' + str(len(self.population)) + ' Current Leader Distance: {:.2f}'.format(bestResult))

 
env = Environment()
nAction = 0
gen = 0
while True:
    if nAction < env.dnaSize:
        env.step(nAction)
        nAction += 1
    else:
        gen += 1
        nAction = 0
        env.createNewPopulation(gen)
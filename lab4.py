'''
Created on Apr 5, 2020

@author: Claudiu
'''
from random import uniform
from random import randint
from random import choice


class Chromosome:
    def __init__(self, problParam = None):

        self.__problParam = problParam
        self.__repres = []        
        self.__fitness = 0.0
        
        
        numberOfCities = problParam['numberOfCities']
        pathOk = False
        while pathOk == False:
            itemsPossible = [i for i in range (problParam['numberOfCities'])]
            self.__repres.clear()
            while len(self.__repres) != numberOfCities:
                nextItem = choice(itemsPossible)
                itemsPossible.remove(nextItem)
                self.__repres.append(nextItem)
            
            pathOk = self.condition(self.__repres)
        
        
        #initializare reprezentare pe baza oraselor legate intre ele
        #ca sa ne asiguram ca nu repetam numere vom extrage dintr-o lista initial plina cu toate orasele pe rand cate un oras
        #mat = problParam['matriceGraf']
        #n = problParam['numberOfCities']
        #freq = []
        #primul oras il alegem random iar apoi alegem din vecinii lui ( ca sa fie o solutie valida )
        #randomNumber = randint(0,numberOfCities - 1)
        #self.__repres.append(randomNumber)
        #freq.append(randomNumber)
        #while len(self.__repres) != numberOfCities:
         #   lastItemAdded = self.__repres[-1]
          #  vecinii =[]
           # for i in range(n):
            #    if mat[lastItemAdded][i] > 0:
             #       vecinii.append(i)
            #nextChoice = choice(vecinii)
            #while nextChoice in freq:
            #    nextChoice = choice(vecinii)
            #self.__repres.append(nextChoice)
            #freq.append(nextChoice)
    @property
    def repres(self):
        return self.__repres
    
    #conditia sa existe drum intre toate orasele
    def condition(self,list):
        mat = self.__problParam['matriceGraf']
        for i in range(self.__problParam['numberOfCities'] - 1):
            if mat[list[i]][list[i+1]] == 0:
                return False
        #inclusiv intre ultimul oras si cel in care ne intoarcem
        if matrice[list[len(matrice) - 1]][list[0]] == 0:
            return False
        return True
    
    @property
    def fitness(self):
        return self.__fitness 
    
    @repres.setter
    def repres(self, l = []):
        self.__repres = l 
    
    @fitness.setter 
    def fitness(self, fit = 0.0):
        self.__fitness = fit 
    
    
    #incrucisare ordonata
    def crossover(self, c):
        
        r1 = randint(0, len(self.__repres) - 1)
        r2 = randint(0,len(self.__repres) - 1)
        while r1 == r2:
            r1 = randint(0, len(self.__repres) - 1)
            r2 = randint(0,len(self.__repres) - 1)
        if r1 > r2:
            aux = r1
            r1 = r2
            r2 = aux
            
        newrepres = [-1 for i in range (len(self.__repres))]
        #prima parte din incrucisarea ordonata
        for i in range(r1,r2):
            newrepres[i] = self.__repres[i]
        
        #pentru a verifica unde suntem in al 2-lea parinte
        indexC = r2
        #pentru a verifica unde suntem in destinatie
        indexN = r2;
        #cate elemente am pus pana acum
        lgNew = r2 - r1
        
        #cat timp nu am adaugat toate elementele in reprezentantul nou
        while lgNew != len(newrepres):
            while c.__repres[indexC] in newrepres:
                indexC += 1
                if indexC > len(c.__repres) - 1:
                    indexC = 0
            newrepres[indexN] = c.__repres[indexC]
            lgNew += 1
            indexN += 1
            indexC += 1
            if indexC > len(newrepres) -1:
                indexC = 0
            if indexN > len(newrepres) - 1:
                indexN = 0
        offspring = Chromosome(self.__problParam)
        offspring.repres = newrepres
        return offspring
    #mutatie prin inversare
    def mutation(self):
        #cu o probabilitate de 30% 
        pm = 3
        prob = randint(1,10)
        if prob <= pm:
            pos1 = randint(0, len(self.__repres) - 1)
            pos2 = randint(0, len(self.__repres) - 1)
            
            if pos1 > pos2:
                aux = pos1
                pos1 = pos2
                pos2 = aux
            
            invertedElements = []
            for i in range(pos1,pos2):
                invertedElements.insert(0, self.__repres[i])
            for i in range(pos1,pos2):
                self.__repres[i] = invertedElements.pop(0)
                
        
    def __str__(self):
        return '\nChromo: ' + str(self.__repres) + ' has fit: ' + str(self.__fitness)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness



class GA:
    def __init__(self, param = None, problParam = None):
        self.__param = param
        self.__problParam = problParam
        self.__population = []
        
    @property
    def population(self):
        return self.__population
    
    def initialisation(self):
        for _ in range(0, self.__param['popSize']):
            c = Chromosome(self.__problParam)
            self.__population.append(c)
    
    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__problParam['function'](c.repres,self.__problParam['matriceGraf'])
            
    def bestChromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if (c.fitness < best.fitness):
                best = c
        return best
        
   

    def selection(self):
        pos1 = randint(0, self.__param['popSize'] - 1)
        pos2 = randint(0, self.__param['popSize'] - 1)
        if (self.__population[pos1].fitness < self.__population[pos2].fitness):
            return pos1
        else:
            return pos2 
        
    #conditia sa existe drum intre toate orasele ( verificam si aici pentru cand facem mutation si crossover
   
    def condition(self,list):
        mat = self.__problParam['matriceGraf']
        for i in range(self.__problParam['numberOfCities'] - 1):
            if mat[list[i]][list[i+1]] == 0:
                return False
        #inclusiv intre ultimul oras si cel in care ne intoarcem
        if matrice[list[len(matrice) - 1]][list[0]] == 0:
            return False
        return True
    
    
    
    def oneGeneration(self):
        newPop = []
        for _ in range(self.__param['popSize']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            #descendent nou
            off = p1.crossover(p2)
            off.mutation()
            #cat timp nu indeplineste conditia necesara ( drum intre toate orasele vecine ) 
            while self.condition(off.repres) == False:
               off = p1.crossover(p2)
               off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()



matrice =[]
numberOfCities = 0
def readFromFile():
    f = open("hard_06_tsp.txt","r")
    global numberOfCities
    global matrice
    numberOfCities = int(f.readline())
    content = f.readlines()
    for line in range(0,numberOfCities):
        matrice.append([])
        elements = content[line].split(',')
        for element in elements:
            matrice[line].append(int(element))

def costDrum(list,mat):
    sum = 0
    for i in range(len(list) - 1):
        sum += mat[list[i]][list[i+1]]
    sum += mat[list[len(list) - 1]][list[0]]
    return sum



def main():    
    global matrice
    global numberOfCities
    
    readFromFile()
    
    # initialise de GA parameters
    gaParam = {'popSize' : 100, 'noGen' : 10000}
    # problem parameters
    problParam = { 'matriceGraf':matrice , 'numberOfCities' : numberOfCities , 'function':costDrum}
    
    print(costDrum([3,2,1,0],matrice))

    ga = GA(gaParam, problParam)
    ga.initialisation()
    ga.evaluation()
    best = ga.bestChromosome()
    
    for iteration in range(gaParam['noGen']):
        ga.oneGeneration()
        best = ga.bestChromosome()
        print(iteration)
        print(str(best))
    
    #file = open("hard_02.txt","w+")
    #file.write(str(best))
    #file.close()
    

main()

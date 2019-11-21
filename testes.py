import numpy as np
import matplotlib.pyplot as plt
import random
import copy
import sys
from operator import add 
from functools import reduce 

plt.ion()
pause = 0.5

#Definição do mapa 
mapaRange = 20
mapa = np.zeros([mapaRange,mapaRange])
#Ex: 10 X 10
""" [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]  
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0]
    [0,0,0,0,0,0,0,0,0,0] """
alvo = [0,2]
mapa[alvo[0],alvo[1]] = -1

#Define a classe de particulas
class Particle:
  def __init__(self):
    #self.rnd = random.Random(seed)
    self.position = [random.randint(0,mapaRange-1) , random.randint(0,mapaRange-1)]
    self.velocity = [2,2]
    self.pbest = copy.copy(self.position)

#Criando particulas
def cria_particulas(N_particulas):
    particulas = [Particle() for i in range(N_particulas)]
    return particulas

def define_gbest_inical(particulas): 
    distances = [distancia_do_alvo(particula.position) for particula in particulas]
    maximo = max(distances) 
    index = distances.index(maximo)
    gbest_inicial = particulas[index].position
    return gbest_inicial

def atualiza_pbest(pbest_antigo,particula_position):
    if distancia_do_alvo(pbest_antigo) > distancia_do_alvo(particula_position):
        return particula_position
    else:
        return pbest_antigo
    
def atualiza_gbest(gbest_antigo,particula_position):
    if distancia_do_alvo(gbest_antigo) > distancia_do_alvo(particula_position):
        return particula_position
    else:
        return gbest_antigo

###########   Funcoes para a mudanca do mapa

#Atualiza o mapa antes do movimento da particula
def atualiza_mapa_antes(particulas):
    for particula in particulas:
        mapa[int(particula.position[0]),int(particula.position[1])] = 1

#Atualiza o mapa depois do movimento da particula
def atualiza_mapa_depois(particulas):
    for particula in particulas:
        mapa[int(particula.position[0]),int(particula.position[1])] = 0

def distancia_do_alvo(particula_position):
    distancia = np.sqrt( (alvo[0] - particula_position[0])**2 + (alvo[1] - particula_position[1])**2 )
    return distancia

def finaliza(particulas):
    distances = [distancia_do_alvo(particula.position) for particula in particulas]
    soma = reduce(add,distances)
    print('Soma das distancias:',soma)
    if soma < 8:
        return True
    else: 
        return False

def PSO(N_particulas,max_epochs,w,c1,c2):
    particulas = cria_particulas(N_particulas)
    epoch = 0
    gbest = define_gbest_inical(particulas)

    while epoch < max_epochs:
        print('===================================')
        print('Época: ',str(epoch))
        for particula in particulas: 
            for i in range(0,2,1): 

                particula.velocity[i] = ( (w * particula.velocity[i]) +
                (c1 * (particula.pbest[i] -
                particula.position[i])) +  
                (c2 * (gbest[i] -
                particula.position[i])) )  

            for i in range(0,2,1): 
                particula.position[i] += particula.velocity[i]

            #Ajusta o pbest de acordo com a distancia nova
            particula.pbest = atualiza_pbest(particula.pbest,particula.position)

            #Ajusta o gbest de acordo com a distancia nova
            gbest = atualiza_gbest(gbest,particula.position)
            print('Gbest: ',gbest)
            print('Distancia: %.4f\n' % distancia_do_alvo(gbest))

        if finaliza(particulas):
            print('----------')
            print('Achado')
            print('----------')
            break

            
        atualiza_mapa_antes(particulas)
        title = 'Época: ' + str(epoch) 
        plt.title(title)
        plt.axis('off')
        plt.imshow(mapa,origin='upper')
        plt.show()
        plt.pause(pause) 
        atualiza_mapa_depois(particulas)
        title = 'Época: ' + str(epoch)
        plt.title(title)
        epoch += 1

w = 0.4   # inercial
c1 = 0.8  # cognitivo
c2 = 0.4  # social 
PSO(10,50,w,c1,c2)
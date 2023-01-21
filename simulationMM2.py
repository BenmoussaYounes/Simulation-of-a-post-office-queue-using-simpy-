from random import random
import simpy
import math

from ananlytiquesPerformances import ananlytiquesPerfom
from graphicPlotting import graphic

"""
 A Post Office has 2 office to
   serve client in parallel.

   Client have to request one of the 2 office. When they got one, they
   can start the service processes and wait for it to finish (which
   takes ``temp_service`` minutes).

  """

# Duree de la simulation
sim_time = 1

# Serveur
Serveur_Guichet_1 = 1
Serveur_Guichet2 = 1

# Serveurs
client_servie_G1 = 0
client_servie_G2 = 0


stat = {'client': [],  # client number
        'QArrivedTime': [],  # client arrive time
        'QSpendtime': [],  # time in the queue
        'Stime': [],  # time in the system
        'Qtime': []
        }


def getNext_arrive_departure_Time(lmbd):
    # λ
    r = random()
    # print('Lambda : ', (-1 / lmbd) * math.log(r))
    return (-1 / lmbd) * math.log(r)

def choi_de_guichet(probability):
    r = random()
    #print('probs : ', probability)
    #print('random value : ', r)
    if r < probability:
        return 1
    else:
        return 2


class Guichet1(object):
    """  Office number 1  """

    def __init__(self,env, mu):
        self.env = env
        self.guichet_younes = simpy.Resource(env, Serveur_Guichet_1)
        self.mu = mu


    def service(self, nom_client):
        temp_darriver = self.env.now
        temp_de_service = getNext_arrive_departure_Time(self.mu)
        temp_departure = temp_de_service + self.env.now
        stat['client'].append((nom_client, round_down(temp_darriver), round_down(temp_departure)))
        #stat['Stime'].append(temp_departure - stat['QArrivedTime'][nom_client-1][1]) # Queue Time + System time
        stat['Stime'].append(temp_de_service)
        yield self.env.timeout(temp_de_service)



class Guichet2(object):
    """" Office number 2 """

    def __init__(self, env, mu):
        self.env = env
        self.guichet_ali = simpy.Resource(env, Serveur_Guichet2)
        self.mu = mu

    def service(self, nom_client):
        temp_darriver = self.env.now
        temp_de_service = getNext_arrive_departure_Time(self.mu)
        temp_departure = temp_de_service + self.env.now
        stat['client'].append((nom_client, round_down(temp_darriver), round_down(temp_departure)))
        stat['Stime'].append(temp_de_service)
        yield self.env.timeout(temp_de_service)





def client_guichet1(env, name, guichet):
    global client_servie_G1
    print(f'Client {name} est entre dans la fille dattend Guichet 1 {env.now}')
    stat['QArrivedTime'].append((name, env.now))
    with guichet.guichet_younes.request() as request:
        yield request
        print(f'Client {name} est arriver au guichet 1 ')
        yield env.process(guichet.service(name))
        print(f'client {name} est servie au guichet 1 {env.now}')
        client_servie_G1 +=1


def client_guichet2(env, name, guichet):
    global client_servie_G2
    print(f'Client {name} est entre dans la fille dattend  Guichet 2 {env.now}')
    stat['QArrivedTime'].append((name, env.now))
    with guichet.guichet_ali.request() as request:
        yield request
        print(f'Client {name} est arriver au guichet 2 ')
        yield env.process(guichet.service(name))
        print(f'client {name} est servie  au guichet 2 {env.now}')
        client_servie_G2 += 1




def process(env, lmbda, mu):
     guichet1 = Guichet1(env, mu)
     guichet2 = Guichet2(env, mu)
     i = 1
     while True:
         yield env.timeout(getNext_arrive_departure_Time(lmbda))
         choi = choi_de_guichet(1 / 2)
         if choi == 1:
             env.process(client_guichet1(env, i, guichet1))
         if choi == 2:
             env.process(client_guichet2(env, i, guichet2))
         if getNext_arrive_departure_Time(lmbda) + env.now > sim_time:
            print('-------------------------------')
            print('--- Feremture de la poste ( Traitemment de la file seulement) ---')
            break
         i += 1




def run_sim_mm2():
    global client_servie_G1, client_servie_G2

    lmbda = 5  # Taux moyenne d'arriver
    mu = 6  # taux moyenne de service

    client_served_list = []  # Served Client list of each simulation iteration
    Stime_list = []  # List of System Queue time of each simulation iteration
    sim_index_list = []  # index of simulation iteration



    print('Overture de Bureau De Poste : ')
    print('-------------------------------')
    iteration_number = 0
    while iteration_number < 100:
      env = simpy.Environment()
      env.process(process(env, lmbda, mu))
      env.run()
      print('-------------------------------')
      print('Fin de Journée ')
      #print('Client Servie G1: ', client_servie_G1)
      #print('Client Servie G2: ', client_servie_G2)
      print('Client Servie Guichet Younes : ', client_servie_G1)
      print('Client Servie Guichet Ali : ', client_servie_G2)
      print('Client Servie : ', client_servie_G2 + client_servie_G1)
      client_served_list.append(client_servie_G2+client_servie_G1)
      client_servie_G1 = 0
      client_servie_G2 = 0
      sim_index_list.append(iteration_number)
      Stime_list.append(sum(stat['Stime']))
      stat['Stime'] = []
      iteration_number += 1
      print('-------------------------------')
    #print('totale client', client_served_list)
    print("Empirical performances :")
    print('Average number of clients in the system : ',
           sum(client_served_list) / iteration_number)  # Le nombre moyen de clients dans le système

    print('Average wait time in the system : ',
           sum(Stime_list) / iteration_number)  # Temp d’attente moyen dans le système

    graphic().plot_v2(sim_index_list, client_served_list, Stime_list)
    ananlytiquesPerfom(lmbda, mu).showPerforamnces()

def round_down(number):
    return math.floor(number * 100) / 100






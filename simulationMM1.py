import random
import math

import simpy

from graphicPlotting import graphic
from  ananlytiquesPerformances import ananlytiquesPerfom


Nombre_Serveur = 1
lmbda = 5  # Taux moyenne d'arriver
mu = 6  # taux moyenne de service
temp_Sim = 1

clients_servie = 0

stat = {'client': [],  # client number
        'QArrivedTime': [],  # client arrive time
        'QSpendtime': [],  # time in the queue
        'Stime': [],  # time in the system
        'Qtime': []

        }


class BureauDePoste:

    def __init__(self, env, nombre_serveur, mu):
        self.env = env
        self.nombre_Serveur = simpy.Resource(env,
                                             nombre_serveur)  # Ressource critique en cas d'utilisation client rejoin la file
        self.mu = mu

    def service(self, client):
        global stat
        # print('Time rn :',env.now)
        temp_darriver = self.env.now
        temp_service = self.getNext_arrive_departure_Time(mu)
        print(f'Temp de service de clien : {client:.0f}', round_down(temp_service))
        temp_departure = temp_service + self.env.now
        # print('temp de partire ',temp_departure)
        stat['client'].append((client, round_down(temp_darriver), round_down(temp_departure)))
        stat['Qtime'].append(temp_darriver - self.env.now)
        stat['Stime'].append(temp_service)
        yield self.env.timeout(
            temp_service)  # on doit utilise le mot clee yieled car il sagit d'un generator Simpy bib fonc comme ca

    # print(f"Client numero {client} est Servie l'heur {self.env.now}")

    def getNext_arrive_departure_Time(self, lmbd):
        # λ
        r = random.random()
        # print('Lambda : ', (-1 / lmbd) * math.log(r))
        return (-1 / lmbd) * math.log(r)


def client(env, name, BureauDePoste):
    global clients_servie
    print(f"Client {name} en file d'attend de la poste en {env.now:.2f}")
    stat['QArrivedTime'].append((name, env.now))
    with BureauDePoste.nombre_Serveur.request() as request:
        yield request
        print(f"Client {name} est arriver au guichet en temp : {env.now:.2f}")
        yield env.process(BureauDePoste.service(name))
        print(f"Client {name} est servie en temp : {env.now:.2f}")
        clients_servie += 1


def process(env, nombre_serveur, mu, lmbda):
    bureauDePoste = BureauDePoste(env, nombre_serveur, mu)
    i = 1
    env.process(client(env, i, bureauDePoste))
    while True:
        yield env.timeout(bureauDePoste.getNext_arrive_departure_Time(lmbda))
        i += 1
        env.process(client(env, i, bureauDePoste))


def Start():
    global clients_servie, stat, lmbda, mu
    client_served_list = []  # Served Client list of each simulation iteration
    Stime_list = []  # List of System Queue time of each simulation iteration
    sim_index_list = []  # index of simulation iteration
    print('Overture de Bureau De Poste : ')
    print('-------------------------------')
    iteration_number = 0
    while iteration_number < 100:
        env = simpy.Environment()
        env.process(process(env, Nombre_Serveur, mu, lmbda))
        env.run(until=temp_Sim)
        client_served_list.append(clients_servie)
        sim_index_list.append(iteration_number)
        Stime_list.append(sum(stat['Stime']))
        clients_servie = 0
        stat['Stime'] = []
        iteration_number += 1
        print('-------------------------------')
    # print('Clint par jour : '+str(clients_servie))
    # print('STAT ')
    # print(stat['client'])
    print("Empirical performances :")
    print('Average number of clients in the system : ',
          sum(client_served_list) / iteration_number)  # Le nombre moyen de clients dans le système

    print('Average wait time in the system : ',
          sum(Stime_list) / iteration_number)  # Temp d’attente moyen dans le système

    #print('Stime_list', Stime_list)
    #print('Client_List', client_served_list)
    ananlytiquesPerfom(lmbda, mu).showPerforamnces()


    graphic().plot_v1(sim_index_list, client_served_list, Stime_list)


def round_down(number):
    return math.floor(number * 100) / 100


'''

print("Average time in the queue : ")
print("Average time in the system : ")
print("Average number of clients in the queue : ")
print("Average number of clients in the system : ")
'''

# (10, 1.8955946429779713, 2.101066865450824)

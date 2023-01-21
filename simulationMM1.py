import random
import math

import simpy

from graphicPlotting import graphic
from  ananlytiquesPerformances import ananlytiquesPerfom



Nombre_Guichet = 1

temp_Sim = 1

clients_servie = 0

stat = {'client': [],  # client number
        'QArrivedTime': [],  # client arrive time
        'QSpendtime': [],  # time in the queue
        'Stime': [],  # time in the system
        'Qtime': []
        }


class BureauDePoste(object):
    """A Post Office has a limited number of office  (``Nombre_Guichet``) to
     serve client in parallel.

     Client have to request one of the office. When they got one, they
     can start the service processes and wait for it to finish (which
     takes ``temp_service`` minutes).

    """
    def __init__(self, env, mu):
        self.env = env
        self.Nombre_Guichet = simpy.Resource(env,
                                             Nombre_Guichet)  # Ressource critique en cas d'utilisation client rejoin la file
        self.mu = mu

    def service(self, client):
        """The service processes. It takes a ``client`` processes and serve him."""
        global stat
        # print('Time rn :',env.now)
        temp_darriver =   self.env.now
        temp_service = self.getNext_arrive_departure_Time(self.mu)
        #print(f'Temp de service de clien {client:.0f}', ':', temp_service)
        temp_departure = temp_service + self.env.now
        # print('temp de partire ',temp_departure)
        stat['client'].append((client, round_down(temp_darriver), round_down(temp_departure)))
        #stat['Qtime'].append(temp_darriver - self.env.now)
        #stat['Stime'].append(temp_departure - stat['QArrivedTime'][client-1][1]) Queue Time + System time
        stat['Stime'].append(temp_service)
        yield self.env.timeout(
            temp_service)  # on doit utilise le mot clee yieled car il sagit d'un generator Simpy bib fonc comme ca

    def getNext_arrive_departure_Time(self, lmbd):
        # λ
        r = random.random()
        # print('Lambda : ', (-1 / lmbd) * math.log(r))
        return (-1 / lmbd) * math.log(r)

def client(env, name, BureauDePoste):
    """The client process (each client has a name ``number``) arrives at the Office (Guichet)
       (``Nombre_Guichet``) and requests a office (Guichet).

       It then starts the serve process, waits for it to finish and
       leaves to never come back ...

       """

    global clients_servie, clients_en_Fill
    print(f"Client {name} en file d'attend de la poste en {env.now:.3f}")
    stat['QArrivedTime'].append((name, env.now))
    with BureauDePoste.Nombre_Guichet.request() as request:
        yield request
        print(f"Client {name} est arriver au guichet en temp : {env.now:.3f}")
        yield env.process(BureauDePoste.service(name))
        print(f"Client {name} est servie en temp : {env.now:.3f}")
        clients_servie += 1


def process(env, mu, lmbda):
    """Create an office, a number of initial client and keep increasing  client as long as the simulation is running
        approx. every ``t_inter`` minutes."""

     # Create the Post office ( Creaation du Bureau de Poste )
    bureauDePoste = BureauDePoste(env, mu)  # mu pour calculer le temp de service de ce client
    i = 1  # nombre de client initiale
    env.process(client(env, i, bureauDePoste))
    while env.now < temp_Sim:
      yield env.timeout(bureauDePoste.getNext_arrive_departure_Time(lmbda))  # lmbda pour calculer le temp de d'arrive pour ce client
      if bureauDePoste.getNext_arrive_departure_Time(lmbda)+env.now > temp_Sim:
          print('-------------------------------')
          print('Fin de journée Arrêt de la réception')
          break
      i += 1
      env.process(client(env, i, bureauDePoste))

def run_sim_mm1():
    global clients_servie, stat
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
        env.process(process(env, mu, lmbda))
        env.run()
        print('-------------------------------')
        print('Fermeture de la Poste')
        print(f'{clients_servie} Client Servie')
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
    ananlytiquesPerfom(lmbda, mu).showPerforamnces()
    graphic().plot_v1(sim_index_list, client_served_list, Stime_list)
    #print('Stime_list', Stime_list)
    #print('Client_List', client_served_list)


def round_down(number):
    return math.floor(number * 100) / 100


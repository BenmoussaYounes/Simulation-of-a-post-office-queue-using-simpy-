import numpy as np
import random
import math




class simulationM1:

    def runtest(self):
      a,b,c=self.simulate(5,6,20)
      print(c)
      print('a',a)


    # duration maxT simulation test time duration
    # λ  c est le temp moyenne d'arrive
    # mu c est le temp moyenne de service
    def simulate(self,lmbda,mu,duration):
        print('START')
        clock = 0
        clientNumber = 0  # client number is customers number in the system
        nb = {}
        arv_time = self.getNext_arrive_departure_Time(lmbda)
        dep_time = duration  # departure check if the test duration is still correct
        arv_list = []  # Arrival times
        dep_list = []  # Departure times
        stats = []
        arv_number = 0
        dep_number = 0  # Arrivals/Departures number
        while clock < duration:
         stats.append((clock,arv_number))  # add event id and time
         print('stat ',stats)
         if arv_time < dep_time:  # arrival event
             arv_number += 1 # = arv_number + 1
             arv_list.append(arv_time)
             nb[clientNumber] = (nb[clientNumber] if clientNumber in nb else 0) + arv_time - clock
             clientNumber +=1
             clock = arv_time
             arv_time = clock + self.getNext_arrive_departure_Time(lmbda)
             if clientNumber == 1 :
              dep_time = clock + self.getNext_arrive_departure_Time(mu)
         else:  # departure event
             dep_list.append(dep_time)
             if clientNumber >= 0 : nb[clientNumber] = (nb[clientNumber] if clientNumber in nb else 0) + dep_time - clock
             clientNumber = clientNumber - 1
             clock = dep_time
             dep_time = clock + self.getNext_arrive_departure_Time(mu) if clientNumber > 0 else duration

        return arv_list,dep_list,stats




    def getNext_arrive_departure_Time(self, lmbd):
        # λ
        r = random.random()
        #print('Lambda : ', (-1 / lmbd) * math.log(r))
        return (-1 / lmbd) * math.log(r)



    def test(self,lmbda,mu,duration):
        print('START')
        clock = 0
        clientNumber = 0  # client number is customers number in the system
        nb = {}
        arv_time = self.getNext_arrive_departure_Time(lmbda)
        dep_time = duration  # departure check if the test duration is still correct
        arv_list = []  # Arrival times
        dep_list = []  # Departure times
        stats = []
        arv_number = 0
        dep_number = 0  # Arrivals/Departures number
        while clock < duration:
            stats.append((clock, arv_number))  # add event id and time
            print('stat ', stats)
            if arv_time < dep_time:  # arrival event
                arv_number += 1  # = arv_number + 1
                arv_list.append(arv_time)
                nb[clientNumber] = (nb[clientNumber] if clientNumber in nb else 0) + arv_time - clock
                clientNumber += 1
                clock = arv_time
                arv_time = clock + self.getNext_arrive_departure_Time(lmbda)
                if clientNumber == 1:
                    dep_time = clock + self.getNext_arrive_departure_Time(mu)
            else:  # departure event
                dep_list.append(dep_time)
                if clientNumber >= 0: nb[clientNumber] = (nb[
                                                              clientNumber] if clientNumber in nb else 0) + dep_time - clock
                clientNumber = clientNumber - 1
                clock = dep_time
                dep_time = clock + self.getNext_arrive_departure_Time(mu) if clientNumber > 0 else duration

        return arv_list, dep_list, stats


    def younes(self,lmbda,mu,duration):
        print('START')
        clock = 0
        clientNumber = 1  # client number is customers number in the system
        nb = {}
        arv_time = self.getNext_arrive_departure_Time(lmbda)
        dep_time = duration  # departure check if the test duration is still correct
        arv_list = []  # Arrival times
        dep_list = []  # Departure times
        stats = []
        arv_number = 0
        dep_number = 0  # Arrivals/Departures number
        while clock < duration:
            clientNumber += 1
            arv_list.append(arv_time)
            print('ARV TIME 1 : ', arv_time)
            print('Clock', clock)
            dep_time = self.getNext_arrive_departure_Time(mu)
            clock = arv_time
            print('DEP TIME ', dep_time)
            arv_time = clock+self.getNext_arrive_departure_Time(lmbda)
            print('ARV TIME ', arv_time)












'''
        while arv_number > dep_number :
            stats.append((clock, clientNumber))
            dep_list.append(dep_time)
            if clientNumber >= 0: nb[clientNumber] = (nb[clientNumber] if clientNumber in nb else 0) + dep_time - clock
            clientNumber = clientNumber - 1
            clock = dep_time
            dep_time = clock + self.getNext_arrive_departure_Time(mu) if clientNumber > 0 else duration
'''



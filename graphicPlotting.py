import matplotlib.pyplot as plt
import numpy as np



class graphic:

    def plot_v1(self, x, y1, y2):


        #print('Y : ', y)
        plt.figure()
        plt.subplot(211)
        plt.plot(x, y1)
        #plt.plot(x, y, 'k', label='clients served', color='green')
        plt.ylabel('Clients Numbers')
        plt.title('M / M / 1  - Queue system')
        plt.subplot(212)
        plt.ylabel('Average wait time')
        plt.xlabel('Sim Number')
        plt.plot(x, y2)
        plt.show()

    def plot_v2(self, x, y1, y2):
        # print('Y : ', y)
        plt.figure()
        plt.subplot(211)
        plt.plot(x, y1)
        # plt.plot(x, y, 'k', label='clients served', color='green')
        plt.ylabel('Clients Numbers')
        plt.title('M / M / 2  - Queue system')
        plt.subplot(212)
        plt.ylabel('Average wait time')
        plt.xlabel('Sim Number')
        plt.plot(x, y2)
        plt.show()
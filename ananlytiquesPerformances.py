


class ananlytiquesPerfom:

    def __init__(self, lmbda, mu):
        self.p = None
        self.l = None
        self.w = None
        self.lmbda = lmbda
        self.mu = mu


    def  showPerforamnces(self):

        print('-------------------------------')
        print('Ananlytiques Performances')
        self.get_p()
        self.get_l()
        self.get_w()


    def get_p(self):
        self.p = self.lmbda/self.mu
        #print('p : ', self.lmbda/self.mu)  # Taux d’utilisation du serveur

    def get_l(self):
        self.l = self.p/(1-self.p)
        print('l :', self.p/(1-self.p))  # Nombre moyen des clients dans le système

    def get_w(self):
        self.w = self.l/self.lmbda
        print('W : ', self.l/self.lmbda)  #  Temps moyen d’attente dans le système
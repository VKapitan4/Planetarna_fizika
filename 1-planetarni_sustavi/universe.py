import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Planet:
    def __init__(self, m, naziv):
        self.m = m
        self.naziv = naziv
        self.F = []
        self.a = []
        self.v = []
        self.r = []
    
    def set_initial_conditions(self, r0, v0):
        self.v0 = np.array(v0)
        self.r0 = np.array(r0)
        self.F = [np.array([0,0])]
        self.a = [np.array([0,0])]
        self.v = [self.v0]
        self.r = [self.r0]

    def reset(self):
        self.__init__(self.m, self.naziv)

    def generate_initial_velocity_1(self, r0, T):     # pretpostavka kružne putanje
        return (2*np.pi*r0)/T

    def generate_initial_velocity_2(self, a, r, m_zvijezda):   #pretpostavka eliptične putanje
        G = 6.67430 * 10**(-11)
        return np.sqrt(G*(m_zvijezda+self.m)*((2/r)-(1/a)))

class Universe:
    def __init__(self, planets):
        self.planets = planets

    def __force(self, k):  # sila na k-ti planet iz liste self.planets
        sila = np.array([0,0])
        M = len(self.planets)
        for l in range(0, k):
            razlika = self.planets[k].r[-1] - self.planets[l].r[-1]
            sila = sila - 6.67408 * 0.00000000001 * ((self.planets[k].m * self.planets[l].m)/np.inner(razlika, razlika)) * (razlika/np.sqrt(np.inner(razlika, razlika)))
        for l in range(k+1, M):
            razlika = self.planets[k].r[-1] - self.planets[l].r[-1]
            sila = sila - 6.67408 * 0.00000000001 * ((self.planets[k].m * self.planets[l].m)/np.inner(razlika, razlika)) * (razlika/np.sqrt(np.inner(razlika, razlika)))
        return sila

    def __move(self):   # evolucija svemira (svih planeta) za jedan korak
        k=0
        for j in self.planets:
            j.F.append(self.__force(k))
            j.a.append(j.F[-1]/j.m)
            j.v.append(j.v[-1] + j.a[-1]*self.dt)
            j.r.append(j.r[-1] + j.v[-1]*self.dt)
            k+=1

    def plot(self, dt, vrijeme):   # crtanje putanja
        self.dt = dt
        N = int(vrijeme/dt)
        for i in range(0,N):           # evolucija kroz cijelo zadano vrijeme
            self.__move()

        #crtanje putanja
        plt.xlabel("$x(m)$")
        plt.ylabel("$y(m)$")
        
        self.x = []
        self.y = []

        for i in self.planets:
            self.x.append([j[0] for j in i.r])  # lista listi x koordinata za svaki planet
            self.y.append([j[1] for j in i.r])
        
        for i in range(0, len(self.planets)):
            plt.plot(self.x[i], self.y[i], label=self.planets[i].naziv)

        plt.axis("equal")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

    def animate_plot(self, dt, vrijeme, frames):    # crtanje i animiranje putanja
        self.dt = dt
        N = int(vrijeme/dt)
        for i in range(0,N):           # evolucija kroz cijelo zadano vrijeme
            self.__move()
        numericki_period = 0
        i=1
        while i<len(self.planets[1].r) and not(self.planets[1].r[i-1][1]<0 and self.planets[1].r[i][1]>0):
            numericki_period += dt
            i+=1
        if not(i<len(self.planets[1].r)):
            numericki_period = "Period nije dostignut"

        #crtanje i animiranje putanja
        fig, ax = plt.subplots()
        plt.xlabel("$x(m)$")
        plt.ylabel("$y(m)$")
        
        self.x = []
        self.y = []
        self.points= []

        for i in self.planets:
            self.x.append([j[0] for j in i.r])  # lista listi x koordinata za svaki planet
            self.y.append([j[1] for j in i.r])

        def animate(j):
            for i in np.arange(0, len(self.planets)):
                self.points[i].set_alpha(1)
                self.points[i].set_offsets([self.x[i][j], self.y[i][j]])  # update the data
            return self.points

        for i in range(0, len(self.planets)):
            ax.plot(self.x[i], self.y[i], label=self.planets[i].naziv, alpha=0.5)
            self.points.append(ax.scatter(self.x[i][0], self.y[i][0], s=50, alpha=0))
        ani = animation.FuncAnimation(fig, animate, np.arange(0, len(self.x[0])), interval=frames, blit=True)

        plt.axis("equal")
        plt.legend(framealpha=1, frameon=True)
        plt.show()

        return numericki_period
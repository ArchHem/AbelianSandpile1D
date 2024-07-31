import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

"""np.random.seed(10)"""
if __name__ == '__main__':
    starting_time = time.time()
from tqdm import tqdm

class Oslo_model:
    def __init__(self,L,zero_state = None,lower_lim=1,upper_lim=2,display=False,hide_labels=True):
        if zero_state == None:
            zero_state = np.zeros(L,dtype='int')
        self.heights = zero_state
        self.L = L
        self.threshold = np.random.randint(lower_lim,upper_lim+1,size=(L,))
        self.output = 0
        self.avalanche_sizes = []
        self.outflows = []
        self.upper_lim = upper_lim
        self.lower_lim = lower_lim
        self.height_doc = np.array([self.heights])
        self.slopes_doc = np.zeros_like(self.height_doc)
        if display:
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlim(-1,self.L+1)
            self.ax.set_ylim(-1,2*self.L+1)
            self.ax.set_xticks(np.arange(-1,self.L+1))
            self.ax.set_yticks(np.arange(-1,2*self.L+1))
            self.ax.grid()
            if hide_labels:
                self.ax.set_xticks([])
                self.ax.set_yticks([])

    def get_pile_height(self):
        return self.height_doc[:,0]


    def slope(self):
        indices = np.indices(self.heights.shape).flatten()
        grad = self.heights - self.heights[np.mod(indices+1,self.heights.shape[0])]
        grad[-1] = self.heights[-1]
        return grad

    def drive(self,index=0):
        self.heights[index] = self.heights[index] + 1

    def relax(self,index):
        self.heights[index] = self.heights[index] - 1
        self.threshold[index] = np.random.randint(self.lower_lim,self.upper_lim+1)
        try:
            self.heights[index+1] = self.heights[index+1] + 1
        except:
            self.output = self.output + 1

    def propegate(self):
        self.drive()
        current_outflow = self.output
        current_avalanche_size = 0
        limiter = 2
        while np.any(self.slope()[0:limiter] > self.threshold[0:limiter]):
            trutharray = np.where(self.slope()[0:limiter] > self.threshold[0:limiter])
            try:
                for index in trutharray[0]:
                    self.relax(index)
                    current_avalanche_size = current_avalanche_size + 1
                limiter = trutharray[0][-1] + 2
            except:
                break
        self.avalanche_sizes.append(current_avalanche_size)
        self.outflows.append(self.output-current_outflow)

    def iterate(self,numbers = 1000):
        current_depth = self.height_doc.shape[0]
        self.height_doc = np.vstack((self.height_doc,np.zeros((numbers,self.L))))
        self.slopes_doc = np.vstack((self.slopes_doc,np.zeros((numbers,self.L))))
        for i in tqdm(range(numbers)):
            self.propegate()
            self.height_doc[current_depth+i] = self.heights
            self.slopes_doc[current_depth+i] = self.slope()

    def animate(self,rate=1,interval=100):
        cords = np.array([i for i in range(self.L+1)])
        pile = self.ax.stairs([0],[0,1],color='red', label='Pile')
        N_t = self.height_doc.shape[0]
        self.ax.legend()

        def init():
            pile.set_data([0],[0,1])

            return pile,

        def animate(frame):

            y = self.height_doc[frame]
            pile.set_data(y, cords)

            return pile,

        self.anim = animation.FuncAnimation(self.fig, animate,
                                            init_func=init,
                                            frames=np.arange(0, N_t, 1)[::rate],
                                            interval=interval,
                                            blit=True)
        self.fig.show()




if __name__ == '__main__':
    test = Oslo_model(32,display=True,upper_lim=1)
    test.iterate(1000)

    print("Running time without animation: {:.2f}s".format(time.time() - starting_time))
    print(test.height_doc[0:20])
    test.animate(interval=60)
    plt.show()
















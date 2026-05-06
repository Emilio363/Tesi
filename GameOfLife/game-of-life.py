import numpy as np
from itertools import product
import csv


class Ambient:
    def __init__(self, ndim : int, size : int):
        """
        dim : int
            the number of dimension of my game
        size : int
            the size of each dimension

        If I create Ambient(3,4), I'll have a cube with edge 4
        """
        self.size = size
        self.ndim = ndim
        self.matrix = np.zeros((size,)*ndim, dtype=bool)
        self.oldmat = np.zeros((size,)*ndim, dtype=bool)

    def randomFill(self):
        allpos = list(product(range(self.size), repeat=self.ndim))
        for pos in allpos:
            self.matrix[pos]=np.random.rand()>0.5

    def set(self, list):
        """
        list : an iterable object of cople

        ex .set([(1,1), (1,2), (2,1), (2,2)])
        """
        for pos in list:
            self.matrix[pos] = True
    
    def _allDirection(self):
        n = self.ndim
        listDir = list(product([-1, 0, 1], repeat=n))
        listDir.remove((0,) * n)
        return listDir

    def epoc(self):
        self.matrix, self.oldmat = self.oldmat, self.matrix

        direction = self._allDirection()
        n = self.ndim
        allpos = list(product(range(self.size), repeat=n))
        for pos in allpos:
            count = 0
            for dir in direction:
                newpos = tuple(np.sum([dir, pos], axis = 0))
                if any(i<0 for i in newpos):
                    continue
                try:
                    count += self.oldmat[newpos]
                except IndexError:
                    pass
            #print(count)
            self.matrix[pos] = count == 3 or (self.oldmat[pos] and count == 2)

    def __str__(self):
        return self.matrix.__str__() + "\n"

    def cellData(self, filename = "life_Data.csv"):
        data = []
        restrictedPositions = list(product(range(1,self.size-1), repeat=self.ndim))
        allDir = self._allDirection()
        with open(filename, "w", newline='') as file:

            csvwriter = csv.writer(file)
            field = ["new cell"] #creation of the header
            for dir in allDir:
                field.append(str(dir))
            field.append(str((0,0)))
            csvwriter.writerow(field)

            for pos in restrictedPositions:
                thisrow = [int(self.matrix[pos])]
                for dir in allDir:
                    newpos = tuple(np.sum([dir, pos], axis = 0))
                    thisrow.append(int(self.oldmat[newpos]))
                thisrow.append(int(self.oldmat[pos]))
                data.append(thisrow)

            csvwriter.writerows(data)

"""
mat = Ambient(2,10)
mat.set([(2,2), (2,3), (3,2), (3,3)])
mat.set([(5,5), (5,6), (6,5), (6,6)])
#mat.set([(_,6) for _ in range(4,9)])

print(mat)
for i in range(3):
    mat.epoc()
    print(mat)
"""

mat = Ambient(2,100)
mat.randomFill()
#mat.set([(_,2) for _ in range(1,4)])
#mat.set(list(product([1, 2, 3], repeat=2)))
mat.epoc()
mat.epoc()
mat.cellData()

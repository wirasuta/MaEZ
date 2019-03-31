from pprint import pprint
from copy import deepcopy
from gui import *
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PrioQueue():
    #Priority Queue dengan isi tuple (value,priority)
    #Elemen dengan priority paling rendah ada di awal
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def __str__(self): 
        return ' > '.join([str(i[0]) + "(" +str(i[1]) + ")" for i in self.queue]) 
    
    def add(self,value,priority):
        for i in range(len(self.queue)):
            if (priority < self.queue[i][1]):
                self.queue[i:i] = [(value,priority)]
                return
        #elemen terakhir
        self.queue.append((value,priority))
    
    def remove(self):
        val = self.queue[0][0]
        self.queue = self.queue[1:]
        return val


class Maze():
    def __init__(self,filename):
        self.matriks = []
        self.drawqueue = []
        with open(filename,'r') as f:
            lines = f.readlines()
            for line in lines:
                self.matriks.append([int(c) for c in line.strip()])
        self.resetmatriks = deepcopy(self.matriks)

    def reset(self):
        self.matriks = deepcopy(self.resetmatriks)
    
    def printCLI(self):
        for line in self.matriks:
            for char in line:
                if char == 0:
                    print(" ", end="")
                elif char == 1:
                    print("█", end="")
                elif char == 2:
                    print(bcolors.OKBLUE+"•"+bcolors.ENDC, end="")
                elif char == 3:
                    print(bcolors.OKGREEN+"×"+bcolors.ENDC, end="")
            print()

    def getMatriks(self):
        return self.matriks

    def getTile(self,x,y):
        if x>=0 and y>=0 and x<len(self.matriks) and y<len(self.matriks[0]):
            return self.matriks[x][y]
        else:
            return -1

    def setTile(self,x,y,i):
        self.matriks[x][y] = i

    def bfs(self,start,end):
        #start dan end adalah tuple (x,y)
        queue = PrioQueue()  #Queue tuple untuk implementasi BFS
        path = []            #Berisi tuple previous tile dan current tile
        queue.add(start,0)
        path.append((start,start))
        while(len(queue) > 0):
            curr = queue.remove()
            self.drawqueue.append(((curr[1],curr[0]),"yellow"))
            if curr == end:
                path.append((end,end))
                break
            else:
                x = curr[0]
                y = curr[1]
                self.setTile(x,y,2)
                if (self.getTile(x+1,y) == 0):
                    path.append((curr,(x+1,y)))
                    queue.add((x+1,y),0)
                if (self.getTile(x-1,y) == 0):
                    path.append((curr,(x-1,y)))
                    queue.add((x-1,y),0)
                if (self.getTile(x,y+1) == 0):
                    path.append((curr,(x,y+1)))
                    queue.add((x,y+1),0)
                if (self.getTile(x,y-1) == 0):
                    path.append((curr,(x,y-1)))
                    queue.add((x,y-1),0)

        #BFS telah selesai karena tidak ada tile yang dapat dikunjungi
        #atau telah mencapai goal node
        if path[-1] != (end,end):
            print("No Path Found")
        else:
            print("Path Found!")
            path.reverse()
            solution = []
            prev = path[0][1]
            distance = 0
            for tile in path:
                if tile[1] == prev:
                    solution.append(tile[1])
                    prev = tile[0]
                    if self.getTile(tile[1][0],tile[1][1]) != 3:
                        self.setTile(tile[1][0],tile[1][1],3)
                        self.drawqueue.append(((tile[1][1],tile[1][0]),"magenta"))
                        distance+=1
            print(f"Solution path length : {distance}")

    @staticmethod
    def mhtdistance(start,end):
        return abs(start[0]-end[0]) + abs(start[1]-end[1])

    def astar(self,start,end):
        #start dan end adalah tuple (x,y)
        queue = PrioQueue()  #Priority Queue tuple untuk implementasi A*
        path = []            #Berisi tuple previous tile dan current tile
        fdistance = [[0 for i in range(len(self.matriks[0]))] for j in range(len(self.matriks))]
        queue.add(start,Maze.mhtdistance(start,end))
        path.append((start,start))
        while(len(queue) > 0):
            curr = queue.remove()
            self.drawqueue.append(((curr[1],curr[0]),"yellow"))
            if curr == end:
                path.append((end,end))
                break
            else:
                x = curr[0]
                y = curr[1]
                nextdistance = fdistance[x][y] + 1
                self.setTile(x,y,2)
                if (self.getTile(x+1,y) == 0):
                    path.append((curr,(x+1,y)))
                    fdistance[x+1][y] = nextdistance
                    queue.add((x+1,y),nextdistance+Maze.mhtdistance((x+1,y),end))
                if (self.getTile(x-1,y) == 0):
                    path.append((curr,(x-1,y)))
                    fdistance[x-1][y] = nextdistance
                    queue.add((x-1,y),nextdistance+Maze.mhtdistance((x-1,y),end))
                if (self.getTile(x,y+1) == 0):
                    path.append((curr,(x,y+1)))
                    fdistance[x][y+1] = nextdistance
                    queue.add((x,y+1),nextdistance+Maze.mhtdistance((x,y+1),end))
                if (self.getTile(x,y-1) == 0):
                    path.append((curr,(x,y-1)))
                    fdistance[x][y-1] = nextdistance
                    queue.add((x,y-1),nextdistance+Maze.mhtdistance((x,y-1),end))

        #A* telah selesai karena tidak ada tile yang dapat dikunjungi
        #atau telah mencapai goal node
        if path[-1] != (end,end):
            print("No Path Found")
        else:
            print("Path Found!")
            path.reverse()
            solution = []
            prev = path[0][1]
            distance = 0
            for tile in path:
                if tile[1] == prev:
                    solution.append(tile[1])
                    prev = tile[0]
                    if self.getTile(tile[1][0],tile[1][1]) != 3:
                        self.setTile(tile[1][0],tile[1][1],3)
                        self.drawqueue.append(((tile[1][1],tile[1][0]),"magenta"))
                        distance+=1
            print(f"Solution path length : {distance}")

    def illustrate(self,title):
        self.gui = UI(self.matriks,title,1)
        self.gui.startdraw(self.drawqueue)
        self.drawqueue = []

def main():
    # Init Maze
    #m1 = Maze("xlarge.txt")
    #m1.bfs((11,0),(27,40))
    #m1.illustrate("BFS")
    #m1.reset()
    #m1.astar((11,0),(27,40))
    #m1.illustrate("A*")

    #m2 = Maze("large.txt")
    #m2.bfs((1,0),(29,30))
    #m2.illustrate("BFS")
    #m2.reset()
    #m2.astar((1,0),(29,30))
    #m2.illustrate("A*")

    m3 = Maze("medium.txt")
    m3.bfs((1,0),(1,20))
    m3.illustrate("BFS")
    m3.reset()
    m3.astar((1,0),(1,20))
    m3.illustrate("A*")

    #m4 = Maze("small.txt")
    #m4.bfs((1,0),(9,10))
    #m4.illustrate("BFS")
    #m4.reset()
    #m4.astar((1,0),(9,10))
    #m4.illustrate("A*")

    #m5 = Maze("1667.txt")
    #m5.bfs((1,0),(199,200))
    #m5.illustrate("BFS")
    #m5.reset()
    #m5.astar((1,0),(199,200))
    #m5.illustrate("A*")

    #m6 = Maze("895.txt")
    #m6.bfs((1,0),(99,100))
    #m6.illustrate("BFS")
    #m6.reset()
    #m6.astar((1,0),(99,100))
    #m6.illustrate("A*")

    #m7 = Maze("205.txt")
    #m7.bfs((1,0),(35,70))
    #m7.illustrate("BFS")
    #m7.reset()
    #m7.astar((1,0),(35,70))
    #m7.illustrate("A*")
    #sys.exit(0)

if __name__ == "__main__":
    main()

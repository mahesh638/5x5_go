import numpy as np
import copy

file1 = open('inputig.txt', 'r')
L = file1.readlines()
col = int(L[0][0])


S = np.zeros((1,5))
BigS = [[]]
k=0
for i in L[6:len(L)]:
    for j in range(0, 5):
        BigS[k].append(int(i[j]))
    k+=1
    BigS.append([])
    
BigS.remove([])

# BigS = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,0,0,0,2],[0,0,0,0,0]]

size = 5
class peices:
    
    def __init__(self, x=None, y=None, colour=None):
        self.x = x
        self.y = y
        self.coor = (x,y)
        self.colour = colour
        self.neighbours = []
        self.connections = []
        self.liberties = [] 
        self.empty = []
    
    def getliberties(self, BigS):
        self.liberties= []
        self.empty = []
        x = self.x
        y = self.y
        if(x-1 > -1):
            self.liberties.append((x-1,y))
        if(x+1 < size):
            self.liberties.append((x+1,y))
        if(y-1 > -1):
            self.liberties.append((x,y-1))
        if(y+1 < size):
            self.liberties.append((x,y+1))
        for i in self.liberties:
            if(BigS[i[0]][i[1]] == 0):
                self.empty.append(i)
            
        
                
    
    def getneighbours(self, BigS):
        self.getneighbours = []
        x = self.x
        y = self.y
        if(x-1 > -1):
            if(BigS[x-1][y] == self.colour):
                self.neighbours.append(D[(x-1,y)])
        if(y-1 > -1):
            if(BigS[x][y-1] == self.colour):
                self.neighbours.append(D[(x,y-1)])
        if(y+1 < size):
            if(BigS[x][y+1] == self.colour):
                self.neighbours.append(D[(x,y+1)])
        if(x+1 < size):
            if(BigS[x+1][y] == self.colour):
                self.neighbours.append(D[(x+1,y)])
    
    def getconnections(self):
        s = []
        s.append(self)
        while(len(s)!= 0):
            p = s.pop(0)
            for i in p.neighbours:
                if(i not in self.connections):
                    self.connections.append(i)
                    s.append(i)
        if(self not in self.connections):
            self.connections.append(self)
    
    def delconnect(self):
        for i in self.connections:
            if i != self:
                i.connections.remove(self)

class moves:
    
    def __init__(self):
        self.validmoves = []
        self.maxcount = 0
        self.mincount = 0
        
    # def pointempties(self, BigS, x, y, colour):
    #     counter = 0
    #     if(D[(x,y)] == None):
    #         D[(x,y)] = peices(i,j,colour)
    #         D[(x,y)].getneighbours()
    #         D[(x,y)].getconnections()
    #         counter = 1
    #     vacant = 0
    #     for p in D[(x,y)].connections:
    #         if(p.x -1 > -1 and BigS[p.x - 1][p.y]==0):
    #             vacant +=1
    #         if(p.x+1 < size and BigS[p.x+1][p.y]==0):
    #             vacant +=1
    #         if(p.y-1 > -1 and BigS[p.x][p.y-1]==0):
    #             vacant +=1
    #         if(p.y+1 < size and BigS[p.x][p.y+1]==0):
    #             vacant +=1
    #     if(counter == 1):
    #         counter = 0
    #         del D[(x,y)]
    #         D[(x,y)] = None
        
    #     return vacant
        
    def pointempties(self, BigS, x, y, colour):
        counter = 0
        if(D[(x,y)].x == None):
            D[(x,y)] = peices(i,j,colour)
            D[(x,y)].getneighbours(BigS)
            D[(x,y)].getconnections()
            counter = 1
        vacant = 0
        if(x -1 > -1 and BigS[x - 1][y]==0):
            vacant +=1
        if(x+1 < size and BigS[x+1][y]==0):
            vacant +=1
        if(y-1 > -1 and BigS[x][y-1]==0):
            vacant +=1
        if(y+1 < size and BigS[x][y+1]==0):
            vacant +=1
        
        return vacant
        
    def count_peices(self, BigS):
        wcount = 2.5
        bcount = 0
        for i in range (0,5):
            for j in range(0,5):
                if(BigS[i][j] == 1):
                    bcount +=1
                elif(BigS[i][j] == 2):
                    wcount +=1
        return(bcount, wcount)
                                                   
                        
    def makeamove(self, S, move, col):
        SS = S.copy()
        SS[move[0]][move[1]] = col
        dead, bdead, wdead = self.kill(BigS)
        for i in dead:
            SS[i[0]][i[1]] = 0
        
        return SS
        
        
                    
    def kill(self, BigS):
        bdead = 0
        wdead = 0

        visited = []
        dead = []
        for i in range(0,5):
            for j in range(0,5):
                if(D[i,j].x!=None):
                    if(D[(i,j)] not in visited):
                        visited.append(D[(i,j)])
                        flag = 0
                        for nei in D[(i,j)].connections:
                            if nei not in visited:
                                visited.append(nei)
                            for lib in nei.liberties:
                                if(BigS[lib[0]][lib[1]] == 0):
                                    flag+=1
                                    
                        if(flag == 0):
                            for nei in D[(i,j)].connections:
                                dead.append(nei.coor)
                                if(nei.colour == 1):
                                    wdead+=1
                                elif(nei.colour == 2):
                                    bdead+=1
        return(dead, bdead, wdead)    
                    
    
    
    def removedead(self, BigS, dead):
        for p in dead:
            BigS[p[0]][p[1]] =0
        return BigS
        
    
    def findvalidmoves(self, B, colour):
        dead, bdead, wdead = self.kill(B)
        BigS = self.removedead(B, dead)
        if(colour == 1):
            for i in range (0,size):
                for j in range(0,size):
                    if(BigS[i][j] == 0): 
                        BigS[i][j] = 1
                        D[(i,j)] = peices(i,j,colour)
                        D[(i,j)].getneighbours(BigS)
                        D[(i,j)].getconnections()
                        ll = []
                        for k in D[(i,j)].connections:
                            if(k.x !=None):
                                k.getliberties(BigS) 
                            if(k.empty !=[]):
                                ll.append(k.empty)
                        BigS[i][j] = 0
                        del D[(i,j)]
                        D[(i,j)] = peices()
                        
                        
                        if(ll != []):
                            prob = 0
                            if(i-1 > -1):
                                if(BigS[i-1][j]!=2):
                                    prob+=1
                            if(i+1 < size):
                                if(BigS[i+1][j]!=2):
                                    prob+=1
                            if(j-1 > -1):
                                if(BigS[i][j-1]!=2):
                                    prob+=1
                            if(j+1 < size):
                                if(BigS[i][j+1]!=2):
                                    prob+=1
                            if(prob != 0):
                                self.validmoves.append((i,j))
        elif(colour == 2):
            for i in range (0,size):
                for j in range(0,size):
                    if(BigS[i][j] == 0): 
                        BigS[i][j] = 2
                        D[(i,j)] = peices(i,j,colour)
                        D[(i,j)].getneighbours(BigS)
                        D[(i,j)].getconnections()
                        ll = []
                        for k in D[(i,j)].connections:
                            if(k.x !=None):
                                k.getliberties(BigS) 
                            if(k.empty !=[]):
                                ll.append(k.empty)
                        BigS[i][j] = 0    
                        del D[(i,j)]
                        
                        D[(i,j)] = peices()
                        if(ll != []):
                            prob = 0
                            if(i-1 > -1):
                                if(BigS[i-1][j]!=1):
                                    prob+=1
                            if(i+1 < size):
                                if(BigS[i+1][j]!=1):
                                    prob+=1
                            if(j-1 > -1):
                                if(BigS[i][j-1]!=1):
                                    prob+=1
                            if(j+1 < size):
                                if(BigS[i][j+1]!=1):
                                    prob+=1
                            if(prob != 0):
                                self.validmoves.append((i,j))
                            
        var = copy.deepcopy(self.validmoves)
        self.validmoves = []
                            
        return(var)
    
    
                    
    def heuristic(self, B, colour):
        dead, bdead, wdead = self.kill(B)
        updated = self.removedead(B, dead)
        bcount, wcount = self.count_peices(updated)
        blib = 0
        wlib = 0
        bcorner = 0
        wcorner = 0
        for i in range(0,5):
            for j in range(0,5):
                if(updated[i][j] == 1):
                    if(i<=2):
                        bcorner += (2-i)
                    elif(i>2):
                        bcorner += (i-2)
                    if(j<=2):
                        bcorner += (2-j)
                    elif(j>2):
                        bcorner += (j-2)

                    blib += self.pointempties(updated, i, j, colour)
                
                elif(updated[i][j] == 2):
                    if(i<=2):
                        wcorner += (2-i)
                    elif(i>2):
                        wcorner += (i-2)
                    if(j<=2):
                        wcorner += (2-j)
                    elif(j>2):
                        wcorner += (j-2)
                    wlib +=self.pointempties(updated, i, j, colour)
        if(colour == 2):
            return(wcount*(wcount-1)/2 - bcount*(bcount-1)/2 +wlib - blib)
            
        elif(colour == 1):
            return(bcount*(bcount-1)/2 - wcount*(wcount-1)/2 +blib - wlib)
        
    def maxi(self, BigS, colour, depth, alpha, beta):
        self.maxcount +=1
        if(depth == 0):
            heur = self.heuristic(BigS, colour)
            return heur, ()
        mmoves = []
        moveset = self.findvalidmoves(BigS, colour).copy()
        # print(len(moveset))
        if(len(moveset) == 25):
            return(100, [(2,2)])
        maxim = float("-inf")
        if moveset == []:
            return(float("inf"), ())
        mreq = ()
        for m in moveset:
            tempS = copy.deepcopy(BigS)
            tempL = self.makeamove(tempS, m, colour)
            heur , move = self.mini(tempL,3-colour, depth-1, alpha, beta)
            
            if heur > maxim:
                maxim = heur
                mreq = m
                # if move == ():
                #     mmoves.append(m)
                # if move!= ():
                #     mmoves.append(move[-1])
                    
            if maxim > beta:
                return maxim, [mreq]
            
            if maxim > alpha:
                alpha = maxim
                
        return maxim, [mreq]
                
    def mini(self, BigS, colour, depth, alpha, beta):
        #print('min')
        self.mincount +=1
        if(depth == 0):
            heur = self.heuristic(BigS, colour)
            return heur, ()
        mmoves = []
        moveset = self.findvalidmoves(BigS, colour).copy()
        if(len(moveset) == 25):
            return(100, (2,2))
        minim = float("inf")
        if moveset == []:
            return(float("-inf"), ())
        mreq = ()
        for m in moveset:
            tempS = copy.deepcopy(BigS)
            tempL = self.makeamove(tempS, m, colour)
            heur, move = self.maxi(tempL, 3-colour, depth-1, alpha, beta)
            
            if heur < minim:
                minim = heur
                mreq = m
                # if move == ():
                #     mmoves.append(m)
                # if move!= ():
                #     mmoves.append(move[-1])
                    
            if minim < alpha:
                return minim, [mreq]
            
            if minim < beta:
                beta = minim
        
        return minim, [mreq]
        
                            
                        
        

D = {}

for i in range (0, size):
    for j in range(0,size):
        D[(i,j)] = peices()
        
for i in range(0,size):
    for j in range(0,size):
        if(BigS[i][j]!= 0):
            D[(i,j)] = peices(i,j,BigS[i][j])
            
for i in range(0,size):
    for j in range(0,size):
        if(D[(i,j)].x!=None):
            D[(i,j)].getliberties(BigS)
            D[(i,j)].getneighbours(BigS)
            
            
for i in range(0,size):
    for j in range(0,size):
        if(D[(i,j)].x!=None):
            D[(i,j)].getconnections()
            
moves = moves()
Work = copy.deepcopy(BigS)
valid = moves.findvalidmoves(Work, col)


dead, bdead, wdead = moves.kill(Work)

heur = moves.heuristic(Work, col)

b,w = moves.count_peices(Work)
            
meh, move = moves.maxi(Work, col, 4, float("-inf"), float("inf"))

#Final = moves.makeamove(Work, move[0], col)

with open("output.txt",'w') as fout:
    if(move == [()] or move == ()):
        fout.write("PASS")
    else:
        fout.write(str(move[-1][0]) + ',' + str(move[-1][1]))

           
            




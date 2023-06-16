# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 16:14:03 2022

@author: Maheshvar
"""

from copy import deepcopy

file1 = open('input.txt', 'r')
L = file1.readlines()
col = int(L[0][0])

board = [[]]
k=0
for i in L[6:len(L)]:
    for j in range(0, 5):
        board[k].append(int(i[j]))
    k+=1
    board.append([])
board.remove([])


Prev = [[]]
k=0
for i in L[1:len(L)-5]:
    for j in range(0, 5):
        Prev[k].append(int(i[j]))
    k+=1
    Prev.append([])    
Prev.remove([])


class Gogo:
    
    def __init__(self, n):
        self.num = n
        self.maxcount = 0
        self.mincount = 0
        
    #Referred from host.py  
    def open_adj(self, x,y):
        adj = []
        if(x-1 > -1):
            adj.append((x-1,y))
        if(y-1 > -1):
            adj.append((x,y-1))
        if(x+1 < 5):
            adj.append((x+1,y))
        if(y+1 < 5):
            adj.append((x,y+1))
        return adj
    
    #Referred from host.py            
    def get_allies(self, x, y, colour, board):
        s = [(x,y)]
        visited = []
        allies = []
        visited.append((x,y))
        while s!=[]:
            p = s.pop(0)
            allies.append(p)
            
            for coor in self.open_adj(p[0], p[1]):
                if(board[coor[0]][coor[1]] == colour):
                    if coor not in visited:
                        visited.append(coor)
                        s.append(coor)
        
        return allies
            
    #Referred from host.py  
    def dead_peices(self, colour, board):
        dead = []
        for i in range(0,5):
            for j in range(0,5):
                if(board[i][j] == colour):
                    breaker = False
                    for allies in self.get_allies(i,j,colour, board):
                        for adj in self.open_adj(allies[0], allies[1]):
                            if board[adj[0]][adj[1]] == 0:
                                breaker = True
                                break
                            
                    
                    if(breaker == False):
                        dead.append((i,j))
                    
        return dead
    
    
    
    def make_a_move(self, x,y, colour, board):
        temp = deepcopy(board)
        temp[x][y] = colour
        opp_count=0
        my_count = 0
        opp_dead = self.dead_peices(3-colour, temp)
        for i in opp_dead:
            opp_count +=1
            temp[i[0]][i[1]] =0
        my_dead = self.dead_peices(colour, temp)
        for i in my_dead:
            my_count +=1
            temp[i[0]][i[1]] =0
            
        return temp, my_count, opp_count
    
    #Referred from host.py 
    def ally_liberties(self, x,y, colour, board):
        lib = set()
        for ally in self.get_allies(x, y, colour, board):
            for coor in self.open_adj(ally[0], ally[1]):
                if board[coor[0]][coor[1]] == 0:
                    lib.add(coor)
        return lib
    
    def check_threat_count(self, colour, board):
        threat = 0
        for i in range(0,5):
            for j in range (0,5):
                if(board[i][j] == colour):
                    if(len(self.ally_liberties(i, j, colour, board)) <= 1 ):
                        threat+=1
        return threat
    
    def open_liberties(self, colour, board):
        lib = 0
        for i in range(0,5):
            for j in range (0,5):
                if(board[i][j] == colour):
                    lib+=len(self.ally_liberties(i, j, colour, board))
        return 0
        
    def heur(self, colour, B):
        board = deepcopy(B)
        bcount, wcount = self.count_pieces(board)
        wcount +=6
        wthreat = self.check_threat_count(2, board)
        bthreat = self.check_threat_count(1, board)
        wlib = self.open_liberties(2, board)
        blib = self.open_liberties(1, board)
                        
        if(colour == 1):
            return( 10*bcount - 10*wcount + 2*wthreat - 1.5*bthreat + 4.5*wlib - 4.5*blib)
        elif(colour == 2):
            return( 10*wcount - 10*bcount + 2*bthreat - 1.5*wthreat + 4.5*blib - 4.5*wlib)
        
        
    def moveset(self, colour, prev, board):
        valid = []
        lib = set()
        for i in range(0,5):
            for j in range(0,5):
                if(board[i][j] !=0):
                    k= self.ally_liberties(i, j, board[i][j], board)
                    lib = lib.union((k))
        
        for i in lib:
            updated, my_count, opp_count = self.make_a_move(i[0], i[1], colour, board)
            pu = opp_count - my_count            
            if updated!=board and updated!=prev:
                valid.append((i, pu))
                
        valid = sorted(valid, key=lambda x: -x[1])
        
        valid_moves = []
        for i in valid:
            valid_moves.append(i[0])
                
        return valid_moves

    def count_pieces(self,board):
        bcount = 0
        wcount = 0
        for i in range (0,5):
            for j in range(0,5):
                if(board[i][j] == 1):
                    bcount +=1
                elif(board[i][j] == 2):
                    wcount +=1
                    
        return bcount, wcount
         

    
    def min_or_max(self,maxi, board, P, colour, depth, alpha, beta):
        self.maxcount +=1
        if(depth == 0):
            return self.heur(colour, board), []  
        
        if(maxi == True):             
            quant = float( "-inf")
        else:
            quant = float( "inf")
        move = []
        M = self.moveset(colour, P, board)
        for m in M:
            B = deepcopy(board)
            new,my_dead, opp_dead = self.make_a_move(m[0], m[1], colour, B)
            heur, getm = self.min_or_max( not maxi,new, board, 3-colour, depth-1, alpha, beta)
            heur += opp_dead*5 - my_dead*8.5         
              
            if(maxi == True): 
                if(heur > quant):
                    quant = heur
                    move = [m]
                if (quant >= beta):
                    return quant, move            
                if(quant > alpha):
                    alpha = quant
                    
            else:
                if(heur < quant):
                    quant = heur
                    move = [m]   
                    
                if(quant <=alpha):
                    return quant, move            
                if(quant < beta):
                    alpha = heur
                
        return quant, move       
             
    
Work = deepcopy(board)
moves = Gogo(2)
bcount, wcount = moves.count_pieces(board)
if col == 1:
    my_count = bcount
    opp_count = wcount
elif col == 2:
    my_count = wcount
    opp_count = bcount
if opp_count==0 and my_count==0:
    move = [(2,2)]
elif opp_count==1 and my_count==0:
    if board[2][2]==3-col:
        move = [(2,1)]
    else:
        move = [(2,2)]

else:
    meh, move = moves.min_or_max(True, Work, Prev,  col, 2, float("-inf"), float("inf"))

with open("output.txt",'w') as fout:
    if(move == [()] or move == ()):
        fout.write("PASS")
    else:
        fout.write(str(move[0][0]) + ',' + str(move[0][1]))
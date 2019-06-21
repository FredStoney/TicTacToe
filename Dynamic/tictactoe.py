
import numpy as np
class Board:
    def __init__(self, orig=None):
        if orig is None:
            self.non_copy_constructor()
        else:
            self.copy_constructor(orig)
    def non_copy_constructor(self):
        #initializes state which holds the board state; positions of X's and O's
        self.b = np.repeat(0, 9)
        #initializes spaces availablie which holds the index of which spots can still be played in (no X or O)
        self.spaces_available = list(range(9))
    def copy_constructor(self, orig):
        self.b = orig.b.copy()
        self.spaces_available = orig.spaces_available.copy()
    def action(self, xo, location):
        #takes xo which is an int referring to X or O (1 for X and 0 for O)
        #sets the location of the board equal to that number
        self.b[location] = xo
        #removes that spot from playable locations
        self.spaces_available.remove(location)
    def __str__(self):
        s='______\n'
        for i in range(9):
           s=s+' '+convert1toX(self.b[i])
           if i in [2,5,8]:
               s=s+'\n'
        return s + '______'
    def __eq__(self, other):
        return np.all(self.b == other.b)


def convert1toX(one):
    #helper function for str in Board
    if one==1:
        return 'X'
    elif one==-1 :
        return 'O'
    return '-'

def game_over(board):
    boardb=board.b
    #checks horizontal wins
    for n in [0, 3, 6]:
        if (boardb[n] == boardb[n + 1] == boardb[n + 2]) & (boardb[n] != 0):

            return True
    #checks vertical wins
    for n in [0, 1, 2]:
        if (boardb[n] == boardb[n + 3] == boardb[n + 6]) & (boardb[n] != 0):

            return True
    #checks diagonal
    if (boardb[0] == boardb[4] == boardb[8]) & (boardb[0] != 0):

        return True
    #checks other diagonal
    if (boardb[2] == boardb[4] == boardb[6]) & (boardb[2] != 0):

        return True
    #checks if no spots left
    if (0 not in boardb):
        return True

    return False

def reward(board):
    boardb=board.b
    #does the same thing as game_over but returns an int based on who wins
    for n in [0, 3, 6]:
        if (boardb[n] == boardb[n + 1] == boardb[n + 2]) & (boardb[n] != 0):

            if boardb[n]>0:
                return 1
            else: return -2
    for n in [0, 1, 2]:
        if (boardb[n] == boardb[n + 3] == boardb[n + 6]) & (boardb[n] != 0):

            if boardb[n]>0:
                return 1
            else: return -2
    if (boardb[0] == boardb[4] == boardb[8]) & (boardb[0] != 0):

        if boardb[0] > 0:
            return 1
        else:
            return -2
    if (boardb[2] == boardb[4] == boardb[6]) & (boardb[2] != 0):

        if boardb[2] > 0:
            return 1
        else:
            return -2

    if (0 not  in boardb):
        return -1

    return 0


states=[]

def init_states():
    #init all possible states that can take place on a tic tac toe board and puts them into a list
    # the first couple of moves are limited to limit the state space.
    # For example 1st move can only be a corner, center, or side.
    print("init states...")
    board1 = Board()
    states.append(board1)
    for i in [0,1,4]:
        board1=Board()

        board1.action(1,i)
        nextspaces=[]
        if i ==0:
            nextspaces=[1,2,4,5,8]
        if i ==4:
            nextspaces=[0,1]
        if i==1:
            nextspaces=[0,3,4,6,7]
        for j in nextspaces:
            board2=Board(board1)
            board2.action(-1,j)

            states.append(Board(board2))

            for k in board2.spaces_available:
                board3 = Board(board2)
                board3.action(1, k)

                for l in board3.spaces_available:
                    board4=Board(board3)
                    board4.action(-1,l)
                    if board4 not in states:
                        states.append(board4)

                    for m in board4.spaces_available:
                        board5=Board(board4)
                        board5.action(1,m)
                        if not game_over(board5):
                            #if board5 not in term_states:
                             #   term_states.append(board4)
                       # else:
                            for n in board5.spaces_available:
                                board6=Board(board5)
                                board6.action(-1,n)
                                if not game_over(board6):
                                    #if board6 not in term_states:
                                     #   term_states.append(board6)

                                    if board6 not in states:
                                        states.append(board6)
                                    for o in board6.spaces_available:
                                        board7=Board(board6)
                                        board7.action(1,o)
                                        if not game_over(board7):
                                      #      if board7 not in term_states:
                                     #           term_states.append(board7)

                                            for p in board7.spaces_available:
                                                board8=Board(board7)
                                                board8.action(-1,p)
                                                if not game_over(board8):
                                       #             if board8 not in term_states:
                                        #                term_states.append(board8)

                                                    if board8 not in states:
                                                        states.append(board8)
                                                    for q in board8.spaces_available:
                                                        board9=Board(board8)
                                                        board9.action(1,q)
                                         #               if board9 not in term_states:
                                          #                  term_states.append(board9)






values=[]

def init_values():
    #initiate values of each state to zero
    for i in states:
        values.append(0)


def value(board):
    #retrieves the value of the board from the global list values
    #print('value\n',board)
    #if its a terminal s
    if game_over(board):
        return 0
    if(board not in states):
        print('Board not in states\n'+str(board))
    n=states.index(board)
    return values[n]

policy=[]
def init_policy():
    #initial policy is just the first location available
    for s in states:
        policy.append(s.spaces_available[0])


def policy_eval(policy):
    theta=.3
    while True:
        delta=0
        for i in range(len(states)):
            board=states[i]
            v=values[i]
            values[i]=iterative(board,policy[i])
            delta=max([delta,v-values[i]])
        if delta<theta:
            break
    print("policy evaluated")
def policy_update(policy):

    for i in range(len(policy)):
        A=[]
        if states[i]==Board():
            for a in [0,1,4]:
                A.append(iterative(states[i], a))
            policy[i] = [0,1,4][np.argmax(A)]

        elif states[i]==board0:
            for a in [1,2,4,5,8]:
                A.append(iterative(states[i], a))
            policy[i] = [1,2,4,5,8][np.argmax(A)]

        elif states[i]==board4:
            for a in [0,1]:
                A.append(iterative(states[i], a))
            policy[i] = [0,1][np.argmax(A)]

        elif states[i]==board4:
            for a in [0,3,4,6,7]:
                A.append(iterative(states[i], a))
            policy[i] = [0,3,4,6,7][np.argmax(A)]
        else:
            for a in states[i].spaces_available:
                A.append(iterative(states[i],a))
            policy[i]=states[i].spaces_available[np.argmax(A)]
        print("policy updated")


def iterative(board,action):
    onestep=[]
    board2 = Board(board)
    board2.action(1, action)
    spaces=board2.spaces_available
    if board2==board0:
        spaces=movesboard0
    elif board2==board1:
        spaces=movesboard1
    elif board2==board4:
        spaces=movesboard4
    elif board2==Board():
        spaces=[0,1,4]

    if game_over(board2):
        return reward(board2)

    else:
        for space in spaces:
            board3=Board(board2)
            board3.action(-1,space)
            onestep.append(board3)
        sum=0
        for s in onestep:
            sum=sum + 1/len(onestep)*(reward(s)+value(s))
        return sum


def savestates():

    with open('states.pkl', 'wb') as f:
        pickle.dump(states, f)
def loadstates():
    with open('states.pkl', 'rb') as f:
       global states
       states = pickle.load(f)


def main():

    init_states()
    savestates()


    loadstates()
    init_values()
    init_policy()
    print(states)
    print(policy)
    print(values)
    print("updating policy...")
    for i in range(10):
        policy_eval(policy)
        policy_update(policy)
    savePolicy()
    print("policy saved")


def play():
    print("playing tic tac toe...")
    getPolicy()
    global policy
    policy=policy[0]
    loadstates()
    while True:
        print("new game")
        playboard=Board()
        while True:
            count=0
            print(playboard)
            index=states.index(playboard)
            playboard.action(1,policy[index])
            print(playboard)
            if game_over(playboard):
                r = reward(playboard)
                print(r)
                if(r < 0):
                    print("you win")
                if (r == 0):
                    print("cats game")
                if (r > 0 ):
                    print ("you lose")
                
                break
            while True:
                action= input("which index?")
                if playboard==board4:
                    if int(action) in movesboard4:
                        break
                elif playboard==board1:
                    if int(action) in movesboard1:
                        break
                elif playboard==board0:
                    if int (action) in movesboard0:
                        break
                elif int(action) in playboard.spaces_available:
                    break
            playboard.action(-1,int(action))
            if game_over(playboard):
                r = reward(playboard)
                print(r)
                if(r < 0):
                    print("you win")
                if (r == 0):
                    print("cats game")
                if (r > 0 ):
                    print ("you lose")
                break

import pickle
def savePolicy():
    # obj0, obj1, obj2 are created here...

    # Saving the objects:
    with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([policy], f)

def getPolicy():
    # Getting back the objects:
    with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
        global policy
        policy = pickle.load(f)


def intro():

    s = "-----------\n" \
        "  0  1  2  \n" \
        "  3  4  5  \n" \
        "  6  7  8  \n" \
        "-----------\n"
    print("Indices")

    print(s)
    print("indexes in first move are limited")
    print("Ex.")

    t = "-----------    -----------\n" \
    "  X  -  0        X  -  -  \n" \
    "  -  -  -   =    -  -  -  \n" \
    "  -  -  -        0  -  -  \n" \
    "-----------    -----------\n"
    print(t)

board0=Board()
board0.action(1,0)
movesboard0=[1,2,4,5,8]
board1 = Board()
board1.action(1, 1)
movesboard1=[0,3,4,6,7]
board4=Board()
board4.action(1,4)
movesboard4=[0,1]



# comment out main after running once to use policy already saved.
# it will take quite a while to create the states and obtain the policy initially.
#main()
intro()
play()
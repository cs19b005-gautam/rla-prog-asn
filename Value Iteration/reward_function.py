import numpy as np
from state_space import get_state_space

global_state_space = []
def winner(markers):
    sum = 0
    winner = 0
    if(sum(markers[0])==3):
        return 1
    elif(sum(markers[1])==3):
        return 1
    elif(sum(markers[2])==3):
        return 1
    elif(markers[0][0]+markers[1][1]+markers[1][2]==3):
        return 1
    elif (markers[1][0] + markers[1][1] + markers[1][2] == 3):
        return 1
    elif (markers[2][0] + markers[2][1] + markers[2][2] == 3):
        return 1
    elif (markers[0][0] + markers[1][1] + markers[2][2] == 3):
        return 1
    elif (markers[0][2] + markers[1][1] + markers[2][0] == 3):
        return 1
    elif (sum(markers[0]) == -3):
        return -1
    elif (sum(markers[1]) == -3):
        return -1
    elif (sum(markers[2]) == -3):
        return -1
    elif (markers[0][0] + markers[1][1] + markers[1][2] == -3):
        return -1
    elif (markers[1][0] + markers[1][1] + markers[1][2] == -3):
        return -1
    elif (markers[2][0] + markers[2][1] + markers[2][2] == -3):
        return -1
    elif (markers[0][0] + markers[1][1] + markers[2][2] == -3):
        return -1
    elif (markers[0][2] + markers[1][1] + markers[2][0] == -3):
        return -1
    else:
        cnt_x,cnt_o,cnt0 = 0,0,0
        ind = [-1,-1]
        for i in range(3):
            for j in range(3):
                if(markers[i][j]==1):
                    cnt_x+=1
                elif(markers[i][j]==-1):
                    cnt_o+=1
                else:
                    cnt0+=1
                    ind = [i,j]
        if(cnt0==0):
            return -2
        elif(cnt_x==4 and cnt_o==4 and ind[0]>0 and ind[1]>0):
            markers[i][j] = 1
            return winner(markers)
        else:
            return 2


def getIndex(e):
    for i in range(len(global_state_space)):
        if(global_state_space[i] == e):
            return i
    return -1

def make_board(x):
    board = np.zeros(shape=(3,3))
    for i in range(3):
        for j in range(3):
            if(x[i*3+j]=='1'):
                board[i][j] = 1
            elif(x[i*3+j]=='2'):
                board[i][j] = -1
            else:
                board[i][j] = 0
    return board

def get_reward_function():
    reward_function = np.zeros(shape=(3139, 9, 3139))
    state_space = get_state_space(3)
    global_state_space = state_space.copy()
    action_space = list(range(9))
    for i in range(len(state_space)):
        curr = state_space[i]
        for j in action_space:
            if(curr[j]=='0'):
                transition_state = curr.copy()
                transition_state[j] = '1'
                winr = 0
                for t in range(len(transition_state)):
                    possible_nxt = transition_state.copy()
                    if(possible_nxt[t]=='0'):
                        possible_nxt[t] = '2'
                        winr = winner(make_board(possible_nxt))
                        k = getIndex(possible_nxt)
                        if(winr==1):
                            reward_function[i][j][k] = 100
                        elif(winr==-1):
                            reward_function[i][j][k] = -100
                        elif(winr==-2):
                            reward_function[i][j][k] = 10
    return reward_function



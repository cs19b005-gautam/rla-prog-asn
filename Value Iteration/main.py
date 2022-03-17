# import modules
import math
import random
from state_space import get_state_space
import pygame
import numpy as np
from pygame.locals import *
from reward_function import get_reward_function

n = 3#int(input("Enter the size of the Tic-Tac-Toe : "))

pygame.init()

nsq = n**2

screen_height = n*100
screen_width = n*100
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# define font
font = pygame.font.SysFont(None, 40)

# define variables
clicked = False
player = 1
pos = (0,0)
markers = []
game_over = False
winner = 0

# setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# create empty 3 x 3 list to represent the grid
for x in range (n):
    row = [0] * n
    markers.append(row)

def C(n,r):
    num,prod = n,1
    for i in range(1,r+1):
        prod *= num
        prod /= i
        num -= 1
    return prod

def factorial(n):
    if(n==0):
        return 1
    else:
        return n*factorial(n-1)


def draw_board():
    bg = (255, 255, 210)
    grid = (50, 50, 50)
    screen.fill(bg)
    for x in range(1,n):
        pygame.draw.line(screen, grid, (0, 100 * x), (screen_width,100 * x), line_width)
        pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
            if y == -1:
                pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
            y_pos += 1
        x_pos += 1


def check_game_over():
    global game_over
    global winner

    x_pos = 0
    for x in markers:
        # check columns
        if sum(x) == n:
            winner = 1
            game_over = True
        if sum(x) == -n:
            winner = 2
            game_over = True
        # check rows
        row_sum = 0
        for i in range(n):
            row_sum += markers[i][x_pos]
        if row_sum == n:
            winner = 1
            game_over = True
        if row_sum == -n:
            winner = 2
            game_over = True
        x_pos += 1

    # check cross
    back_slash,forward_slash = 0,0
    for i in range(n):
        back_slash += markers[i][i]
        forward_slash += markers[i][n-1-i]
    if back_slash == n or forward_slash == n:
        winner = 1
        game_over = True
    if back_slash == -n or forward_slash == -n:
        winner = 2
        game_over = True

    # check for tie
    if game_over == False:
        tie = True
        for row in markers:
            for i in row:
                if i == 0:
                    tie = False
        # if it is a tie, then call game over and set winner to 0 (no one)
        if tie == True:
            game_over = True
            winner = 0



def draw_game_over(winner):

    if winner != 0:
        end_text = "Player " + str(winner) + " wins!"
    elif winner == 0:
        end_text = "You have tied!"

    end_img = font.render(end_text, True, blue)
    pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
    screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, green, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

attempt = []

def calc_state_size(n): # number of grids should be given as argument at function call
    if(n%2==0):
        n+=1
    _sum = 0
    for i in range(0,n,2):
        num = C(n,i)
        num *= factorial(i)
        num /= factorial(i/2)**2
        _sum+= int(num)
        attempt.append(_sum-1)
    return _sum

# set state space, action space and transition function
state_space_size = calc_state_size(n**2)

action_space_size = n**2
action_space = []
state_space = get_state_space(n)
W = [0]*3139
gamma = 0.9 # look over future more often

for i in range(0,n):
    for j in range(0,n):
        action_space.append((i,j))

prob_tans_func = np.array([[[.0]*state_space_size]*action_space_size]*state_space_size)
# Here I have been facing a problem for a tic tac toe with n-rows and n-columns and looks the problem the state size for 4size row and column increases and looks 3D-array of that size couldn't be created

# TODO create a policy



def state_of_board(markers):
    l = []
    for i in range(0, n):
        for j in range(0,n):
            if(markers[i][j]==1):
                l.append('1')
            elif(markers[i][j]==-1):
                l.append('2')
            else:
                l.append('0')
    return l

# TODO List of all state spaces
# TODO insert all state spaces into state_space list
# def swapper(l, start, curr):
#     for i in range(start, curr):
#         if l[i] == l[curr]:
#             return 0
#     return 1
#
# def findPermutations(_l, index, _n):
#     if index >= n:
#         state_space.append(_l.copy())
#         return
#
#     for i in range(index, n):
#
#         check = swapper(_l, index, i)
#         if check:
#             _l[index], _l[i] = _l[i], _l[index]
#             findPermutations(_l, index + 1, n)
#             _l[index], _l[i] = _l[i], _l[index]
#
#
# max_tries = 1+math.floor((n**2)/2)
# for i in range(1,max_tries):
#     lis = list('0'*(n**2))
#     _num = 0
#     for j in (0,i):
#         lis[j] = '1'
#         _num = j
#     for j in (_num+1,_num+1+i):
#         if(j<n**2 - 1):
#             lis[j] = '2'
#             _num = j
#     findPermutations(lis, 0, n**2)
#

print('len = ',len(state_space))
# TODO make a function to map state space to index of probability transition function
def getIndex(e):
    for i in range(len(state_space)):
        if(state_space[i] == e):
            return i
    return -1
# TODO give probability values in probability state function

def setProbabilityFunction():
    for i in range(len(state_space)):
        for j in range(n**2):
            curr = state_space[i].copy()
            if(curr[j]=='0'):
                nxt = curr.copy()
                nxt[j] = '1'
                indices = []
                __sum = 0
                for l in range(len(nxt)):
                    temp = nxt.copy()
                    if(nxt[l]=='0'):
                        temp[l] = '2'
                        k = getIndex(temp)
                        indices.append(k)
                        prob_tans_func[i][j][k] = random.randint(1,9)
                        __sum += prob_tans_func[i][j][k]
                if(__sum!=0):
                    for k in range(len(indices)-1):
                        prob_tans_func[i][j][indices[k]] = prob_tans_func[i][j][indices[k]]/__sum
                    prob_tans_func[i][j][indices[len(indices)-1]] = 1-sum(prob_tans_func[i][j])


setProbabilityFunction()

# TODO make a random policy


def get_policy_position(markers):
    for i in range(0,n):
        for j in range(0,n):
            if(markers[i][j]==0):
                return [i,j]
    return [-1,-1]

def str_to_list(s):
    l = []
    for i in s:
        l.append(i)
    return l

def list_to_str(l):
    s = ''
    for i in l:
        s = s+i
    return s

def get_RL_position(markers, action):

    state = state_of_board(markers)
    j = action[0] * n + action[1]
    curr = state.copy()
    curr[j] = '0'
    i = getIndex(curr)
    nxt = state.copy()
    indices = []
    prb = []
    possible_states = []
    for l in range(len(nxt)):
        temp = nxt.copy()
        if(nxt[l]=='0'):
            temp[l] = '2'
            state_index = getIndex(temp)
            possible_states.append(list_to_str(temp))
            indices.append(state_index)
            prb.append(prob_tans_func[i][j][state_index])
    curr_state = curr.copy()
    if(len(possible_states)==0):
        return [-1,-1]
    nxt_st = np.random.choice(possible_states, 1, prb)[0]
    nxt_state = str_to_list(nxt_st)
    pos = -1
    print('state = ',state)
    print('nxt_st = ', nxt_st)
    print('nxt_state = ',nxt_state)
    for el in range(n**2):
        if(state[el]!=nxt_state[el]):
            pos = el

    # print('state = ', state)
    # i = getIndex(state)
    # curr = state.copy()
    # nxt = state.copy()
    # nxt[j] = '1'
    # print(nxt)
    # possible_states = []
    # prb = []
    # indices = []
    # for k in range(len(nxt)):
    #     temp = nxt.copy()
    #     if(nxt[k]=='0'):
    #         temp[k] = '2'
    #         possible_states.append(list_to_str(temp))
    #         gau = getIndex(temp)
    #         indices.append(gau)
    #         p = prob_tans_func[i][j][gau]
    #         prb.append(p)
    # if(len(possible_states)==0):
    #     return [-1,-1]
    # print('i = ', i, ' j = ', j)
    # for i in range(len(prb)):
    #     print('state = ', possible_states[i], ':: p = ', prb[i], ':: var = ', indices[i] )
    # for i in range(1,9):
    #     print(prob_tans_func[0][0][i], end= ',')
    # print(' ')
    # nxt_st = np.random.choice(possible_states, 1, p = prb)[0]
    # print(nxt_st)
    # nxt_state = str_to_list(nxt_st)
    # pos = -1
    # for i in range(n**2):
    #     if(curr[i]!=nxt_state[i]):
    #         pos = i

    # if sum(prob_tans_func[i][j]) !=1:
    #     print(state_space[i])
    # nxt_index = np.random.choice(range(len(state_space)), 1, p = prob_tans_func[i][j])
    # nxt = state_space[nxt_index[0]]
    # pos = -1
    # curr = state
    # for i in range(n**2):
    #     if(curr[i]!=nxt[i]):
    #         pos = i
    pos_x = pos//n
    pos_y = pos%n
    return [pos_x, pos_y]

reward_function = get_reward_function()
policy = np.zeros(shape=(3139,1))

def get_value_function():
    W1 = np.zeros(shape=(3139,1))
    for _p in range(1000):
        Wnew = W1.copy()
        for i in range(len(W1)):
            temp_val = []
            for a in range(len(action_space)): # checking for each action where does this action occur
                temp = 0
                for j in range(len(state_space)): # summation of j
                    temp+=prob_tans_func[i][a][j]*(reward_function[i][a][j]+(gamma*Wnew[j]))
                    # W1[i] = max{aEA} Sigma j =0 to n-1 [P(i,a,j)*(R(i,a,j)+gamma*W0[j])]
                # if(temp_val[0]<temp):
                #     temp_val[0] = temp
                #     temp_val[1] = a
                temp_val.append(temp)
            maxi = -400
            act = -1
            for a in range(len(temp_val)):
                if(maxi<temp_val[a]):
                    maxi = temp_val[a]
                    act = a
            Wnew[i] = maxi
            policy[i] = a
        W1 = Wnew
    return W1

V = get_value_function()

# def policy_extraction():
#     for i in range(len(state_space)):
#         temp =
#         for a in range(len(action_space)):
#
#     return 1


def val_pi(markers):
    curr = state_of_board(markers)
    i = getIndex(curr)
    action = policy[i]
    cell_x = action%3
    cell_y = action//3
    return [cell_x, cell_y]


# main loop
run = True
while run:

    # draw board and markers first
    draw_board()
    draw_markers()

    #handle events
    for event in pygame.event.get():
        #handle game exit
        if event.type == pygame.QUIT:
            run = False
        #run new game
        if game_over == False:
            # #check for mouseclick
            # if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            #     clicked = True
            # if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            #     clicked = False
            #     pos = pygame.mouse.get_pos()
            #     cell_x = pos[0] // 100
            #     cell_y = pos[1] // 100

                pos = val_pi(markers)
                cell_x = pos[0]
                cell_y = pos[1]
                if markers[cell_x][cell_y] == 0:
                    #get an RL position

                    if markers[cell_x][cell_y] == 0:
                        board = markers.copy()
                        markers[cell_x][cell_y] = 1
                        check_game_over()
                        RL_cell = [-1,-1]
                        if not game_over:
                            RL_cell = get_RL_position(board, pos)
                    if RL_cell[0] != -1 or RL_cell[1]!=-1:
                        if(markers[RL_cell[0]][RL_cell[1]]==0):
                            markers[RL_cell[0]][RL_cell[1]] = -1
                    check_game_over()

    #check if game has been won
    if game_over == True:
        draw_game_over(winner)
        #check for mouseclick to see if we clicked on Play Again
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                #reset variables
                game_over = False
                player = 1
                pos = (0,0)
                markers = []
                winner = 0
                #create empty 3 x 3 list to represent the grid
                for x in range (n):
                    row = [0] * n
                    markers.append(row)

    #update display
    pygame.display.update()

pygame.quit()

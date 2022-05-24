import torch
import random
from snake import AISnakeGame, Initialize, Vector2
import numpy as np
from collections import deque
import os
from model import Linear_QNet, QTrainer
from helper import plot
from math import floor
import asyncio
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.size = open(f"{os.path.dirname(os.path.abspath(__file__))}\config.snake","r").readlines()[1].rstrip().split(" ")[1].split(":")
        self.position = Vector2(int(floor(int(self.size[0])/2)),int(floor(int(self.size[1])/2)))
        self.model = Linear_QNet(12,256,4) #TODO
        self.trainer = QTrainer(self.model, lr=LR,gamma=self.gamma) # HOW TO LOAD MODEL: THESE 3 LINES OF CODE
        #self.model.load_state_dict(torch.load("./model/model.smort"))
        #self.model.eval()
        #TODO model, trainer
    def get_state(self,game):
        head = game.position
        #s = open(f"{os.path.dirname(os.path.abspath(__file__))}\config.snake","r").readlines()[1].rstrip().split(" ")[1].split(":")
        s = game.size
        #up down left right
        apple_loc_raw = game.apple.position.ToList()
        state = [head.y == 2,head.y == int(s[1])-2,head.x == 3,head.x == int(s[0])-1,game.rotation == 1,game.rotation == 2,game.rotation == 3,game.rotation == 4,apple_loc_raw[1] < head.y,apple_loc_raw[1] > head.y,apple_loc_raw[0] < head.x,apple_loc_raw[0] > head.x]
        #open("app.txt","a").write(str(state[len(state):len(state)-5:-1]) + "\n")
        return np.array(state, dtype=int)
    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
    def train_lmemory(self):
        if len(self.memory) > BATCH_SIZE:mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:mini_sample = self.memory
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)
    def train_smemory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    def get_action(self, state):
        #random moves in beginning
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,3)
            final_move[move] = 1
        else:
            #print(state)
            #print(torch.tensor(state,dtype=torch.float))
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
def train():
    plot_scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = AISnakeGame()
    while True:
        #time.sleep(0.2)
        #get old state
        state_old = agent.get_state(game)
        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, done, score, pos = asyncio.run(game.Step(final_move))
        state_new = agent.get_state(game)

        agent.train_smemory(state_old,final_move,reward,state_new,done)

        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            #lmemory training
            #game.reset()
            game = AISnakeGame()
            agent.n_games += 1
            agent.train_lmemory()
            agent.position = pos
            if score > record: 
                record = score
                agent.model.save()
            #print("Game",agent.n_games,"Score: ",score,"Record:",record)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            mean_scores.append(mean_score)
            plot(plot_scores,mean_scores)
if __name__ == '__main__':
    #game = AISnakeGame()
    #game.Initialize()
    #game.CreateMap()
    Initialize()
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(apple.position.x)
    train()
def import_stuff():
    global torch,random,AISnakeGame,Initialize,Vector2,np,deque,os,Linear_QNet,QTrainer,plot,asyncio,floor,keyboard,time,Config_editor,playsound
    import torch
    import random
    from snake import AISnakeGame, Vector2
    import numpy as np
    from collections import deque
    import os
    from model import Linear_QNet, QTrainer
    from helper import plot
    from math import floor
    import asyncio
    import keyboard
    from config_editor import Config_editor
    import time
    from playsound import playsound
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
input_value = 0

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.rdm = 80
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        try:
            self.size = open(f"{os.path.dirname(os.path.abspath(__file__))}\config.snake","r").readlines()[1].rstrip().split(" ")[1].split(":")
        except:
            self.size = ['10','10']
        self.position = Vector2(int(floor(int(self.size[0])/2)),int(floor(int(self.size[1])/2)))
        self.model = Linear_QNet(12,256,4) #TODO
        self.trainer = QTrainer(self.model, lr=LR,gamma=self.gamma) # HOW TO LOAD MODEL: THESE 3 LINES OF CODE
        try:
            self.rdm = 0
            self.model.load_state_dict(torch.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake')).readlines()[5].rstrip().split(' ')[1])) #self.model.load_state_dict(torch.load("./model/model.smort"))
            self.model.eval()
        except:
            pass
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
        self.epsilon = self.rdm - self.n_games
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
async def train():
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
        reward, done, score, pos = await game.Step(final_move)
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
        if keyboard.is_pressed('ctrl + a'): agent.model.save()
        if keyboard.is_pressed('ctrl + s'): input(); agent.model.save(input("Model name: ")+'.smort');os.system('cls' if os.name == 'nt' else 'clear')
        if keyboard.is_pressed('q'):quit()
#MENU
def play_switch():
    if bool(int(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake')).readlines()[3].split(' ')[1])): playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sounds','Menuswitch2.wav'),False)
def play_select():
    if bool(int(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake')).readlines()[3].split(' ')[1])): playsound(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sounds','Menuselect.wav'),False)
async def file_manager():
    input()
    os.system('cls' if os.name == 'nt' else 'clear')
    val = 0
    last_input_received = -2
    dirs = [name for name in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'model'))]
    while len(dirs)>0:
        await asyncio.sleep(0.01)
        if should_return: return
        if keyboard.is_pressed("w") and val > 0 and last_input_received != 0:val-=1;last_input_received = 0;play_switch()
        elif not keyboard.is_pressed("w") and last_input_received == 0: last_input_received = -1
        if keyboard.is_pressed("s") and val < len(dirs)-1 and last_input_received != 1:val+=1;last_input_received = 1;play_switch()
        elif not keyboard.is_pressed("s") and last_input_received == 1: last_input_received = -1
        if keyboard.is_pressed("q"):quit()
        print("\033[F"*(len(dirs)+2))
        out = ""
        for file in dirs:
            if file == dirs[val]:
                out += file + " ■" + '\n'
            else:    
                out += file + "  " + '\n'
        print("\033[92m",out,"\033[0m")
        if keyboard.is_pressed('enter') and last_input_received != -2: play_select();return dirs[val]
async def change_value(typea,name,b = False):
    input()
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            if typea == 'float': input();return float(input(f"New value of \033[92m{name}\033[0m: "))
            elif typea == 'int': return int(input(f"New value of \033[92m{name}\033[0m): "))
            elif typea == 'bool': return int(b)
            elif typea == 'str': input();return input(f"New value of \033[92m{name}\033[0m: ")
            elif typea == 'path': return await file_manager()
            break
        except:
            pass
should_return = False
async def act(inp,n, b = False):
    global should_return
    out = True
    if inp == 0:out = await change_value('float',n)
    elif inp == 1: out = await change_value('str',n)
    elif inp == 2: out = await change_value('bool',n, b)
    elif inp == 3: out = await change_value('bool',n, b)
    elif inp == 4: out = await change_value('bool',n, b)
    elif inp == 5: out = os.path.join(os.path.dirname(os.path.abspath(__file__)),'model', await change_value('path',n))
    elif inp == 6: should_return = True
    os.system('cls' if os.name == 'nt' else 'clear')
    return out
async def options():
    global should_return
    should_return = False
    os.system('cls' if os.name == 'nt' else 'clear')
    c_editor = Config_editor()
    last_input_received = -2
    val = 0
    while True:
        await asyncio.sleep(0.01)
        if should_return: return
        if keyboard.is_pressed("w") and val > 0 and last_input_received != 0:val-=1;last_input_received = 0;play_switch()
        elif not keyboard.is_pressed("w") and last_input_received == 0: last_input_received = -1
        if keyboard.is_pressed("s") and val < 6 and last_input_received != 1:val+=1;last_input_received = 1;play_switch()
        elif not keyboard.is_pressed("s") and last_input_received == 1: last_input_received = -1
        if keyboard.is_pressed("q"):quit()
        settings = c_editor.get_settings()
        settings.append("back")
        #settings = {i.split(" ")[0]:i.split(" ")[1] for i in names}
        print("\033[F"*(len(settings)+4))
        active_line = settings[val]
        out = ""
        for setting in settings:
            if active_line == setting:
                out += str(setting).replace(',',' ').replace('\'','') + " ■" + "\n"
            else:
                out += str(setting).replace(',',' ').replace('\'','') + "  " + "\n"
        out += "\nNavigate with W/A interact with Enter"
        print("\033[92m",out,"\033[0m")
        b = False
        try:
            b = bool(int(settings[val].split(' ')[1 if val > 1 and val < 5 else 0]))
        except:
            pass
        if keyboard.is_pressed('enter') and last_input_received != -2: last_input_received = -2; play_select() ;c_editor.change_setting(list(c_editor.TYPE_OF_SETTINGS.keys())[val],await act(val,settings[val].split(' ')[0],False if b else True))
        elif not keyboard.is_pressed('enter') and last_input_received == -2: last_input_received = -1
        c_editor.save()
class button:
    def __init__(self,w = 20,h = 5,text = "Button",pl = "\t",pb = 2,sc = "|",tcbc = "_",cursor = '■',v = True) -> None:
        self.width = w
        self.height = h
        self.text = text
        self.indent = pl
        self.bottom_margin = pb
        self.side_char = sc
        self.top_bottom_char = tcbc
        self.active = False
        self.cursor = cursor
        self.visible = v
    def change_text(self,txt):
        self.text = txt
    async def activate(self):
        global buttons,c_editor
        if self.text == 'Quit': quit()
        elif self.text == 'Train AI': await train()
        elif self.text == 'Play without AI ': game = AISnakeGame(); await asyncio.gather(game.heuristic_loop(),AISnakeGame.GetInput())
        elif self.text == 'Configure ':
            os.system('cls' if os.name == 'nt' else 'clear')
            await options()
        #    buttons[0].change_text('Refresh rate')
        #    buttons[1].change_text('Sound')
        #    buttons[2].change_text('Animations')
        #    buttons[3].change_text('Load')
        #elif self.text == 'Refresh rate': c_editor.change_setting('refresh_rate',self.ask_input('refresh rate'))
        #elif self.text == 'Sound': c_editor.change_setting('playsound',self.ask_input('sound','[0/1]'))
        #elif self.text == 'Animations': c_editor.change_setting('animations',self.ask_input('animations','[0/1]'))
        #elif self.text == 'Load' : self.file_manager()
    def ask_input(self,name,other=''):
        os.system('cls' if os.name == 'nt' else 'clear')
        return input(f"\tSet {name} to{other}: ")
   # def file_manager(self):
   #     os.system('cls' if os.name == 'nt' else 'clear')
   #     folders = [os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)]
   #     while True:
   #         time.sleep(0.01)
   #         if keyboard.is_pressed("w") and val > 0 and last_input_received != 0:val-=1;last_input_received = 0
   #         elif not keyboard.is_pressed("w") and last_input_received == 0: last_input_received = -1
   #         if keyboard.is_pressed("s") and val < 3 and last_input_received != 1:val+=1;last_input_received = 1
   #         elif not keyboard.is_pressed("s") and last_input_received == 1: last_input_received = -1
   #         if keyboard.is_pressed("q"):quit()
   #         
async def get_input_menu():
    global input_value,buttons
    Config_editor()
    last_input_received = -1
    val = 0
    buttons = [button(text="Train AI"),button(text="Play without AI "),button(text="Configure "),button(text="Quit")]
    d = {
        buttons[0] : 0,
        buttons[1] : 1,
        buttons[2] : 2,
        buttons[3] : 3
    }
    while True:
        await asyncio.sleep(0.01)
        if keyboard.is_pressed("w") and val > 0 and last_input_received != 0:val-=1;last_input_received = 0;play_switch()
        elif not keyboard.is_pressed("w") and last_input_received == 0: last_input_received = -1
        if keyboard.is_pressed("s") and val < 3 and last_input_received != 1:val+=1;last_input_received = 1;play_switch()
        elif not keyboard.is_pressed("s") and last_input_received == 1: last_input_received = -1
        if keyboard.is_pressed("q"):quit()  
        #\033[F puts cursor in start of line
        print("\033[F"*(len(buttons)*(buttons[0].height+buttons[0].bottom_margin)+2))
        #os.system('cls' if os.name == 'nt' else 'clear')
        out = ""
        active_btn = 0
        for btn in buttons:
            if d[btn] == val: 
                btn.active = True
                active_btn = btn
            else:
                btn.active = False
            for i in range(btn.height):
                if i == floor(btn.height/2): out += f"{btn.indent}{btn.cursor if btn.active else btn.side_char}{' '*(floor(btn.width/2) - floor(len(btn.text)/2))}{btn.text}{' '*(floor(btn.width/2) - floor(len(btn.text)/2))}{btn.cursor if btn.active else btn.side_char}\n"
                else: out += f"{btn.indent}{btn.top_bottom_char*(btn.width+1) if i == 0 or i == btn.height-1 else btn.side_char + ' ' * (btn.width) + btn.side_char}\n";
            out+= "\n"*btn.bottom_margin
        print("\033[92m",out,"\033[0m")
        if keyboard.is_pressed('enter') and last_input_received != -2: last_input_received = -2; play_select();await active_btn.activate()
        elif not keyboard.is_pressed('enter') and last_input_received == -2: last_input_received = -1
if __name__ == '__main__':
    #game = AISnakeGame()
    #game.Initialize()
    #game.CreateMap()
    import snake
    snake.Initialize()
    import_stuff()
    os.system('cls' if os.name == 'nt' else 'clear')
    asyncio.run(get_input_menu())
    #print(apple.position.x)
    #train()
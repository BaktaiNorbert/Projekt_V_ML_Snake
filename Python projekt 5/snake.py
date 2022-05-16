#must install keyboard module pip install keyboard
#must install aioconsole module pip install aioconsole maybe
#Python 3.10 or above required
import keyboard
import time 
from math import floor
import asyncio #több loop egyszerre tudjon futni
import os #Konzol tisztításának módszeréhez
class Vector2: #for convinience, should contain 2 numbers.
    def __init__(self, ix, iy):
        self.x = ix
        self.y = iy
class Viewport:
    def __init__(self, size = Vector2(30,30), top_character="_",bottom_character="_",wall_character="|"):
        self.resolution = size
        self.top = top_character
        self.bottom = bottom_character
        self.wall = wall_character
    def display(self, s):
        out = ""
        if isinstance(s,str):
            out = s
        elif isinstance(s,list):
            for i in range(len(s)):
                out += str(s[i])
        os.system('cls' if os.name == 'nt' else 'clear')
        print(out) #clear console then print output.
    def replaceCharacter(x,y,s):
        middle[y] = middle[y][:x] + s + middle[y][x+1:]
class Player:
    def __init__(self, pos, rot, hd):
        self.position = pos
        self.rotation = rot
        self.head = hd
        self.points = 0
    def add_point(self, amount = 1):
        self.points += amount
class Body:
    def __init__(self, char = '■', pos = Vector2(0,0), offs = Vector2(0,0)):
        self.character = char
        self.position = pos
        self.local_position = offs #offset, eltolás
#class Food:
#CREATING MAP
heuristic = False
if os.path.exists("./config.snake"):
    l = open("config.snake","r").readlines()
    refresh_rate = float(l[0].rstrip().split(" ")[1])
    area = l[1].rstrip().split(" ")[1].split(":")
    heuristic = bool(int(l[2].rstrip().split(" ")[1]))
else:
    area = (input("Kérem adja meg a pálya méretét szóközökkel elválasztva: ").split(" ")) #kézileg pálya megadása
    refresh_rate = 0.3
screen = Viewport(Vector2(int(area[0]),int(area[1])))#Kijelző készítése
top = f" {screen.top*screen.resolution.x}\n" #plafon
middle = (f"|{' '*screen.resolution.x}|\nz"*screen.resolution.y).split("z") #sides + playable area
bottom = f"{screen.wall}{screen.bottom*screen.resolution.x}{screen.wall}" #alja a pályának
#CREATING PLAYER(the Snake)
head = Body(">")
player = Player(Vector2(int(floor(screen.resolution.x/2)),int(floor(screen.resolution.y/2))),0,head)
#Viewport.replaceCharacter(player.position.x,player.position.y,head.character)
#for i in range(len(player.bodies)):
#    Viewport.replaceCharacter(player.position.x - i - 1, player.position.y, player.bodies[i].character)
middle_out = ""
for line in middle:
    middle_out += line
#START GAME
os.system('cls' if os.name == 'nt' else 'clear')
inp = 0
last_positions = [Vector2(int(floor(screen.resolution.x/2))-3,int(floor(screen.resolution.y/2))),Vector2(int(floor(screen.resolution.x/2))-2,int(floor(screen.resolution.y/2))),Vector2(int(floor(screen.resolution.x/2))-1,int(floor(screen.resolution.y/2)))]
async def GetInput(): # w - 1, s - 2, a - 3, d - 4, q gomb - quit()
    global inp
    global player
    while True:
        await asyncio.sleep(0.017)
        if keyboard.is_pressed("w") and player.rotation != 2:player.rotation = 1
        elif keyboard.is_pressed("s")and player.rotation != 1:player.rotation = 2
        elif keyboard.is_pressed("a")and player.rotation != 4:player.rotation = 3
        elif keyboard.is_pressed("d")and player.rotation != 3:player.rotation = 4
        elif keyboard.is_pressed("q"):quit() #Mit nyomott le a jatekos
async def RunGame():
    while True:
        await asyncio.sleep(refresh_rate)#0.3 másodpercenként frissül a játék
        middle = (f"|{' '*screen.resolution.x}|\nz"*screen.resolution.y).split("z") #sides + playable area
        if player.position.x == screen.resolution.x + 1 or player.position.x == 1 or player.position.y == screen.resolution.y-1 or player.position.y == 0:
                screen.display([top,f"|{' '*int(floor(screen.resolution.x/2-4))}GAME OVER\n",bottom])#kiírás
                time.sleep(2)
                quit()
        match player.rotation: #switch
            case 1:
                player.position.y -= 1
                player.head.character = "^"
            case 2:
                player.position.y += 1
                player.head.character = "ˇ"
            case 3:
                player.position.x -= 1
                player.head.character = "<" 
            case 4:
                player.position.x += 1
                player.head.character =">"   
        Viewport.replaceCharacter(player.position.x,player.position.y,head.character)
        last_positions.append(player.position)
        if len(last_positions) > player.points+3:
            Viewport.replaceCharacter(last_positions[0].x,last_positions[0].y," ")
            last_positions.pop(0)
        for position in last_positions:
            Viewport.replaceCharacter(position.x,position.y,"■")
        middle_out = ""
        for line in middle:
            middle_out += line
        screen.display([top,middle_out,bottom]) 
        print("Length: ",len(last_positions),"Position:",player.position.x,player.position.y)
        
async def Main():
    await asyncio.gather(GetInput(),RunGame())
asyncio.run(Main())
#must install keyboard module pip install keyboard
#must install playsound module pip install playsound=1.2.2
#Python 3.10 or above required
import keyboard
import time 
from math import floor
import asyncio #több loop egyszerre tudjon futni
from os import system, path, name #Konzol tisztításának módszeréhez
from random import randint
from playsound import playsound
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
        print("\033[F"*(len(middle)+4)) #clear console then print output.
        print(out)
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
#Initialize
#CREATING MAP
heuristic = False
if path.exists("./config.snake"):
    f = open("config.snake","r")
    l = f.readlines()
    refresh_rate = float(l[0].rstrip().split(" ")[1])
    area = l[1].rstrip().split(" ")[1].split(":")
    heuristic = bool(int(l[2].rstrip().split(" ")[1]))
    f.close()
else:
    area = (input("Kérem adja meg a pálya méretét szóközökkel elválasztva: ").split(" ")) #kézileg pálya megadása
    refresh_rate = 0.3
screen = Viewport(Vector2(int(area[0]),int(area[1])))#Kijelző készítése
top = f" {screen.top*screen.resolution.x}\n" #plafon
middle = (f"|{' '*screen.resolution.x}|\nz"*screen.resolution.y).split("z") #sides + playable area
bottom = f"{screen.wall}{screen.bottom*screen.resolution.x}{screen.wall}" #alja a pályának
#CREATING PLAYER(the Snake)
head = Body(">")
player = Player(Vector2(int(floor(screen.resolution.x/2)),int(floor(screen.resolution.y/2))),4,head)
middle_out = ""
apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
for line in middle:
    middle_out += line
#START GAME
system('cls' if name == 'nt' else 'clear')#clear screen
inp = 4
last_positions = []
pause = False
sound_allowed = True
def GameOver():
        system('cls' if name == 'nt' else 'clear')
        playsound("./sounds/ouch.wav", 0)
        print("\u001b[31m  .-_'''-.      ____    ,---.    ,---.    .-''-.              ,-----.    ,---.  ,---.   .-''-.  .-------.     \n '_( )_   \   .'  __ `. |    \  /    |  .'_ _   \           .'  .-,  '.  |   /  |   | .'_ _   \ |  _ _   \    \n|(_ o _)|  ' /   '  \  \|  ,  \/  ,  | / ( ` )   '         / ,-.|  \ _ \ |  |   |  .'/ ( ` )   '| ( ' )  |    \n. (_,_)/___| |___|  /  ||  |\_   /|  |. (_ o _)  |        ;  \  '_ /  | :|  | _ |  |. (_ o _)  ||(_ o _) /    \n|  |  .-----.   _.-`   ||  _( )_/ |  ||  (_,_)___|        |  _`,/ \ _/  ||  _( )_  ||  (_,_)___|| (_,_).' __  \n'  \  '-   .'.'   _    || (_ o _) |  |'  \   .---.        : (  '\_/ \   ;\ (_ o._) /'  \   .---.|  |\ \  |  | \n \  `-'`   | |  _( )_  ||  (_,_)  |  | \  `-'    /         \ `\"/  \  ) /  \ (_,_) /  \  `-'    /|  | \ `'   / \n  \        / \ (_ o _) /|  |      |  |  \       /           '. \_/``\".'    \     /    \       / |  |  \    /  \n   `'-...-'   '.(_,_).' '--'      '--'   `'-..-'              '-----'       `---`      `'-..-'  ''-'   `'-'   \n \033[0m")
        time.sleep(2)
        quit()
async def PlaySound():
    playsound("./sounds/click.wav")
async def GetInput(): # w - 1, s - 2, a - 3, d - 4, p - quit(), p - pause
    global player
    global pause
    global inp
    while True:
        await asyncio.sleep(0.005)
        if keyboard.is_pressed("w") and player.rotation != 2 and inp != 1:inp = 1; await PlaySound()
        elif keyboard.is_pressed("s")and player.rotation != 1 and inp != 2:inp = 2; await PlaySound()
        elif keyboard.is_pressed("a")and player.rotation != 4 and inp != 3:inp = 3; await PlaySound()
        elif keyboard.is_pressed("d")and player.rotation != 3 and inp != 4:inp = 4; await PlaySound()
        elif keyboard.is_pressed("q"):quit() #Kilépés
        elif keyboard.is_pressed("p"):pause = not pause #Megállítás átmenetileg
async def RunGame():
    first_frame = True
    global apple
    while True:
        await asyncio.sleep(refresh_rate)#refresh_rate másodpercenként frissül a játék
        player.rotation = inp
        if not pause:
            if player.position.x == screen.resolution.x + 1 or player.position.x == 1 or player.position.y == screen.resolution.y or player.position.y == 0:
                GameOver()
            for vectors in last_positions:
                if player.position.x == vectors.x and player.position.y == vectors.y and last_positions.index(vectors) != len(last_positions)-1:
                    GameOver()
            if player.position.x == apple.position.x and player.position.y == apple.position.y:
                player.points += 1
                playsound("./sounds/Score.wav",0)
                apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
                for i in last_positions:
                    if apple.position.x == i.x and apple.position.y == i.y:
                        apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
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
            Viewport.replaceCharacter(apple.position.x,apple.position.y,apple.character)
            if not first_frame or player.position.x != int(floor(screen.resolution.x/2)) or player.position.y != int(floor(screen.resolution.y/2)):
                last_positions.append(Vector2(player.position.x,player.position.y))
            if len(last_positions) > player.points+3:
                Viewport.replaceCharacter(last_positions[0].x,last_positions[0].y," ")
                last_positions.pop(0)
            for position in last_positions:
                Viewport.replaceCharacter(position.x,position.y,"■")
            Viewport.replaceCharacter(player.position.x,player.position.y,player.head.character)
            middle_out = ""
            for line in middle:
                middle_out += line
            screen.display([top,middle_out,bottom])
            first_frame = False
            print("Length: \033[33m",len(last_positions),"\033[00m Position:\033[33m",player.position.x,player.position.y,"\033[00m\033[0m")
async def Main():
    print(f"\033[92m           _____                    _____                    _____                    _____                    _____          \n          /\    \                  /\    \                  /\    \                  /\    \                  /\    \         \n         /::\    \                /::\____\                /::\    \                /::\____\                /::\    \        \n        /::::\    \              /::::|   |               /::::\    \              /:::/    /               /::::\    \       \n       /::::::\    \            /:::::|   |              /::::::\    \            /:::/    /               /::::::\    \      \n      /:::/\:::\    \          /::::::|   |             /:::/\:::\    \          /:::/    /               /:::/\:::\    \     \n     /:::/__\:::\    \        /:::/|::|   |            /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \    \n     \:::\   \:::\    \      /:::/ |::|   |           /::::\   \:::\    \      /::::\    \              /::::\   \:::\    \   \n   ___\:::\   \:::\    \    /:::/  |::|   | _____    /::::::\   \:::\    \    /::::::\____\________    /::::::\   \:::\    \  \n  /\   \:::\   \:::\    \  /:::/   |::|   |/\    \  /:::/\:::\   \:::\    \  /:::/\:::::::::::\    \  /:::/\:::\   \:::\    \ \n /::\   \:::\   \:::\____\/:: /    |::|   /::\____\/:::/  \:::\   \:::\____\/:::/  |:::::::::::\____\/:::/__\:::\   \:::\____\ \n \:::\   \:::\   \::/    /\::/    /|::|  /:::/    /\::/    \:::\  /:::/    /\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /\n  \:::\   \:::\   \/____/  \/____/ |::| /:::/    /  \/____/ \:::\/:::/    /  \/____|::|   |           \:::\   \:::\   \/____/ \n   \:::\   \:::\    \              |::|/:::/    /            \::::::/    /         |::|   |            \:::\   \:::\    \     \n    \:::\   \:::\____\             |::::::/    /              \::::/    /          |::|   |             \:::\   \:::\____\    \n     \:::\  /:::/    /             |:::::/    /               /:::/    /           |::|   |              \:::\   \::/        \n      \:::\/:::/    /              |::::/    /               /:::/    /            |::|   |               \:::\   \/____/     \n       \::::::/    /               /:::/    /               /:::/    /             |::|   |                \:::\    \         \n        \::::/    /               /:::/    /               /:::/    /              \::|   |                 \:::\____\        \n         \::/    /                \::/    /                \::/    /                \:|   |                  \::/    /        \n          \/____/                  \/____/                  \/____/                  \|___|                   \/____/         \n                                                                                                                              \033[0m")
    s = " "*123
    for i in range(63):
        s = s[:64-i] + "_"*i*2 + s[64 + i+1::]
        print("\033[F\033[92m",s)
        time.sleep(0.006)
    print("\033[F"*23 + "           _____                    _____                    _____                    _____                    _____          \n          /\    \                  /\    \                  /\    \                  /\    \                  /\    \         \n         /oo\    \                /oo\____\                /oo\    \                /oo\____\                /oo\    \        \n        /oooo\    \              /oooo|   |               /oooo\    \              /ooo/    /               /oooo\    \       \n       /oooooo\    \            /ooooo|   |              /oooooo\    \            /ooo/    /               /oooooo\    \      \n      /ooo/\ooo\    \          /oooooo|   |             /ooo/\ooo\    \          /ooo/    /               /ooo/\ooo\    \     \n     /ooo/__\ooo\    \        /ooo/|oo|   |            /ooo/__\ooo\    \        /ooo/____/               /ooo/__\ooo\    \    \n     \ooo\   \ooo\    \      /ooo/ |oo|   |           /oooo\   \ooo\    \      /oooo\    \              /oooo\   \ooo\    \   \n   ___\ooo\   \ooo\    \    /ooo/  |oo|   | _____    /oooooo\   \ooo\    \    /oooooo\____\________    /oooooo\   \ooo\    \  \n  /\   \ooo\   \ooo\    \  /ooo/   |oo|   |/\    \  /ooo/\ooo\   \ooo\    \  /ooo/\ooooooooooo\    \  /ooo/\ooo\   \ooo\    \ \n /oo\   \ooo\   \ooo\____\/oo /    |oo|   /oo\____\/ooo/  \ooo\   \ooo\____\/ooo/  |ooooooooooo\____\/ooo/__\ooo\   \ooo\____\ \n \ooo\   \ooo\   \oo/    /\oo/    /|oo|  /ooo/    /\oo/    \ooo\  /ooo/    /\oo/   |oo|~~~|~~~~~     \ooo\   \ooo\   \oo/    /        \n  \ooo\   \ooo\   \/____/  \/____/ |oo| /ooo/    /  \/____/ \ooo\/ooo/    /  \/____|oo|   |           \ooo\   \ooo\   \/____/ \n   \ooo\   \ooo\    \              |oo|/ooo/    /            \oooooo/    /         |oo|   |            \ooo\   \ooo\    \     \n    \ooo\   \ooo\____\             |oooooo/    /              \oooo/    /          |oo|   |             \ooo\   \ooo\____\    \n     \ooo\  /ooo/    /             |ooooo/    /               /ooo/    /           |oo|   |              \ooo\   \oo/    /    \n      \ooo\/ooo/    /              |oooo/    /               /ooo/    /            |oo|   |               \ooo\   \/____/     \n       \oooooo/    /               /ooo/    /               /ooo/    /             |oo|   |                \ooo\    \         \n        \oooo/    /               /ooo/    /               /ooo/    /              \oo|   |                 \ooo\____\        \n         \oo/    /                \oo/    /                \oo/    /                \o|   |                  \oo/    /        \n          \/____/                  \/____/                  \/____/                  \|___|                   \/____/         \n ")
    print(" "*50,"Made by: Cyberfox Version 1.1")
    playsound("./sounds/blOOOP.mp3")
    print("\033[0m",end="\n")
    system('cls' if name == 'nt' else 'clear')
    await asyncio.gather(GetInput(),RunGame())
asyncio.run(Main())
#must install keyboard module pip install keyboard
#must install playsound module pip install playsound=1.2.2
#Python 3.10 or above required
#Check packages
import pip
import time
from math import floor
import asyncio #több loop egyszerre tudjon futni
from os import system, path, name #Konzol tisztításához
from platform import system as p_system
from random import randint
def install(modul):
    pip.main(['install',modul])
def Initialize(): #modulok ellenorzese
    global keyboard;global playsound
    t = "module was not found. Installing..."
    try:
        import keyboard
    except ImportError:
        system('cls' if name == 'nt' else 'clear')
        print("\u001b[31mkeyboard",t,"\u001b[30m")
        time.sleep(0.6)
        install('keyboard')
        import keyboard
    try:
        from playsound import playsound
    except ImportError:
        print("\u001b[31mplaysound",t,"\u001b[30m")
        time.sleep(0.6)
        install('playsound==1.2.2')
        from playsound import playsound
class Vector2: #2 számot tartalmaz (x és y-t)
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
#CREATING MAP
heuristic = False
slash = "/"
if p_system() == "Windows": slash = "\\"
if path.exists(f"{path.dirname(path.abspath(__file__))}{slash}config.snake"): #ellenorzi van-e ilyen fájl
    #adatokat beolvassa
    f = open(f"{path.dirname(path.abspath(__file__))}{slash}config.snake","r") 
    l = f.readlines()
    refresh_rate = float(l[0].rstrip().split(" ")[1])
    area = l[1].rstrip().split(" ")[1].split(":")
    heuristic = bool(int(l[2].rstrip().split(" ")[1]))
    sound = bool(int(l[3].rstrip().split(" ")[1]))
    f.close()
else:
    #ha nincs ilyen fájl bekéri a szükséges adatokat
    system('cls' if name == 'nt' else 'clear')
    print("\u001b[31mConfig file nem található, \033[33múj készítése...\n   ______                __  _                ______            _____          _____ __   \n   / ____/_______  ____ _/ /_(_)___  ____ _   / ____/___  ____  / __(_)___ _   / __(_) /__ \n  / /   / ___/ _ \/ __ `/ __/ / __ \/ __ `/  / /   / __ \/ __ \/ /_/ / __ `/  / /_/ / / _ \ \n / /___/ /  /  __/ /_/ / /_/ / / / / /_/ /  / /___/ /_/ / / / / __/ / /_/ /  / __/ / /  __/\n \____/_/   \___/\__,_/\__/_/_/ /_/\__, /   \____/\____/_/ /_/_/ /_/\__, /  /_/ /_/_/\___/ \n                                  /____/                           /____/                  \n\033[00m")
    area = (input("Kérem adja meg a pálya \033[33mméretét\033[00m szóközökkel elválasztva: \033[33m").split(" ")) #kézileg pálya megadása
    sound = 1 if input("\033[00mLegyen \033[33mhang\033[00m? [Y/n]\033[33m") == "Y" else 0
    refresh_rate = float(input("Frissítési ciklus\033[00m sűrűsége: "))
    w = open(f"{path.dirname(path.abspath(__file__))}{slash}config.snake","w")
    w.write(f"refresh_rate {refresh_rate}\nsize {area[0]}:{area[1]}\nheuristic 1\nplaysound {int(sound)}")
    w.close()
screen = Viewport(Vector2(int(area[0]),int(area[1])))#Kijelző készítése
top = f" {screen.top*screen.resolution.x}\n" #plafon
middle = (f"|{' '*screen.resolution.x}|\nz"*screen.resolution.y).split("z") #sides + playable area
bottom = f"{screen.wall}{screen.bottom*screen.resolution.x}{screen.wall}" #alja a pályának
#CREATING PLAYER(the Snake)
head = Body(">")
player = Player(Vector2(int(floor(screen.resolution.x/2)),int(floor(screen.resolution.y/2))),4,head)
middle_out = ""
apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
last_frame_rotation = 3 #to check if should play audio
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
        if sound: playsound(f"{path.dirname(path.abspath(__file__))}{slash}sounds{slash}ouch.wav", 0)
        print("\u001b[31m  .-_'''-.      ____    ,---.    ,---.    .-''-.              ,-----.    ,---.  ,---.   .-''-.  .-------.     \n '_( )_   \   .'  __ `. |    \  /    |  .'_ _   \           .'  .-,  '.  |   /  |   | .'_ _   \ |  _ _   \    \n|(_ o _)|  ' /   '  \  \|  ,  \/  ,  | / ( ` )   '         / ,-.|  \ _ \ |  |   |  .'/ ( ` )   '| ( ' )  |    \n. (_,_)/___| |___|  /  ||  |\_   /|  |. (_ o _)  |        ;  \  '_ /  | :|  | _ |  |. (_ o _)  ||(_ o _) /    \n|  |  .-----.   _.-`   ||  _( )_/ |  ||  (_,_)___|        |  _`,/ \ _/  ||  _( )_  ||  (_,_)___|| (_,_).' __  \n'  \  '-   .'.'   _    || (_ o _) |  |'  \   .---.        : (  '\_/ \   ;\ (_ o._) /'  \   .---.|  |\ \  |  | \n \  `-'`   | |  _( )_  ||  (_,_)  |  | \  `-'    /         \ `\"/  \  ) /  \ (_,_) /  \  `-'    /|  | \ `'   / \n  \        / \ (_ o _) /|  |      |  |  \       /           '. \_/``\".'    \     /    \       / |  |  \    /  \n   `'-...-'   '.(_,_).' '--'      '--'   `'-..-'              '-----'       `---`      `'-..-'  ''-'   `'-'   \n \033[0m")
        time.sleep(2)
        quit()
async def PlaySound():
    if sound: playsound(f"{path.dirname(path.abspath(__file__))}{slash}sounds{slash}click.wav", False)
async def GetInput(): # w - 1, s - 2, a - 3, d - 4, p - quit(), p - pause
    global player;global pause;global inp
    while True:
        await asyncio.sleep(0.01)
        if keyboard.is_pressed("w") and player.rotation != 2 and player.rotation != 1 and inp != 1:inp = 1
        elif keyboard.is_pressed("s")and player.rotation != 1 and player.rotation != 2 and inp != 2:inp = 2
        elif keyboard.is_pressed("a")and player.rotation != 4 and player.rotation != 3 and inp != 3:inp = 3
        elif keyboard.is_pressed("d")and player.rotation != 3 and player.rotation != 4 and inp != 4:inp = 4
        elif keyboard.is_pressed("q"):quit() #Kilépés
        elif keyboard.is_pressed("p"):pause = not pause #Megállítás átmenetileg
async def RunGame():
    first_frame = True
    global apple; global last_frame_rotation
    while True:
        await asyncio.sleep(refresh_rate)#refresh_rate másodpercenként frissül a játék
        player.rotation = inp
        if not pause:
            if player.position.x == screen.resolution.x + 1 or player.position.x == 1 or player.position.y == screen.resolution.y or player.position.y == 0: GameOver()
            for position in last_positions:
                if player.position.x == position.x and player.position.y == position.y and last_positions.index(position) != len(last_positions)-1: GameOver()
            if player.position.x == apple.position.x and player.position.y == apple.position.y:
                player.points += 1
                if sound: playsound(f"{path.dirname(path.abspath(__file__))}{slash}sounds{slash}Score.wav",0)
                apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
                for i in last_positions:
                    if apple.position.x == i.x and apple.position.y == i.y: apple = Body("O",Vector2(randint(2,screen.resolution.x),randint(1,screen.resolution.y-2)))
            if player.rotation == 1: player.position.y -= 1;player.head.character = "△"
            elif player.rotation == 2: player.position.y += 1;player.head.character = "▽"
            elif player.rotation == 3: player.position.x -= 1;player.head.character = "<"
            elif player.rotation == 4: player.position.x += 1;player.head.character = ">"
            if last_frame_rotation != player.rotation: await PlaySound()
            last_frame_rotation = int(player.rotation)
            Viewport.replaceCharacter(apple.position.x,apple.position.y,apple.character)
            if not first_frame or player.position.x != int(floor(screen.resolution.x/2)) or player.position.y != int(floor(screen.resolution.y/2)): last_positions.append(Vector2(player.position.x,player.position.y))
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
    Initialize()
    system('cls' if name == 'nt' else 'clear')
    print(f"\033[92m           _____                    _____                    _____                    _____                    _____          \n          /\    \                  /\    \                  /\    \                  /\    \                  /\    \         \n         /::\    \                /::\____\                /::\    \                /::\____\                /::\    \        \n        /::::\    \              /::::|   |               /::::\    \              /:::/    /               /::::\    \       \n       /::::::\    \            /:::::|   |              /::::::\    \            /:::/    /               /::::::\    \      \n      /:::/\:::\    \          /::::::|   |             /:::/\:::\    \          /:::/    /               /:::/\:::\    \     \n     /:::/__\:::\    \        /:::/|::|   |            /:::/__\:::\    \        /:::/____/               /:::/__\:::\    \    \n     \:::\   \:::\    \      /:::/ |::|   |           /::::\   \:::\    \      /::::\    \              /::::\   \:::\    \   \n   ___\:::\   \:::\    \    /:::/  |::|   | _____    /::::::\   \:::\    \    /::::::\____\________    /::::::\   \:::\    \  \n  /\   \:::\   \:::\    \  /:::/   |::|   |/\    \  /:::/\:::\   \:::\    \  /:::/\:::::::::::\    \  /:::/\:::\   \:::\    \ \n /::\   \:::\   \:::\____\/:: /    |::|   /::\____\/:::/  \:::\   \:::\____\/:::/  |:::::::::::\____\/:::/__\:::\   \:::\____\ \n \:::\   \:::\   \::/    /\::/    /|::|  /:::/    /\::/    \:::\  /:::/    /\::/   |::|~~~|~~~~~     \:::\   \:::\   \::/    /\n  \:::\   \:::\   \/____/  \/____/ |::| /:::/    /  \/____/ \:::\/:::/    /  \/____|::|   |           \:::\   \:::\   \/____/ \n   \:::\   \:::\    \              |::|/:::/    /            \::::::/    /         |::|   |            \:::\   \:::\    \     \n    \:::\   \:::\____\             |::::::/    /              \::::/    /          |::|   |             \:::\   \:::\____\    \n     \:::\  /:::/    /             |:::::/    /               /:::/    /           |::|   |              \:::\   \::/        \n      \:::\/:::/    /              |::::/    /               /:::/    /            |::|   |               \:::\   \/____/     \n       \::::::/    /               /:::/    /               /:::/    /             |::|   |                \:::\    \         \n        \::::/    /               /:::/    /               /:::/    /              \::|   |                 \:::\____\        \n         \::/    /                \::/    /                \::/    /                \:|   |                  \::/    /        \n          \/____/                  \/____/                  \/____/                  \|___|                   \/____/         \n                                                                                                                              \033[0m")
    s = " "*126
    for i in range(63):
        s = s[:64-i] + "_"*i*2 + s[64 + i+1::]
        print("\033[F\033[92m",s)
        time.sleep(0.006)
    print("\033[F"*23 + "           _____                    _____                    _____                    _____                    _____          \n          /\    \                  /\    \                  /\    \                  /\    \                  /\    \         \n         /oo\    \                /oo\____\                /oo\    \                /oo\____\                /oo\    \        \n        /oooo\    \              /oooo|   |               /oooo\    \              /ooo/    /               /oooo\    \       \n       /oooooo\    \            /ooooo|   |              /oooooo\    \            /ooo/    /               /oooooo\    \      \n      /ooo/\ooo\    \          /oooooo|   |             /ooo/\ooo\    \          /ooo/    /               /ooo/\ooo\    \     \n     /ooo/__\ooo\    \        /ooo/|oo|   |            /ooo/__\ooo\    \        /ooo/____/               /ooo/__\ooo\    \    \n     \ooo\   \ooo\    \      /ooo/ |oo|   |           /oooo\   \ooo\    \      /oooo\    \              /oooo\   \ooo\    \   \n   ___\ooo\   \ooo\    \    /ooo/  |oo|   | _____    /oooooo\   \ooo\    \    /oooooo\____\________    /oooooo\   \ooo\    \  \n  /\   \ooo\   \ooo\    \  /ooo/   |oo|   |/\    \  /ooo/\ooo\   \ooo\    \  /ooo/\ooooooooooo\    \  /ooo/\ooo\   \ooo\    \ \n /oo\   \ooo\   \ooo\____\/oo /    |oo|   /oo\____\/ooo/  \ooo\   \ooo\____\/ooo/  |ooooooooooo\____\/ooo/__\ooo\   \ooo\____\ \n \ooo\   \ooo\   \oo/    /\oo/    /|oo|  /ooo/    /\oo/    \ooo\  /ooo/    /\oo/   |oo|~~~|~~~~~     \ooo\   \ooo\   \oo/    /        \n  \ooo\   \ooo\   \/____/  \/____/ |oo| /ooo/    /  \/____/ \ooo\/ooo/    /  \/____|oo|   |           \ooo\   \ooo\   \/____/ \n   \ooo\   \ooo\    \              |oo|/ooo/    /            \oooooo/    /         |oo|   |            \ooo\   \ooo\    \     \n    \ooo\   \ooo\____\             |oooooo/    /              \oooo/    /          |oo|   |             \ooo\   \ooo\____\    \n     \ooo\  /ooo/    /             |ooooo/    /               /ooo/    /           |oo|   |              \ooo\   \oo/    /    \n      \ooo\/ooo/    /              |oooo/    /               /ooo/    /            |oo|   |               \ooo\   \/____/     \n       \oooooo/    /               /ooo/    /               /ooo/    /             |oo|   |                \ooo\    \         \n        \oooo/    /               /ooo/    /               /ooo/    /              \oo|   |                 \ooo\____\        \n         \oo/    /                \oo/    /                \oo/    /                \o|   |                  \oo/    /        \n          \/____/                  \/____/                  \/____/                  \|___|                   \/____/         \n ")
    print(" "*50,"Made by: Cyberfox Version 1.2")
    if sound: playsound(f"{path.dirname(path.abspath(__file__))}{slash}sounds{slash}blOOOP.mp3")
    print("\033[0m",end="\n")
    system('cls' if name == 'nt' else 'clear')
    await asyncio.gather(GetInput(),RunGame())
if __name__ == '__main__': asyncio.run(Main())
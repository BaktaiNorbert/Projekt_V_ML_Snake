import os

class Config_editor:
    TYPE_OF_SETTINGS={'refresh_rate':'float','size':'string:string','heuristic':'bool','playsound':'bool','animations':'bool','load':'path','padding':'None'}
    def __init__(self) -> None:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake')):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\u001b[31mConfig file nem található, \033[33múj készítése...\n   ______                __  _                ______            _____          _____ __   \n   / ____/_______  ____ _/ /_(_)___  ____ _   / ____/___  ____  / __(_)___ _   / __(_) /__ \n  / /   / ___/ _ \/ __ `/ __/ / __ \/ __ `/  / /   / __ \/ __ \/ /_/ / __ `/  / /_/ / / _ \ \n / /___/ /  /  __/ /_/ / /_/ / / / / /_/ /  / /___/ /_/ / / / / __/ / /_/ /  / __/ / /  __/\n \____/_/   \___/\__,_/\__/_/_/ /_/\__, /   \____/\____/_/ /_/_/ /_/\__, /  /_/ /_/_/\___/ \n                                  /____/                           /____/                  \n\033[00m")
            input()
            if input("Auto config? [Y/n]") == "Y":
                area = [str(10),str(10)]
                sound = 1
                animations = 1
                refresh_rate = 0.1
            else:
                area = (input("Kérem adja meg a pálya \033[33mméretét\033[00m szóközökkel elválasztva: \033[33m").split(" ")) #kézileg pálya megadása
                sound = 1 if input("\033[00mLegyen \033[33mhang\033[00m? [Y/n]\033[33m") == "Y" else 0
                animations = 1 if input("\033[00mLegyenek \033[33manimációk\033[00m? [Y/n]\033[33m") == "Y" else 0
                refresh_rate = float(input("Frissítési ciklus\033[00m sűrűsége: "))
            os.system('cls' if os.name == 'nt' else 'clear')
            open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake'),'w').write(f"refresh_rate {refresh_rate}\nsize {area[0]}:{area[1]}\nheuristic 1\nplaysound {int(sound)}\nanimations {animations}\nload .")
        self.file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake'))
        self.lines = [x.rstrip() for x in self.file.readlines()]
    def get_setting(self,setting):
        for line in self.lines:
            if line.find(setting) != -1:
                return line
    def get_settings(self,sep=""):
        l = []
        for line in self.lines:
            l.append(line+sep)
        return l
    def change_setting(self,s,value):
        for line in self.lines:
            if line.find(s) != -1:
                out = line.split(' ')
                out[1] = value
                self.lines[self.lines.index(line)] = f"{out[0]} {out[1]}"
    def save(self):
        w = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.snake'),'w')
        w.writelines([l+"\n" for l in self.lines])
#c = Config_editor()
#print(c.get_names())
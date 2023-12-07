import json
import socket
from tkinter import NW, Tk, Canvas, PhotoImage
from collision.collision import Rect, Circle
import math
from dataclasses import dataclass


@dataclass
class Data:
    position: tuple[int, int]
    foto: str
    aanvallen: list


class Afbeeldingen:
    def __init__(self):
        self.stilstaan_img = PhotoImage(file="images/manstil.png")
        self.looprechts = [PhotoImage(file="images/looprechts1.png"), PhotoImage(file="images/looprechts2.png")]
        self.looplinks = [PhotoImage(file="images/looplinks1.png"), PhotoImage(file="images/looplinks2.png")]
        self.img = PhotoImage(file="images/achtergrond.png")
        self.block = PhotoImage(file="images/doos.png")
        self.block2 = PhotoImage(file="images/doos2.png")


class Socketconnector:
    def __init__(self, man):
        self.s = socket.socket()
        port = 12346
        self.s.connect(('127.0.0.1', port))
        self.man = man

    def kijk(self):
        self.s.send(json.dumps(Data((self.man.x, self.man.geheel_y), self.man.image_string, self.man.aanvallen_en_botsingen.aanvallen_pos).__dict__).encode())
        data = self.s.recv(1024).decode()
        data_type_data = [Data(**data_persoon) for data_persoon in json.loads(data)]
        self.man.andere_spelers.andere_spelers = data_type_data
        self.man.aanvallen_en_botsingen.andere_spelers = data_type_data


class AanvallenEnBotsController:
    def __init__(self, canvas, doosjes1, doosjes2, waters):
        self.andere_spelers = []
        self.aanvallen = []
        self.aanvallen_pos = []
        self.lading = 3
        self.lading_sec = 0
        self.doosjes1 = doosjes1
        self.doosjes2 = doosjes2
        self.waters = waters
        self.canvas = canvas
        self.x = 240
        self.y = 115
        self.geheel_y = 115
        self.lading_balk_rood = self.canvas.create_rectangle(self.x, self.y - 15, self.x + 30, self.y - 10, fill="red")

    def botsen(self, x, y, recten, waters_pos):
        man = (self.x + 5, self.y + 15, self.x + 19, self.y + 30)
        for rect in recten:
            if Rect.rect_and_rect(man[0], man[1], man[2], man[3], rect[0], rect[1], rect[2], rect[3]):
                self.x -= x
                self.y -= y
                return True
        for water in waters_pos:
            if Rect.rect_and_rect(man[0], man[1], man[2], man[3], water[0], water[1], water[2], water[3]):
                self.x -= x
                self.y -= y
                return True

    def coords(self):
        recten = []
        waters_pos = [self.canvas.coords(water) for water in  self.waters]
        for vierkant in  self.doosjes1:
            coords = self.canvas.coords(vierkant)
            plek = [coords[0], coords[1], coords[0]+20, coords[1]+15]
            recten.append(plek)
        return recten, waters_pos

    def ladingen_bijvullen(self):
        self.lading_sec += 1
        if self.lading_sec >= 100:
            self.lading_sec = 0
            if self.lading < 3:
                self.lading += 1
                self.canvas.coords(self.lading_balk_rood, self.x, self.y - 15, self.x + 10 * self.lading, self.y - 10)
        if self.lading == 3:
            self.lading_sec = 0

    def set_x_en_y(self, x, y, geheel_y):
        self.x = x
        self.y = y
        self.geheel_y = geheel_y

    def aanval(self, event):
        if self.lading:
            self.aanvallen_pos.append((self.x, self.geheel_y))
            self.aanvallen.append(Aanvallen(event.x-self.x, event.y-self.y, (self.x, self.y), self.canvas))
            self.lading -= 1
            self.canvas.coords(self.lading_balk_rood, self.x, self.y - 15, self.x + 10 * self.lading, self.y - 10)

    def aanval_naar_aanvaller(self, event):
        if self.lading:
            persoon_max = None
            max_afstand = 0
            for persoon in self.andere_spelers:
                afstand = math.sqrt(((self.x-persoon.position[0])**2)+((self.y-(persoon.position[1]-self.geheel_y+self.y))**2))
                if (afstand if afstand >= 0 else -afstand) >= max_afstand:
                    max_afstand = afstand
                    persoon_max = persoon
            if persoon_max:
                self.aanvallen_pos.append((self.x, self.geheel_y))
                self.aanvallen.append(Aanvallen(persoon_max.position[0]+15 - self.x, (persoon_max.position[1]-self.geheel_y+self.y)+10 - self.y, (self.x, self.y), self.canvas))
                self.lading -= 1
                self.canvas.coords(self.lading_balk_rood, self.x, self.y - 15, self.x + 10 * self.lading, self.y - 10)


class AndereSpelers:
    def __init__(self, canvas, images):
        self.andere_spelers = []
        self.andere_spelers_images = []
        self.andere_spelers_aanvallen = []
        self.canvas = canvas
        self.images = images

    def move_andere_personen(self, y, geheel_y):
        aanvallen = []
        for persoon in range(max(len(self.andere_spelers_images), len(self.andere_spelers))):
            if (len(self.andere_spelers_images)-1)<persoon:
                self.andere_spelers_images.append(self.canvas.create_image(self.andere_spelers[persoon].position[0],
                                                                           (self.andere_spelers[persoon].position[1]-geheel_y)+y,
                                                                           anchor=NW, image=self.images.stilstaan_img))
            else:
                if persoon <= len(self.andere_spelers_images)-1 and persoon <= len(self.andere_spelers)-1:
                    exec(f"self.canvas.itemconfig(self.andere_spelers_images[persoon], image={self.andere_spelers[persoon].foto})")
                    self.canvas.moveto(self.andere_spelers_images[persoon], self.andere_spelers[persoon].position[0],
                                                                            (self.andere_spelers[persoon].position[1]-geheel_y)+y)

            if len(self.andere_spelers) > persoon:
                for aanval in self.andere_spelers[persoon].aanvallen:
                    aanvallen.append(aanval)

        for aanval in range(max(len(self.andere_spelers_aanvallen), len(aanvallen))):
            if (len(self.andere_spelers_aanvallen) - 1) < aanval < len(aanvallen):
                self.andere_spelers_aanvallen.append(self.canvas.create_oval(aanvallen[aanval][0],
                                                                           (aanvallen[aanval][1]-geheel_y)+y,
                                                                           aanvallen[aanval][0]+10,
                                                                           (aanvallen[aanval][1] - geheel_y) + y+10, fill="red"))
            else:
                if aanval < len(self.andere_spelers_aanvallen) and aanval < len(aanvallen):
                    self.canvas.moveto(self.andere_spelers_aanvallen[aanval], aanvallen[aanval][0], (aanvallen[aanval][1]-geheel_y)+y)
                elif len(self.andere_spelers_aanvallen) > aanval >= len(aanvallen):
                    self.canvas.delete(self.andere_spelers_aanvallen[aanval])
                    del self.andere_spelers_aanvallen[aanval]


class Man:
    def __init__(self, canvas):
        self.s = None
        self.image_string = "self.images.stilstaan_img"
        self.richting = None
        self.img_in_lijst = 0
        self.images = Afbeeldingen()
        self.andere_spelers = AndereSpelers(canvas, self.images)
        self.doosjes1 = []
        self.doosjes2 = []
        self.waters = []
        self.canvas = canvas
        self.x = 240
        self.y = 115
        self.verander_x = 0
        self.verander_y = 0
        self.geheel_y = 115
        self.imy = -125
        self.achtergrond_img = self.canvas.create_image(0, 0, anchor=NW, image=self.images.img)
        self.lees_in()
        self.aanvallen_en_botsingen = AanvallenEnBotsController(canvas, self.doosjes1, self.doosjes2, self.waters)
        self.man_img = self.canvas.create_image(self.x, self.y - 15, anchor=NW, image=self.images.stilstaan_img)

    def socket(self, s):
        self.s = s
        self.s.kijk()
        self.andere_spelers.move_andere_personen(self.y, self.geheel_y)
        self.lees_in2()
        self.canvas.bind_all('<KeyPress-Left>', lambda ev: self.verander_verander_x(-3))
        self.canvas.bind_all('<KeyRelease-Left>', lambda ev: self.verander_verander_x(0))
        self.canvas.bind_all('<KeyPress-Right>', lambda ev: self.verander_verander_x(3))
        self.canvas.bind_all('<KeyRelease-Right>', lambda ev: self.verander_verander_x(0))
        self.canvas.bind_all('<KeyPress-Up>', lambda ev: self.verander_verander_y(-3))
        self.canvas.bind_all('<KeyRelease-Up>', lambda ev: self.verander_verander_y(0))
        self.canvas.bind_all('<KeyPress-Down>', lambda ev: self.verander_verander_y(3))
        self.canvas.bind_all('<KeyRelease-Down>', lambda ev: self.verander_verander_y(0))
        self.canvas.bind_all('<Key-s>', self.aanvallen_en_botsingen.aanval_naar_aanvaller)
        self.canvas.bind_all('<Button-1>', self.aanvallen_en_botsingen.aanval)

    def move(self):
        recten, waters_pos = self.coords()
        self.aanvallen_en_botsingen.ladingen_bijvullen()
        if self.verander_x and self.verander_y:
            self.x += self.verander_x
            self.y += self.verander_y
            self.aanvallen_en_botsingen.set_x_en_y(self.x, self.y, self.geheel_y)
            if self.aanvallen_en_botsingen.botsen(self.verander_x, self.verander_y, recten, waters_pos):
                self.x = self.aanvallen_en_botsingen.x
                self.y = self.aanvallen_en_botsingen.y
                return
            self.y -= self.verander_y
            self.bots_achtergrond(self.verander_y)
            if not (485 > self.x > 0):
                self.x -= self.verander_x
            if self.verander_x > 0:
                self.animate(self.images.looprechts)
            else:
                self.animate(self.images.looplinks)
        elif self.verander_x and (not self.verander_y):
            self.x += self.verander_x
            self.aanvallen_en_botsingen.set_x_en_y(self.x, self.y, self.geheel_y)
            if self.aanvallen_en_botsingen.botsen(self.verander_x, self.verander_y, recten, waters_pos):
                self.x = self.aanvallen_en_botsingen.x
                self.y = self.aanvallen_en_botsingen.y
                return
            if not (485 > self.x > 0):
                self.x -= self.verander_x
            if self.verander_x > 0:
                self.animate(self.images.looprechts)
            else:
                self.animate(self.images.looplinks)
        elif self.verander_y and (not self.verander_x):
            self.y += self.verander_y
            self.aanvallen_en_botsingen.set_x_en_y(self.x, self.y, self.geheel_y)
            if self.aanvallen_en_botsingen.botsen(self.verander_x, self.verander_y, recten, waters_pos):
                self.x = self.aanvallen_en_botsingen.x
                self.y = self.aanvallen_en_botsingen.y
                return
            self.y -= self.verander_y
            self.bots_achtergrond(self.verander_y)
        self.aanvallen_en_botsingen.set_x_en_y(self.x, self.y, self.geheel_y)
        self.canvas.moveto(self.man_img, self.x, self.y)
        self.canvas.moveto(self.aanvallen_en_botsingen.lading_balk_rood, self.x, self.y - 15)

    def coords(self):
        recten = []
        waters_pos = [self.canvas.coords(water) for water in  self.waters]
        for vierkant in  self.doosjes1:
            coords = self.canvas.coords(vierkant)
            plek = [coords[0], coords[1], coords[0]+20, coords[1]+15]
            recten.append(plek)
        return recten, waters_pos

    def bots_achtergrond(self, y):
        if (50 > self.y > 0 > y and -125 > self.imy) or (235 > self.y > 185 and self.imy > -250 and y > 0):
            self.imy -= y
            self.canvas.move(self.achtergrond_img, 0, -y)
            self.geheel_y += y
            for rect in self.doosjes1:
                self.canvas.move(rect, 0, -y)
            for rect in self.doosjes2:
                self.canvas.move(rect, 0, -y)
            for water in self.waters:
                self.canvas.move(water, 0, -y)
            for aanval in self.aanvallen_en_botsingen.aanvallen:
                self.canvas.move(aanval.aanval, 0, -y)
        else:
            self.y += self.verander_y
            self.geheel_y += self.verander_y
            if self.y < 0 and self.verander_y < 0:
                self.y -= self.verander_y
                self.geheel_y -= self.verander_y
            elif self.y > 235 and self.verander_y > 0:
                self.y -= self.verander_y
                self.geheel_y -= self.verander_y

    def animate(self, r):
        self.img_in_lijst += 1
        if r != self.richting:
            self.richting = r
            self.img_in_lijst = 0
        if self.richting:
            if self.img_in_lijst >= len(self.richting):
                self.img_in_lijst = 0
        if r == self.images.looplinks:
            self.image_string = f"self.images.looplinks[{self.img_in_lijst}]"
        elif r == self.images.looprechts:
            self.image_string = f"self.images.looprechts[{self.img_in_lijst}]"
        self.canvas.itemconfig(self.man_img, image=self.richting[self.img_in_lijst])

    def lees_in(self):
        lijst = open("kaarten/kaart1.txt").read().split("\n")
        for x in range(25):
            for y in range(25):
                if lijst[y][x] == "B":
                    vierkant = self.canvas.create_image(x * 20, (y + 1) * 15, anchor=NW, image=self.images.block)
                    self.doosjes1.append(vierkant)
                elif lijst[y][x] == "W":
                    water = self.canvas.create_rectangle(x*20, y*15, (x+1)*20, (y+1)*15, fill="blue")
                    self.waters.append(water)

    def lees_in2(self):
        lijst = open("kaarten/kaart1.txt").read().split("\n")
        for x in range(25):
            for y in range(25):
                if lijst[y][x] == "B":
                    vierkant = self.canvas.create_image(x * 20, y * 15, anchor=NW, image=self.images.block2)
                    self.doosjes2.append(vierkant)

    def verander_verander_x(self, x):
        self.verander_x = x

    def verander_verander_y(self, y):
        self.verander_y = y


class Aanvallen:
    def __init__(self, afstand_x, afstand_y, begin, canvas):
        self.canvas = canvas
        afstand = math.sqrt((afstand_x ** 2)+(afstand_y ** 2))
        self.richting_x = afstand_x / afstand
        self.richting_y = afstand_y / afstand
        self.keer = 0
        self.begin = begin
        self.aanval = canvas.create_oval(begin[0], begin[1], begin[0]+10, begin[1]+10, fill="blue")

    def move(self, recten):
        self.keer += 1
        recten2 = []
        for vierkant in recten:
            coords = self.canvas.coords(vierkant)
            plek = [coords[0], coords[1], coords[0] + 20, coords[1] + 15]
            recten2.append(plek)
        if int(math.sqrt(((self.richting_x * self.keer) ** 2)+((self.richting_y*self.keer) ** 2))) >= 100:
            self.canvas.delete(self.aanval)
            return False
        if self.botsen(recten2):
            self.canvas.delete(self.aanval)
            return False
        self.canvas.move(self.aanval, self.richting_x, self.richting_y)
        return self.begin[0] + self.richting_x * self.keer, self.begin[1] + self.richting_y * self.keer

    def botsen(self, recten):
        for rect in recten:
            if Circle.circle_and_rect((self.richting_x * self.keer)+self.begin[0]+5, (self.richting_y * self.keer)+self.begin[1]+5,
                                      5, rect[0], rect[1], rect[2], rect[3]):
                return True


tk = Tk()
canvas = Canvas(tk, width=500, height=250)
canvas.pack()
bal = Man(canvas)
s = Socketconnector(bal)
bal.socket(s)


def redraw():
    s.kijk()
    bal.andere_spelers.move_andere_personen(bal.y, bal.geheel_y)
    bal.move()
    for x, aanval in enumerate(bal.aanvallen_en_botsingen.aanvallen):
        data = aanval.move(bal.doosjes1)
        if not data:
            bal.aanvallen_en_botsingen.aanvallen.remove(aanval)
            del bal.aanvallen_en_botsingen.aanvallen_pos[x]
        else:
            bal.aanvallen_en_botsingen.aanvallen_pos[x] = (data[0], data[1]+(bal.geheel_y-bal.y))

    tk.after(20, redraw)

tk.after(20, redraw)

tk.mainloop()


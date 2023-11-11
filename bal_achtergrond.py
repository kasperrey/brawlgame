import json
import socket
from time import sleep
from tkinter import NW, Tk, Canvas, PhotoImage
from collision.collision import Rect


class Data:
    def __init__(self, position):
        self.position = position


class Afbeeldingen:
    def __init__(self):
        self.stilstaan_img = PhotoImage(file="manstil.png")
        self.looprechts = [PhotoImage(file="looprechts1.png"), PhotoImage(file="looprechts2.png")]
        self.looplinks = [PhotoImage(file="looplinks1.png"), PhotoImage(file="looplinks2.png")]
        self.img = PhotoImage(file="achtergrond.png")
        self.block = PhotoImage(file="doos.png")
        self.block2 = PhotoImage(file="doos2.png")



class Socketconnector:
    def __init__(self, man):
        self.s = socket.socket()
        port = 12346
        self.s.connect(('127.0.0.1', port))
        self.man = man

    def kijk(self):
        self.s.send(json.dumps({"position": (self.man.x, self.man.geheel_y-15),
                                "foto": self.man.image_string}, indent=4).encode())
        data = self.s.recv(1024).decode()
        self.man.andere_spelers = json.loads(data)

class Man:
    def __init__(self, tk, canvas):
        self.s = None
        self.image_string = "self.images.stilstaan_img"
        self.andere_spelers = []
        self.andere_spelers_images = []
        self.richting = None
        self.img_in_lijst = 0
        self.images = Afbeeldingen()
        self.doosjes1 = []
        self.doosjes2 = []
        self.waters = []
        self.tk = tk
        self.canvas = canvas
        self.x = 240
        self.y = 115
        self.geheel_y = 115
        self.imy = -125
        self.achtergrond_img = self.canvas.create_image(0, 0, anchor=NW, image=self.images.img)
        self.lees_in()
        self.man_img = self.canvas.create_image(self.x, self.y - 15, anchor=NW, image=self.images.stilstaan_img)

    def socket(self, s):
        self.s = s
        self.s.kijk()
        self.move_andere_personen()
        self.lees_in2()
        self.canvas.bind_all('<KeyPress-Left>', lambda ev: self.move(-5, 0))
        self.canvas.bind_all('<KeyPress-Right>', lambda ev: self.move(5, 0))
        self.canvas.bind_all('<KeyPress-Up>', lambda ev: self.move(0, -5))
        self.canvas.bind_all('<KeyPress-Down>', lambda ev: self.move(0, 5))

    def move(self, x, y):
        recten = []
        waters_pos = []
        for vierkant in  self.doosjes1:
            coords = self.canvas.coords(vierkant)
            plek = [coords[0], coords[1], coords[0]+20, coords[1]+15]
            recten.append(plek)
        for water in  self.waters:
            waters_pos.append(self.canvas.coords(water))
        if x:
            self.x += x
            man = (self.x + 5, self.y + 5, self.x + 19, self.y + 15)
            for rect in recten:
                if Rect.rect_and_rect(man[0], man[1], man[2], man[3], rect[0], rect[1], rect[2], rect[3]):
                    self.x -= x
                    self.canvas.moveto(self.man_img, self.x, self.y-15)
                    return
            for water in waters_pos:
                if Rect.rect_and_rect(man[0], man[1], man[2], man[3], water[0], water[1], water[2], water[3]):
                    self.x -= x
                    self.canvas.moveto(self.man_img, self.x, self.y-15)
                    return
            self.x -= x
            self.x += x
            if 480 > self.x > 0:
                self.canvas.move(self.man_img, x, y)
            else:
                self.x -= x
                self.y -= y
            if x > 0:
                self.animate(self.images.looprechts)
            else:
                self.animate(self.images.looplinks)
        if y:
            self.y += y
            man = (self.x + 5, self.y + 5, self.x + 19, self.y + 15)
            for rect in recten:
                if Rect.rect_and_rect(man[0], man[1], man[2], man[3], rect[0], rect[1], rect[2], rect[3]):
                    self.y -= y
                    self.canvas.moveto(self.man_img, self.x, self.y-15)
                    return
            for water in waters_pos:
                if Rect.rect_and_rect(man[0], man[1], man[2], man[3], water[0], water[1], water[2], water[3]):
                    self.y -= y
                    self.canvas.moveto(self.man_img, self.x, self.y-15)
                    return
            self.y -= y
            if y > 0:
                if 230 > self.y > 185 and self.imy > -250:
                    self.imy -= y
                    self.canvas.move(self.achtergrond_img, -x, -y)
                    self.geheel_y += y
                    for rect in self.doosjes1:
                        self.canvas.move(rect, -x, -y)
                    for rect in self.doosjes2:
                        self.canvas.move(rect, -x, -y)
                    for water in self.waters:
                        self.canvas.move(water, -x, -y)
                else:
                    self.y += y
                    self.geheel_y += y
                    if 230 > self.y > 0:
                        self.canvas.move(self.man_img, x, y)
                    elif self.y > 230 and y > 0:
                        self.y -= y
                        self.geheel_y -= y
            else:
                if 50 > self.y > 0 and -125 > self.imy:
                    self.imy -= y
                    self.geheel_y += y
                    self.canvas.move(self.achtergrond_img, -x, -y)
                    for rect in self.doosjes1:
                        self.canvas.move(rect, -x, -y)
                    for rect in self.doosjes2:
                        self.canvas.move(rect, -x, -y)
                    for water in self.waters:
                        self.canvas.move(water, -x, -y)
                else:
                    self.y += y
                    self.geheel_y += y
                    if 230 > self.y > 0:
                        self.canvas.move(self.man_img, x, y)
                    elif self.y < 0 and y < 0:
                        self.y -= y
                        self.geheel_y -= y

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
        lijst = open("blokjes.txt").read().split("\n")
        for x in range(25):
            for y in range(25):
                if lijst[y][x] == "B":
                    vierkant = self.canvas.create_image(x * 20, (y + 1) * 15, anchor=NW, image=self.images.block)
                    self.doosjes1.append(vierkant)
                elif lijst[y][x] == "W":
                    water = self.canvas.create_rectangle(x*20, y*15, (x+1)*20, (y+1)*15, fill="blue")
                    self.waters.append(water)

    def lees_in2(self):
        lijst = open("blokjes.txt").read().split("\n")
        for x in range(25):
            for y in range(25):
                if lijst[y][x] == "B":
                    vierkant = self.canvas.create_image(x * 20, y * 15, anchor=NW, image=self.images.block2)
                    self.doosjes2.append(vierkant)

    def move_andere_personen(self):
        for persoon in range(max(len(self.andere_spelers_images), len(self.andere_spelers))):
            if (len(self.andere_spelers_images)-1)<persoon:
                self.andere_spelers_images.append(self.canvas.create_image(self.andere_spelers[persoon]["position"][0],
                                                                           (self.andere_spelers[persoon]["position"][1]-self.geheel_y)+self.y,
                                                                           anchor=NW, image=self.images.stilstaan_img))
            else:
                vijand = None
                if len(self.andere_spelers) == len(self.andere_spelers_images):
                    if self.andere_spelers[persoon]["foto"] == "self.images.looplinks[0]":
                        vijand = self.images.looplinks[0]
                    elif self.andere_spelers[persoon]["foto"] == "self.images.looplinks[1]":
                        vijand = self.images.looplinks[1]
                    elif self.andere_spelers[persoon]["foto"] == "self.images.looprechts[0]":
                        vijand = self.images.looprechts[0]
                    elif self.andere_spelers[persoon]["foto"] == "self.images.looprechts[1]":
                        vijand = self.images.looprechts[1]
                    self.canvas.itemconfig(self.andere_spelers_images[persoon], image=vijand)
                    self.canvas.moveto(self.andere_spelers_images[persoon], self.andere_spelers[persoon]["position"][0],
                                                                            (self.andere_spelers[persoon]["position"][1]-self.geheel_y)+self.y)


tk = Tk()
canvas = Canvas(tk, width=500, height=250)
canvas.pack()
bal = Man(tk, canvas)
s = Socketconnector(bal)
bal.socket(s)
while True:
    s.kijk()
    bal.move_andere_personen()
    tk.update()
    tk.update_idletasks()

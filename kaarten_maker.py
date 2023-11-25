from tkinter import PhotoImage, Tk, Canvas


class Systeem:
    def __init__(self):
        self.typen = "."
        self.x = 0
        self.y = 0
        self.data = []
        for x in range(25):
            self.data.append(". . . . . . . . . . . . . . . . . . . . . . . . .".split(" "))
        self.file = open("kaarten/kaart2.txt", "w")
        self.tk = Tk()
        self.canvas = Canvas(self.tk, width=500, height=375)
        self.canvas.pack()
        self.block = PhotoImage(file="images/doos.png")
        self.block2 = PhotoImage(file="images/doos2.png")
        self.achtergrond = PhotoImage(file="images/achtergrond.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.achtergrond)
        self.vierkant = None
        self.tk.bind("<Button-1>", self.click)
        self.tk.bind("<Motion>", self.motion)
        self.tk.bind("<KeyRelease-b>", self.blokje)
        self.tk.bind("<KeyRelease-w>", self.water)
        self.tk.bind("<KeyRelease-s>", self.save)
        self.tk.after(20, self.redraw)
        self.tk.mainloop()

    def motion(self, event):
        self.x = event.x-(event.x % 20)
        self.y = event.y-(event.y % 15)

    def blokje(self, event):
        self.typen = "B"

    def water(self, event):
        self.typen = "W"

    def click(self, event):
        self.data[int(self.y / 15)][int(self.x / 20)] = self.typen
        if self.typen == "W":
            self.canvas.create_rectangle(self.x, self.y, self.x + 20, self.y + 15, fill="blue")
        elif self.typen == "B":
            self.canvas.create_image(self.x, self.y+15, anchor="nw", image=self.block)
            self.canvas.create_image(self.x, self.y, anchor="nw", image=self.block2)

    def redraw(self):
        if self.vierkant:
            self.canvas.delete(self.vierkant)
        self.vierkant = self.canvas.create_rectangle(self.x, self.y,
                                                     self.x+20, self.y+15, fill="gray")
        self.tk.after(20, self.redraw)

    def save(self, event):
        str_data = []
        for x in self.data:
            str_data.append("".join(x))
        self.file.write("\n".join(str_data))
        self.file.close()
        self.tk.destroy()


Systeem()

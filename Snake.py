from tkinter import *
import time
from random import randint
import mysql.connector as m

score = 0
speed = 100
canvasw = 700
canvash = 500
blocks = 25
snakst = 10
foodc = "Yellow"
snakec = "Blue"
dir = "down"

k = 0


class snake:
    def __init__(self):
        self.bods = snakst
        self.coords = []
        self.bloks = []
        for i in range(snakst):
            self.coords.append([0, 0])
        for x, y in self.coords:
            a = can.create_rectangle(x, y, x + blocks, y + blocks, fill=snakec)
            self.bloks.append(a)


class food:
    def __init__(self):
        x = randint(0, (canvasw / blocks) - 2) * blocks
        y = randint(0, (canvash / blocks) - 2) * blocks
        self.coords = [x, y]
        can.create_rectangle(x, y, x + blocks, y + blocks, fill=foodc, tag="mayiru")


def subb():
    myt = m.connect(host='localhost', user='root',port='3307', passwd='adangotha69', database='snake_game_sesh')
    myc = myt.cursor()
    a = tex.get()
    b = "insert into highscore(name,points) values('{}',{})".format(a, score)
    myc.execute(b)
    myt.commit()


def show():
    myt = m.connect(host='localhost', user='root',port='3307', passwd='adango9', database='snake_game_sesh')
    myc = myt.cursor()
    myc.execute("select * from highscore")
    g = []
    for i in myc:
        g.append(i)
    print(g)


def adleaderB():
    pass


def gameover():
    can.delete(ALL)
    can.create_text(canvasw / 2, (canvash / 2) - 20, font=("Jokerman", 30), text="Game Over", fill="Red")

    time.sleep(2)
    can.create_text(canvasw / 2, (canvash / 2) + 10, font=("Jokerman", 15), text="Your score was " + str(score),
                    fill="Red")


def refre(snake):
    global score, foo, snakst
    x, y = snake.coords[0]
    if dir == 'up':
        y -= blocks
    elif dir == "down":
        y += blocks
    elif dir == "left":
        x -= blocks
    elif dir == "right":
        x += blocks
    if x > canvasw:
        x = 0
    elif x < 0:
        x = canvasw - blocks
    elif y < 0:
        y = canvash - blocks
    elif y > canvash:
        y = 0
    snake.coords.insert(0, [x, y])
    ns = can.create_rectangle(x, y, x + blocks, y + blocks, fill=snakec)
    snake.bloks.append(ns)
    if x == foo.coords[0] and y == foo.coords[1]:
        if score >= 10:
            score += 2
        else:
            score += 1
        le.config(text="Score :" + str(score))
        can.delete("mayiru")
        snakst += 1
        foo = food()
    else:
        del snake.coords[-1]
        can.delete(snake.bloks[0])
        del snake.bloks[0]
    if checkcol() is True:
        gameover()
        print("Gameover")
    else:
        window.after(speed, refre, snake)


def checkcol():
    x, y = snake.coords[0]
    for i in snake.coords[1:]:
        if x == i[0] and y == i[1]:
            return True
    return False


def changedir(a):
    global dir
    if a == "up":
        if dir != "down":
            dir = "up"
    if a == "down":
        if dir != "up":
            dir = "down"
    if a == "right":
        if dir != "left":
            dir = "right"
    if a == "left":
        if dir != "right":
            dir = "left"


window = Tk()

le = Label(text="Score: " + str(score), font=("consolas", 25))
le.pack(side='top')
can = Canvas(bg="Black", width=canvasw, height=canvash)
can.pack()
tex = Entry(window, font=('jokerman', 20))
tex.pack(side='bottom')
sub = Button(window, text='submit', command=subb)
sub.pack()
window.update()
snake = snake()
foo = food()
window.bind("<w>", lambda event: changedir("up"))
window.bind("<s>", lambda event: changedir("down"))
window.bind("<a>", lambda event: changedir("left"))
window.bind("<d>", lambda event: changedir("right"))
refre(snake)
show()
window.mainloop()

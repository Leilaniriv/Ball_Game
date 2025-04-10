import numpy as np
from tkinter import *
import keyboard
import time

def randdim():
    x = int(np.random.randint(5, 10, 1))
    y = int(np.random.randint(25, 50, 1))
    return x, y

l1 = [0, randdim()]
l2 = [200, randdim()]
l3 = [400, randdim()]
l4 = [600, randdim()]
l5 = [800, randdim()]
c = [200, (20, 20)]
u = 0
d = 0
jump = 0
point = 0
end = 0

jump_height = 0
space_pressed_time = None

def reset():
    global l1, l2, l3, l4, l5, c, u, d, jump, point
    jump = 0
    u = 0
    d = 0
    point = 0
    l1 = [0, randdim()]
    l2 = [200, randdim()]
    l3 = [400, randdim()]
    l4 = [600, randdim()]
    l5 = [800, randdim()]
    c = [200, (20, 20)]

def rect(l, canvas):
    n = l[0]
    dim = l[1]
    y = 200
    canvas.create_rectangle(n, y, n + dim[0], y - dim[1], fill="#476042")

def circle(c, canvas):
    n = 50
    dim = c[1]
    y = c[0]
    canvas.create_oval(n, y - dim[1], n + dim[0], y, fill="yellow")

def destroy():
    w.destroy()
    display()

def endfunct(w):
    w.create_text(350, 100, text='Game Over')

def touch(c):
    global l1, l2, l3, l4, l5, end
    for l in [l1, l2, l3, l4, l5]:
        if 25 < l[0] < 75:
            for i in range(l[1][1]):
                check = np.add(np.square(60 - l[0]), np.square(c[0] - 210 + i))
                if check <= np.square(10):
                    end = 1
                    break

def logic():
    global l1, l2, l3, l4, l5, c, u, d, jump, point, space_pressed_time, jump_height

    for l in [l1, l2, l3, l4, l5]:
        if l[0] <= 0:
            n = np.random.randint(30, 100)
            l[0], l[1] = 950 + n, randdim()
        else:
            l[0] -= 1

    if keyboard.is_pressed(' '):
        if space_pressed_time is None:
            space_pressed_time = time.time()
    elif space_pressed_time is not None:
        held_time = time.time() - space_pressed_time
        space_pressed_time = None
        held_time = max(0.1, min(held_time, 1.0))
        jump_height = int(held_time * 100)
        if c[0] == 200:
            jump = 1
            u = 0
            d = 0

    if jump == 1:
        if u < jump_height:
            c[0] -= 1
            u += 1
        elif d < jump_height:
            c[0] += 1
            d += 1
        else:
            jump = 0

    if any(l[0] == 50 for l in [l1, l2, l3, l4, l5]):
        point += 1

    touch(c)

def display():
    global w, l1, l2, l3, l4, l5, c, point
    canvas_width = 700
    canvas_height = 400
    w.delete("all")
    w.create_line(0, 200, canvas_width, 200, fill="#400000")
    for l in [l1, l2, l3, l4, l5]:
        rect(l, w)
    circle(c, w)
    w.create_text(40, 40, text=f'points ==> {point}')
    logic()
    print(point)

    if end == 0:
        w.after(30, display)
    elif end == 1:
        endfunct(w)

def game():
    global w
    master = Tk()
    canvas_width = 700
    canvas_height = 400
    w = Canvas(master, width=canvas_width, height=canvas_height)
    display()
    w.after(100, display)
    w.pack()
    mainloop()

game()
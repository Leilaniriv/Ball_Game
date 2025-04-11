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
game_speed = 15
jump_height = 0
space_pressed_time = None
#variables for powerups
power_up = [1000, 180]  # x,y
shield_active = False
shield_timer = 0


def reset():
    global l1, l2, l3, l4, l5, c, u, d, jump, point, game_speed, end
    global power_up, shield_active, shield_timer
    power_up = [1000, 180]
    shield_active = False
    shield_timer = 0
    jump = 0
    u = 0 # potentially depricated variables, remove once finished maybe?
    d = 0
    point = 0
    end = 0
    game_speed = 15
    l1 = [0, randdim()]
    l2 = [200, randdim()]
    l3 = [400, randdim()]
    l4 = [600, randdim()]
    l5 = [800, randdim()]
    c = [200, (20, 20)]

def draw_power_up(canvas):
    if 0 < power_up[0] < 700:
        canvas.create_oval(power_up[0], power_up[1] - 10, power_up[0] + 20, power_up[1] + 10, fill="blue")

def activate_shield():
    global shield_active, shield_timer
    shield_active = True
    shield_timer = 300  # lasts ~5 seconds at 60fps

def deactivate_shield():
    global shield_active
    shield_active = False

def rect(l, canvas):
    n = l[0]
    dim = l[1]
    y = 200
    canvas.create_rectangle(n, y, n + dim[0], y - dim[1], fill="#476042")

def circle(c, canvas):
    global shield_active
    n = 50
    dim = c[1]
    y = c[0]
    color = "blue" if shield_active else "yellow"
    canvas.create_oval(n, y - dim[1], n + dim[0], y, fill=color)

def destroy():
    w.destroy()
    display()

def endfunct(w):
    w.create_text(350, 100, text='Game Over')
    w.create_text(350, 50, text='Press R to restart')

def on_space(event):
    global space_pressed_time
    if space_pressed_time is None:
        space_pressed_time = time.time()

def on_space_release(event):
    global jump, u, d, c, space_pressed_time, jump_height
    if space_pressed_time is not None:
        held_time = time.time() - space_pressed_time
        space_pressed_time = None
        held_time = max(0.1, min(held_time, 1.0))
        jump_height = int(held_time * 100)
        if not jump and c[0] == 200:
            jump = 1
            u = 0
            d = 0

def restart(event):
    global end
    if end == 1:
        reset()
        end = 0
        w.after(game_speed, display)

def touch(c):
    global end
    if shield_active:
        return
    for l in [l1, l2, l3, l4, l5]:
        if 25 < l[0] < 75:
            for i in range(l[1][1]):
                check = np.add(np.square(60 - l[0]), np.square(c[0] - 210 + i))
                if check <= np.square(10):
                    end = 1
                    break

def logic():
    global l1, l2, l3, l4, l5, c, u, d, jump, point, game_speed
    for l in [l1, l2, l3, l4, l5]:
        if l[0] <= 0:
            n = np.random.randint(30, 100)
            l[0], l[1] = 950 + n, randdim()
        else:
            l[0] -= 1

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
        if point % 5 == 0 and game_speed > 0:
            game_speed -= 2
    touch(c)
    power_up[0] -= 1
    if power_up[0] <= -20:
        if np.random.rand() < 0.01:  # small chance to respawn
            power_up[0] = 950
            power_up[1] = np.random.randint(140, 180)

    # Check for power-up pickup
    if 40 < power_up[0] < 70 and 180 < c[0] < 220:
        power_up[0] = -100  # move it off-screen
        activate_shield()

    # Handle shield timing
    if shield_active:
        global shield_timer
        shield_timer -= 1
        if shield_timer <= 0:
            deactivate_shield()


def display():
    global w, c, point
    canvas_width = 700
    canvas_height = 400
    w.delete("all")
    w.create_line(0, 200, canvas_width, 200, fill="#400000")
    for l in [l1, l2, l3, l4, l5]:
        rect(l, w)
    circle(c, w)
    draw_power_up(w)
    w.create_text(50, 40, text=f'points ==> {point}')
    logic()
    if end == 0:
        w.after(game_speed, display)
    elif end == 1:
        endfunct(w)
    w.create_text(600, 40, text=f'speed: {game_speed}')

def game():
    global w
    master = Tk()
    w = Canvas(master, width=700, height=400)
    master.bind('<space>', on_space)
    master.bind('<KeyRelease-space>', on_space_release)
    master.bind("r", restart)
    display()
    w.pack()
    mainloop()

game()
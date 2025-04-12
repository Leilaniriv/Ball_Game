import numpy as np
from tkinter import *
import keyboard
import time


def randdim():
    # Random width between 5 and 10
    x = int(np.random.randint(5, 10, 1))

    # Random height between 25 and 50
    y = int(np.random.randint(25, 50, 1))

    # Random vertical offset for the coin (above the obstacle)
    coin_offset = int(np.random.randint(30, 70))  # 30 to 70 pixels above

    # Return obstacle width, height, coin collected flag (False), and coin height offset
    return x, y, False, coin_offset

l1 = [0, randdim()]
l2 = [200, randdim()]
l3 = [400, randdim()]
l4 = [600, randdim()]
l5 = [800, randdim()]
c = [200, (20, 20)]
u = 0
d = 0
# Variables for gravity
jump_strength = -8
gravity = 0.5
velocity = 0
on_ground = True
game_started = False
jump = 0
point = 0
end = 0
coins_collected = 0
high_score = 0
game_speed = 12
jump_height = 0
space_pressed_time = None
paused = False
#variables for powerups
power_up = [1000, 180]  # x,y
shield_active = False
shield_timer = 0


def reset():
    global l1, l2, l3, l4, l5, c, u, d, jump, point, game_speed, end
    global coins_collected
    global power_up, shield_active, shield_timer
    global velocity, on_ground

    velocity = 0                  # reset fall speed
    coins_collected = 0          # reset coins
    on_ground = True             # reset grounded state
    power_up = [1000, 180]       # reset power-up position
    shield_active = False        # turn off shield
    shield_timer = 0             # reset shield timer
    jump = 0                     # reset jump state
    u = 0                        # unused jump var
    d = 0                        # unused jump var
    point = 0                    # reset score
    end = 0                      # reset game over flag
    game_speed = 12              # reset starting speed

    # reset obstacle positions with new dimensions
    l1 = [0, randdim()]
    l2 = [200, randdim()]
    l3 = [400, randdim()]
    l4 = [600, randdim()]
    l5 = [800, randdim()]
    # reset player position
    c = [200, (20, 20)]

# Draws power up circle on screen
def draw_power_up(canvas):
    if 0 < power_up[0] < 700:
        # draw blue circle for shield power-up
        canvas.create_oval(power_up[0], power_up[1] - 10, power_up[0] + 20, power_up[1] + 10, fill="blue")

# Self explanatory shield helper functions here
def activate_shield():
    global shield_active, shield_timer
    shield_active = True
    shield_timer = 300  # lasts ~5 seconds

def deactivate_shield():
    global shield_active
    shield_active = False

# Draws rectangle for the obstacles
def rect(l, canvas):
    n = l[0]  # obstacle x position
    dim = l[1]  # obstacle width and height
    y = 200  # baseline for obstacle height
    canvas.create_rectangle(n, y, n + dim[0], y - dim[1], fill="#476042")

# draws the player character as a circle, blue if shield is active
def circle(c, canvas):
    global shield_active
    n = 50                        # x position of player
    dim = c[1]                    # width and height
    y = c[0]                      # y position
    color = "blue" if shield_active else "yellow"  # switch color based on shield
    canvas.create_oval(n, c[0] - dim[1], n + dim[0], c[0], fill=color)

# Destroys window for restart
def destroy():
    w.destroy()
    display()

# Function for when game ends, computes high score as well
def endfunct(w):
    global high_score, point
    if point > high_score:
        high_score = point
    w.create_text(350, 100, text='Game Over')
    w.create_text(350, 50, text='Press R to restart')

# Function for when space is pressed, either starts game or computes time held for jump height
def on_space(event):
    global space_pressed_time, game_started
    if not game_started:
        game_started = True
        display()
    else:
        if space_pressed_time is None:
            space_pressed_time = time.time()

# handles logic when the spacebar is released to trigger a jump
def on_space_release(event):
    global space_pressed_time, jump_height
    global velocity, on_ground
    if on_ground and space_pressed_time is not None:
        # calculate how long spacebar was held
        held_time = time.time() - space_pressed_time
        space_pressed_time = None
        held_time = max(0.1, min(held_time, 1.0))
        jump_height = int(-held_time * 100)

            # apply velocity
        held_time = max(0.1, min(held_time, 1.0))
        velocity = jump_height  #* held_time * 1.5  # boost based on hold time
        on_ground = False

# uses reset() to restart the game
def restart(event):
    global end
    if end == 1:
        reset()
        end = 0
        w.after(int(game_speed), display)

# checks for object collision, unless shield present
def touch(c):
    global end
    # stop if shield is on
    if shield_active:
        return
    for l in [l1, l2, l3, l4, l5]:
        if 25 < l[0] < 75:
            for i in range(l[1][1]):
                # Checks distance between player and object
                check = np.add(np.square(60 - l[0]), np.square(c[0] - 210 + i))
                if check <= np.square(10):
                    end = 1 # game over
                    break

# Primary driver of the game, handles calling all functions that control gameplay
def logic():
    global l1, l2, l3, l4, l5, c, u, d, jump, point, game_speed, coins_collected
    for l in [l1, l2, l3, l4, l5]:
        if l[0] <= 0:
            n = np.random.randint(30, 100)
            l[0], l[1] = 950 + n, randdim()
        else:
            l[0] -= 1

    global velocity, gravity, on_ground
    velocity += gravity
    c[0] += velocity

    # stop at ground
    if c[0] >= 200:
        c[0] = 200
        velocity = 0
        on_ground = True

    if any(l[0] == 50 for l in [l1, l2, l3, l4, l5]):
        point += 1
        if point % 5 == 0 and game_speed > 2:
            game_speed -= 2
    
    touch(c)
    for l in [l1, l2, l3, l4, l5]:
        if not l[1][2]:  # coin not collected
            cx = l[0] + l[1][0] // 2
            cy = 200 - l[1][1] - l[1][3]
            dx = abs(cx - 60)
            dy = abs(cy - c[0])
            if dx < 10 and dy < 10:
                l[1] = (l[1][0], l[1][1], True)  # mark coin as collected
                point += 1
                coins_collected += 1
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

def get_background_color():
    max_speed = 12  # starting speed
    min_speed = 2  # fastest

    # Normalize speed between 0 and 1 (0 = max speed, 1 = start)
    norm = (game_speed - min_speed) / (max_speed - min_speed)
    norm = max(0, min(norm, 1))  # clamp just in case

    # Math to go from blue to red as speed icnreases
    r = int(255 * (1 - norm) + 173 * norm)
    g = int(32 * (1 - norm) + 216 * norm)
    b = int(32 * (1 - norm) + 230 * norm)

    return f'#{r:02x}{g:02x}{b:02x}'

def toggle_pause(event):
    global paused
    paused = not paused

def show_start_screen():
    w.delete("all")
    w.create_text(350, 150, text="OBSTACLE JUMPER", font=("Helvetica", 24), fill="black")
    w.create_text(350, 200, text="Press SPACE to Start", font=("Helvetica", 14), fill="black")

# frame by frame handler of what is displayed, primary canvas driver
def display():
    global w, c, point
    canvas_width = 700
    canvas_height = 400
    bg_color = get_background_color()
    w.delete("all")
    w.create_rectangle(0, 0, canvas_width, 200, fill=get_background_color(), outline="")
    w.create_line(0, 200, canvas_width, 200, fill="#400000")
    for l in [l1, l2, l3, l4, l5]:
        rect(l, w)

        # Draw coin if not collected
        if not l[1][2]:  # if coin not collected
            cx = l[0] + l[1][0] // 2
            cy = 200 - l[1][1] - l[1][3]
            w.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="gold")

    circle(c, w) # draw player
    draw_power_up(w) # draw shield if applicable
    w.create_text(40, 15, text=f'Points ==> {point}')
    w.create_text(40, 30, text=f'Coins ==> {coins_collected}')
    w.create_text(622, 20, text=f'High score ==> {high_score}')
    if shield_active:
        w.create_text(50, 70, text=f'Shield: {shield_timer // 60}', fill='blue')
    if not paused:
        logic()
    if end == 0:
        if not paused:
            w.after(game_speed, display) # schedule next frame
        else:
            w.create_text(350, 100, text="PAUSED", font=("Helvetica", 20), fill="black")
            w.after(100, display)  # keep refreshing slowly while paused
    elif end == 1:
        endfunct(w) # show game over screen

    w.create_text(600, 40, text=f'Speed: {game_speed}')
    
# The main game function that sets up window and keybinds
def game():
    global w
    master = Tk()
    w = Canvas(master, width=700, height=400)
    #keybinds
    master.bind("p", toggle_pause)
    master.bind('<space>', on_space)
    master.bind('<KeyRelease-space>', on_space_release)
    master.bind("r", restart)
    #display() removed for start menu to work
    w.pack()
    # start with the intro screen instead of launching the game immediately
    show_start_screen()
    mainloop()

game()
import tkinter
import time
from tkinter import messagebox

# Window and canvas configuration
canvasWidth = 750
canvasHeight = 500
window = tkinter.Tk()
window.title("Ball and Bat Game")
canvas = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight, bg="dodgerblue4")
canvas.pack()

# Creating the bat and ball objects
bat = canvas.create_rectangle(0, 0, 40, 10, fill="dark turquoise")
ball = canvas.create_oval(20, 0, 30, 10, fill="deep pink")

# Game state variables
windowOpen = True
score = 0
bounceCount = 0

# Input tracking variables
leftPressed = 0
rightPressed = 0

# Initial speeds for bat and ball
batSpeed = 6
ballMoveX = 4
ballMoveY = -4

# Bat position constants
setBatTop = canvasHeight - 40
setBatBottom = canvasHeight - 30

def main_loop():
    """Main game loop to update game state and redraw elements."""
    while windowOpen:
        move_bat()
        move_ball()
        window.update()
        time.sleep(0.02)
        if windowOpen:
            check_game_over()

def on_key_press(event):
    """Handles key press events for bat movement."""
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 1
    elif event.keysym == "Right":
        rightPressed = 1

def on_key_release(event):
    """Handles key release events for bat movement."""
    global leftPressed, rightPressed
    if event.keysym == "Left":
        leftPressed = 0
    elif event.keysym == "Right":
        rightPressed = 0

def move_bat():
    """Moves the bat based on user input while ensuring it stays within bounds."""
    batMove = batSpeed * rightPressed - batSpeed * leftPressed
    batLeft, _, batRight, _ = canvas.coords(bat)
    # Prevent the bat from moving out of canvas boundaries
    if (batLeft > 0 or batMove > 0) and (batRight < canvasWidth or batMove < 0):
        canvas.move(bat, batMove, 0)

def move_ball():
    """Moves the ball, handles collisions, and increases difficulty after a few bounces."""
    global ballMoveX, ballMoveY, score, bounceCount, batSpeed

    # Get current ball coordinates
    ballLeft, ballTop, ballRight, ballBottom = canvas.coords(ball)

    # Ball collision with canvas walls
    if ballMoveX > 0 and ballRight > canvasWidth:  # Right wall
        ballMoveX = -ballMoveX
    if ballMoveX < 0 and ballLeft < 0:  # Left wall
        ballMoveX = -ballMoveX
    if ballMoveY < 0 and ballTop < 0:  # Top wall
        ballMoveY = -ballMoveY

    # Ball collision with the bat
    batLeft, batTop, batRight, batBottom = canvas.coords(bat)
    if ballMoveY > 0 and ballBottom >= batTop and ballBottom <= batBottom:
        if ballRight > batLeft and ballLeft < batRight:  # Ball hits the bat
            ballMoveY = -ballMoveY
            score += 1
            bounceCount += 1

            # Increase difficulty every 4 bounces
            if bounceCount == 4:
                bounceCount = 0
                batSpeed += 1
                ballMoveX += 1 if ballMoveX > 0 else -1
                ballMoveY -= 1

    # Move the ball
    canvas.move(ball, ballMoveX, ballMoveY)

def check_game_over():
    """Checks if the game is over and prompts the user to restart or quit."""
    global windowOpen
    ballLeft, ballTop, ballRight, ballBottom = canvas.coords(ball)

    if ballTop > canvasHeight:  # Ball falls below the bat
        print(f"Your score is {score}")
        playAgain = messagebox.askyesno("Game Over", f"Your score is {score}. Play again?")
        if playAgain:
            reset()
        else:
            close()

def close():
    """Closes the game window and terminates the program."""
    global windowOpen
    windowOpen = False
    window.destroy()

def reset():
    """Resets the game state to start a new game."""
    global score, bounceCount, batSpeed, leftPressed, rightPressed, ballMoveX, ballMoveY
    leftPressed = 0
    rightPressed = 0
    ballMoveX = 4
    ballMoveY = -4
    canvas.coords(bat, 10, setBatTop, 50, setBatBottom)
    canvas.coords(ball, 20, setBatTop - 10, 30, setBatTop)
    score = 0
    bounceCount = 0
    batSpeed = 6

# Configure window close protocol and key bindings
window.protocol("WM_DELETE_WINDOW", close)
window.bind("<KeyPress>", on_key_press)
window.bind("<KeyRelease>", on_key_release)

# Start the game
reset()
main_loop()

import streamlit as st
import numpy as np
import time

# Constants
BOARD_SIZE = 20
SPEED = 0.2

# Directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Game State Initialization
def init_state():
    snake = [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
    food = (np.random.randint(BOARD_SIZE), np.random.randint(BOARD_SIZE))
    direction = RIGHT
    return snake, food, direction

# Move the snake
def move_snake(snake, direction):
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    new_snake = [head] + snake[:-1]
    return new_snake

# Check if the snake has collided with walls or itself
def check_collision(snake):
    head = snake[0]
    return (head[0] < 0 or head[0] >= BOARD_SIZE or
            head[1] < 0 or head[1] >= BOARD_SIZE or
            head in snake[1:])

# Check if the snake has eaten the food
def check_food_collision(snake, food):
    return snake[0] == food

# Generate new food location
def generate_food(snake):
    while True:
        food = (np.random.randint(BOARD_SIZE), np.random.randint(BOARD_SIZE))
        if food not in snake:
            return food

# Render the board
def render_board(snake, food):
    board = np.zeros((BOARD_SIZE, BOARD_SIZE))
    for segment in snake:
        board[segment] = 1
    board[food] = 2
    return board

# Game loop
snake, food, direction = init_state()

st.title("Snake Game")

st.write("Use arrow keys to control the snake.")
score_display = st.empty()
board_display = st.empty()

# Capture keyboard inputs
if 'direction' not in st.session_state:
    st.session_state.direction = direction

def update_direction(key):
    if key == 'ArrowUp' and st.session_state.direction != DOWN:
        st.session_state.direction = UP
    elif key == 'ArrowDown' and st.session_state.direction != UP:
        st.session_state.direction = DOWN
    elif key == 'ArrowLeft' and st.session_state.direction != RIGHT:
        st.session_state.direction = LEFT
    elif key == 'ArrowRight' and st.session_state.direction != LEFT:
        st.session_state.direction = RIGHT

key_press = st.text_input("Press any arrow key", value="", max_chars=1, key="keyboard")
update_direction(key_press)

# Game loop
while True:
    # Move the snake
    snake = move_snake(snake, st.session_state.direction)

    # Check for collisions
    if check_collision(snake):
        st.write("Game Over! Your score is:", len(snake) - 1)
        break

    # Check for food
    if check_food_collision(snake, food):
        snake.append(snake[-1])
        food = generate_food(snake)

    # Render the board
    board = render_board(snake, food)
    score_display.text(f"Score: {len(snake) - 1}")
    board_display.image(board, width=300)

    # Control game speed
    time.sleep(SPEED)

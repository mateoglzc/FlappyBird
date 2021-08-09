import pygame
import sys
from player import Bird
from Pipes import PipePair
from button import Button
from inputBox import InputBox
import pandas as pd

def saveRecord(name : str, score : int):
    records = pd.read_csv("./records.csv")
    new_score = [name,score]
    records.loc[len(records)] = new_score
    records.to_csv("./records.csv", index=False)

def getRecords():
    records = pd.read_csv("./records.csv")
    records = records.sort_values(by=["Score"], ascending=False)
    return records.to_dict(orient="list")

def render_pipes(screen, pipes, width, height, itr):

    current_pipe = pipes[0]

    if current_pipe.x_1 + current_pipe.width + 34 <= 0:
        pipes.pop(0)
        del current_pipe
        pipes.append(PipePair(width, height))

    # Pipes
    if itr > 0:
        pipes[0].move()
    if itr > 34:
        pipes[1].move()
    if itr > 68:
        pipes[2].move()

    if not itr >= 81:
        itr += 1

    for pipe in pipes:
        pipe.draw(screen)

    return itr

def MainMenu(screen, title, start_button, exit_button, scene, pipes, bird, w, h):

    itr = 0

    # Draw Buttons
    start_button.draw(screen)
    exit_button.draw(screen)
    
    rigth_click, left_click, _ = pygame.mouse.get_pressed()

    if rigth_click and start_button.click(pygame.mouse.get_pos()):
        scene = 'Game'
    elif rigth_click and exit_button.click(pygame.mouse.get_pos()):
        pygame.quit()
        sys.exit()
        
    screen.blit(title, (55, 50))

    for pipe in pipes:
        pipe.reset()

    bird.reset(w//2, h//2)

    return scene, itr

def Game(flappy, pipes, events, keys, width, height, itr, screen, scene, score, font):

    # Check for events 
    for event in events:

        if event.type == pygame.KEYDOWN and keys[pygame.K_SPACE]:
            flappy.flap()

    # Which pipe is infront of our bird
    current_pipe = 0

    for i, pipe in enumerate(pipes):
        if (pipe.x_1 + pipe.width) > width//2:
            current_pipe = i
            break

    p = pipes[current_pipe]

    # Scoring
    if p.x_1 + 40 == flappy.x:
        score += 1

    # Bird
    flappy.fall()
    flappy.draw(screen)

    # Collision detection
    for pipe in pipes:
        if pipe.collide(flappy, screen) or flappy.y >= height or flappy.y <= 0:
            scene = "Records"

    itr = render_pipes(screen, pipes, width, height, itr)

    score_text = font.render(f'Score: {score}', True, (0,0,0))
    screen.blit(score_text, (20,4))

    return scene, itr, score

def registerRecord(screen, input_box, events, title, font, sc) -> str:
        scene = "Records"

        input_box.draw(screen)        
        ready, record_name = input_box.write(events)

        # Render records
        records = getRecords()
        names = records["Name"]
        scores = records["Score"]

        screen.blit(title, (50,25))

        x = 105
        y = 145

        for i in range(15):

            if i < len(names):
                name = font.render(f'{names[i]}', True, (0,0,0))
                score = font.render(f'{scores[i]}', True, (0,0,0))

                screen.blit(name, (x, y))
                screen.blit(score, (x+160, y))

                y += 20

        if ready:
            saveRecord(record_name, sc)
            scene = "MainMenu"
            input_box.text = ''
            sc = 0

        return scene, sc

    

def main():
    
    pygame.init()

    # Clock
    clock = pygame.time.Clock()

    # Game Screen
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)

    # Bird and pipe creation
    flappy = Bird(width/2, height/2)
    pipes = []

    for _ in range(3):
        pipes.append(PipePair(width, height))

    # Game iterations
    itr = 0

    # Background
    background = pygame.image.load("./Images/background.png")

    # Menu title
    title = pygame.image.load("./Images/Title.png")

    # Input text box
    record_input = InputBox(105, 110, 100, 50, (255, 134, 192))

    # Menu Buttons
    start_button = Button(80, 220, "./Images/start.png")
    exit_button = Button(220, 220, "./Images/exit.png")

    # Scene
    scene = "MainMenu"

    # Score
    score = 0
    font = pygame.font.SysFont(None, 24)

    running = True

    # Game Loop
    while running:

        events = pygame.event.get()

        # Check which keys are pressed
        keys = pygame.key.get_pressed()

        # Check for events 
        for event in events:

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()

        screen.blit(background, (0,0))

        if scene == "Game":
            scene, itr, score = Game(flappy, pipes, events, keys, width, height, itr, screen, scene, score, font)

        if scene == "MainMenu":
            scene, itr = MainMenu(screen, title, start_button, exit_button, scene, pipes, flappy, width, height)
        
        if scene == "Records":
            scene, score = registerRecord(screen, record_input, events, title, font, score)

        pygame.display.flip()
        clock.tick(20)

if __name__ == "__main__":
    main()
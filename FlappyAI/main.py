import pygame
import neat
import sys, math
from player import Bird
from Pipes import PipePair


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]

    return math.sqrt(dx**2 + dy**2)


def remove(index, birds, ge, nets):
    birds.pop(index)
    ge.pop(index)
    nets.pop(index)


def visualize(screen, p, birds):
    # Visualizing the space between pipes
    square = pygame.Rect(p.x_1 - 5, p.h_2, p.width, 100)
    pygame.draw.rect(screen, (255,67,190), square)

    # Draw line between bird and pipe
    for bird in birds:
        pygame.draw.line(screen, (255,255,250), (bird.x + 15, bird.y + 15), (p.x_1 + 80, p.h_2 + 50), width=2)

        pygame.draw.line(screen, (255,0,0), (0, p.h_2), (p.x_1 + 80, p.h_2), width=2)
        pygame.draw.line(screen, (255,0,0), (0, p.h_2 + 100), (p.x_1 + 80, p.h_2 + 100), width=2)

        pygame.draw.line(screen, (255,100,0), (bird.x + 20, bird.y + 10), (p.x_1 - 10, p.h_2), width=2)
        pygame.draw.line(screen, (255,40,0), (bird.x + 20, bird.y + 10), (p.x_1 - 10, p.h_2 + 100 ), width=2)


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


def evol_genomes(genomes, config):
    
    pygame.init()

    # Clock
    clock = pygame.time.Clock()

    # Game Screen
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)

    # Bird creation 
    pipes = []
    birds = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        birds.append(Bird(width//2, height//2))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    # Starting pipes
    for _ in range(3):
        pipes.append(PipePair(width, height))


    # Background 
    background = pygame.image.load("./Images/background.png")

    # Score
    score = 0
    font = pygame.font.SysFont(None, 24)

    # Number of iterations
    itr = 0

    # Game Loop
    while True:
        
        # User Input Detection
        events = pygame.event.get()

        # Check which keys are pressed
        keys = pygame.key.get_pressed()

        # Check for events 
        for event in events:

            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                pygame.quit()
                sys.exit()

        # Draw background
        screen.blit(background, (0,0))

        # Which pipe is infront of our bird
        current_pipe = 0

        for i, pipe in enumerate(pipes):
            if pipe.x_1 + 80 > width//2:
                current_pipe = i
                for i, bird in enumerate(birds):
                    ge[i].fitness += 2
                break

        p = pipes[current_pipe]

        visualize(screen, p, birds)

        # Render Birds
        for bird in birds:
            bird.fall()
            bird.draw(screen)

        # Render Pipes   
        itr = render_pipes(screen, pipes, width, height, itr)

        # If there are no more birds restart the game
        if len(birds) == 0:
            break

        # Scoring
        b = birds[-1]
        if p.x_1 + 40 == b.x:
            score += 1

        # Collision detection
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird, screen):
                    ge[i].fitness -= 1
                    remove(i, birds, ge, nets)

        for i, bird in enumerate(birds):
            if bird.y >= height or bird.y <= 0:
                bird.reset(width//2, height//2)

        # Output 
        for i, bird in enumerate(birds):
            output = nets[i].activate(
                    (
                    bird.y, 
                    p.x_1 - bird.x + 80,
                    bird.y - p.h_2,
                    (p.h_2 + 100) - bird.y//2 + 30,
                    )
            )

            if output[0] > 0.5:
                bird.flap()



        score_text = font.render(f'Score: {score}', True, (0,0,0))
        birds_left = font.render(f'Birds Left: {len(birds)}', True, (0,0,0))
        screen.blit(score_text, (20,4))
        screen.blit(birds_left, (20,24))

        pygame.display.flip()
        clock.tick(20)

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(evol_genomes, 50)


if __name__ == "__main__":
    run("./config.txt")
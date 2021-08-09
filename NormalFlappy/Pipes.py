import pygame
import random

class PipePair():

    def __init__(self, width, height) -> None:

        self.screen_width = width
        self.screen_height = height
        
        self.width = 80
        self.height = random.randint(100, 200)

        self.x_2 = self.screen_width
        self.y_2 = 0
        
        self.x_1 = self.screen_width
        self.y_1 = self.screen_height - self.height


        self.pipe_head = pygame.image.load("./Images/PipeHead.png")
        self.pipe_tail = pygame.image.load("./Images/PipeTail.png")

        self.h_2 = self.y_1 - 100


    def move(self):
        self.x_1 -= 5
        self.x_2 -= 5

    def draw(self, screen):

        y = self.h_2-50


        screen.blit(self.pipe_head, (self.x_1, y + 150))
        screen.blit(self.pipe_head, (self.x_2, y))
        
        screen.blit(self.pipe_tail, (self.x_1, y + 200))
        screen.blit(self.pipe_tail, (self.x_2, -250 + self.h_2))

        

    def reset(self):
        self.height = random.randint(100, 150)

        self.x_1 = self.screen_width
        self.y_1 = self.screen_height - self.height

        self.x_2 = self.screen_width
        self.y_2 = 0

    def collide(self, bird, screen):

        y = self.h_2-50

        pipe_1 = pygame.Rect(self.x_1, y + 150, self.width, self.height + 50)
        pipe_2 = pygame.Rect(self.x_2, self.h_2 - self.height, self.width, self.height)

        if pipe_1.colliderect(bird.rect()) or pipe_2.colliderect(bird.rect()):
            return True
        else:
            return False

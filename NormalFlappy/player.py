import pygame

class Bird():

    def __init__(self, pos_x, pos_y):

        self.x = pos_x
        self.y = pos_y

        self.width = 30
        self.height = 30

        self.image = pygame.image.load("./Images/Flappy.png")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fall(self):
        self.y += 5

    def flap(self):
        self.y -= 40

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self, x, y):
        self.x = x
        self.y = y
        


import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image 

    def get_guppy(self, frame, width, height, scale=1, colour=(1, 1, 1)):
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill((1, 1, 1))
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        
        return image
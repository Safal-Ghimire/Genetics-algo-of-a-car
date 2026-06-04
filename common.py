import pygame
pygame.font.init()
screen = pygame.display.set_mode((900,900))
pygame.display.set_caption("Self driving ai")
clock = pygame.time.Clock()
vision_threshold=80
ray_count=9
font = pygame.font.SysFont("Arial", 16)
elite_count=3
n=3

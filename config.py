import pygame

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

COLOR_BG = (8, 11, 9)
COLOR_CARD_BG = (15, 19, 16)
COLOR_TEXT = (210, 230, 215)
COLOR_ACCENT = (70, 210, 120)
COLOR_DANGER = (210, 50, 40)
COLOR_WARNING = (220, 180, 50)
COLOR_ANOMALY = (60, 210, 235)
COLOR_BLACK = (0, 0, 0)

FONT_MAIN = pygame.font.SysFont("Courier New", 18, bold=True)
FONT_TITLE = pygame.font.SysFont("Courier New", 26, bold=True)
FONT_SMALL = pygame.font.SysFont("Courier New", 14, bold=True)
FONT_HUD = pygame.font.SysFont("Courier New", 13, bold=True)
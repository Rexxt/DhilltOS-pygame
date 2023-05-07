# we'll eventually replace this, this is just for test purposes
import pygame

TITLE_HEIGHT = 30

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y + TITLE_HEIGHT, w, h)
        self.title_rect = pygame.Rect(x, y, w, TITLE_HEIGHT)
        self.cursor_pos = (0, 0)
        self.origin_pos = (x, y)
        self.dragging = False
    
    def mouse_down(self, event):
        if event.pos[0] >= self.rect.x and event.pos[0] <= (self.rect.x + self.rect.w) and event.pos[1] >= (self.rect.y - TITLE_HEIGHT) and event.pos[1] <= self.rect.y:
            self.dragging = True
            self.cursor_pos = event.pos

    def mouse_move(self, event):
        if self.dragging:
            self.rect.x = self.origin_pos[0] + event.pos[0] - self.cursor_pos[0]
            self.title_rect.x = self.rect.x
            self.rect.y = self.origin_pos[1] + event.pos[1] - self.cursor_pos[1]
            self.title_rect.y = self.rect.y - TITLE_HEIGHT
    
    def mouse_up(self, event):
        self.dragging = False
        self.origin_pos = (self.rect.x, self.rect.y)
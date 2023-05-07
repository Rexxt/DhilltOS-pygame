# we'll eventually replace this, this is just for test purposes
import pygame

class Box:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.cursor_pos = (0, 0)
        self.origin_pos = (x, y)
        self.dragging = False
    
    def mouse_down(self, event):
        if event.pos[0] >= self.rect.x and event.pos[0] <= (self.rect.x + self.rect.w) and event.pos[1] >= self.rect.y and event.pos[1] <= (self.rect.y + self.rect.h):
            self.dragging = True
            self.cursor_pos = event.pos

    def mouse_move(self, event):
        if self.dragging:
            self.rect.x = self.origin_pos[0] + event.pos[0] - self.cursor_pos[0]
            self.rect.y = self.origin_pos[1] + event.pos[1] - self.cursor_pos[1]
    
    def mouse_up(self, event):
        self.dragging = False
        self.origin_pos = (self.rect.x, self.rect.y)
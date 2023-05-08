import pygame

class Button:
    def __init__(self, caption='Button', x=0, y=0, w=0, h=0, colour=(200, 200, 200), text_colour=(0, 0, 0)):
        self.caption = caption
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.colour = colour
        self.text_colour = text_colour

        self.handlers = {}
        self.hovered = False

    def on(self, event_type, func):
        self.handlers[event_type] = func
        return func

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos

            if x >= self.x and x <= (self.x+self.w) and y >= self.y and y <= (self.y+self.h):
                if not self.hovered and 'mouse_enter' in self.handlers:
                    self.handlers['mouse_enter'](self, event)
                self.hovered = True
            else:
                if self.hovered and 'mouse_leave' in self.handlers:
                    self.handlers['mouse_leave'](self, event)
                self.hover = False
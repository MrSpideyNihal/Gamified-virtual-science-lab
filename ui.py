import pygame
import json, os, sys

# ✅ Ensure Pygame initializes before any Pygame function is used
if not pygame.get_init():
    pygame.init()

# ------------------------------
# Configuration and Style Guide
# ------------------------------
COLORS = {
    "background": (245, 245, 245),
    "text": (33, 33, 33),
    "button": (255, 193, 7),
    "button_text": (0, 0, 0),   
}

WIDTH, HEIGHT = 800, 600

# ✅ Ensure fonts load properly
try:
    heading_font = pygame.font.Font("OpenSans-Bold.ttf", 36)
    button_font = pygame.font.Font("UbuntuMono-Regular.ttf", 24)
except Exception as e:
    print("Font loading failed, using default fonts:", e)
    heading_font = pygame.font.SysFont("sans", 36)
    button_font = pygame.font.SysFont("monospace", 24)

# ------------------------------
# UI Components
# ------------------------------
class Button:
    def __init__(self, text, x, y, width, height, on_click, color=COLORS["button"], text_color=COLORS["button_text"], font=button_font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.on_click = on_click
        self.color = color
        self.text_color = text_color # Make sure this line is present and correct
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Label:
    def __init__(self, text, x, y, font=heading_font, color=COLORS["text"]):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
    
    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        surface.blit(text_surf, text_rect)

class Window:
    def __init__(self, title="Window", width=WIDTH, height=HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.running = True
        self.elements = []
        self.clock = pygame.time.Clock()
        self.keydown_handler = None  # Add a keydown handler

    def add_element(self, element):
        self.elements.append(element)
    
    def set_keydown_handler(self, handler):
        """Allows setting a function to handle keyboard input."""
        self.keydown_handler = handler

    def run(self):
        while self.running:
            self.screen.fill(COLORS["background"])
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and self.keydown_handler:
                    self.keydown_handler(event)  # Call the key handler function
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for element in self.elements:
                        if isinstance(element, Button) and element.is_hovered(mouse_pos):
                            element.on_click()
            
            for element in self.elements:
                element.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

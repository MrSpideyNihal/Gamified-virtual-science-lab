from ui import Window, Label, Button, HEIGHT, WIDTH
import sys
import pygame
import json, os, sys

# ✅ Ensure Pygame initializes before any Pygame function is used
if not pygame.get_init():
    pygame.init()

def start():
    from Menu import menu  
    menu()

def Welcome_window():
    window = Window("Modular Pygame UI")
    window.add_element(Label("Welcome to Modular UI", WIDTH//2, 100))
    window.add_element(Button("New", WIDTH//2 - 75, HEIGHT//2 - 30, 150, 50, lambda: start()))
    window.add_element(Button("Continue", WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50, lambda: print("Continue Clicked")))
    window.add_element(Button("Exit", WIDTH//2 - 75, HEIGHT//2 + 110, 150, 50, sys.exit))
    window.run()

if __name__ == "__main__":
    Welcome_window()

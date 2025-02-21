import pygame
import json, os, sys

# Initialize Pygame
pygame.init()

# ------------------------------
# Configuration and Style Guide
# ------------------------------
# Colors (converted from hex to RGB)
COLORS = {
    "physics": (75, 0, 130),       # Indigo for Physics
    "chemistry": (244, 67, 54),    # Red for Chemistry
    "biology": (124, 179, 66),     # Green for Biology
    "background": (245, 245, 245), # Light grey background
    "text": (33, 33, 33),          # Dark grey text
    "accent": (255, 193, 7)        # Achievement gold accent
}

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Science Lab")

# Fonts
try:
    heading_font = pygame.font.Font("OpenSans-Bold.ttf", 36)
    button_font = pygame.font.Font("UbuntuMono-Regular.ttf", 24)
    small_font = pygame.font.Font("UbuntuMono-Regular.ttf", 18)
except:
    # Fallback to default if custom fonts are not available.
    heading_font = pygame.font.SysFont("sans", 36)
    button_font = pygame.font.SysFont("monospace", 24)
    small_font = pygame.font.SysFont("monospace", 18)

# ------------------------------
# Progress Management Functions
# ------------------------------
PROGRESS_FILE = "progress.json"
default_progress = {"physics": 0, "chemistry": 0, "biology": 0, "achievements": []}

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return None

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4)

def new_progress():
    progress = default_progress.copy()
    save_progress(progress)
    return progress

# Global progress variable
progress_data = None

# ------------------------------
# Utility Functions for Buttons
# ------------------------------
def draw_button(surface, text, rect, color, text_color, font):
    pygame.draw.rect(surface, color, rect, border_radius=8)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    surface.blit(text_surf, text_rect)

def is_mouse_over(rect, mouse_pos):
    x, y, w, h = rect
    return x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h

# ------------------------------
# Dummy Subject Functions
# ------------------------------
def run_physics():
    print("Launching Physics Experiments...")

def run_chemistry():
    print("Launching Chemistry Experiments...")

def run_biology():
    print("Launching Biology Experiments...")

# ------------------------------
# UI Screens and States
# ------------------------------
# States: "session" for the initial menu, "subject" for subject selection.
state = "session"

# Button definitions for session screen (x, y, width, height)
btn_width, btn_height = 150, 50
padding = 20

# Calculate positions for session buttons (2 columns x 2 rows)
session_buttons = {
    "Start": pygame.Rect(WIDTH//2 - btn_width - padding//2, HEIGHT//2 - btn_height - padding//2, btn_width, btn_height),
    "Load": pygame.Rect(WIDTH//2 + padding//2, HEIGHT//2 - btn_height - padding//2, btn_width, btn_height),
    "New": pygame.Rect(WIDTH//2 - btn_width - padding//2, HEIGHT//2 + padding//2, btn_width, btn_height),
    "Exit": pygame.Rect(WIDTH//2 + padding//2, HEIGHT//2 + padding//2, btn_width, btn_height),
}

# Button definitions for subject selection screen
subject_btn_width, subject_btn_height = 180, 50
subject_buttons = {
    "Physics": pygame.Rect(100, 200, subject_btn_width, subject_btn_height),
    "Chemistry": pygame.Rect((WIDTH - subject_btn_width) // 2, 200, subject_btn_width, subject_btn_height),
    "Biology": pygame.Rect(WIDTH - subject_btn_width - 100, 200, subject_btn_width, subject_btn_height),
    "Back": pygame.Rect(20, HEIGHT - 70, 100, 40)
}

clock = pygame.time.Clock()

# ------------------------------
# Main Loop
# ------------------------------
running = True
while running:
    screen.fill(COLORS["background"])
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "session":
                # Session screen button clicks
                for label, rect in session_buttons.items():
                    if is_mouse_over(rect, mouse_pos):
                        if label in ("Start", "Load"):
                            loaded = load_progress()
                            if loaded:
                                progress_data = loaded
                                state = "subject"
                            else:
                                print("No saved progress found. Please start a new session.")
                        elif label == "New":
                            progress_data = new_progress()
                            state = "subject"
                        elif label == "Exit":
                            pygame.quit()
                            sys.exit()
            elif state == "subject":
                # Subject selection screen button clicks
                for label, rect in subject_buttons.items():
                    if is_mouse_over(rect, mouse_pos):
                        if label == "Back":
                            state = "session"
                        elif label == "Physics":
                            run_physics()
                        elif label == "Chemistry":
                            run_chemistry()
                        elif label == "Biology":
                            run_biology()

    # ------------------------------
    # Render based on state
    # ------------------------------
    if state == "session":
        # Title
        title_surf = heading_font.render("Virtual Science Lab", True, COLORS["text"])
        title_rect = title_surf.get_rect(center=(WIDTH//2, 100))
        screen.blit(title_surf, title_rect)
        # Draw session buttons
        for label, rect in session_buttons.items():
            draw_button(screen, label, rect, COLORS["accent"], COLORS["text"], button_font)
    elif state == "subject":
        # Title
        sub_title = heading_font.render("Select a Subject", True, COLORS["text"])
        sub_title_rect = sub_title.get_rect(center=(WIDTH//2, 80))
        screen.blit(sub_title, sub_title_rect)
        # Draw subject buttons
        draw_button(screen, "Physics", subject_buttons["Physics"], COLORS["physics"], (255,255,255), button_font)
        draw_button(screen, "Chemistry", subject_buttons["Chemistry"], COLORS["chemistry"], (255,255,255), button_font)
        draw_button(screen, "Biology", subject_buttons["Biology"], COLORS["biology"], (255,255,255), button_font)
        draw_button(screen, "Back", subject_buttons["Back"], COLORS["accent"], COLORS["text"], small_font)
        # Display progress information
        if progress_data:
            progress_text = f"Progress - Physics: {progress_data['physics']}% | Chemistry: {progress_data['chemistry']}% | Biology: {progress_data['biology']}%"
            progress_surf = small_font.render(progress_text, True, COLORS["text"])
            progress_rect = progress_surf.get_rect(center=(WIDTH//2, HEIGHT - 40))
            screen.blit(progress_surf, progress_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

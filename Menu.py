from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame, sys
from chem import chemistry_experiment  
from user_data import get_user_data  # ✅ Import get_user_data from user_data.py
from main import Welcome_window

from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame, sys
from chem import chemistry_experiment  
from user_data import get_user_data  
from main import Welcome_window  

def open_subject(subject, user_name):
    """Launch the selected subject experiment with user_name."""
    print(f"Launching {subject} experiments...")
    if subject == "Chemistry":
        chemistry_experiment(user_name)  
    elif subject == "Physics":
        pass
    elif subject == "Biology":
        pass
    else:
        print("Undefined Subject")

def menu(user_name):
    """Displays the subject selection menu and shows badges."""
    print("Opening Subject Selection Menu")
    window = Window("Select Subject")

    user_data = get_user_data(user_name)  
    badges = user_data.get("badges", [])

    badge_text = " Badges: " + ", ".join(badges) if badges else " No Badges Yet"
    window.add_element(Label(badge_text, WIDTH - 600, 100, color=(255, 215, 0)))  

    window.add_element(Label("Choose a Subject", WIDTH//2, 50))

    subjects = ["Physics", "Chemistry", "Biology"]
    for i, subject in enumerate(subjects):
        window.add_element(Button(subject, WIDTH//2 - 90, 200 + i * 70, 180, 50, lambda s=subject: open_subject(s, user_name)))

    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, lambda: Welcome_window()))  
    
    window.run()

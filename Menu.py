from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame, sys
from chem import chemistry_experiment
# ------------------------------
# Subject Selection Menu
# ------------------------------
def open_subject(subject):
    print(f"Launching {subject} experiments...")
    if subject == "Chemistry":
        chemistry_experiment()
    elif subject == "Physics":
        pass
    elif subject == "Biology":
        pass
    else:
        print("Undefined Subject")

def menu(go_back=None):  # ✅ Added go_back parameter
    print("Opening Subject Selection Menu")  # Debugging message
    window = Window("Select Subject")
    window.add_element(Label("Choose a Subject", WIDTH//2, 50))

    subjects = ["Physics", "Chemistry", "Biology"]
    for i, subject in enumerate(subjects):
        window.add_element(Button(subject, WIDTH//2 - 90, 200 + i * 70, 180, 50, lambda s=subject: open_subject(s)))

    if go_back:  # ✅ Use go_back function instead of direct import
        window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, go_back))

    window.run()

if __name__ == "__main__":
    menu()

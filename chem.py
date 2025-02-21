import json
import pygame
from ui import Window, Label, Button, WIDTH, HEIGHT
from user_data import award_badge  
from animation import VideoPlayer  

DATA_FILE = "chemistry_data.json"

reaction_videos = {
    "water": "reaction_water.mp4",  
    "salt": "reaction_salt.mp4",  
}
video_player = VideoPlayer(reaction_videos)

def load_chemistry_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"elements": {}, "reactions": {}}

def save_chemistry_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

class Chem:
    def __init__(self):
        self.data = load_chemistry_data()

    def add_element(self, symbol, name, atomic_number):
        if symbol in self.data["elements"]:
            return f"Element '{symbol}' already exists."
        
        self.data["elements"][symbol] = {
            "name": name,
            "atomic_number": atomic_number
        }
        save_chemistry_data(self.data)
        return f"Element '{name}' added successfully."

    def add_reaction(self, elem1, elem2, result):
        key = tuple(sorted([elem1, elem2]))
        if key in self.data["reactions"]:
            return f"Reaction '{elem1} + {elem2}' already exists."
        
        self.data["reactions"][key] = result
        save_chemistry_data(self.data)
        return f"Reaction '{elem1} + {elem2} → {result}' added."

    def mix(self, elem1, elem2):
        key = tuple(sorted([elem1, elem2]))
        if key in self.data["reactions"]:
            result = self.data["reactions"][key]
            if "Water" in result:
                award_badge("User", "Water Creator")
                video_player.play_reaction_video("water")
            elif "Salt" in result:
                award_badge("User", "Salt Maker")
                video_player.play_reaction_video("salt")
            return f"{elem1} + {elem2} → {result}"
        else:
            return "No reaction occurs."

def chemistry_experiment(user_name):
    chem = Chem()
    window = Window("Chemistry Lab")
    window.add_element(Label("Choose Two Elements to Mix", WIDTH//2, 50))

    selected = []
    selected_label = Label("", WIDTH//2, HEIGHT//2 - 50, color=(0, 0, 255))
    result_label = Label("", WIDTH//2 + 100, HEIGHT//2 + 50, color=(255, 165, 0))
    window.add_element(selected_label)
    window.add_element(result_label)
    
    def select_element(symbol):
        if len(selected) < 2:
            selected.append(symbol)
            selected_label.text = " + ".join(selected)
    
    def mix_elements():
        if len(selected) == 2:
            pygame.time.delay(500)  
            reaction_result = chem.mix(selected[0], selected[1])
            result_label.text = reaction_result
            selected.clear()
            selected_label.text = ""

    y_offset = 100
    for element in chem.data["elements"]:
        window.add_element(Button(f"{element}", 50, y_offset, 180, 50, lambda e=element: select_element(e)))
        y_offset += 70

    window.add_element(Button("Mix", WIDTH - 120, 20, 100, 50, mix_elements))
    window.add_element(Button("Add Element", WIDTH - 180, HEIGHT - 70, 150, 40, lambda: add_element_ui(chem)))
    window.add_element(Button("Add Reaction", WIDTH - 350, HEIGHT - 70, 150, 40, lambda: add_reaction_ui(chem)))
    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, window.run))
    
    window.run()

def add_reaction_ui(chem):
    window = Window("Add Reaction")

    elem1_input = Label("|", WIDTH//2, 150, color=(0, 0, 255))
    elem2_input = Label("|", WIDTH//2, 200, color=(0, 0, 255))
    result_input = Label("|", WIDTH//2, 250, color=(0, 0, 255))
    result_label = Label("", WIDTH//2, 350)

    def save_reaction():
        elem1 = elem1_input.text.strip("| ")
        elem2 = elem2_input.text.strip("| ")
        result = result_input.text.strip("| ")

        if elem1 and elem2 and result:
            result_label.text = chem.add_reaction(elem1, elem2, result)
        else:
            result_label.text = "Invalid input."

    window.add_element(Label("Element 1:", WIDTH//4, 150))
    window.add_element(elem1_input)
    window.add_element(Label("Element 2:", WIDTH//4, 200))
    window.add_element(elem2_input)
    window.add_element(Label("Reaction Result:", WIDTH//4, 250))
    window.add_element(result_input)
    window.add_element(Button("Add", WIDTH//2 - 50, 300, 100, 40, save_reaction))
    window.add_element(result_label)
    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, chemistry_experiment))

    window.run()

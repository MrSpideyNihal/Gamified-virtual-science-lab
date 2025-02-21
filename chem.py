import pygame
from ui import Window, Label, Button, WIDTH, HEIGHT
from user_data import load_all_users, save_user_data, get_user_data  
from audioplayer import player
import sys

pygame.init()

class Chem:
    def __init__(self):
        self.elements = {
            "H": {"name": "Hydrogen", "atomic_number": 1},
            "O": {"name": "Oxygen", "atomic_number": 8},
            "Na": {"name": "Sodium", "atomic_number": 11},
            "Cl": {"name": "Chlorine", "atomic_number": 17},
            "Fe": {"name": "Iron", "atomic_number": 26},
            "Cu": {"name": "Copper", "atomic_number": 29},
        }
        
        self.reactions = {
            ("H", "O"): " H₂O (Water) is formed!",
            ("Na", "Cl"): " NaCl (Salt) is formed!",
            ("Fe", "O"): " Iron Oxide (Rust) is formed!",
            ("Cu", "O"): " Copper Oxide is formed!",
        }
    
    def list_elements(self):
        return [symbol for symbol in self.elements]
    
    def mix(self, elem1, elem2):
        if (elem1, elem2) in self.reactions:
            return self.reactions[(elem1, elem2)]
        elif (elem2, elem1) in self.reactions:
            return self.reactions[(elem2, elem1)]
        else:
            return " No reaction occurs."
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
        # player.play_reaction_video("water")

    def mix_elements():
        if len(selected) == 2:
            reaction_result = chem.mix(selected[0], selected[1])
            player.play_random_appreciation()

            result_label.text = f"✨ {selected[0]} + {selected[1]} → {reaction_result} ✨"
            selected.clear()
            selected_label.text = ""

    y_offset = 100
    for element in chem.list_elements():
        btn = Button(f"{element}", 50, y_offset, 180, 50, lambda e=element: select_element(e))
        window.add_element(btn)
        y_offset += 70

    window.add_element(Button(" Mix", WIDTH - 120, 20, 100, 50, mix_elements))
    window.add_element(Button(" Back", 20, HEIGHT - 70, 100, 40, Welcome_window))
    window.run()

def ask_name():
    window = Window("Enter Your Name")
    input_box = Label("|", WIDTH//2, HEIGHT//2, color=(0, 0, 255))  
    user_name = ""

    def on_key(event):
        nonlocal user_name
        if event.key == pygame.K_BACKSPACE:
            user_name = user_name[:-1]
        elif event.key == pygame.K_RETURN:  
            if user_name.strip():
                user_name = user_name.strip()
                save_user_data(user_name, {"badges": []})  
                start(user_name)
                window.running = False
        elif len(user_name) < 20:
            user_name += event.unicode
        input_box.text = user_name + "|"

    window.add_element(Label("Enter Your Name:", WIDTH//2, HEIGHT//2 - 50))
    window.add_element(input_box)
    window.set_keydown_handler(on_key)  
    window.run()

def select_user():
    users = load_all_users()
    if not users:
        print("⚠ No previous students found. Please start a new game.")
        ask_name()
        return  

    window = Window("Select Student")
    window.add_element(Label("Select Your Name", WIDTH//2, 50))

    user_list = list(users.keys())
    visible_count = 5  
    scroll_index = 0  

    def update_display():
        window.elements = [window.elements[0]]
        y_pos = 120
        for i in range(scroll_index, min(scroll_index + visible_count, len(user_list))):
            window.add_element(Button(user_list[i], WIDTH//2 - 75, y_pos, 150, 50, lambda n=user_list[i]: start(n)))
            y_pos += 70

        window.add_element(Label("Press Up or Down Key", WIDTH//2, HEIGHT - 20, color=(128, 128, 128)))
        window.add_element(Button("Back", WIDTH//2 - 50, HEIGHT - 100, 100, 50, Welcome_window))

    def on_scroll(event):
        nonlocal scroll_index
        if event.key == pygame.K_DOWN and scroll_index + visible_count < len(user_list):
            scroll_index += 1  
        elif event.key == pygame.K_UP and scroll_index > 0:
            scroll_index -= 1  
        update_display()  

    update_display()
    window.set_keydown_handler(on_scroll)  
    window.run()

def start(user_name):
    user_data = get_user_data(user_name)  
    print(f"Welcome back, {user_name}! Your progress is saved.")
    print(f"Badges Earned: {', '.join(user_data['badges']) if user_data['badges'] else 'No badges yet'}")
    chemistry_experiment(user_name)

def Welcome_window():
    window = Window("Virtual Science Lab")
    window.add_element(Label("Virtual Science Lab", WIDTH//2, 100))
    
    window.add_element(Button("New Student", WIDTH//2 - 75, HEIGHT//2 - 90, 150, 50, ask_name))
    window.add_element(Button("Continue", WIDTH//2 - 75, HEIGHT//2 - 30, 150, 50, select_user))
    # window.add_element(Button("Chemistry Lab (Guest Mode)", WIDTH//2 - 75, HEIGHT//2 + 30, 250, 50, chemistry_experiment(user_name="Guest")))
    window.add_element(Button("Exit", WIDTH//2 - 75, HEIGHT//2 + 90, 150, 50, sys.exit))
    
    window.run()

if __name__ == "__main__":
    Welcome_window()
from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame

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
            ("H", "O"): "💧 H₂O (Water) is formed!",
            ("Na", "Cl"): "🧂 NaCl (Salt) is formed!",
            ("Fe", "O"): "🛠️ Iron Oxide (Rust) is formed!",
            ("Cu", "O"): "🟤 Copper Oxide is formed!",
        }
    
    def list_elements(self):
        return [symbol for symbol in self.elements]
    
    def mix(self, elem1, elem2):
        if (elem1, elem2) in self.reactions:
            return self.reactions[(elem1, elem2)]
        elif (elem2, elem1) in self.reactions:
            return self.reactions[(elem2, elem1)]
        else:
            return "❌ No reaction occurs."

def chemistry_experiment():
    chem = Chem()
    window = Window("🧪 Chemistry Lab")
    window.add_element(Label("🔬 Choose Two Elements to Mix", WIDTH//2, 50))

    selected = []
    selected_label = Label("", WIDTH//2, HEIGHT//2 - 50, color=(0, 0, 255))
    result_label = Label("", WIDTH//2 +100, HEIGHT//2 + 50, color=(255, 165, 0))
    window.add_element(selected_label)
    window.add_element(result_label)
    
    def select_element(symbol):
        if len(selected) < 2:
            selected.append(symbol)
            selected_label.text = " + ".join(selected)
            selected_label.color = (0, 0, 255)  # Change color when selecting
    
    def mix_elements():
        if len(selected) == 2:
            pygame.time.delay(500)  # Small delay for effect
            result_label.text = f"✨ {selected[0]} + {selected[1]} → {chem.mix(selected[0], selected[1])} ✨"
            result_label.color = (0, 128, 0)  # Change color after reaction
            selected.clear()
            selected_label.text = ""
    
    y_offset = 100
    for element in chem.list_elements():
        btn = Button(f"🔘 {element}", 50, y_offset, 180, 50, lambda e=element: select_element(e))
        window.add_element(btn)
        y_offset += 70
    
    window.add_element(Button("🔄 Mix", WIDTH - 120, 20, 100, 50, mix_elements))
    window.add_element(Button("🔙 Back", 20, HEIGHT - 70, 100, 40, window.run))
    window.run()

if __name__ == "__main__":
    chemistry_experiment()

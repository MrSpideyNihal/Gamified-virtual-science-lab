import pygame
from ui import Window, Label, Button, WIDTH, HEIGHT
from user_data import load_all_users, save_user_data, get_user_data  
import sys
pygame.init()

def ask_name():
    """UI-based name input window for new students."""
    window = Window("Enter Your Name")
    input_box = Label("|", WIDTH//2, HEIGHT//2, color=(0, 0, 255))  
    user_name = ""

    def on_key(event):
        """Handles keyboard input."""
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
    """UI-based student selection with a scrollable list."""
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
        """Update the user list display based on scroll position."""
        window.elements = [window.elements[0]]
        y_pos = 120
        for i in range(scroll_index, min(scroll_index + visible_count, len(user_list))):
            window.add_element(Button(user_list[i], WIDTH//2 - 75, y_pos, 150, 50, lambda n=user_list[i]: start_game(n)))
            y_pos += 70

        window.add_element(Label("Press Up or Down Key", WIDTH//2, HEIGHT - 20, color=(128, 128, 128)))
        window.add_element(Button("Back", WIDTH//2 - 50, HEIGHT - 100, 100, 50, lambda: Welcome_window()))

    def on_scroll(event):
        """Handle scrolling up/down."""
        nonlocal scroll_index
        if event.key == pygame.K_DOWN and scroll_index + visible_count < len(user_list):
            scroll_index += 1  
        elif event.key == pygame.K_UP and scroll_index > 0:
            scroll_index -= 1  
        update_display()  

    from Menu import menu  
    from main import start as start_game  
    from main import Welcome_window  

    update_display()
    window.set_keydown_handler(on_scroll)  
    window.run()

def start(user_name):
    """Start game with a specific student's progress."""
    from Menu import menu  

    user_data = get_user_data(user_name)  
    print(f"Welcome back, {user_name}! Your progress is saved.")
    print(f"Badges Earned: {', '.join(user_data['badges']) if user_data['badges'] else 'No badges yet'}")

    menu(user_name)  

def Welcome_window():
    """Main welcome screen."""
    window = Window("Virtual Science Lab")
    window.add_element(Label("Virtual Science Lab", WIDTH//2, 100))
    
    window.add_element(Button("New Student", WIDTH//2 - 75, HEIGHT//2 - 30, 150, 50, ask_name))
    window.add_element(Button("Continue", WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50, select_user))
    window.add_element(Button("Exit", WIDTH//2 - 75, HEIGHT//2 + 110, 150, 50, sys.exit))
    
    window.run()

if __name__ == "__main__":
    Welcome_window()

from ui import Window, Label, Button, WIDTH, HEIGHT, COLORS
import pygame, sys, math
from audioplayer import player
def show_visual_explanation(visual_type):
    """
    Opens a new window that provides a visual explanation.
    Depending on the visual_type, it displays an animated diagram.
    """
    visual_window = Window("Visual Explanation", WIDTH, HEIGHT)
    # Create a "Close Visual" button in the visual window
    done = False
    clock = pygame.time.Clock()
    
    def exit_visual():
        nonlocal done
        done = True
    
    close_btn = Button("Close Visual", WIDTH - 150, HEIGHT - 70, 130, 40, exit_visual)
    visual_window.add_element(close_btn)
    
    while not done:
        visual_window.screen.fill(COLORS["background"])
        
        if visual_type == "heart":
            # Animated pulsating heart (red circle that changes size)
            time_sec = pygame.time.get_ticks() / 1000
            radius = 40 + 10 * abs(math.sin(time_sec * 3))
            pygame.draw.circle(visual_window.screen, (255, 0, 0), (WIDTH//2, HEIGHT//2), int(radius))
            explanation = Label("This is the heart – it pumps blood!", WIDTH//2, HEIGHT//2 + 100, font=pygame.font.SysFont("sans", 24))
            explanation.draw(visual_window.screen)
        elif visual_type == "lungs":
            # Draw two lung-like ellipses side by side
            rect1 = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 50, 100, 150)
            rect2 = pygame.Rect(WIDTH//2 + 50, HEIGHT//2 - 50, 100, 150)
            pygame.draw.ellipse(visual_window.screen, (173, 216, 230), rect1)
            pygame.draw.ellipse(visual_window.screen, (173, 216, 230), rect2)
            explanation = Label("These are the lungs – where oxygen exchange occurs.", WIDTH//2, HEIGHT//2 + 100, font=pygame.font.SysFont("sans", 24))
            explanation.draw(visual_window.screen)
        else:
            default_label = Label("No visual available.", WIDTH//2, HEIGHT//2)
            default_label.draw(visual_window.screen)
        
        # Process events in the visual window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if close_btn.is_hovered(mouse_pos):
                    exit_visual()
                    
        # Draw the close button
        close_btn.draw(visual_window.screen)
        pygame.display.flip()
        clock.tick(60)

def biology_experiment():
    """
    Main function for the Biology Lab experiment.
    Uses a list of questions (with options, answers, badge, and visual type)
    to run an interactive quiz enhanced with visual learning elements.
    """
    window = Window("Biology Lab", WIDTH, HEIGHT)
    
    # Title
    title_label = Label("🧬 Virtual Biology Lab", WIDTH//2, 50)
    window.add_element(title_label)
    
    # Define the quiz questions
    questions = [
        {
            "question": "Which organ pumps blood?",
            "options": ["Heart", "Liver", "Kidney"],
            "answer": "Heart",
            "badge": "Heart of a Champion",
            "visual": "heart"
        },
        {
            "question": "Which system is responsible for oxygen exchange?",
            "options": ["Respiratory", "Digestive", "Nervous"],
            "answer": "Respiratory",
            "badge": "Breath of Life",
            "visual": "lungs"
        },
        # You can add more questions with their visuals here...
    ]
    
    current_question_index = 0
    answer_buttons = []
    
    question_label = Label("", WIDTH//2, 100)
    window.add_element(question_label)
    
    result_label = Label("", WIDTH//2, 400)
    window.add_element(result_label)
    
    # Placeholder for visual button (to be re-added for each question)
    visual_btn = None

    def display_question(index):
        nonlocal answer_buttons, visual_btn
        # Remove previous answer buttons and visual button
        for btn in answer_buttons:
            if btn in window.elements:
                window.elements.remove(btn)
        answer_buttons = []
        if visual_btn and visual_btn in window.elements:
            window.elements.remove(visual_btn)
        result_label.text = ""
        
        if index < len(questions):
            q = questions[index]
            question_label.text = "Quiz: " + q["question"]
            # Dynamically position answer buttons based on number of options
            option_count = len(q["options"])
            spacing = 150
            start_x = WIDTH//2 - (option_count * spacing)//2 + spacing//2
            for i, option in enumerate(q["options"]):
                def on_click(opt=option, q=q):
                    if opt == q["answer"]:
                        result_label.text = f" Correct! Badge earned: {q['badge']}"
                        player.play_random_appreciation()

                        pygame.time.delay(1000)
                        next_question()
                    else:
                        result_label.text = " Wrong answer! Try again."
                btn = Button(option, start_x + i * spacing - 60, 200, 120, 50, on_click)
                answer_buttons.append(btn)
                window.add_element(btn)
            # Add a "Show Visual" button
            visual_btn = Button("Show Visual", WIDTH//2 - 60, 280, 120, 40, lambda q=q: show_visual_explanation(q["visual"]))
            window.add_element(visual_btn)
        else:
            question_label.text = "Quiz Completed!"
            result_label.text = "Congratulations, you've completed the Biology Lab quiz!"
            # Remove any remaining answer buttons and the visual button
            for btn in answer_buttons:
                if btn in window.elements:
                    window.elements.remove(btn)
            if visual_btn and visual_btn in window.elements:
                window.elements.remove(visual_btn)
    
    def next_question():
        nonlocal current_question_index
        current_question_index += 1
        display_question(current_question_index)
    
    display_question(current_question_index)
    
    # Back button to return to the main menu
    def back_to_menu():
        from Menu import menu
        window.running = False
        menu()
    
    back_btn = Button(" Back", 20, HEIGHT - 70, 100, 40, back_to_menu)
    window.add_element(back_btn)
    
    window.run()

if __name__ == "__main__":
    biology_experiment()

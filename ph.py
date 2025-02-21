from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame
import math

# ------------------------------
# Physics Experiments
# ------------------------------
def free_fall_experiment():
    window = Window("⚙️ Free Fall Experiment")
    window.add_element(Label("⚖️ Free Fall Simulation", WIDTH//2, 50))
    
    gravity = [9.8]
    ball_size = [20]
    ball_y = [100]
    velocity = [0]
    time = [0]
    dragging = [False]
    running = True
    clock = pygame.time.Clock()
    
    def reset():
        time[0] = 0
        velocity[0] = 0
        ball_y[0] = 100
        dragging[0] = False
        gravity[0] = 9.8
        ball_size[0] = 20
        gravity_label.text = f"Gravity: {gravity[0]} m/s²"
        ball_size_label.text = f"Ball Size: {ball_size[0]}"
    
    def adjust_gravity(amount):
        gravity[0] = max(1, min(30, gravity[0] + amount))
        gravity_label.text = f"Gravity: {gravity[0]} m/s²"
        time[0] = 0  # Reset time to apply new gravity effect
        velocity[0] = 0
    
    def adjust_ball_size(amount):
        ball_size[0] = max(10, min(50, ball_size[0] + amount))
        ball_size_label.text = f"Ball Size: {ball_size[0]}"
    
    window.add_element(Label("Drag and release the ball to drop", WIDTH//2, HEIGHT - 270))
    
    # UI options for gravity and ball size
    gravity_label = Label(f"Gravity: {gravity[0]} m/s²", WIDTH - 180, 80)
    ball_size_label = Label(f"Ball Size: {ball_size[0]}", WIDTH - 180, 140)
    window.add_element(gravity_label)
    window.add_element(ball_size_label)
    
    decrease_gravity_btn = Button("-", WIDTH - 250, 70, 40, 40, lambda: adjust_gravity(-1))
    increase_gravity_btn = Button("+", WIDTH - 110, 70, 40, 40, lambda: adjust_gravity(1))
    decrease_ball_btn = Button("-", WIDTH - 250, 130, 40, 40, lambda: adjust_ball_size(-5))
    increase_ball_btn = Button("+", WIDTH - 110, 130, 40, 40, lambda: adjust_ball_size(5))
    reset_btn = Button("🔄 Reset", WIDTH//2 - 50, HEIGHT - 140, 100, 50, reset)
    back_btn = Button("🔙 Back", 20, HEIGHT - 70, 100, 40, lambda: physics_experiments())
    
    buttons = [decrease_gravity_btn, increase_gravity_btn, decrease_ball_btn, increase_ball_btn, reset_btn, back_btn]
    for button in buttons:
        window.add_element(button)
    
    while running:
        window.screen.fill((245, 245, 245))
        pygame.draw.circle(window.screen, (255, 0, 0), (WIDTH//2, int(ball_y[0])), ball_size[0])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if math.sqrt((mouse_x - WIDTH//2) ** 2 + (mouse_y - ball_y[0]) ** 2) <= ball_size[0]:
                    dragging[0] = True
                for button in buttons:
                    if button.is_hovered((mouse_x, mouse_y)):
                        button.on_click()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging[0] = False
                time[0] = 0  # Reset time to start fall from release point
            elif event.type == pygame.MOUSEMOTION and dragging[0]:
                ball_y[0] = event.pos[1]
                velocity[0] = 0
                time[0] = 0
                
        if not dragging[0] and ball_y[0] < HEIGHT - 100:
            time[0] += 0.1
            velocity[0] = gravity[0] * time[0]
            ball_y[0] += velocity[0] * 0.1
        
        gravity_label.draw(window.screen)
        ball_size_label.draw(window.screen)
        
        for button in buttons:
            button.draw(window.screen)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

def physics_experiments():
    window = Window("Physics Lab")
    window.add_element(Label("Choose a Physics Experiment", WIDTH//2, 50))
    window.add_element(Button("⚙️ Free Fall", WIDTH//2 - 90, 200, 180, 50, free_fall_experiment))
    window.add_element(Button("🔙 Back", 20, HEIGHT - 70, 100, 40, lambda: menu()))
    window.run()

if __name__ == "__main__":
    physics_experiments()
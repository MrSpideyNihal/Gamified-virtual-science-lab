from ui import Window, Label, Button, WIDTH, HEIGHT
import pygame
import math

# ------------------------------
# Physics Experiments
# ------------------------------
def free_fall_experiment():
    window = Window("Free Fall Experiment")
    window.add_element(Label("Free Fall Simulation", WIDTH//2, 50))
    
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
        time[0] = 0
        velocity[0] = 0
    
    def adjust_ball_size(amount):
        ball_size[0] = max(10, min(50, ball_size[0] + amount))
        ball_size_label.text = f"Ball Size: {ball_size[0]}"
    
    window.add_element(Label("Drag and release the ball to drop", WIDTH//2, HEIGHT - 270))
    
    gravity_label = Label(f"Gravity: {gravity[0]} m/s²", WIDTH - 180, 80)
    ball_size_label = Label(f"Ball Size: {ball_size[0]}", WIDTH - 180, 140)
    window.add_element(gravity_label)
    window.add_element(ball_size_label)
    
    decrease_gravity_btn = Button("-", WIDTH - 250, 70, 40, 40, lambda: adjust_gravity(-1))
    increase_gravity_btn = Button("+", WIDTH - 110, 70, 40, 40, lambda: adjust_gravity(1))
    decrease_ball_btn = Button("-", WIDTH - 250, 130, 40, 40, lambda: adjust_ball_size(-5))
    increase_ball_btn = Button("+", WIDTH - 110, 130, 40, 40, lambda: adjust_ball_size(5))
    reset_btn = Button("Reset", WIDTH//2 - 50, HEIGHT - 140, 100, 50, reset)
    back_btn = Button("Back", 20, HEIGHT - 70, 100, 40, lambda: physics_experiments())
    
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
                time[0] = 0
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
    window.add_element(Button("Free Fall", WIDTH//2 - 90, 150, 180, 50, free_fall_experiment))
    window.add_element(Button("Electrical Circuit", WIDTH//2 - 90, 220, 180, 50, electrical_circuit_experiment))
    window.add_element(Button("Pendulum Motion", WIDTH//2 - 90, 290, 180, 50, pendulum_experiment))
    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, lambda: menu()))
    window.run()

def electrical_circuit_experiment():
    window = Window("Electrical Circuit Experiment")
    window.add_element(Label("Simple Circuit Simulation", WIDTH//2, 50))
    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, lambda: physics_experiments()))
    window.run()

def pendulum_experiment():
    window = Window("Pendulum Motion Experiment")
    window.add_element(Label("Pendulum Simulation", WIDTH//2, 50))
    window.add_element(Button("Back", 20, HEIGHT - 70, 100, 40, lambda: physics_experiments()))

    # Pendulum parameters (example values - adjust as needed)
    pendulum_length = 200  # Length of the pendulum arm
    pendulum_bob_radius = 20 # Radius of the pendulum bob
    pendulum_angle = 45     # Initial angle in degrees
    gravity = 9.8           # Acceleration due to gravity
    damping = 0.99          # Damping factor to reduce swing over time

    # Convert angle to radians
    pendulum_angle_rad = math.radians(pendulum_angle)

    # Function to update pendulum position
    def update_pendulum():
        nonlocal pendulum_angle_rad, pendulum_angle
        # Calculate acceleration (angular)
        angular_acceleration = -gravity / pendulum_length * math.sin(pendulum_angle_rad)

        # Update angle and angular velocity
        pendulum_angle_rad += angular_acceleration * 0.1 #dt = 0.1
        #Convert back to degrees
        pendulum_angle = math.degrees(pendulum_angle_rad)
        # Apply damping to slow down the pendulum
        pendulum_angle_rad *= damping

    # Main loop for the pendulum experiment
    running = True
    clock = pygame.time.Clock()

    while running:
        window.screen.fill((245, 245, 245))  # Clear the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        # Update pendulum position
        update_pendulum()

        # Calculate bob position
        bob_x = WIDTH // 2 + pendulum_length * math.sin(pendulum_angle_rad)
        bob_y = HEIGHT // 2 + pendulum_length * math.cos(pendulum_angle_rad)

        # Draw pendulum arm and bob
        pygame.draw.line(window.screen, (0, 0, 0), (WIDTH // 2, HEIGHT // 2), (bob_x, bob_y), 2)
        pygame.draw.circle(window.screen, (0, 0, 255), (int(bob_x), int(bob_y)), pendulum_bob_radius)

        # Draw UI elements
        for element in window.elements:
            element.draw(window.screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    physics_experiments()
import pygame
import socket
import json
import time

# === Configuration ===
LAPTOP_IP = '192.168.x.x'  # <-- replace with your laptop IP
PORT = 5050
DISPLAY_DURATION = 1.0  # seconds to show key pressed on screen

# === Network Setup ===
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((LAPTOP_IP, PORT))

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Phone Keyboard Sender')
font = pygame.font.SysFont(None, 64)
clock = pygame.time.Clock()

# === State ===
last_key = None
last_time = 0

running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    # Show last key pressed
    if last_key and time.time() - last_time < DISPLAY_DURATION:
        key_surface = font.render(last_key, True, (255, 255, 255))
        rect = key_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(key_surface, rect)
    else:
        last_key = None  # Clear the display if time passed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key_name = pygame.key.name(event.key)
            action = 'down' if event.type == pygame.KEYDOWN else 'up'

            # Send key event
            try:
                message = json.dumps({'key': key_name, 'action': action})
                sock.sendall(message.encode())
            except:
                print("Connection lost!")
                running = False

            if action == 'down':
                last_key = key_name
                last_time = time.time()

    pygame.display.flip()
    clock.tick(60)

# === Cleanup ===
pygame.quit()
sock.close()

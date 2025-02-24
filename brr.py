import pygame
from networktables import NetworkTables
import time

pygame.init()
pygame.joystick.init()

NetworkTables.initialize(server="127.0.0.1")
table = NetworkTables.getTable("Testing")

joysticks = []

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Initialized joystick {i}: {joystick.get_name()}")

if not joysticks:
    print("No joysticks")
    exit(1)

previous_value = False

def value_changed(table, key, value, is_new):
    global previous_value
    
    print(f"[PYTHON] Received {key} = {value}")
    
    if value and not previous_value:
        print("Going Brr")
        for joystick in joysticks:
            try:
                joystick.rumble(1.0, 1.0, 1000)  
            except Exception as e:
                print(f"Error rumbling {joystick.get_name()}: {e}")
        
    previous_value = value

table.addEntryListener(
    value_changed,
    immediateNotify=True,
    key="IsHeld"
)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Exiting")
finally:
    pygame.quit()

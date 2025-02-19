import pygame
from networktables import NetworkTables
import time

pygame.init()
pygame.joystick.init()

NetworkTables.initialize(server="127.0.0.1")
table = NetworkTables.getTable("Testing")

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Initialized joystick: {joystick.get_name()}")
else:
    print("No joystick found!")
    exit(1)

previous_value = False

def value_changed(table, key, value, is_new):
    global previous_value
    
    print(f"[PYTHON] Received {key} = {value}")
    
    if value and not previous_value:
        print("Triggering rumble!")
        joystick.rumble(1.0, 1.0, 1000)  
        
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
    print("Exiting...")
finally:
    pygame.quit()

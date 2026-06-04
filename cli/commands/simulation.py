# here we manage the simulation either
# simulation start -> starts and sets up all the pins according to the settings/GPIOPins.txt file and enables moving with
# simulation move [position] -> moves the arm to the specified position (back right, front left, etc.)
# simulation stop -> stops the simulation and resets all pins to 0

# we can use enums for positions maybe idk

from registry import register
from mechanisms.TrashController import TrashController

# we need a way of sotring wether the trashcontroller exist or not to be able to maipulate but the way the code currently work is not just OOP the controler is but no this command so
# we can use a global variable to store the controller instance and check if it exists before trying to move it
trash_controller = None

@register('simulation')
def simulation(args):
    if not args:
        print("Usage: simulation <start|move|stop> [position]")
        return
    
    action = args[0].lower()

    if action == 'start':
        start_sim()
    elif action == 'move' and len(args) >= 2 and trash_controller is not None:
        if len(args) < 2:
            print("Usage: simulation move <position>")
            return
        position = args[1].lower()
        move_to_position(position)
    elif action == 'stop':
        print("Stopping simulation...")
        # Clean up the simulation environment here
    elif action == 'move' and trash_controller is None:
        print("Simulation not started. Please run 'simulation start' first.")
    elif action == 'move' and len(args) < 2:
        print("Usage: simulation move <position>")
    else:
        print(f"Unknown action: {action}")

def start_sim():
    print("Starting simulation...")
    # extract gpio pings
    # set up the pins according to the settings/GPIOPins.txt file
    # initialize the TrashController with the appropriate pins
    # format is per line 'arm1=14'
    # we can use a dict to store the pin numbers
    # example: pins = {'arm1': 14, 'arm2': 15, 'pivot': 16}
    pins = {}
    with open('settings/GPIOPins.txt') as f:
        for line in f:
            key, value = line.strip().split('=')
            pins[key] = int(value)
    print(f"Extracted pins: {pins}")
    
    global trash_controller 
    trash_controller = TrashController(pins['arm1'], pins['arm2'], pins['pivot'], debug=True)  # Set debug to True to avoid actual servo movement during testing
    trash_controller.calibrate()

def move_to_position(position):
    print(f"Moving to position: {position}")
    if position == 'back_right':
        trash_controller.move_back_right()
    elif position == 'front_left':
        trash_controller.move_front_left()
    else:
        print(f"Unknown position: {position}")
  
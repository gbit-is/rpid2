from random import randrange


default_joystick_deadzone=20

def calculate_motors(direction,turn,deadzone=default_joystick_deadzone):

    def check_deadzone(value,threshold):
        if abs(value) < threshold:
            return 0
        else:
            return value

	
    direction = check_deadzone(direction, deadzone)
    turn = check_deadzone(turn, deadzone)

    left_motor = direction + turn
    right_motor = direction - turn

    left_motor = max(-256, min(256, left_motor))
    right_motor = max(-256, min(256, right_motor))

    return left_motor, right_motor

def test_formula():

    print("Dir".ljust(10),"Turn".ljust(10),"M1".ljust(10),"m2".ljust(10))

    for i in range(15):

        a = randrange(-256,256)
        b = randrange(-256,256)

        c,d = calculate_motors(a,b)
        
        for i in a,b,c,d:
            print(str(i).ljust(10),end="")

        print()
        
        
test_formula()

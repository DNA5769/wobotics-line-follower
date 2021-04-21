"""Controller for our Robot"""
__author__ = "Neeraj Chatterjee and Dennis Thomas" 

from controller import Robot

# Created instance of Robot class which will help us interact with the environment
robot = Robot()

timestep = 32
max_speed = 10
max_ir = 1000

# Setting up indentifiers for our motors
right_motor = robot.getDevice('motor1')
left_motor = robot.getDevice('motor2')

# Setting up indentifiers for our infrared sensors
# left, straight and right ir will be used to detect the line the robot has to follow
# top ir will be used in detecting if we have reached the END or not
straight_ir = robot.getDevice('ir0')
left_ir = robot.getDevice('ir1')
right_ir = robot.getDevice('ir2')
top_ir = robot.getDevice('ir3')

# We are going to use flag variable to check if the robot has reached the end or not
flag = False

# Even if we reached the end, we want the robot to move a bit forward so that it sits nicely
# in the centre of the END box. So we will use counter to setup a pseudo loop, so that it
# moves for a "while"
counter = 13

# We are going to be using the IR sensors to check for the path. Now if the reading of the
# IR sensor is greater than limit variable, it means that there is a black line i.e path in
# front of the sensor 
limit = max_ir//2

# We will keep track of the left motor speed and right motor speed in dictionary called
# state. As the robot runs, we will be making changes to state, depending on the IR sensor
# values
state = {
    'left_speed': 0.0,
    'right_speed': 0.0
}

def dispatch(state, action):
    """Function to make changes in the state

    Parameters
    ----------
    state : dict
        A reference to the state to which we want to make a change on
    action : dict
        A dict which will have a 'type' key which will tell the function
        what changes are to be made on the state
    """
    if action['type'] == 'L': # Move Left
        state['left_speed'] = 0.0
        state['right_speed'] = max_speed
        print("Left")
    elif action['type'] == 'S': # Move Straight
        state['left_speed'] = max_speed
        state['right_speed'] = max_speed
        print("Straight")
    elif action['type'] == 'R': # Move Right
        state['left_speed'] = max_speed
        state['right_speed'] = 0.0
        print("Right")
    elif action['type'] == 'B': # Move Back
        state['left_speed'] = -max_speed
        state['right_speed'] = max_speed
        print("Back")
    elif action['type'] == 'STOP': # Move NOT
        state['left_speed'] = 0.0
        state['right_speed'] = 0.0
        print("WOOHOO!")
    else:
        pass

# void main()
if __name__ == "__main__":
	# Setting up the positions to infinity and velocity to 0.0 for the
	# left and right motors
    for motor in [left_motor, right_motor]:
        motor.setPosition(float('inf'))
        motor.setVelocity(0.0)
    
    # Setting up the infrared sensors by enabling them
    for ir in [left_ir, straight_ir, right_ir, top_ir]:
        ir.enable(timestep)
    
    # Robot loop
    # Important thing to note here is the robot loop not only depends on the robot
    # but also depends on counter. So once our pseudo loop finishes the controller stops
    while robot.step(timestep) != -1 and counter:
    	# If the ir sensor of a particular direction has a greater value than limit
    	# that means it will be True or in other words, we can move to that direction.
    	# Note: straight, left anf right are Boolean (True/False) variables
        straight = straight_ir.getValue()>limit
        left = left_ir.getValue()>limit
        right = right_ir.getValue()>limit

        # To check if we have reached the end or not
        # If you check the robot setup, you will see that this sensor is very far away from the
        # ground which results in it giving high values even if the ground is white. That's why
        # this is True only if it gives maximum ir output
        top = top_ir.getValue()==max_ir

        # If top, left, right and straight are all True, then that means we have reached the end
        # and hence we set the flag variable to True which will start our pseudo loop
        if top and left and right and straight:
            flag = True

        # We are following the LSRB algorithm, so the order in which the
        # direction are compared is very important
        if flag:
        	# Now if we reached the end, there are two decisions we can make
        	# If counter == 1, that means our pseudo loop is over and we have to STOP
        	# else, pseudo loop isn't over so we keep moving forward
            dispatch(state, { 'type': ['S', 'STOP'][counter==1] })
        elif left:
            dispatch(state, { 'type': 'L' })
        elif straight:
            dispatch(state, { 'type': 'S' })
        elif right:
            dispatch(state, { 'type': 'R' })
        else:
            dispatch(state, { 'type': 'B' })

        # Mostly for debugging purposes but helps us to see the values of each IR sensor in the console
        if counter != 1: print(f'Left: {left_ir.getValue()} Straight: {straight_ir.getValue()} Right: {right_ir.getValue()} Top: {top_ir.getValue()}')
        
        # Setting the speed of the left and right motor from our state
        left_motor.setVelocity(state['left_speed'])
        right_motor.setVelocity(state['right_speed'])

        # Implementing the pseudo loop IF we have reached the end
        if flag: counter -= 1

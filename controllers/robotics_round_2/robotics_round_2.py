from controller import Robot

robot = Robot()

timestep = 32
max_speed = 6.28

# Getting identifiers for our left and right motor
right_motor = robot.getDevice('motor1')
left_motor = robot.getDevice('motor2')

# Getting identifiers for our left, straight and
# right infrared sensors
straight_ir = robot.getDevice('ir0')
left_ir = robot.getDevice('ir1')
right_ir = robot.getDevice('ir2')

if __name__ == "__main__":
    # Setting positions of both of our
    # motors to infinity i.e we want the
    # motor to keep rotating endlessly
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    
    # Setting velocties of both of our
    # motors to 0 i.e we want our motors
    # to start at rest
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    # Enabling our infrared sensors so
    # that we can take readings from them
    straight_ir.enable(timestep)
    left_ir.enable(timestep)
    right_ir.enable(timestep)
    
    while robot.step(timestep) != -1:
        # Checking if there is a path in
        # the straight, left and right direction.
        # We first define a limit and check if the
        # infrared sensor for a direction gives a 
        # value higher than the limit
        limit = 500
        straight = straight_ir.getValue() > limit
        left = left_ir.getValue() > limit
        right = right_ir.getValue() > limit
        
        # Implementing LSRB algorithm
        # We decide the left and right motor speed
        # depending on which direction we want to
        # go based on the LSRB algorithm
        if left:
            left_speed = 0
            right_speed = max_speed
            print("Left")
        elif straight:
            left_speed = max_speed
            right_speed = max_speed
            print("Straight")
        elif right:
            left_speed = max_speed
            right_speed = 0
            print("Right")
        else:
            left_speed = 0
            right_speed = max_speed
            print("Back")

        print(f'Left: {left_ir.getValue()} Straight: {straight_ir.getValue()} Right: {right_ir.getValue()}')
        
        # Setting the left and right motor speed
        # to the ones we decided earlier
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

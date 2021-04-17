from controller import Robot

robot = Robot()

timestep = 32
max_speed = 6.28

right_motor = robot.getDevice('motor1')
left_motor = robot.getDevice('motor2')

straight_ir = robot.getDevice('ir0')
left_ir = robot.getDevice('ir1')
right_ir = robot.getDevice('ir2')

if __name__ == "__main__":
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    straight_ir.enable(timestep)
    left_ir.enable(timestep)
    right_ir.enable(timestep)
    
    while robot.step(timestep) != -1:
        limit = 500
        straight = straight_ir.getValue()>limit
        left = left_ir.getValue()>limit
        right = right_ir.getValue()>limit
        
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
    
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

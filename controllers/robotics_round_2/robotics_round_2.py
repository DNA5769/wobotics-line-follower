from controller import Robot

robot = Robot()

timestep = 32
max_speed = 6.28

left_motor = robot.getDevice('motor1')
right_motor = robot.getDevice('motor2')

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
        straight_ir_value = straight_ir.getValue()
        left_ir_value = left_ir.getValue()
        right_ir_value = right_ir.getValue()
        
        print("Left: {} Straight: {} Right: {}".format(left_ir_value,straight_ir_value,right_ir_value))

        left_motor.setVelocity(max_speed*0.5)
        right_motor.setVelocity(max_speed*0.5)

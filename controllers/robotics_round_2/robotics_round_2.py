"""my_first_lfr controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

if __name__ == "__main__":

    # create the Robot instance.
    robot = Robot()
    
    # get the time step of the current world.
    timestep = 32
    max_speed = 6.28
    
    left_motor = robot.getDevice('motor1')
    right_motor = robot.getDevice('motor2')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    left_ir = robot.getDistanceSensor('ir1')
    left_ir.enable(timestep)
    right_ir = robot.getDistanceSensor('ir2')
    right_ir.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    left_ir_value = left_ir.getValue()
    right_ir_value = right_ir.getValue()
    print("Left: {} right: {}".format(left_ir_value,right_ir_value))
    left_speed = max_speed*0.25
    right_speed = max_speed*0.25
    if(left_ir_value > right_ir_value) and (6<left_ir_value<15):
        print("Go Left")
        left_speed = -max_speed*0.25
    elif(left_ir_value < right_ir_value) and (6<right_ir_value<15):
        print("Go Right")
        right_speed = -max_speed*0.25
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

# Enter here exit cleanup code.

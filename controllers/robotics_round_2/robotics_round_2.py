from controller import Robot

robot = Robot()

timestep = 32
max_speed = 6.28

right_motor = robot.getDevice('motor1')
left_motor = robot.getDevice('motor2')

straight_ir = robot.getDevice('ir0')
left_ir = robot.getDevice('ir1')
right_ir = robot.getDevice('ir2')
top_ir = robot.getDevice('ir3')

flag = False

counter = 25

limit = 500

state = {
    'left_speed': 0.0,
    'right_speed': 0.0
}

def dispatch(state, action):
    if action['type'] == 'L':
        state['left_speed'] = 0.0
        state['right_speed'] = max_speed
        print("Left")
    elif action['type'] == 'S':
        state['left_speed'] = max_speed
        state['right_speed'] = max_speed
        print("Straight")
    elif action['type'] == 'R':
        state['left_speed'] = max_speed
        state['right_speed'] = 0.0
        print("Right")
    elif action['type'] == 'B':
        state['left_speed'] = -max_speed
        state['right_speed'] = max_speed
        print("Back")
    elif action['type'] == 'STOP':
        state['left_speed'] = 0.0
        state['right_speed'] = 0.0
        print("WOOHOO!")
    else:
        pass

if __name__ == "__main__":
    for motor in [left_motor, right_motor]:
        motor.setPosition(float('inf'))
        motor.setVelocity(0.0)
    
    for ir in [left_ir, straight_ir, right_ir, top_ir]:
        ir.enable(timestep)
    
    while robot.step(timestep) != -1 and counter:
        straight = straight_ir.getValue()>limit
        left = left_ir.getValue()>limit
        right = right_ir.getValue()>limit

        top = top_ir.getValue()==1000

        if top and left and right and straight:
            flag = True

        if flag:
            dispatch(state, { 'type': ['S', 'STOP'][counter==1] })
        elif left:
            dispatch(state, { 'type': 'L' })
        elif straight:
            dispatch(state, { 'type': 'S' })
        elif right:
            dispatch(state, { 'type': 'R' })
        else:
            dispatch(state, { 'type': 'B' })

        if counter != 0: print(f'Left: {left_ir.getValue()} Straight: {straight_ir.getValue()} Right: {right_ir.getValue()} Top: {top_ir.getValue()}')
        
        left_motor.setVelocity(state['left_speed'])
        right_motor.setVelocity(state['right_speed'])

        if flag: counter -= 1

import logging

from p3.pad import Button, Trigger, Stick
from p3.ddq import Decider

ZERO = 0.0000001
BUTTONS = {
    Button.A: 0,
    Button.B: 1,
    Button.X: 2,
    Button.Y: 3,
    Button.Z: 4,
    Button.L: 5,
    Button.R: 6,
    Button.D_UP: 7,
    Button.D_DOWN: 8,
    Button.D_LEFT: 9,
    Button.D_RIGHT: 10,
}
TRIGGERS = {
    Trigger.L: 11,
    Trigger.R: 12,
}
STICKS = {
    Stick.MAIN: 13,
    Stick.C: 15,
}

class Fox:
    def __init__(self, pad):
        self.pad = pad
        self.action_list = []
        self.last_action = 0
        self.decider = Decider([])
        self.key_pressed = dict()

    def advance(self, sess, state):
        while self.action_list:
            wait, func, args = self.action_list[0]
            if state.frame - self.last_action < wait:
                return
            else:
                self.action_list.pop(0)
                if func is not None:
                    func(*args)
                self.last_action = state.frame
        else:
            self.apply(self.decider.act(sess, self.state_to_observation(state)))

    def apply(self, action):
        for stick, i in STICKS.items():
            self.action_list.append((0, self.pad.tilt_stick, [stick, action[i], action[i+1]]))

        for trigger, i in TRIGGERS.items():
            if action[i] > ZERO:
                self.action_list.append((0, self.pad.press_trigger, [trigger, action[i]]))

        for button, i in BUTTONS.items():
            if action[i] > ZERO:
                print("press: %s" % (button))
                self.action_list.append((0, self.pad.press_button, [button]))

        self.action_list.append((int(action[17]*30+15), None, []))

        for button, i in BUTTONS.items():
            if action[i] > ZERO:
                self.action_list.append((0, self.pad.release_button, [button]))

        self.action_list.append((int(action[18]*30+15), None, []))

    def state_to_observation(self, state):
        pass

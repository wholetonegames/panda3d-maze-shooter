from panda3d.core import InputDevice


class ConfigControls:
    TYPE_KEYBOARD = 1
    TYPE_GAMEPAD = 2

    def __init__(self):
        self.gamepad = None
        self.axis_threshold = 0.5
        self.axis_threshold_negative = 0 - self.axis_threshold
        self.control_type = self.TYPE_KEYBOARD
        self.controlList = [
            # TYPE_KEYBOARD
            ["arrow_left", self.setDirection,  [
                "left", True], self.TYPE_KEYBOARD, "Arrow Left"],
            ["arrow_right", self.setDirection, [
                "right", True], self.TYPE_KEYBOARD, "Arrow Right"],
            ["arrow_up", self.setDirection,    [
                "up", True], self.TYPE_KEYBOARD, "Arrow Up"],
            ["arrow_down", self.setDirection,  [
                "down", True], self.TYPE_KEYBOARD, "Arrow Down"],
            ["arrow_left-up", self.setDirection,
                ["left", False], self.TYPE_KEYBOARD, None],
            ["arrow_right-up", self.setDirection,
                ["right", False], self.TYPE_KEYBOARD, None],
            ["arrow_up-up", self.setDirection,
                ["up", False], self.TYPE_KEYBOARD, None],
            ["arrow_down-up", self.setDirection,
                ["down", False], self.TYPE_KEYBOARD, None],
            ["space", self.setCommand,  ["confirm", True],
                self.TYPE_KEYBOARD, "Spacebar"],
            ["space-up", self.setCommand,  ["confirm", False],
                self.TYPE_KEYBOARD, None],
            ["enter", self.setCommand,  ["confirm", True],
                self.TYPE_KEYBOARD, "Enter"],
            ["enter-up", self.setCommand,  ["confirm", False],
                self.TYPE_KEYBOARD, None],
            ["z", self.setCommand,  ["cancel", True], self.TYPE_KEYBOARD, "Z Key"],
            ["z-up", self.setCommand,  ["cancel", False], self.TYPE_KEYBOARD, None],
            ["x", self.setCommand,  ["confirm", True], self.TYPE_KEYBOARD, "X Key"],
            ["x-up", self.setCommand,  ["confirm", False], self.TYPE_KEYBOARD, None],
            ["escape", self.setCommand,  ["cancel", True],
                self.TYPE_KEYBOARD, "Escape"],
            ["escape-up", self.setCommand,
                ["cancel", False], self.TYPE_KEYBOARD, None],
            ["backspace", self.setCommand,  ["cancel", True],
                self.TYPE_KEYBOARD, "Backspace"],
            ["backspace-up", self.setCommand,
                ["cancel", False], self.TYPE_KEYBOARD, None],
            # TYPE_GAMEPAD
            ["gamepad-dpad_right", self.setDirection,
                ["right", True], self.TYPE_GAMEPAD, "D-pad Right"],
            ["gamepad-dpad_right-up", self.setDirection,
                ["right", False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_left", self.setDirection,
                ["left", True], self.TYPE_GAMEPAD, "D-pad Left"],
            ["gamepad-dpad_left-up", self.setDirection,
                ["left", False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_up", self.setDirection,
                ["up", True], self.TYPE_GAMEPAD, "D-pad Up"],
            ["gamepad-dpad_up-up", self.setDirection,
                ["up", False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_down", self.setDirection,
                ["down", True], self.TYPE_GAMEPAD, "D-pad Down"],
            ["gamepad-dpad_down-up", self.setDirection,
                ["down", False], self.TYPE_GAMEPAD, None],
            ["gamepad-face_a", self.setCommand,
                ["confirm", True], self.TYPE_GAMEPAD, "A Button"],
            ["gamepad-face_a-up", self.setCommand,
                ["confirm", False], self.TYPE_GAMEPAD, None],
            ["gamepad-face_b", self.setCommand,
                ["cancel", True], self.TYPE_GAMEPAD, "B Button"],
            ["gamepad-face_b-up", self.setCommand,
                ["cancel", False], self.TYPE_GAMEPAD, None],
        ]
        self.initController()
        self.resetButtons()

    def initController(self):
        self.disableController()

        for control in self.controlList:
            base.accept(control[0], control[1], control[2])

        # Accept device dis-/connection events
        base.accept("connect-device", self.connect)
        base.accept("disconnect-device", self.disconnect)

    def connect(self, device):
        # gamepads = base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            self.gamepad = device
            base.attachInputDevice(device, prefix="gamepad")
            self.control_type = self.TYPE_GAMEPAD

    def disconnect(self, device):
        if self.gamepad != device:
            return
        base.detachInputDevice(device)
        self.gamepad = None
        self.control_type = self.TYPE_KEYBOARD

    def resetButtons(self):
        self.directionMap = {"left": False,
                             "right": False, "down": False, "up": False}
        self.commandMap = {"confirm": False, "cancel": False}

    def setDirection(self, key, value):
        self.directionMap[key] = value

    def setCommand(self, key, value):
        self.commandMap[key] = value

    def anyCommand(self):
        for key in self.commandMap:
            if self.commandMap[key]:
                return True
        return False

    def disableController(self):
        self.resetButtons()

        base.ignore("connect-device")
        base.ignore("disconnect-device")

        for control in self.controlList:
            base.ignore(control[0])

    def read_axis_left(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}

        left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
        left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
        return {'x': left_x.value, 'y': left_y.value}

    def read_axis_right(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}
        right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
        right_y = self.gamepad.findAxis(InputDevice.Axis.right_y)
        return {'x': right_x.value, 'y': right_y.value}

    def move_from_axis(self, is_left_axis):
        axis_obj = self.read_axis_left() if is_left_axis else self.read_axis_right()
        if axis_obj['x'] <= self.axis_threshold_negative:
            self.setDirection('left', True)
        else:
            self.setDirection('left', False)
        if axis_obj['x'] >= self.axis_threshold:
            self.setDirection('right', True)
        else:
            self.setDirection('right', False)

        if axis_obj['y'] <= self.axis_threshold_negative:
            self.setDirection('down', True)
        else:
            self.setDirection('down', False)
        if axis_obj['y'] >= self.axis_threshold:
            self.setDirection('up', True)
        else:
            self.setDirection('up', False)

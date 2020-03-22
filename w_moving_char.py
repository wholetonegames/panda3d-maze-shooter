from i_moving_char import FiringCharacter
from panda3d.core import TransparencyAttrib


class MovingCharacter(FiringCharacter):
    TASK_INITIAL_TIME = 2.0
    TASK_CHANGE_TIME = 8.5
    TASK_CHANGE_NAME = 'randomStateChange'

    def __init__(self, stage, indexNumber):
        FiringCharacter.__init__(self, 1.0)
        self.can_fire = False
        self.indexNumber = indexNumber
        self.stage = stage
        self.name = 'enemy'
        self.speed = 5
        self.direction_index = 0
        self.collision_size = (0, 0, 0.2, 1.0)
        self.taskName = '{}_{}_{}'.format(
            self.TASK_CHANGE_NAME, self.name, self.indexNumber)
        self.initActor()
        taskMgr.doMethodLater(self.TASK_INITIAL_TIME,
                              self.initState, 'init' + self.taskName)

    def initActor(self):
        faEmpty = self.stage.find(
            "**/{}_{}".format(self.name, self.indexNumber))
        faPos = faEmpty.getPos()
        self.loadActor(faPos)
        self.initCollision()

    def initState(self, task):
        self.can_fire = True
        self.randomDirection()
        taskMgr.doMethodLater(self.TASK_CHANGE_TIME,
                              self.taskStateChange, self.taskName)
        return task.done

    def taskStateChange(self, task):
        self.randomDirection()
        return task.again

    def randomDirection(self):
        self.direction_index += 1
        if self.direction_index >= len(self.DIRECTIONS):
            self.direction_index = 0
        self.direction = self.DIRECTIONS[self.direction_index]

    def moveAwayFrom(self, normal):
        x, y, z = normal
        isYLarger = abs(y) > abs(x)
        if isYLarger:
            self.direction = self.WEST if x > 0 else self.EAST
        else:
            self.direction = self.SOUTH if y > 0 else self.NORTH

    def kill(self):
        self.direction = None
        self.can_fire = False
        self.actor.setPos((-10, -10, 0))


class MainCharacter(FiringCharacter):
    def __init__(self, startPos, stage):
        FiringCharacter.__init__(self, 0.3)
        self.hp = 3
        self.indexNumber = 0  # if multiplayer, this will need to be passed on creation
        self.stage = stage
        self.startPos = startPos
        self.name = 'hero'
        self.speed = 5
        self.collision_size = (0, 0, 0.2, 1.0)

        self.initActor()

    def initActor(self):
        self.loadActor(self.startPos)
        self.actor.setTransparency(TransparencyAttrib.MAlpha)
        self.actor.setAlphaScale(1.0)
        self.initCollision()
        self.direction = None

    def flash(self):
        self.can_hurt = False
        taskMgr.add(self.flashing_colour, 'hero_flash')

    def flashing_colour(self, task):
        if task.time < 2.0:
            self.actor.setAlphaScale(task.time % 1.0)
            return task.cont
        self.actor.setAlphaScale(1.0)
        self.can_hurt = True
        return task.done

    def kill(self):
        self.direction = None
        self.can_fire = False
        self.actor.setPos((-10, -10, 0))

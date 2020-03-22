from panda3d.core import (
    CollisionNode,
    CollisionSphere)


class GameCharacter:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    DIRECTIONS = (NORTH, EAST, SOUTH, WEST)

    def __init__(self):
        self.direction = None
        self.actor = None
        self.indexNumber = None
        self.name = None
        self.stage = None
        self.speed = None
        self.clamp_on_ground = False
        self.collision_size = [0, 0, 0, 0]

    def updatePos(self, dt):
        x, y, z = self.actor.getPos(render)
        z = 0 if self.clamp_on_ground else z
        speed = self.speed * dt

        if self.direction == self.NORTH:
            self.actor.setY(y+speed)
            self.actor.setHpr(180, 0, 0)
        elif self.direction == self.SOUTH:
            self.actor.setY(y-speed)
            self.actor.setHpr(0, 0, 0)
        elif self.direction == self.EAST:
            self.actor.setX(x+speed)
            self.actor.setHpr(90, 0, 0)
        elif self.direction == self.WEST:
            self.actor.setX(x-speed)
            self.actor.setHpr(-90, 0, 0)
        self.actor.setZ(z)

    def loadActor(self, pos):
        self.actor = loader.loadModel(self.name)
        self.actor.reparentTo(self.stage)
        self.actor.setPos(pos)

    def initCollision(self):
        cNode = CollisionNode("{}_{}".format(self.name, self.indexNumber))
        (x, y, z, s) = self.collision_size
        cNode.addSolid(CollisionSphere(x, y, z, s))
        faCollision = self.actor.attachNewNode(cNode)
        base.pusher.addCollider(
            faCollision, self.actor, base.drive.node())
        base.cTrav.addCollider(faCollision, base.pusher)


class HealthCharacter(GameCharacter):
    def __init__(self):
        GameCharacter.__init__(self)
        self.clamp_on_ground = True
        self.hp = 1
        self.can_hurt = True

    def decrement_hp(self):
        if not self.can_hurt:
            return
        self.hp -= 1
        if self.is_ko:
            self.kill()
        else:
            self.flash()

    @property
    def is_ko(self):
        return self.hp <= 0

    def kill(self):
        pass

    def flash(self):
        pass


class FiringCharacter(HealthCharacter):
    def __init__(self, fire_later_time):
        HealthCharacter.__init__(self)
        self.can_fire = True
        self.fire_later_time = fire_later_time

    def gunPos(self):
        gun = self.actor.find('**/gun')
        # to get global position, call render
        return gun.getPos(render)

    def fire(self):
        self.can_fire = False
        taskMgr.doMethodLater(self.fire_later_time,
                              self.reset_fire, self.name+"_fire")

    def reset_fire(self, task):
        self.can_fire = True
        return task.done

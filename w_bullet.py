from i_moving_char import GameCharacter


class Bullet(GameCharacter):
    def __init__(self, stage, indexNumber, name,  INIT_POS):
        GameCharacter.__init__(self)
        self.name = name
        self.indexNumber = indexNumber
        self.INIT_POS = INIT_POS
        self.stage = stage
        self.speed = 10
        self.collision_size = (0, 0, 0, 0.6)
        self.initActor()

    def initActor(self):
        self.loadActor(self.INIT_POS)
        self.initCollision()

    def fire(self, pos, direction):
        self.direction = direction
        self.actor.setPos(pos)

    def reset(self):
        self.direction = None
        self.actor.setPos(self.INIT_POS)


class BulletHero(Bullet):
    def __init__(self, stage, indexNumber):
        INIT_POS = (indexNumber * 2, 0, 10)
        Bullet.__init__(self, stage, indexNumber, 'bullet_h', INIT_POS)


class BulletEnemy(Bullet):
    def __init__(self, stage, indexNumber):
        INIT_POS = (indexNumber * 2, -2, 10)
        Bullet.__init__(self, stage, indexNumber, 'bullet_e', INIT_POS)

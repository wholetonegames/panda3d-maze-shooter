import abc
from panda3d.core import (
    CollisionHandlerPusher,
    CollisionNode,
    CollisionSphere,
    CollisionBox)
# from w_gui_dialog import GUIDialog
from w_grid import StageGrid
from w_moving_char import MovingCharacter, MainCharacter
from w_bullet import BulletEnemy, BulletHero


class IStage(metaclass=abc.ABCMeta):
    MAX_BULLET = 15

    def __init__(self):
        # self.dialogBox = GUIDialog()
        self.init_vars()

    def init_vars(self):
        self.stage = None
        self.enemyActors = []
        self.npcActors = []
        self.hero_bullets = []
        self.enemy_bullets = []
        self.hero_bullet_index = 0
        self.enemy_bullet_index = 0

    def initStage(self):
        if self.stage:
            self.stage.removeNode()
        this_map = base.mapData.maps[base.gameData.currentMap]
        self.stage = loader.loadModel(this_map['model'])
        self.stage_grid = StageGrid(
            this_map['pattern'], self.stage, this_map['blockTypes'])
        self.stage.reparentTo(render)
        self.controlCamera()
        self.stage.hide()

    def controlCamera(self):
        camPos = self.stage.find('**/camPos').getPos()
        camFocus = self.stage.find('**/camFocus').getPos()
        base.cam.setPos(camPos)
        base.cam.lookAt(camFocus)

        base.sunNp.setPos(-4, -34, 50)
        base.sunNp.lookAt(camFocus)

    def initEnemy(self):
        this_map = base.mapData.maps[base.gameData.currentMap]
        enemyNumber = this_map["enemyNumber"]
        if enemyNumber <= 0:
            return
        self.enemyActors = []
        for enemyIndex in list(range(0, enemyNumber)):
            e = MovingCharacter(self.stage, enemyIndex)
            self.enemyActors.append(e)

    def initPlayer(self):
        startPos = self.stage_grid.startPosList[0]
        self.player = MainCharacter(startPos, self.stage)

    def initBullet(self):
        # create an object pool here
        for i in list(range(0, self.MAX_BULLET)):
            b = BulletHero(self.stage, i)
            self.hero_bullets.append(b)
            b = BulletEnemy(self.stage, i)
            self.enemy_bullets.append(b)

    def setup(self):
        self.init_vars()
        self.initStage()
        self.initPlayer()
        self.initEnemy()
        self.initBullet()

    def setCollision(self):
        inEvent = "into"
        base.pusher.addInPattern(inEvent)
        base.accept(inEvent, self.intoEvent)

        againEvent = "again"
        base.pusher.addAgainPattern(againEvent)
        base.accept(againEvent, self.againEvent)

    def changeMap(self):
        base.callLoadingScreen()
        self.resetMap()

    def resetMap(self):
        self.setup()
        self.start()
        base.initController()

    def enemy_fire(self, e):
        g = e.gunPos()
        e.fire()
        if self.enemy_bullet_index >= self.MAX_BULLET:
            self.enemy_bullet_index = 0
        self.enemy_bullets[self.enemy_bullet_index].fire(g, e.direction)
        self.enemy_bullet_index += 1

    def aiUpdate(self, task):
        dt = globalClock.getDt()
        for e in self.enemyActors:
            if e.is_ko:
                continue
            e.updatePos(dt)
            if e.can_fire:
                self.enemy_fire(e)
        for b in (self.hero_bullets + self.enemy_bullets):
            if not b.direction:
                continue
            b.updatePos(dt)
        self.check_if_game_over()
        return task.cont

    def check_if_game_over(self):
        all_enemies_ko = all(x.is_ko for x in self.enemyActors)
        if self.player.is_ko or all_enemies_ko:
            taskMgr.doMethodLater(1.0, base.messenger.send, 'callGameOver', extraArgs=['Menu-GameOver'])

    def readDirection(self, p):
        if base.directionMap["left"]:
            p.direction = p.WEST
        elif base.directionMap["right"]:
            p.direction = p.EAST
        elif base.directionMap["up"]:
            p.direction = p.NORTH
        elif base.directionMap["down"]:
            p.direction = p.SOUTH

    def readCommand(self, p):
        if base.commandMap["confirm"] and p.can_fire:
            g = p.gunPos()
            p.fire()
            if self.hero_bullet_index >= self.MAX_BULLET:
                self.hero_bullet_index = 0
            self.hero_bullets[self.hero_bullet_index].fire(g, p.direction)
            self.hero_bullet_index += 1
        elif base.commandMap["cancel"]:
            self.cancelCommand()

    def readKeys(self, task):
        if self.player.is_ko:
            return
        self.readCommand(self.player)
        self.readDirection(self.player)
        dt = globalClock.getDt()
        self.player.updatePos(dt)
        return task.cont

    def start(self):
        render.setLight(base.alnp)
        render.setLight(base.sunNp)
        self.stage.show()
        taskMgr.add(self.aiUpdate, "AIUpdate")
        taskMgr.add(self.readKeys, "readKeys")

    def stop(self):
        taskMgr.remove("AIUpdate")
        taskMgr.remove("readKeys")

    def quit(self):
        self.stage.removeNode()

    @abc.abstractmethod
    def cancelCommand(self):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def intoEvent(self, entry):
        raise NotImplementedError('subclass must define this method')

    @abc.abstractmethod
    def againEvent(self, entry):
        raise NotImplementedError('subclass must define this method')

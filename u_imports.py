from x_maps import MapsModel
from x_game import GameModel
from u_render import ConfigRender
from panda3d.core import (
    PandaSystem,
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionHandlerPusher,
    loadPrcFileData,
    VirtualFileSystem)
from panda3d.core import Filename


class ConfigImports(ConfigRender):
    def __init__(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        ConfigRender.__init__(self)

        self.elapsedSeconds = 0
        self.mapData = MapsModel()
        self.gameData = GameModel('./saves/')
        self.load_fonts()

        # this needs to be called only when game starts
        taskMgr.add(self.updateTime, 'updateTime')

    def userExit(self):
        quit()

    def updateTime(self, task):
        self.elapsedSeconds = int(globalClock.getFrameTime())
        return task.cont

    def load_fonts(self):
        self.font_title = base.loader.loadFont('GenericMobileSystem.ttf')
        self.font_title.setPixelsPerUnit(80)

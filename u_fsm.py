from w_menu_start import StartMenu
from w_grid_stage import GridStage
from u_imports import ConfigImports
from u_controls import ConfigControls
from w_menu_config import ConfigMenu
from w_menu_gameover import GameOverMenu
from direct.fsm.FSM import FSM


class ConfigFSM(FSM, ConfigImports, ConfigControls):
    def __init__(self):
        self.gridStage = None
        FSM.__init__(self, "FSM-Game")
        ConfigImports.__init__(self)
        ConfigControls.__init__(self)
        self.defaultTransitions = {
            'StartMenu': ['GameLoop'],
            'GameLoop': ['PauseMenu', 'GameOver'],
            'PauseMenu': ['StartMenu', 'GameLoop'],
            'GameOver': ['StartMenu']
        }

    # FSM ##################################################################

    def enterStartMenu(self):
        self.initController()
        self.startMenu = StartMenu()

        if self.gridStage:
            self.gridStage.quit()

        self.accept("Menu-Start", self.startNewGame)
        self.accept("Menu-Load", self.request, ["LoadMenu"])
        self.accept("Menu-Website", self.startMenu.websiteTask)
        self.accept("Menu-Quit", self.userExit)

        taskMgr.add(self.startMenu.readKeys, "readKeysTask")

    def exitStartMenu(self):
        self.resetButtons()
        self.ignore("Menu-Start")
        self.ignore("Menu-Load")
        self.ignore("Menu-Website")
        self.ignore("Menu-Quit")

        taskMgr.remove("readKeysTask")
        self.startMenu.quit()
        del self.startMenu

    def enterGameLoop(self):
        self.initController()
        self.accept("Menu-Pause", self.request, ["PauseMenu"])
        self.accept("Menu-GameOver", self.request, ["GameOver"])
        self.gridStage.start()

    def exitGameLoop(self):
        self.resetButtons()
        self.ignore("Menu-Pause")
        self.ignore("Menu-GameOver")
        self.gridStage.stop()

    def enterPauseMenu(self):
        self.initController()
        self.configMenu = ConfigMenu()
        self.accept("Chara-Add", self.configMenu.change_config, [1])
        self.accept("Chara-Sub", self.configMenu.change_config, [-1])
        self.accept("Back-Game", self.request, ["GameLoop"])
        self.accept("Back-Start", self.request, ["StartMenu"])
        taskMgr.add(self.configMenu.readKeys, "readKeysTask")

    def exitPauseMenu(self):
        self.resetButtons()
        self.ignore("Chara-Add")
        self.ignore("Chara-Sub")
        self.ignore("Back-Game")
        self.ignore("Back-Start")
        taskMgr.remove("readKeysTask")
        self.configMenu.quit()
        del self.configMenu

    def enterGameOver(self):
        self.accept("Back-Start", self.request, ["StartMenu"])
        self.game_over = GameOverMenu(self.gridStage.player.is_ko)

    def exitGameOver(self):
        self.ignore("Back-Start")
        self.game_over.quit()
        del self.game_over

    # FSM ##################################################################

    def startNewGame(self):
        base.gameData.resetGameModel()
        base.messenger.send("MapReload")
        self.gridStage = GridStage()
        self.request("GameLoop")

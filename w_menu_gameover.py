from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
    DirectRadioButton)
from i_menu import IMenu


class GameOverMenu(IMenu):
    def __init__(self, is_player_ko):
        self.message = 'Game Over' if is_player_ko else 'You Win!'
        frame = DirectFrame(frameSize=(base.a2dLeft, base.a2dRight,
                                       base.a2dBottom, base.a2dTop),
                            frameColor=(0, 0, 0, 0.5))
        IMenu.__init__(self, frame=frame)
        self.menuVerticalChoicesList = [
            # {"event": "Back-Game", "text": "Resume Game"},
            # {"event": "Back-Start", "text": "Back to Start Menu"}
        ]
        self.menuHorizontalChoices = []
        self.statsSheet = None
        self.createVerticalButtons()
        self.addTitle()
        taskMgr.doMethodLater(3.0, base.messenger.send,
                              'callStartMenu', extraArgs=['Back-Start'])

    def createButton(self, text, index, eventArgs):
        btn = DirectRadioButton(text=text,
                                text_align=TextNode.ALeft,
                                scale=0.05,
                                frameColor=(0, 0, 0, 0.0),
                                pos=(base.a2dLeft + 0.7, 0,
                                     (0.5 - (index * .15))),
                                variable=self.menuVerticalChoice,
                                value=[index],
                                text_fg=(1, 1, 1, 1),
                                command=self.menuVerticalEvent)

        self.menuVerticalButtons.append(btn)
        btn.reparentTo(self.frameMain)

    def addTitle(self):
        self.title = OnscreenText(
            self.message, 1,
            fg=(1, 0, 0, 1),
            pos=(base.a2dLeft + 0.7, 0.8),
            font=base.font_title,
            align=TextNode.ALeft,
            scale=.15,
            mayChange=1)
        self.title.reparentTo(self.frameMain)

    def cancelCommand(self):
        base.messenger.send("Back-Game")

    def add_stat(self, text, index):
        stat = DirectLabel(
            scale=0.05,
            text_align=TextNode.ALeft,
            pos=(0, 0, (0.5 - (index * .15))),
            pad=(0.5, 0.5),
            frameColor=(0, 0, 0, 0.0),
            text=text,
            text_fg=(1, 1, 1, 1))
        stat.reparentTo(self.statsSheet)

    def readKeys(self, task):
        keysPressed = sum(base.directionMap.values())

        if keysPressed == 0:
            self.isButtonUp = True

            if base.commandMap["confirm"]:
                self.menuVerticalEvent()
                base.messenger.send("playConfirm")
            elif base.commandMap["cancel"]:
                self.cancelCommand()
                base.messenger.send("playCancel")

            base.resetButtons()
            return task.cont

        if not self.isButtonUp:
            return task.cont

        if base.directionMap["up"]:
            self.navigateChoice(-1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap["down"]:
            self.navigateChoice(1, self.menuVerticalChoice,
                                self.menuVerticalChoicesList)
            self.isButtonUp = False
        elif base.directionMap["left"]:
            self.menuHorizontalChoice[0] = 0
            self.isButtonUp = False
            self.menuHorizontalEvent()
        elif base.directionMap["right"]:
            self.menuHorizontalChoice[0] = 1
            self.isButtonUp = False
            self.menuHorizontalEvent()

        base.resetButtons()
        return task.cont

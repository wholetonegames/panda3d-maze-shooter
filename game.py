from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, PandaSystem
from direct.gui.OnscreenText import OnscreenText, TextNode
from direct.gui.DirectGui import DirectFrame

from u_fsm import ConfigFSM

appName = "car game"
loadPrcFileData("",
                """
    window-title {}
    win-size 1280 720
    fullscreen 0
    cursor-hidden 0
    show-frame-rate-meter 0
    model-path $MAIN_DIR/egg/
    framebuffer-multisample 1
    #multisamples 8
    #texture-anisotropic-degree 2
    #textures-auto-power-2 1
    #notify-level-device debug
    #notify-level-device spam
    #want-pstats 1
""".format(appName))


class Main(ShowBase, ConfigFSM):
    def __init__(self, appName):
        self.appName = appName
        self.loadingText = None
        ShowBase.__init__(self)
        ConfigFSM.__init__(self)
        self.request('StartMenu')

    def callLoadingScreen(self):
        self.loadingText = DirectFrame(
            frameSize=(base.a2dLeft, base.a2dRight,
                       base.a2dBottom, base.a2dTop),
            frameColor=(0, 0, 0, 1.0))

        txt = OnscreenText("Loading...", 1, fg=(1, 1, 1, 1), pos=(
            0, 0), align=TextNode.ACenter, scale=.07, mayChange=1)
        txt.reparentTo(self.loadingText)
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def removeLoadingScreen(self):
        if self.loadingText:
            self.loadingText.removeNode()
        self.loadingText = None


game = Main(appName)
game.run()

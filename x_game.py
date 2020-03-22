from x_save_load import SaveLoadJSON
import y_helpers
import os


class GameModel(SaveLoadJSON):
    def __init__(self, saveFolderPath):
        SaveLoadJSON.__init__(self, saveFolderPath)
        self.saveSlotNumbers = (1, 2, 3)
        self.protectedFields.append('saveSlotNumbers')
        self.selectedSaveSlot = 1
        self.protectedFields.append('selectedSaveSlot')
        self.itemInventory = []
        self.currentMap = 0
        self.previousSavedTime = 0
        # at the end, always
        self.resetGameModel()

    def getSaveFileInfo(self, filename):
        json_data = self.get_text(filename)
        totalTime = 0
        thisMap = 'Nowhere'
        if 'currentMap' in json_data:
            thisMap = json_data['currentMap']
        if 'totalTimePlayed' in json_data:
            totalTime = y_helpers.pretty_print_time(
                json_data['totalTimePlayed'])
        return (thisMap, totalTime)

    def runManualUpdates(self):
        self.filepath = os.path.dirname(self.filepath) + \
            "/slot{}.txt".format(self.selectedSaveSlot)
        self.totalTimePlayed += (base.elapsedSeconds - self.previousSavedTime)
        self.previousSavedTime = base.elapsedSeconds

    def resetGameModel(self):
        self.currentMap = 0
        self.totalTimePlayed = 0
        self.textDisplayTime = 2.0
        self.sfx_vol = 1
        self.bgm_vol = 1

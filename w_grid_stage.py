from i_stage import IStage


class GridStage(IStage):
    NAME_HERO = 'hero'
    NAME_ENEMY = 'enemy'
    NAME_WALL = 'wall'
    NAME_ENEMY_BULLET = 'bullet_e'
    NAME_HERO_BULLET = 'bullet_h'

    def __init__(self):
        IStage.__init__(self)
        self.setup()
        self.setCollision()
        self.stop()

    def getIntoFromNames(self, entry):
        intoName = entry.getIntoNode().getName()
        fromName = entry.getFromNode().getName()
        return (intoName, fromName)

    def intoEvent(self, entry):
        if not entry.hasInto():
            return

        intoName, fromName = self.getIntoFromNames(entry)

        if self.NAME_ENEMY in fromName:
            if self.NAME_HERO in intoName or self.NAME_WALL in intoName or self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(fromName)
                normal = entry.getSurfaceNormal(entry.getIntoNodePath())
                e = self.enemyActors[index]
                e.moveAwayFrom(normal)
            if self.NAME_HERO in intoName:
                self.player.decrement_hp()
            return

        if self.NAME_HERO_BULLET in fromName:
            if self.NAME_WALL in intoName or self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(fromName)
                b = self.hero_bullets[index]
                b.reset()
            if self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(intoName)
                e = self.enemyActors[index]
                e.decrement_hp()
            return

        if self.NAME_ENEMY_BULLET in fromName:
            if self.NAME_WALL in intoName or self.NAME_HERO in intoName:
                index = self.getIndexFromEvent(fromName)
                b = self.enemy_bullets[index]
                b.reset()
            if self.NAME_HERO in intoName:
                self.player.decrement_hp()
            return

    def againEvent(self, entry):
        if not entry.hasInto():
            return

        intoName, fromName = self.getIntoFromNames(entry)

        if self.NAME_ENEMY in fromName:
            if self.NAME_HERO in intoName or self.NAME_WALL in intoName or self.NAME_ENEMY in intoName:
                index = self.getIndexFromEvent(fromName)
                e = self.enemyActors[index]
                e.randomDirection()
            return

    def cancelCommand(self):
        base.messenger.send("Menu-Pause")

    def getIndexFromEvent(self, eventName):
        l = eventName.split("_")
        # -1 is the last part of the name
        return int(l[-1])

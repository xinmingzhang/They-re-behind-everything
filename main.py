import random
import math
import datetime
import pygame as pg


class Marker(pg.sprite.Sprite):
    def __init__(self, game):
        super(Marker, self).__init__()
        self.game = game
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 0, 0), (10, 10), self.game.marker_size)
        surface.blit(self.image, self.rect)


class Hands(pg.sprite.Sprite):
    def __init__(self, game):
        super(Hands, self).__init__()
        self.game = game
        self.image = pg.Surface((800, 600), pg.SRCALPHA)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        self.image = pg.Surface((800, 600), pg.SRCALPHA)
        if self.game.time_show == 'hour':
            hour = self.game.hour % 12 + self.game.minute / 60.0
            angle = hour / 12.0 * 360
            end_point = (400 + 100 * math.sin(math.radians(angle)), 300 - 100 * math.cos(math.radians(angle)))
            pg.draw.line(self.image, (0, 0, 0), (400, 300), end_point, 5)
        elif self.game.time_show == 'minute':
            minute = self.game.minute + self.game.second / 60.0
            angle = minute / 60.0 * 360
            end_point = (400 + 150 * math.sin(math.radians(angle)), 300 - 150 * math.cos(math.radians(angle)))
            pg.draw.line(self.image, (0, 0, 0), (400, 300), end_point, 2)
        elif self.game.time_show == 'second':
            second = self.game.second
            angle = second / 60.0 * 360
            end_point = (400 + 180 * math.sin(math.radians(angle)), 300 - 180 * math.cos(math.radians(angle)))
            pg.draw.line(self.image, (0, 0, 0), (400, 300), end_point, 1)
        surface.blit(self.image, self.rect)


class Game(object):
    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((800, 600))
        self.caption = pg.display.set_caption("click the mouse crazily to see what's behind:)")
        self.clock = pg.time.Clock()
        self.time_show = None
        self.hour = None
        self.minute = None
        self.second = None
        self.marker_size = 0
        self.hands = Hands(self)
        self.marker = Marker(self)
        self.marker2 = Marker(self)
        self.marker3 = Marker(self)
        self.marker4 = Marker(self)
        self.frame = 0
        self.fps = 100
        self.cps = 0
        self.timer = 1000
        self.counter = 0
        self.total_click = 1
        self.fresh_rate = 0
        self.level = 1


    def draw(self):
        rr = random.randint
        self.screen.fill((rr(0, 255), rr(0, 255), rr(0, 255)))
        self.marker.draw(self.screen)
        self.marker2.draw(self.screen)
        self.marker3.draw(self.screen)
        self.marker4.draw(self.screen)
        self.hands.draw(self.screen)
        for i in range(int(60 - self.cps-self.level)):
            pg.draw.circle(self.screen, (0, 0, 0), (rr(0, 800), rr(0, 600)), rr(5, 10))
            pg.draw.line(self.screen, (0, 0, 0), (rr(0, 800), rr(0, 800)), (rr(0, 800), rr(0, 800)), rr(1, 5))
        pg.display.update()

    def update(self):
        now = datetime.datetime.now()
        self.hour = now.hour
        self.minute = now.minute
        self.second = now.second
        self.frame += 1
        self.number = self.frame % 60
        self.marker.rect.center = (
        400 + 200 * math.sin(math.radians(self.number * 6)), 300 - 200 * math.cos(math.radians(self.number * 6)))
        self.marker2.rect.center = (400 + 200 * math.sin(math.radians(self.number * 6 + 90)),
                                    300 - 200 * math.cos(math.radians(self.number * 6 + 90)))
        self.marker3.rect.center = (400 + 200 * math.sin(math.radians(self.number * 6 + 180)),
                                    300 - 200 * math.cos(math.radians(self.number * 6 + 180)))
        self.marker4.rect.center = (400 + 200 * math.sin(math.radians(self.number * 6 + 270)),
                                    300 - 200 * math.cos(math.radians(self.number * 6 + 270)))
        if self.number % 5 == 0:
            self.marker_size = 10
        else:
            self.marker_size = 5
        if self.frame % 3 == 0:
            self.time_show = 'hour'
        elif self.frame % 3 == 1:
            self.time_show = 'minute'
        elif self.frame % 3 == 2:
            self.time_show = 'second'

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                self.cps += 1
                self.total_click += 1
                self.level = int(math.sqrt(self.total_click))

    def run(self):
        pg.init()
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.counter += dt
            if self.counter >= self.timer:
                self.counter -= self.timer
                self.cps = 0
            self.event_loop()
            self.fresh_rate += dt
            if  self.cps:
                if self.fresh_rate >= 1000.0/(self.cps+self.level):
                    self.draw()
                    self.update()
                    self.fresh_rate = 0
            else:
                self.screen.fill((0,0,0))
                pg.display.update()
            if self.cps:
                self.caption = pg.display.set_caption('CPS = {}, total click = {}, level = {}'.format(str(self.cps),str(self.total_click),str(self.level)))
            else:
                self.caption = pg.display.set_caption("click the mouse crazily to see what's behind:)")
        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()

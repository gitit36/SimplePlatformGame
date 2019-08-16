import pygame
import screens
import objects
import colours

# classes of different levels in a game

class Level1(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [10, 100], [530, 200])
        i = 0
        while i < 640:
            self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.elements.append(objects.Image('grass.png'))
            self.element_locations.append([-30 + i, 430])
            i += 70

        self.elements.append(objects.Text('In it, I find myself driven', 48))
        self.element_locations.append([10, 10])
        self.elements.append(objects.Text('by my desire for boxes . . .', 48))
        self.element_locations.append([55, 56])


class Level2(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [10, 100], [530, 100])
        i = 0
        while i < 640:
            if 200 < i <= 330:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.ground.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 360])

            elif 330 < i <= 470:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.walls.append(pygame.Rect(-30 + i, 360, 70, 70))
                self.element_locations.append([-30 + i, 360])
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.ground.append(pygame.Rect(-30 + i, 270, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 270, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 290])

            else:
                self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 430])
            i += 70

        self.elements.append(objects.Text('No matter the obstacles', 48))
        self.element_locations.append([10, 10])
        self.elements.append(objects.Text('I find on my way.', 48))
        self.element_locations.append([55, 56])

        self.is_stuck = False
        self.message_shown = False

    def update(self, death_count):
        super().update(death_count)
        if 400 < self.player.pos_x and 270 < self.player.pos_y:
            self.is_stuck = True

        if self.is_stuck and not self.message_shown:
            self.elements.append(objects.Text('I also know that', 24))
            self.element_locations.append([200, 380])
            self.elements.append(objects.Text('if I am ever stuck', 24))
            self.element_locations.append([200, 400])
            self.elements.append(objects.Text('I can always press R', 24))
            self.element_locations.append([200, 420])
            self.elements.append(objects.Text('to Restart.', 24))
            self.element_locations.append([200, 440])

            self.is_stuck = False
            self.message_shown = True


class Level3(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [10, 100], [530, 120])

        self.bg = colours.deep_sky_blue

        i = 0
        while i < 640:
            if 130 < i <= 190 or 330 < i <= 400:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.ground.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 360])

            elif 190 < i <= 330 or 400 < i:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.elements.append(objects.Image('spikes.png'))
                self.spikes.append(pygame.Rect(-30 + i, 395, 70, 35))
                self.element_locations.append([-30 + i, 360])

            else:
                self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 430])
            i += 70

        self.elements.append(objects.Text('Even if they look scary.', 48))
        self.element_locations.append([10, 10])


class Level4(screens.Level):
    def __init__(self, char_id, enemy_id):
        super().__init__(char_id, [10, 100], [530, 200])

        self.bg = colours.deep_sky_blue

        i = 0
        while i < 640:
            self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.elements.append(objects.Image('grass.png'))
            self.element_locations.append([-30 + i, 430])
            i += 70

        self.elements.append(objects.Text('Sometimes, I find others', 48))
        self.element_locations.append([10, 10])
        self.elements.append(objects.Text('who look just like me . . .', 48))
        self.element_locations.append([55, 56])

        self.enemies.append(objects.Enemy(enemy_id, 320, 340, False))

        self.has_died = False
        self.message_shown = False

    def update(self, death_count):
        super().update(death_count)
        if self.player.was_hurt:
            self.has_died = True

        if self.has_died and not self.message_shown:
            self.elements.append(objects.Text('. . . only to realise', 30))
            self.element_locations.append([10, 100])
            self.elements.append(objects.Text('they are', 36))
            self.element_locations.append([275, 110])
            self.elements.append(objects.Text('dangerous.', 72))
            self.element_locations.append([230, 140])
            self.has_died = False
            self.message_shown = True


class Level5(screens.Level):
    def __init__(self, char_id, enemy_id):
        super().__init__(char_id, [10, 100], [530, 150])

        self.bg = colours.dodger_blue

        i = 0
        while i < 640:
            if i > 200:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.ground.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 360])

            else:
                self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 430])
            i += 70

        self.enemies.append(objects.Enemy(enemy_id, 100, 350, False))
        self.enemies.append(objects.Enemy(enemy_id, 300, 350, False))

        self.elements.append(objects.Text('And as I move forward . . .', 48))
        self.element_locations.append([10, 10])


class Level6(screens.Level):
    def __init__(self, char_id, enemy_id):
        super().__init__(char_id, [10, 100], [550, 100])

        self.bg = colours.dodger_blue

        i = 0
        while i < 640:
            if 200 < i <= 270:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 360])

                self.ground.append(pygame.Rect(-30 + i, 270, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 270, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 290])

            elif 270 < i <= 410:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.elements.append(objects.Image('spikes.png'))
                self.spikes.append(pygame.Rect(-30 + i, 395, 70, 35))
                self.element_locations.append([-30 + i, 360])

            elif 410 < i <= 480:
                self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 410, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 430])

            else:
                self.elements.append(objects.Image('dirtBlock.png'))
                self.element_locations.append([-30 + i, 430])

                self.ground.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 340, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 360])

            i += 70

        self.enemies.append(objects.Enemy(enemy_id, 100, 350, False))
        self.enemies.append(objects.Enemy(enemy_id, 380, 350, False))
        self.enemies.append(objects.Enemy(enemy_id, 530, 350, False))

        self.elements.append(objects.Text('more and more appear.', 48))
        self.element_locations.append([10, 10])


class Level7(screens.Level):
    def __init__(self, char_id, enemy_id):
        super().__init__(char_id, [70, -10], [550, 350])

        self.bg = colours.medium_blue

        i = 0
        while i < 640:
            if i <= 500:
                self.ground.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.roof.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 90])

            if 140 <= i:
                self.ground.append(pygame.Rect(-30 + i, 245, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 245, 70, 70))
                self.roof.append(pygame.Rect(-30 + i, 245, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 265])

            self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.walls.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.elements.append(objects.Image('grass.png'))
            self.element_locations.append([-30 + i, 430])
            i += 70

        self.elements.append(objects.Text('Some of them chase me.', 48))
        self.element_locations.append([10, 50])

        self.enemies.append(objects.Enemy(enemy_id, -50, 0, True))
        self.enemies.append(objects.Enemy(enemy_id, 600, 100, True))
        self.enemies.append(objects.Enemy(enemy_id, -30, 300, True))

        self.was_shown1 = False
        self.was_shown2 = False

    def update(self, death_count):
        super().update(death_count)
        if self.player.pos_y > 100 and not self.was_shown1:
            self.elements.append(objects.Text('But I outrun them.', 48))
            self.element_locations.append([110, 225])
            self.was_shown1 = True

        if self.player.pos_y > 250 and not self.was_shown2:
            self.elements.append(objects.Text('Every single time.', 48))
            self.element_locations.append([10, 390])
            self.was_shown2 = True


class Level8(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [10, -30], [30, 260])

        self.bg = colours.medium_blue

        self.elements.pop(0)
        self.elements.append(objects.Image("FinalBox.png"))

        self.elements.append(objects.Text('There it is.', 48))
        self.element_locations.append([300, 50])
        self.elements.append(objects.Text('The most beautiful box', 48))
        self.element_locations.append([10, 170])
        self.elements.append(objects.Text('I have ever seen.', 48))
        self.element_locations.append([55, 216])

        i = 0
        while i < 640:
            if i <= 500:
                self.ground.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.walls.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.roof.append(pygame.Rect(-30 + i, 70, 70, 70))
                self.elements.append(objects.Image('grass.png'))
                self.element_locations.append([-30 + i, 90])

            self.ground.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.walls.append(pygame.Rect(-30 + i, 410, 70, 70))
            self.elements.append(objects.Image('grass.png'))
            self.element_locations.append([-30 + i, 430])
            i += 70

        self.walls.append(pygame.Rect(0, 150, 120, 400))

        self.was_shown = False
        self.has_waited = False

    def update(self, death_count):
        super().update(death_count)
        if self.player.pos_y > 200 and not self.was_shown:
            self.elements.append(objects.Text('And right before getting it', 24))
            self.element_locations.append([110, 270])
            self.elements.append(objects.Text('I realise how pointless all of this is.', 24))
            self.element_locations.append([110, 300])
            self.was_shown = True
            return

        if self.player.pos_y > 300 and not self.has_waited:
            pygame.time.wait(2000)
            self.elements.append(objects.Text('And I start falling . . .', 48))
            self.element_locations.append([110, 400])
            self.has_waited = True
            return

        if self.was_shown and self.has_waited:
            self.ground = []
            el_temp = []
            loc_temp = []
            for i in range(len(self.elements)):
                if self.element_locations[i][1] < 410:
                    el_temp.append(self.elements[i])
                    loc_temp.append(self.element_locations[i])

            self.elements = el_temp
            self.element_locations = loc_temp

    def is_finished(self):
        if 0 < self.player.pos_x < 640 and 700 < self.player.pos_y:
            pygame.time.wait(1000)
            return True
        return False


class Level9(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [320, -100], [-300, -300])

        self.bg = colours.navy_blue

        self.walls.append(pygame.Rect(0, -200, 100, 1000))
        self.walls.append(pygame.Rect(540, -200, 100, 1000))

        self.elements.append(objects.Text('. . . and falling . . .', 40))
        self.element_locations.append([120, 10])

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(screen, colours.black, (0, -200, 100, 1000))
        pygame.draw.rect(screen, colours.black, (540, -200, 100, 1000))

    def is_finished(self):
        if 0 < self.player.pos_x < 640 and 700 < self.player.pos_y:
            pygame.time.wait(1000)
            return True
        return False


class Level10(screens.Level):
    def __init__(self, char_id):
        super().__init__(char_id, [320, -100], [-300, -300])

        self.bg = colours.midnight_blue

        self.walls.append(pygame.Rect(0, -200, 150, 1000))
        self.walls.append(pygame.Rect(490, -200, 150, 1000))

        self.elements.append(objects.Text('. . . and falling . . .', 32))
        self.element_locations.append([180, 10])

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(screen, colours.black, (0, -200, 150, 1000))
        pygame.draw.rect(screen, colours.black, (490, -200, 150, 1000))

    def is_finished(self):
        if 0 < self.player.pos_x < 640 and 700 < self.player.pos_y:
            pygame.time.wait(1000)
            return True
        return False

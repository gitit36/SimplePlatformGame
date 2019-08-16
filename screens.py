import colours
import objects
import random


class Screen:
# fill background color and elements
    def __init__(self):
        self.bg = colours.sky_blue
        self.elements = []
        self.element_locations = []

    def draw(self, screen):
        screen.fill(self.bg)
        for i in range(len(self.elements)):
            self.elements[i].draw(screen, self.element_locations[i])


class Level(Screen):
    def __init__(self, char_id, init_pos, end_pos):
        super().__init__()
        self.player = objects.Player(char_id, init_pos[0], init_pos[1])
        self.ground = []
        self.walls = []
        self.spikes = []
        self.roof = []
        self.enemies = []
        self.elements.append(objects.Image('BoxFinish.png'))
        self.element_locations.append(end_pos)

    def draw(self, screen): # draw player and enemy(-ies)
        super().draw(screen)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

    def update(self, death_count):
        self.player.update(self.ground, self.walls, self.spikes, self.enemies, self.roof, death_count)
        for enemy in self.enemies:
            enemy.update(self.ground, self.walls, self.player)

    def is_finished(self):
        if self.element_locations[0][0] - 50 < self.player.pos_x < self.element_locations[0][0] + 50 and\
           self.element_locations[0][1] - 50 < self.player.pos_y < self.element_locations[0][1] + 50:
            return True
        return False


class MainMenu(Screen):
    def __init__(self):
        super().__init__()

        self.elements.append(objects.Text('I keep having this dream . . .', 48))
        self.element_locations.append([10, 10])

        self.elements.append(objects.Button('PlayButton.png'))
        self.element_locations.append([5, 359])
        self.elements.append(objects.Button('MenuButton.png'))
        self.element_locations.append([163, 359])
        self.elements.append(objects.Button('ScoreButton.png'))
        self.element_locations.append([321, 359])
        self.elements.append(objects.Button('ExitButton.png'))
        self.element_locations.append([479, 359])

        self.clouds = []
        self.cloud_locations = []
        self.cloud_speeds = []
        for i in range(random.randint(5, 10)):
            cloud = random.choice(['1', '2', '3'])
            self.clouds.append(objects.Image('cloud' + cloud + '.png'))
            self.cloud_locations.append([random.randint(-1000, -100), random.randint(0, 278)])
            self.cloud_speeds.append(random.randint(1, 3))

    def draw(self, screen):
        super().draw(screen)
        for i in range(len(self.clouds)):
            self.clouds[i].draw(screen, self.cloud_locations[i])

    def update(self, screen):
        for i in range(len(self.clouds)):
            self.cloud_locations[i][0] += self.cloud_speeds[i]
            if self.cloud_locations[i][0] > screen.get_width():
                self.cloud_locations[i][0] = random.randint(-1000, -100)
                self.cloud_locations[i][1] = random.randint(0, 278)


class PauseMenu(Screen):
    def __init__(self):
        super().__init__()


class Credits(Screen):
    def __init__(self):
        super().__init__()

        self.bg = colours.black

        self.elements.append(objects.Text('I Keep Having This Dream', 48))
        self.element_locations.append([50, 500])

        self.elements.append(objects.Text('Created by:', 32))
        self.element_locations.append([60, 550])
        self.elements.append(objects.Text('Sangjin Lee', 32))
        self.element_locations.append([350, 550])
        self.elements.append(objects.Text('Jose Sandoval', 32))
        self.element_locations.append([340, 580])

        self.elements.append(objects.Text('Artwork by:', 32))
        self.element_locations.append([60, 620])
        self.elements.append(objects.Text('Alexander Greye', 32))
        self.element_locations.append([310, 620])
        self.elements.append(objects.Text('Kenney.nl', 32))
        self.element_locations.append([410, 650])

        self.elements.append(objects.Text('Music by:', 32))
        self.element_locations.append([60, 690])
        self.elements.append(objects.Text('Ross Bugden', 32))
        self.element_locations.append([380, 690])

        self.elements.append(objects.Text('Typeface by:', 32))
        self.element_locations.append([60, 730])
        self.elements.append(objects.Text('Jakob Fischer', 32))
        self.element_locations.append([360, 730])

        self.elements.append(objects.Text('Inspired by the flash game', 32))
        self.element_locations.append([100, 770])
        self.elements.append(objects.Text('The Company of Myself', 32))
        self.element_locations.append([130, 800])
        self.elements.append(objects.Text('developed by 2DArray', 32))
        self.element_locations.append([135, 830])

        self.elements.append(objects.Text('Click -> Main Menu', 32))
        self.element_locations.append([140, 930])

    def update(self):
        for i in range(len(self.elements)):
            self.element_locations[i][1] -= 1

    def have_rolled(self):
        if self.element_locations[-1][1] < -100:
            return True
        return False


class Scores(Screen):
    def __init__(self):
        super().__init__()

        self.elements.append(objects.Button('ExitButton.png'))
        self.element_locations.append([479, 359])

        self.elements.append(objects.Text('Date', 32))
        self.element_locations.append([10, 20])
        self.elements.append(objects.Text('Deaths', 32))
        self.element_locations.append([185, 20])
        self.elements.append(objects.Text('Time', 32))
        self.element_locations.append([360, 20])
        self.elements.append(objects.Text('Score', 32))
        self.element_locations.append([535, 20])

        scoreboard = open('Files/scoreboard.txt', 'r')
        scores = []
        for line in scoreboard:
            scores.append(line.split(','))
        scoreboard.close()

        scores.sort(key=lambda x: int(x[-1]))
        # lambda creates an inline function
        # Sorts score list based on the value of 'key'
        # Takes a single argument x and returns int(x[-1]).

        for i in range(9):
            try:
                for j in range(len(scores[-1 - i])):
                    self.elements.append(objects.Text(scores[-1 - i][j], 32))
                    self.element_locations.append([10 + (j * 175), 50 + (i * 30)])

            except IndexError:
                break


class Settings(Screen):
    def __init__(self):
        super().__init__()

        self.elements.append(objects.Button('ExitButton.png'))
        self.element_locations.append([479, 359])

        self.elements.append(objects.Switch('On', 'Off'))
        self.element_locations.append([450, 60])

        self.elements.append(objects.ButtonText('Clear', 32))
        self.element_locations.append([450, 110])

        self.elements.append(objects.ImageSwitch('PrevChar1.png', 'PrevChar2.png'))
        self.element_locations.append([450, 160])

        self.elements.append(objects.ImageSwitch('PrevChar2.png', 'PrevChar1.png'))
        self.element_locations.append([450, 210])

        self.elements.append(objects.Text('Music:', 32))
        self.element_locations.append([100, 60])

        self.elements.append(objects.Text('Settings', 32))
        self.element_locations.append([300, 20])

        self.elements.append(objects.Text('Clear scoreboard:', 32))
        self.element_locations.append([100, 110])

        self.elements.append(objects.Text('Player appearance:', 32))
        self.element_locations.append([100, 160])

        self.elements.append(objects.Text('Enemy appearance:', 32))
        self.element_locations.append([100, 210])

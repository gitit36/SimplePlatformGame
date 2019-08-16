import pygame
import screens
import levels
import objects
import time
pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self, dim_x, dim_y):
        self.window = pygame.display.set_mode((dim_x, dim_y))
        self.music = pygame.mixer.music.load('Files/SoundTrack.ogg')

        self.is_open = True
        self.is_playing = False
        self.is_in_menu = False
        self.is_in_scores = False
        self.is_finished = False
        self.current_level = 0
        self.death_count = [0]
        self.pos_mouse = (0, 0)

        self.char_id = 1
        self.enemy_id = 2

        self.menus = [screens.MainMenu(), screens.Scores(), screens.Settings()]
        self.levels = [levels.Level1(self.char_id),
                       levels.Level2(self.char_id),
                       levels.Level3(self.char_id),
                       levels.Level4(self.char_id, self.enemy_id),
                       levels.Level5(self.char_id, self.enemy_id),
                       levels.Level6(self.char_id, self.enemy_id),
                       levels.Level7(self.char_id, self.enemy_id),
                       levels.Level8(self.char_id),
                       levels.Level9(self.char_id),
                       levels.Level10(self.char_id)]
        self.credits = screens.Credits()
        self.time_init = 0
        self.time_game = 0
        self.score = 0

        self.is_paused = False

        pygame.display.set_caption('I Keep Having This Dream')

    def reset(self): #resetting the game to the start
        self.is_playing = False
        self.is_finished = False
        self.current_level = 0
        self.death_count = [0]
        self.pos_mouse = (0, 0)

        self.menus[1] = screens.Scores()

        self.levels = [levels.Level1(self.char_id),
                       levels.Level2(self.char_id),
                       levels.Level3(self.char_id),
                       levels.Level4(self.char_id, self.enemy_id),
                       levels.Level5(self.char_id, self.enemy_id),
                       levels.Level6(self.char_id, self.enemy_id),
                       levels.Level7(self.char_id, self.enemy_id),
                       levels.Level8(self.char_id),
                       levels.Level9(self.char_id),
                       levels.Level10(self.char_id)]
        self.credits = screens.Credits()
        self.time_init = 0
        self.time_game = 0
        self.score = 0

    def run(self):
        pygame.mixer.music.play(-1)
        while self.is_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_open = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos_mouse = pygame.mouse.get_pos()
                    break

                if self.is_playing:
                    try:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                self.levels[self.current_level].player.velocity_x = 7

                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                self.levels[self.current_level].player.velocity_x = -7

                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                if not self.levels[self.current_level].player.is_jumping:
                                    self.levels[self.current_level].player.velocity_y = -15
                                    self.levels[self.current_level].player.is_jumping = True

                            if event.key == pygame.K_r:
                                self.levels[self.current_level].player.was_hurt = True
                                self.death_count[0] += 1

                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or \
                               event.key == pygame.K_d or event.key == pygame.K_a:
                                self.levels[self.current_level].player.velocity_x = 0

                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                self.levels[self.current_level].player.velocity_y = 0

                    except IndexError:
                        pass

            if not self.is_playing and not self.is_in_menu and not self.is_in_scores:
                self.menus[0].draw(self.window)
                self.menus[0].update(self.window)

                if self.menus[0].elements[1].is_pressed(self.menus[0].element_locations[1], self.pos_mouse):
                    self.is_playing = True
                    self.time_init = time.time()

                self.is_in_menu = self.menus[0].elements[2].is_pressed(self.menus[0].element_locations[2],
                                                                       self.pos_mouse)
                self.is_in_scores = self.menus[0].elements[3].is_pressed(self.menus[0].element_locations[3],
                                                                         self.pos_mouse)
                self.is_open = not self.menus[0].elements[4].is_pressed(self.menus[0].element_locations[4],
                                                                        self.pos_mouse)

            elif self.is_finished:
                self.credits.draw(self.window)
                self.credits.update()
                if self.credits.have_rolled():
                    self.is_playing = False
                    self.reset()

            elif self.is_in_menu:
                self.menus[2].draw(self.window)
                if self.menus[2].elements[0].is_pressed(self.menus[2].element_locations[0], self.pos_mouse):
                    self.is_in_menu = False
                    self.pos_mouse = (0, 0)

                if self.menus[2].elements[1].is_pressed(self.menus[2].element_locations[1], self.pos_mouse):
                    if not self.is_paused:
                        self.is_paused = True
                        pygame.mixer.music.pause()
                    else:
                        self.is_paused = False
                        pygame.mixer.music.unpause()
                    self.pos_mouse = (0, 0)

                if self.menus[2].elements[2].is_pressed(self.menus[2].element_locations[2], self.pos_mouse):
                    open('Files/scoreboard.txt', 'w').close()
                    self.pos_mouse = (0, 0)
                    self.menus[1] = screens.Scores()

                if self.menus[2].elements[3].is_pressed(self.menus[2].element_locations[3], self.pos_mouse):
                    if self.char_id == 1:
                        self.char_id = 2
                    else:
                        self.char_id = 1

                    self.levels = [levels.Level1(self.char_id),
                                   levels.Level2(self.char_id),
                                   levels.Level3(self.char_id),
                                   levels.Level4(self.char_id, self.enemy_id),
                                   levels.Level5(self.char_id, self.enemy_id),
                                   levels.Level6(self.char_id, self.enemy_id),
                                   levels.Level7(self.char_id, self.enemy_id),
                                   levels.Level8(self.char_id),
                                   levels.Level9(self.char_id),
                                   levels.Level10(self.char_id)]

                    self.pos_mouse = (0, 0)

                if self.menus[2].elements[4].is_pressed(self.menus[2].element_locations[4], self.pos_mouse):
                    if self.enemy_id == 1:
                        self.enemy_id = 2
                    else:
                        self.enemy_id = 1

                    self.levels = [levels.Level1(self.char_id),
                                   levels.Level2(self.char_id),
                                   levels.Level3(self.char_id),
                                   levels.Level4(self.char_id, self.enemy_id),
                                   levels.Level5(self.char_id, self.enemy_id),
                                   levels.Level6(self.char_id, self.enemy_id),
                                   levels.Level7(self.char_id, self.enemy_id),
                                   levels.Level8(self.char_id),
                                   levels.Level9(self.char_id),
                                   levels.Level10(self.char_id)]

                    self.pos_mouse = (0, 0)

            elif self.is_in_scores:
                self.menus[1].draw(self.window)
                if self.menus[1].elements[0].is_pressed(self.menus[1].element_locations[0], self.pos_mouse):
                    self.is_in_scores = False
                    self.pos_mouse = (0, 0)

            else:
                try:
                    self.levels[self.current_level].draw(self.window)

                    deaths = objects.Text(str(self.death_count[0]), 24)
                    deaths.draw(self.window, [10, 450])

                    self.levels[self.current_level].update(self.death_count)

                    if self.levels[self.current_level].is_finished():
                        self.current_level += 1
                        pygame.time.wait(1000)

                except IndexError:
                    self.time_game = time.time() - self.time_init
                    self.score = 10000 - self.time_game - (self.death_count[0] * 50)
                    self.is_finished = True
                    scoreboard = open('Files/scoreboard.txt', 'a')
                    scoreboard.write(time.strftime("%d/%m/%Y") + ',' + str(int(self.death_count[0])) + ',' +
                                     str(int(self.time_game)) + ',' + str(int(self.score)) + '\n')
                    scoreboard.close()

            pygame.display.update()

if __name__ == '__main__':
    g = Game(640, 480)
    g.run()

pygame.mixer.quit()
pygame.quit()

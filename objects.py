import pygame
import colours


class Text:
    def __init__(self, text, size):
        self.font_white = pygame.font.Font('Files/Nickname.otf', size)
        self.text_white = self.font_white.render(text, True, colours.white)

        self.font_black = pygame.font.Font('Files/Nickname.otf', size)
        self.text_black = self.font_black.render(text, True, colours.black)

    def draw(self, screen, pos):
        screen.blit(self.text_black, (pos[0], pos[1]))
        screen.blit(self.text_white, (pos[0] + 2, pos[1] + 2))


class Image:
    # loading image and copying in onto the screen
    def __init__(self, image):
        self.image = pygame.image.load('Files/' + image)

    def draw(self, screen, pos):
        screen.blit(self.image, (pos[0], pos[1]))


class Button(Image):
    def is_pressed(self, pos_button, pos_mouse):
        if pos_button[0] < pos_mouse[0] < pos_button[0] + self.image.get_width() and\
           pos_button[1] < pos_mouse[1] < pos_button[1] + self.image.get_height():
            return True
        return False


class ButtonText(Text):
    def is_pressed(self, pos_button, pos_mouse):
        if pos_button[0] < pos_mouse[0] < pos_button[0] + self.text_white.get_width() and\
           pos_button[1] < pos_mouse[1] < pos_button[1] + self.text_white.get_height():
            return True
        return False


class ImageSwitch:
    def __init__(self, img1, img2):
    # constructor where images are loaded into a list
        self.l = [Image(img1), Image(img2)]
        self.index = 0

    def draw(self, screen, pos):
    # images are located(drawn) on the screen
        self.l[self.index].draw(screen, pos)

    def is_pressed(self, pos_button, pos_mouse):
    # change image when button is pressed
        if pos_button[0] < pos_mouse[0] < pos_button[0] + self.l[self.index].image.get_width() and\
           pos_button[1] < pos_mouse[1] < pos_button[1] + self.l[self.index].image.get_height():
            if self.index == 0:
                self.index = 1
            else:
                self.index = 0
            return True
        return False


class Switch:
# change text when the button is pressed
    def __init__(self, text1, text2):
        self.l = [Text(text1, 32), Text(text2, 32)]
        self.index = 0

    def draw(self, screen, pos):
        self.l[self.index].draw(screen, pos)

    def is_pressed(self, pos_button, pos_mouse):
        if pos_button[0] < pos_mouse[0] < pos_button[0] + self.l[self.index].text_white.get_width() and \
           pos_button[1] < pos_mouse[1] < pos_button[1] + self.l[self.index].text_white.get_height():
            if self.index == 0:
                self.index = 1
            else:
                self.index = 0
            return True
        return False


class SpriteSheet:
    def __init__(self, ss_name):
    # Load sprite sheet
        self.sheet = pygame.image.load('Files/' + ss_name)

        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0


    def get_graphic(self, x, y, w, h):
    # Pull a single sprite from a sprite sheet
    # Pass in the x, y location of the sprite
    # and the width and height of the sprite.
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        graphic = pygame.Surface([w, h], pygame.SRCALPHA, 32) # creating blank graphic
        graphic = graphic.convert_alpha()
        graphic.blit(self.sheet, (0, 0), (x, y, w, h)) # Copy sprite from a sprite sheet onto a graphic

        return graphic


class Player:
    def __init__(self, char_id, pos_x, pos_y):
    # constructor that pass in the character and the x and y coordinate position.
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.init_pos = [pos_x, pos_y]

        self.gravity = 1

        self.orientation = "right" # player direction
        self.walking_player_graphic_l = [] # holds graphics for when the player walks left
        self.index_l = 0
        self.walking_player_graphic_r = [] # holds graphics for when the player walks right
        self.index_r = 0
        self.velocity_x = 0
        self.velocity_y = 0

        self.is_jumping = True
        self.was_hurt = False

        # grabbing individual sprite from the sprite sheet
        s = SpriteSheet('SSChar' + str(char_id) + '.png')

        # Putting all the right-facing graphics to a list
        graphics = [s.get_graphic(67, 196, 66, 92),
                    s.get_graphic(438, 93, 67, 94),
                    s.get_graphic(438, 0, 69, 92),
                    s.get_graphic(0, 0, 72, 97),
                    s.get_graphic(73, 0, 72, 97),
                    s.get_graphic(146, 0, 72, 97),
                    s.get_graphic(0, 98, 72, 97),
                    s.get_graphic(73, 98, 72, 97),
                    s.get_graphic(146, 98, 72, 97),
                    s.get_graphic(219, 0, 72, 97),
                    s.get_graphic(292, 0, 72, 97),
                    s.get_graphic(219, 98, 72, 97),
                    s.get_graphic(365, 0, 72, 97),
                    s.get_graphic(292, 98, 72, 97)]

        for i in range(len(graphics[3:])):
            self.walking_player_graphic_r.append(graphics[i+3])
            rotated_image = pygame.transform.flip(graphics[i+3], True, False)
            self.walking_player_graphic_l.append(rotated_image)
            # flipping the right-facing graphics to the left-facing ones and appending to a list

        self.standing_right = graphics[0]
        self.standing_left = pygame.transform.flip(self.standing_right, True, False)

        self.jumping_right = graphics[1]
        self.jumping_left = pygame.transform.flip(self.jumping_right, True, False)

        self.hurt_right = graphics[2]
        self.hurt_left = pygame.transform.flip(self.hurt_right, True, False)

        self.image = self.standing_right # initial graphic to begin with

        self.c = 0

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))

    def update(self, ground, walls, spikes, enemies, roof, death_count):
        if not self.was_hurt:
            self.gravity = 1

            # move right/left, up/down
            self.pos_x += self.velocity_x
            self.pos_y += self.velocity_y

            if self.is_jumping: # assigning graphic when jumping right/left
                if self.orientation == "right":
                    self.image = self.jumping_right
                else:
                    self.image = self.jumping_left

            elif self.velocity_x > 0: # series of graphics when the player is walking right
                self.image = self.walking_player_graphic_r[self.index_r]
                self.index_r += 1
                self.orientation = "right"

                # when the walk-right sprite reaches the end, come back to the first sprite image
                if self.index_r == len(self.walking_player_graphic_r):
                    self.index_r = 0

            elif self.velocity_x < 0: # series of graphics when the player is walking left
                self.image = self.walking_player_graphic_l[self.index_l]
                self.index_l += 1
                self.orientation = "left"

                # when the walk-left sprite reaches the end, come back to the first sprite image
                if self.index_l == len(self.walking_player_graphic_l):
                    self.index_l = 0

            else: # assigning graphic when standing right/left
                if self.orientation == "right":
                    self.image = self.standing_right
                else:
                    self.image = self.standing_left

            self.velocity_y += self.gravity # calculating the effect of gravity

            for block in ground:
                if block.left - 60 < self.pos_x < block.right - 10:
                    if block.top <= self.pos_y + 72 and self.pos_y <= block.centery:
                        self.pos_y = block.top - 72
                        self.velocity_y = 0
                        self.is_jumping = False

            for block in walls:
                if block.top - 72 < self.pos_y < block.bottom - 10:
                    if block.left <= self.pos_x + 72 and self.pos_x <= block.centerx and self.velocity_x > 0:
                        self.pos_x = block.left - 70

                    if block.right >= self.pos_x >= block.centerx and self.velocity_x < 0:
                        self.pos_x = block.right

            for block in roof:
                if block.left - 60 < self.pos_x < block.right - 10:
                    if block.bottom >= self.pos_y >= block.centery:
                        self.pos_y = block.bottom + 15
                        self.velocity_y *= -1

            for block in spikes:
                if block.top - 72 < self.pos_y < block.bottom and block.left - 72 < self.pos_x < block.right:
                    if self.orientation == "right":
                        self.image = self.hurt_right
                    else:
                        self.image = self.hurt_left

                    self.gravity = 0

                    self.was_hurt = True
                    death_count[0] += 1

            for enemy in enemies:
                if enemy.pos_y - 80 < self.pos_y < enemy.pos_y + 80 and\
                   enemy.pos_x - 50 < self.pos_x < enemy.pos_x + 50:
                    if self.orientation == "right":
                        self.image = self.hurt_right
                    else:
                        self.image = self.hurt_left

                    # enemy walks towards the player, hence the velocity of -1
                    self.velocity_x *= -1
                    self.velocity_y *= -1
                    self.is_jumping = False

                    for e in enemies:
                        e.pos_x = e.init_pos[0]
                        e.pos_y = e.init_pos[1]

                    self.was_hurt = True
                    death_count[0] += 1

        else:
            self.c += 1
            if self.c > 10:
                self.was_hurt = False
                self.c = 0
                self.pos_x = self.init_pos[0]
                self.pos_y = self.init_pos[1]
                self.velocity_x = 0
                self.velocity_y = 0


class Enemy:
    # a variation class from class Player
    def __init__(self, char_id, pos_x, pos_y, is_chasing):
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.init_pos = [pos_x, pos_y]

        self.gravity = 1

        self.orientation = "left"
        self.walking_player_graphic_l = []
        self.index_l = 0
        self.walking_player_graphic_r = []
        self.index_r = 0
        self.velocity_x = 0
        self.velocity_y = 0

        self.is_chasing = is_chasing

        s = SpriteSheet('SSChar' + str(char_id) + '.png')

        graphics = [s.get_graphic(67, 196, 66, 92),
                    s.get_graphic(0, 0, 72, 97),
                    s.get_graphic(73, 0, 72, 97),
                    s.get_graphic(146, 0, 72, 97),
                    s.get_graphic(0, 98, 72, 97),
                    s.get_graphic(73, 98, 72, 97),
                    s.get_graphic(146, 98, 72, 97),
                    s.get_graphic(219, 0, 72, 97),
                    s.get_graphic(292, 0, 72, 97),
                    s.get_graphic(219, 98, 72, 97),
                    s.get_graphic(365, 0, 72, 97),
                    s.get_graphic(292, 98, 72, 97)]

        for i in range(len(graphics[1:])):
            self.walking_player_graphic_r.append(graphics[i+1])
            rotated_image = pygame.transform.flip(graphics[i+1], True, False)
            self.walking_player_graphic_l.append(rotated_image)

        self.standing_right = graphics[0]
        self.standing_left = pygame.transform.flip(self.standing_right, True, False)

        self.image = self.standing_right

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))

    def update(self, ground, walls, player):
        # start moving only when chasing the player
        if self.is_chasing and self.pos_y - 10 < player.pos_y < self.pos_y + 70:
            if self.pos_x < player.pos_x:
                self.velocity_x = 2
            elif self.pos_x > player.pos_x:
                self.velocity_x = -2
        else:
            self.velocity_x = 0

        self.pos_x += self.velocity_x
        self.pos_y += self.velocity_y

        if self.velocity_x > 0:
            self.image = self.walking_player_graphic_r[self.index_r]
            self.index_r += 1
            self.orientation = "right"

            if self.index_r == len(self.walking_player_graphic_r):
                self.index_r = 0

        elif self.velocity_x < 0:
            self.image = self.walking_player_graphic_l[self.index_l]
            self.index_l += 1
            self.orientation = "left"

            if self.index_l == len(self.walking_player_graphic_l):
                self.index_l = 0

        else:
            if self.orientation == "right":
                self.image = self.standing_right
            else:
                self.image = self.standing_left

        self.velocity_y += self.gravity

        for block in ground:
            if block.left - 60 < self.pos_x < block.right - 5:
                if block.top <= self.pos_y + 72 and self.pos_y <= block.centery:
                    self.pos_y = block.top - 72
                    self.velocity_y = 0

        for block in walls:
            if block.top - 72 < self.pos_y < block.bottom:
                if block.left <= self.pos_x + 72 and self.pos_x <= block.centerx and self.velocity_x > 0:
                    self.pos_x = block.left - 70

                if block.right >= self.pos_x >= block.centerx and self.velocity_x < 0:
                    self.pos_x = block.right


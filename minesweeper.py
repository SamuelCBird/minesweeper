import pygame
import random
import timer_widget as timer
import threading
import time
import constants


class Smiley(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = image_dict.get("smile")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.dead = False
        self.cool = False

    def draw(self, surface):
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)

    def change_face(self, face="smile"):
        if self.dead:
            face = "dead"
        elif self.cool:
            face = "cool"

        if face == "shock":
            self.image = image_dict.get("scared")
        elif face == "dead":
            self.dead = True
            self.image = image_dict.get("dead")
        elif face == "cool":
            self.cool = True
            self.image = image_dict.get("cool")
        elif face == "smile":
            self.image = image_dict.get("smile")
        else:
            return


class Hitbox(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 20])

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


# basic sprite class
class Sprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image_dict.get("unclicked")
        self.rect = self.image.get_rect()
        self.image.blit(self.image, self.rect)

        self.rect.x, self.rect.y = x * BLOCK_SIZE, y * BLOCK_SIZE

        # hitbox used to gather numbers of nearby bombs
        self.hitbox = Hitbox(self.rect.x - 2, self.rect.y - 2)

        self.unmarked = True
        self.flagged = False
        self.qmarked = False
        self.clicked = False
        self.mine = False
        self.number = 0
        self.endgame = False

    def check_if_empty(self):
        for spr in all_sprites.sprites():
            if spr.clicked:
                continue
            elif self.hitbox.rect.colliderect(spr.hitbox.rect) and not spr.mine and not spr.flagged:
                spr.left_clicked()

    def configure_number(self):
        for spr in mine_sprites.sprites():
            if self.hitbox.rect.colliderect(spr.hitbox.rect):
                self.number += 1

    def left_clicked(self):
        # hitboxes.add(self.hitbox)

        self.clicked = True
        if self.mine:
            if not self.flagged:
                self.end_game()

        elif self.number != 0:
            if not self.flagged:
                self.image = image_dict.get(str(self.number))
        else:
            if not self.flagged:
                self.image = image_dict.get("clicked_empty")
                self.check_if_empty()

    def right_clicked(self):
        # this functionality in there but can't remember how exactly it works
        # if self.number != 0:
        #     self.check_if_empty()
        if self.clicked:
            return
        else:
            if self.unmarked:
                self.image = image_dict.get("flagged")
                self.unmarked = False
                self.qmarked = False
                self.flagged = True
                flagged_sprites.add(self)
                self.check_flagged_sprites()
            elif self.flagged:
                self.image = image_dict.get("unclicked_qmark")
                self.flagged = False
                self.unmarked = False
                self.qmarked = True
                flagged_sprites.remove(self)
                self.check_flagged_sprites()
            else:
                self.image = image_dict.get("unclicked")
                self.qmarked = False
                self.flagged = False
                self.unmarked = True
                self.check_flagged_sprites()

    def check_flagged_sprites(self):
        if len(flagged_sprites.sprites()) == len(mine_sprites.sprites()):
            i = 1
            for spr in flagged_sprites.sprites():
                if mine_sprites.has(spr):
                    if i == len(mine_sprites.sprites()):
                        new_smiley.change_face("cool")
                        self.end_game()
                        break
                    i += 1
                else:
                    break

    def end_game(self):
        # END GAME
        self.endgame = True
        for mine in mine_sprites:
            if mine.clicked:
                new_smiley.change_face("dead")
                mine.image = image_dict.get("exploded")
            elif mine.flagged:
                pass
            else:
                mine.image = image_dict.get("bomb")
        for spr in all_sprites:
            if spr.flagged and not spr.mine:
                spr.image = image_dict.get("bomb_cross")
            if spr.qmarked and not spr.mine:
                continue


def setup_game():
    # fill the game board with unclicked sprites
    for x in range(game_board_size):
        for y in range(game_board_size):
            spr = Sprite(x, y)
            spr.add(all_sprites)

    # choose random sprites to be mines and add to temporary list
    for i in range(mines_ratio.get(str(game_board_size))):
        random_sprite = None
        while random_sprite is None:
            random_sprite = random.choice(all_sprites.sprites())
            if random_sprite in mine_sprites.sprites():
                random_sprite = None
            else:
                mine_sprites.add(random_sprite)
                random_sprite.mine = True

    for spr in all_sprites.sprites():
        if not spr.mine:
            spr.configure_number()

    # create mine counter
    mine_counter = timer.WholeFace(3, (0, 0), "mine_counter")
    timer_widget_group.add(mine_counter)
    mine_counter.display(len(mine_sprites.sprites()))

    # create stopwatch
    stopwatch_timer = timer.WholeFace(3, (0, 0), "stopwatch")
    stopwatch_widget_group.add(stopwatch_timer)
    stopwatch_timer.display(0)


def load_images():
    images = {}
    image_names = ["1", "2", "3", "4", "5", "6", "7", "8", "bomb", "bomb_cross",
                   "clicked_empty", "clicked_qmark", "exploded", "flagged", "unclicked", "unclicked_qmark",
                   "cool", "dead", "scared", "smile"]
    for name in image_names:
        image = pygame.image.load(f"images/{name}.png")
        images[name] = image

    return images


def update_mine_counter():
    for count in timer_widget_group:
        if count.ID == "mine_counter":
            mine_len = len(mine_sprites.sprites())
            flag_len = len(flagged_sprites.sprites())
            if mine_len - flag_len < 0:
                count.display(0)
            else:
                count.display(mine_len - flag_len)


def get_offset_mouse_pos():
    # offset mouse x, y
    # mouse(x, y) measured from main surface
    # sprite(x, y) measured by game_display surface
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x, y = GAME_DISPLAY_ANCHOR
    mouse_x -= x
    mouse_y -= y
    return mouse_x, mouse_y


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and (
                event.key == pygame.K_ESCAPE
                )):
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            new_smiley.change_face("shock")
            mouse_position = get_offset_mouse_pos()
            for spr in all_sprites:
                if spr.rect.collidepoint(mouse_position):
                    spr.left_clicked()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_position = get_offset_mouse_pos()
            for spr in all_sprites:
                if spr.rect.collidepoint(mouse_position):
                    spr.right_clicked()
        elif event.type == pygame.MOUSEBUTTONUP:
            # at the moment the the button opens before the mouse button up
            new_smiley.change_face()


def stopwatch():
    # if timer gets to 999 .display method just returns so
    # 999 just remains on the display
    i = 0
    while not end_game:
        for widget in stopwatch_widget_group.sprites():
            widget.display(i)
        time.sleep(1)
        i += 1


if __name__ == "__main__":
    # --==| GAME SETUP |==--
    pygame.init()

    # define some colours
    DEFAULT_GREY = constants.DEFAULT_GREY

    # define game settings
    BLOCK_SIZE = 16
    game_board_size = 16
    mines_ratio = {"9": 10,
                   "16": 40,
                   "24": 99}

    start_game = False
    end_game = False

    image_dict = load_images()

    # set up the main surface
    main_window_width = 276
    main_window_height = 316
    main_window = pygame.display.set_mode((main_window_width, main_window_height))
    main_window.fill(DEFAULT_GREY)
    pygame.display.set_caption("Sweeper!")

    # todo - need to make these a child of main_window
    # surface for mines remaining counter
    COUNTER_DISPLAY_ANCHOR = 10, 10
    counter_display_width_height = 51, 31
    counter_display = pygame.Surface(counter_display_width_height)
    counter_display.fill((0, 0, 0))

    # surface for mines remaining counter
    TIMER_DISPLAY_ANCHOR = 214, 10
    timer_display_width_height = 51, 31
    timer_display = pygame.Surface(timer_display_width_height)
    timer_display.fill((0, 0, 0))

    # surface for smiley
    SMILEY_DISPLAY_ANCHOR = 122, 10
    smiley_display_width_height = 31, 31
    smiley_display = pygame.Surface(smiley_display_width_height)

    # create surface for game area
    GAME_DISPLAY_ANCHOR = 10, 50
    game_display_width_height = BLOCK_SIZE * game_board_size
    game_display = pygame.Surface((game_display_width_height, game_display_width_height))
    game_display.fill(DEFAULT_GREY)


    # create groups for different sprite types
    all_sprites = pygame.sprite.Group()
    mine_sprites = pygame.sprite.Group()
    number_sprites = pygame.sprite.Group()
    flagged_sprites = pygame.sprite.Group()

    # group for timer widget
    timer_widget_group = pygame.sprite.Group()

    # group for stopwatch widget
    stopwatch_widget_group = pygame.sprite.Group()

    # todo - stop clicks after endgame apart from smiley face
    new_smiley = Smiley()

    setup_game()

    # set up stopwatch
    stopwatch_thread = threading.Thread(target=stopwatch)
    stopwatch_thread.setDaemon(True)
    stopwatch_started = False

    def start_stopwatch():
        stopwatch_thread.start()

    while True:
        event_handler()
        pygame.display.update()
        main_window.blit(game_display, GAME_DISPLAY_ANCHOR)
        main_window.blit(counter_display, COUNTER_DISPLAY_ANCHOR)
        main_window.blit(timer_display, TIMER_DISPLAY_ANCHOR)
        main_window.blit(smiley_display, SMILEY_DISPLAY_ANCHOR)

        update_mine_counter()
        stopwatch_widget_group.draw(timer_display)
        stopwatch_widget_group.update()

        timer_widget_group.draw(counter_display)
        timer_widget_group.update()
        all_sprites.draw(game_display)

        new_smiley.draw(smiley_display)

        # start stopwatch on first click
        for sprite in all_sprites.sprites():
            if sprite.clicked or sprite.flagged:
                if not stopwatch_started:
                    start_stopwatch()
                    stopwatch_started = True
            # and check for end game scenario
            if sprite.endgame:
                end_game = True

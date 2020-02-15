import pygame


class Segment(pygame.sprite.Sprite):

    def __init__(self, pointlist, xy):
        pygame.sprite.Sprite.__init__(self)
        self.WHITE = (255, 255, 255)
        self.pointlist = pointlist
        self.image = pygame.Surface((13, 13))
        self.image.fill(self.WHITE)
        self.shape = pygame.draw.polygon(self.image, (0, 0, 0), self.pointlist, 0)
        self.image.set_colorkey(self.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy

    def turn_on(self):
        self.shape = pygame.draw.polygon(self.image, (252, 13, 27), self.pointlist, 0)

    def turn_off(self):
        self.shape = pygame.draw.polygon(self.image, (66, 2, 6), self.pointlist, 0)


class SingleFace(pygame.sprite.Sprite):

    def __init__(self, xy, ident):
        pygame.sprite.Sprite.__init__(self)
        self.ID = ident
        self.image = pygame.Surface((17, 31))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = xy
        self.pointlist_dict = {"left": [(0, 0), (3, 3), (3, 9), (0, 12), (0, 0)],
                               "right": [(0, 3), (3, 0), (3, 12), (0, 9), (0, 3)],
                               "top": [(0, 0), (12, 0), (9, 3), (3, 3), (0, 0)],
                               "bottom": [(3, 0), (9, 0), (12, 3), (0, 3), (3, 0)],
                               "middle": [(0, 2), (2, 0), (10, 0), (12, 2), (10, 4), (2, 4), (0, 2)]}
        self.segment_dict = {}
        self.segments = pygame.sprite.Group()
        self.init_segments()

    def display(self, number):
        # segments configured like so
        #   2
        # 1   3
        #   4
        # 5   7
        #   6

        if number not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            return
        elif number == "1":
            self.segment_dict.get("1").turn_off()
            self.segment_dict.get("2").turn_off()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_off()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_off()
            self.segment_dict.get("7").turn_on()
        elif number == "2":
            self.segment_dict.get("1").turn_off()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_on()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_off()
        elif number == "3":
            self.segment_dict.get("1").turn_off()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_on()
        elif number == "4":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_off()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_off()
            self.segment_dict.get("7").turn_on()
        elif number == "5":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_off()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_on()
        elif number == "6":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_off()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_on()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_on()
        elif number == "7":
            self.segment_dict.get("1").turn_off()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_off()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_off()
            self.segment_dict.get("7").turn_on()
        elif number == "8":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_on()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_on()
        elif number == "9":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_on()
            self.segment_dict.get("5").turn_off()
            self.segment_dict.get("6").turn_off()
            self.segment_dict.get("7").turn_on()
        elif number == "0":
            self.segment_dict.get("1").turn_on()
            self.segment_dict.get("2").turn_on()
            self.segment_dict.get("3").turn_on()
            self.segment_dict.get("4").turn_off()
            self.segment_dict.get("5").turn_on()
            self.segment_dict.get("6").turn_on()
            self.segment_dict.get("7").turn_on()

    def update(self, *args):
        pygame.sprite.Sprite.update(self)
        self.segments.draw(self.image)

    def init_segments(self):
        counter = 0
        segs = ["left", "top", "right", "middle", "left", "bottom", "right"]
        coordinates = [(1, 2), (2, 1), (12, 2), (2, 13), (1, 16), (2, 26), (12, 16)]

        for seg in segs:
            new_segment = Segment(self.pointlist_dict.get(seg), coordinates[counter])
            self.segment_dict[str(counter + 1)] = new_segment
            self.segments.add(new_segment)
            counter += 1


class WholeFace(pygame.sprite.Sprite):

    def __init__(self,  faces, xy, ident):
        pygame.sprite.Sprite.__init__(self)
        self.ID = ident
        self.faces = faces
        self.faces_width = 17
        self.image = pygame.Surface((self.faces_width * self.faces, 31))
        self.rect = self.image.get_rect()
        x, y = xy
        self.rect.x = x
        self.rect.y = y
        self.face_widgets = pygame.sprite.Group()
        self.build_faces()

    def display(self, number):
        number = str(number)
        number_len = len(number)

        # if there are not enough faces for the number, return
        if number_len > self.faces:
            return

        # below adds leading zeros
        elif number_len < self.faces:
            i = number_len
            while i < self.faces:
                number = f'0{number}'
                i += 1
            number_len = len(number)

        # displays the number
        while number_len > 0:
            for face in self.face_widgets:
                if face.ID == number_len:
                    face.display(number[number_len - 1])
            number_len -= 1

    def build_faces(self):
        for i in range(self.faces):
            new_face = SingleFace((self.faces_width * i, 0), i + 1)
            self.face_widgets.add(new_face)

    def update(self, *args):
        pygame.sprite.Sprite.update(self)
        self.face_widgets.draw(self.image)
        self.face_widgets.update()

    def draw(self, surface):
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()

    def event_handler():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_ESCAPE)):
                pygame.quit()
                quit()

    main_window_width = 51
    main_window_height = 31
    main_window = pygame.display.set_mode((main_window_width, main_window_height))
    # main_window.fill((0, 0, 0))
    pygame.display.set_caption("Timer Widget")

    # demo the widget
    whole_faces = pygame.sprite.Group()
    the_whole_face = WholeFace(3, (0, 0), "demo")
    whole_faces.add(the_whole_face)

    the_whole_face.display(99)

    while True:
        event_handler()
        pygame.display.update()

        whole_faces.draw(main_window)
        whole_faces.update()

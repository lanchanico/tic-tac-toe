import sys
import pygame
from random import choice, randint
from itertools import cycle

CAPTION = 'tic tac toe'
SCREEN_SIZE = (300, 300)
MARGIN = 5
FIELD_SIZE = 3
TILE_SIZE = SCREEN_SIZE[0] // 3 
PLAY_RECT = pygame.Rect(0, 0, 300, 300)

CROSS = pygame.image.load("images/cross.png")
CIRCLE = pygame.image.load("images/crl.png")


class TicTacToe:
    def __init__(self):
        self.FIELD_SIZE = 3
        self.field = {}
        self.turn = 0
        self.win = None
    
    def get_field(self):
        return self.field
    
    def init_game(self):
        for y in range(self.FIELD_SIZE):
            for x in range(self.FIELD_SIZE):
                self.field[(y, x)] = self.turn
        self.turn = cycle([1, 2])
    
    def make_turn(self, pos):
        self.field[pos] = next(self.turn)
    
    def check_win(self):
        for i in range(self.FIELD_SIZE):
            row = []
            col = []
            for j in range(self.FIELD_SIZE):
                row.append(self.field[(i, j)])
                col.append(self.field[(j, i)])
            
            if len(set(row)) == 1 and row[0] != 0:
                return row[0]
            elif len(set(col)) == 1 and col[0] != 0:
                return col[0]

        main_d = []
        side_d = []

        for j in range(self.FIELD_SIZE):
            main_d.append(self.field[(j, j)])
            side_d.append(self.field[(j, abs(j - self.FIELD_SIZE + 1))])
        
        if len(set(main_d)) == 1 and main_d[0] != 0:
            return main_d[0]
        elif len(set(side_d)) == 1 and side_d[0] != 0:
            return side_d[0]
        
        if 0 not in self.field.values():
            return True
        
    
    def clear(self):
        self.turn = 0
        self.init_game()


class Game:
    def __init__(self):
        self.tic_tac_toe = TicTacToe()
        self.tic_tac_toe.init_game()
        self.done = False

    def set_tile_state(self, pos, turn):
        row, col = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
        self.tic_tac_toe.make_turn((row, col))

    def update(self):
        self.tic_tac_toe.win = self.tic_tac_toe.check_win()
        if self.tic_tac_toe.win:
            self.done = True

    def draw_back(self, surf):
        for y in range(self.tic_tac_toe.FIELD_SIZE):
            for x in range(self.tic_tac_toe.FIELD_SIZE):
                pygame.draw.rect(surf, pygame.Color('lightgray'), 
                                 (x * TILE_SIZE + MARGIN, y * TILE_SIZE + MARGIN, 
                                 TILE_SIZE - MARGIN * 2, TILE_SIZE - MARGIN * 2), 
                                 0, 10)
                

    def draw(self, surf):
        self.draw_back(surf)

        field = self.tic_tac_toe.get_field()
        for pos in field.keys():
            if field[pos] == 1:
                draw_x(surf, pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
            elif field[pos] == 2:
                draw_o(surf, pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
    
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            self.set_tile_state(event.pos, self.tic_tac_toe.turn)


class Control:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False
        self.state = Game()
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.state.get_event(event)

    def update(self):
        self.state.update()
        if self.state.done:
            self.done = True
    
    
    def draw(self):
        self.state.draw(self.screen)
    
    def main_loop(self):
        while not self.done:
            self.screen.fill(pygame.Color('beige'))
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

    def display_fps(self):
        """Show the programs FPS in the window handle."""
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)


def draw_x(surf: pygame.Surface, x, y):
    rect = surf.get_rect()
    image = pygame.transform.scale(
        CROSS, 
        (TILE_SIZE - MARGIN * 3, TILE_SIZE - MARGIN * 3))
    surf.blit(image, (x + MARGIN, y + MARGIN))
    

def draw_o(surf: pygame.Surface, x, y):
    rect = surf.get_rect()
    image = pygame.transform.scale(
        CIRCLE, 
        (TILE_SIZE - MARGIN * 3, TILE_SIZE - MARGIN * 3))
    surf.blit(image, (x + MARGIN, y + MARGIN))


def main():
    pygame.init()

    pygame.display.set_mode(SCREEN_SIZE)
    Control().main_loop()


main()

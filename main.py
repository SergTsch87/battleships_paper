#!usr/bin/env
import pygame, sys

import pygame.draw_py

# env1\bin\python -m pip freeze > requirements.txt
# env2\bin\python -m pip install -r requirements.txt

SCREEN_WIDTH, SCREEN_HIGHT = 600, 600
LINE_WIDTH = 5
CELL_SIZE = 60
BOARD_SIZE = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOWER_COLOR = (150, 150, 150)
BASE_COLOR = WHITE

pygame.init()


class Board:
    def __init__(self, size = BOARD_SIZE) -> None:
        self.size = size
        
            # self.board = [["" for _ in range(size)] for _ in range(size)]
        # Швидший аналог цього коду:
        row = [''] * size
        self.board = [row[:] for _ in range(size)]
        self.ships = [] # Додаємо список для кораблів

    def add_ship(self, ship):
        self.ships.append(ship)
        

    def reset(self):
        row = [''] * self.size
        self.board = [row[:] for _ in range(self.size)]

    # draw_x / draw_hit / draw_x_hit
    def draw_x_hit(self, screen, col, row):
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), 
                                      ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
        
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20),
                                      ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20), LINE_WIDTH)

    # draw_dot / draw_miss / draw_dot_miss
    def draw_dot_miss(self, screen, col, row):
        pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 4), (CELL_SIZE // 4 + 1), LINE_WIDTH)

    def draw_x_or_dot(self, screen, row, col):
        if self.board[row][col] == "X":
            self.draw_x_hit(screen, col, row)
        elif self.board[row][col] == ".":
            self.draw_dot_miss(screen, col, row)

    def draw_grid(self, screen):
        for row in range(1, self.size):
            pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, SCREEN_HIGHT), LINE_WIDTH)

    # Малює сітку та символи на полі
    def draw(self, screen):
        self.draw_grid(screen)

        for row in range(self.size):
            for col in range(self.size):
                self.draw_x_or_dot(screen, row, col)

    # Вставити символ у порожню чарунку
    def update(self, row, col, player_symbol):
        if self.board[row][col] == "":
            self.board[row][col] = player_symbol
            return True
        
        return False

    def check_win(self):
        for ship in self.ships:
            if ship.state != 'sink':  # Якщо є хоча б один не потоплений корабель
                return False
        
        return True # Якщо усі кораблі потоплені


# для гравця (наприклад, людина або комп’ютер)
class Player:
    def __init__(self, symbol) -> None:
        self.symbol = symbol

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        pygame.display.set_caption("Battleships Paper Grid")
        self.board = Board()
        self.players = [Player("I"), Player("Other")]
        self.current_player_index = 0
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board.reset()
        self.current_player_index = 0
        self.game_over = False
        self.winner = None

    def switch_player(self): # 0 or 1  >>>  "I" or "Other"
        self.current_player_index = 1 - self.current_player_index

    def process_turn(self, row, col):
        current_player = self.players[self.current_player_index]
        opponent_board = self.board if self.current_player_index == 1 else self.board  # передбачено дві дошки

        if opponent_board.board[row][col] == '':  # Промах
            opponent_board.update(row, col, '.')
            self.switch_player()
            return False  # Гра продовжується
        
        elif opponent_board.board[row][col] == 'S':  # Влучив у корабель
            opponent_board.update(row, col, 'X')
            for ship in opponent_board.ships:
                if ship.contains_position(row, col):
                    ship.hit()
                    if ship.is_sunk():
                        # Позначаємо знищений корабель, та змінюємо його стан
                        ship.state = 'sink'
                    break
            # Перевірка на перемогу
            if opponent_board.check_win():
                self.game_over = True
                self.winner = current_player.symbol
            
            return True # Гра триває
        
        return False


    def change_color(self, rect, mouse_pos):
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOWER_COLOR, rect)
        else:
            pygame.draw.rect(self.screen, BASE_COLOR, rect)

    def change_color_for_rects(self, mouse_pos):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self.change_color(rect, mouse_pos)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Обробка курсору та малювання дошки

                mouse_pos = pygame.mouse.get_pos()
                # Очищення екрану
                self.screen.fill(WHITE)
                
                self.change_color_for_rects(mouse_pos)

                # Temp:
                # for row in range(BOARD_SIZE):
                #     for col in range(BOARD_SIZE):
                #         if col <= 5:
                #             self.board.draw_x_hit(self.screen, col, row)
                #         else:
                #             self.board.draw_dot_miss(self.screen, col, row)
                    
                # if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                #     mouse_x, mouse_y = event.pos
                #     clicked_row = mouse_y // CELL_SIZE
                #     clicked_col = mouse_x // CELL_SIZE

                #     self.game_over, self.winner, count_step, dict_winning_coords = self.process_turn(clicked_row, clicked_col, count_step, dict_winning_coords)
                    
            # Малювання дошки поверх усього екрану
            self.board.draw(self.screen)
            # Оновлення дисплею
            pygame.display.flip()

        pygame.quit()
        sys.exit()


class Ship:
    def __init__(self, size, x, y, orientation) -> None:
        self.size = size
        self.hits = 0
        self.state = 'norm' # Початковий стан корабля   norm / hit / sink
        self.positions = self.calculate_positions(x, y, orientation)

    def calculate_positions(self, x, y, orientation):
        positions = []
        if orientation == 'horz':
            for i in range(self.size):
                positions.append((x, y + i))
        
        else:  # orientation == 'vert'
            for i in range(self.size):
                positions.append((x + i, y))
        
        return positions
    
    def contains_position(self, row, col):
        return (row, col) in self.positions
    
    def hit(self):
        self.hits += 1
        if self.hits == self.size:
            self.state = 'sink'

    def is_sunk(self):
        return self.state == 'sink'


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
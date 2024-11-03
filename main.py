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
        

    def reset(self):
        row = [''] * self.size
        self.board = [row[:] for _ in range(self.size)]

    # draw_x / draw_hit / draw_x_hit
    def draw_x_hit(self, screen, col, row):
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, row * CELL_SIZE + 5), 
                                      ((col + 1) * CELL_SIZE - 10, (row + 1) * CELL_SIZE - 5), LINE_WIDTH)
        
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 10, (row + 1) * CELL_SIZE - 5),
                                      ((col + 1) * CELL_SIZE - 10, row * CELL_SIZE + 5), LINE_WIDTH)

    # draw_dot / draw_miss / draw_dot_miss
    def draw_dot_miss(self, screen, col, row):
        pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 10), (CELL_SIZE // 10 - 5), LINE_WIDTH)

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
        pass
        # Чи є хоч один цілий корабель суперника?


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
        self.currrent_player_index = 0
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board.reset()
        self.currrent_player_index = 0
        self.game_over = False
        self.winner = None

    def switch_player(self): # 0 or 1  >>>  "I" or "Other"
        self.currrent_player_index = 1 - self.currrent_player_index

    def process_turn():
        pass
        # Виграв / Не виграв / Зміна гравця
        # Покроковий процес гри

        # 1) Кожен гравець розставляє свої кораблі
        # 2) Перевірка розміщення кораблів за правилами
        # 3) Вибір гравця / Зміна гравця
        # 4) Показ поля суперника з його прихованими цілими та поціленими кораблями
        # 5) Курсором / Вводом у консоль  задаємо координати пострілу

        # 6) Якщо влучив:
        #      Якщо є цілий корабель суперника:
        #          go to: 4
        #      Інакше:
        #          Цей гравець переміг!)
        #   Інакше (не влучив):
        #          go to: 3
             

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
    def __init__(self, size, state, x, y) -> None:
        self.size = size
        self.state = state # norm / hit / sink
        self.x = x
        self.y = y


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
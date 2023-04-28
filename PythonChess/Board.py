import pygame
import os
from math import floor

from StockfishAPI import check_legal, get_next_fen

piece_imgs = {
    "bp": pygame.image.load("texture\\black\\pawn.png"),
    "bR": pygame.image.load("texture\\black\\rook.png"),
    "bN": pygame.image.load("texture\\black\\knight.png"),
    "bB": pygame.image.load("texture\\black\\bishop.png"),
    "bK": pygame.image.load("texture\\black\\king.png"),
    "bQ": pygame.image.load("texture\\black\\queen.png"),
    "wp": pygame.image.load("texture\\white\\pawn.png"),
    "wR": pygame.image.load("texture\\white\\rook.png"),
    "wN": pygame.image.load("texture\\white\\knight.png"),
    "wB": pygame.image.load("texture\\white\\bishop.png"),
    "wK": pygame.image.load("texture\\white\\king.png"),
    "wQ": pygame.image.load("texture\\white\\queen.png"),
}

for i in piece_imgs:
    piece_imgs[i] = pygame.transform.scale(piece_imgs[i], (80, 80))

l = "abcdefgh"

class Board:
    def __init__(self, surface, cols, rows):
        self.surface = surface
        self.squares = [[]]

        self.cols = cols
        self.rows = rows

        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.load_fen(self.fen)

        self.selected_square = (None, None)
        self.move = ""

        for i in range(self.cols):
            self.squares.append([])
            for j in range(self.rows):
                self.squares[i].append(
                    Square(
                        self.surface, 
                        (j * 80, i * 80, 80, 80), 
                        (226, 204, 180) if (i + j) % 2 == 0 else (159, 115, 95)
                    )
                )

    def render(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.squares[i][j].draw()
                
                if self.board[i][j] == "--":
                    continue

                self.surface.blit(piece_imgs[self.board[i][j]], (j * 80, i * 80))
                    


    def select(self, position):
        x = floor(position[1]/80)
        y = floor(position[0]/80)

        if self.selected_square != (None, None):
            self.move += l[y]
            self.move += str(8 - x)
            print(self.move)
            if check_legal(self.fen, self.move):
                self.fen = get_next_fen(self.fen, self.move)
                pass
            self.selected_square = (None, None)
            self.move = ""
        else:
            if self.squares[x][y].selected == False:
                if self.board[x][y] != "--":
                    if self.board[x][y][0] == self.fen.split(" ")[1]:
                        self.squares[x][y].colour = (100, 255, 255)
                        self.squares[x][y].selected = True
                        self.selected_square = (x, y)
                        self.move = l[y] + str(8 - x)
            else:
                self.squares[x][y].colour = (159, 115, 95) if (x + y) % 2 == 0 else (226, 204, 180)
                self.squares[x][y].selected = False


    def unselect_all(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.squares[i][j].colour = (159, 115, 95) if (i + j) % 2 == 0 else (226, 204, 180)
                self.squares[i][j].selected = False

    def load_fen(self, fen):
        self.fen = fen

        self.board = []
        for row in self.fen.split('/'):
            brow = []
            for c in row:
                if c == ' ':
                    break
                elif c in '12345678':
                    brow.extend(['--'] * int(c))
                elif c == 'p':
                    brow.append('bp')
                elif c == 'P':
                    brow.append('wp')
                elif c > 'Z':
                    brow.append('b'+c.upper())
                else:
                    brow.append('w'+c)

            self.board.append(brow)
            

class Square:
    def __init__(self, surface, rect, colour):
        self.surface = surface
        self.colour = colour
        self.rect = pygame.Rect(rect)
        self.selected = False
        
    def draw(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)




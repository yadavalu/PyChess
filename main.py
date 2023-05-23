import os
import pygame
pygame.init()

import Pieces
import Board
import Analysis

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board.Board(screen)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = Pieces.Pieces(screen, "4k3/7P/6P1/1p6/8/8/p7/4K3 w - - 0 1")

ignore = False

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse
            pieces.mouse_pos = pos
            index = board.select(pos, pieces)
            if not pieces.select(*index):
                board.unselect()
                ignore = True
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            if not ignore:
                pos = pygame.mouse.get_pos()
                button = pygame.mouse
                pieces.mouse_pos = pos
                index = board.drop(pos)
                flag = None
                if pieces.promotion:
                    flag = board.get_promotions(pieces.analysis.turn)
                if not pieces.drop(*index, flag=flag):
                    board.unselect()
            else:
                ignore = False


    screen.fill((36, 34, 30))
    board.render(pieces.analysis)
    pieces.mouse_pos = pygame.mouse.get_pos()
    board.mouse_pos = pygame.mouse.get_pos()
    pieces.render()
    pygame.display.update()

from re import T
import numpy as np
import cv2 as cv
import pyautogui
import pytesseract
from matplotlib import pyplot as plt
from operator import itemgetter
from BoardDefiner import BoardDefiner
from ChessBoardAuto import ChessBoardAuto
from agent2 import Agent2


def main():
    while(True):
        endGameByNew10MinRated = False
        board = ChessBoardAuto()
        chessSiteBoard = BoardDefiner()
        agent = Agent2()

        chessSiteBoard.takeScreenshotForFindingBoard()
        chessSiteBoard.findBoardBorders()
        chessSiteBoard.findBoardDimensions()
        chessSiteBoard.splitBoardIntoGrid()
        # board.moveMouseIntoGridCoords()
        side = chessSiteBoard.determineSide()
        board.currBoard = chessSiteBoard.findPieces()
        gameOver = False

        # '''
        if side == 0:
            print("Playing as White")
            currMove = 0
            chessSiteBoard.resetAfterMoveScreenshot()
            board.currBoard = chessSiteBoard.findPieces()
            board.currPlayerMove = 0
            side = 0
            board.printBoard()
            while not gameOver:
                # break
                if currMove == side:
                    moveList = board.getAllPossibleMoves()
                    if moveList == -1 or len(moveList) == 0:
                        print("Good Game, black won")
                        board.printBoard()
                        break
                    else:
                        moveIndex = agent.pickMove(moveList)
                        move = moveList[moveIndex]
                        movePieceLoc = move[1][0]
                        movePieceToLoc = move[1][1]
                        board.move(movePieceLoc[0], movePieceLoc[1],
                                   movePieceToLoc[0], movePieceToLoc[1])

                        chessSiteBoard.movePiece(movePieceLoc, movePieceToLoc)
                        # handle pawn promotion
                        if movePieceToLoc[0] == 0 and board.currBoard[movePieceToLoc[0]][movePieceToLoc[1]] == 1:
                            pyautogui.sleep(1)
                            print("Promoting Pawn")
                            chessSiteBoard.movePiece(
                                movePieceToLoc, movePieceToLoc)

                else:
                    diff = 0
                    while diff == 0:
                        diff = chessSiteBoard.findDifferences()
                        if chessSiteBoard.findNew10MinRatedChat() == 1:
                            endGameByNew10MinRated = True
                            print("Stopped by detecting - can create new game")
                            break
                        pyautogui.sleep(1)

                    if endGameByNew10MinRated:
                        break

                    board.currBoard = chessSiteBoard.findPieces()
                    board.currPlayerMove = 0
                    pyautogui.sleep(1)

                    if chessSiteBoard.checkGameOver() == 1:
                        print("Stopped by image recognition")
                        print("Good Game, black won")
                        board.printBoard()
                        break

                currMove = (currMove + 1) % 2
        else:
            print("Playing as Black")
            currMove = 0
            chessSiteBoard.resetAfterMoveScreenshot()

            # wait for white to move
            while(True):
                if not np.array_equal(np.array(chessSiteBoard.findPieces()) * -1, np.array(board.blackBoard)):
                    break
                else:
                    pyautogui.sleep(1)

            board.currBoard = list(np.array(chessSiteBoard.findPieces()) * -1)
            board.currPlayerMove = 0
            side = 0
            board.printBoard()
            while not gameOver:
                # break
                if currMove == side:
                    moveList = board.getAllPossibleMoves()
                    if moveList == -1 or len(moveList) == 0:
                        print("Good Game, white won")
                        board.printBoard()
                        break
                    else:
                        moveIndex = agent.pickMove(moveList)
                        move = moveList[moveIndex]
                        movePieceLoc = move[1][0]
                        movePieceToLoc = move[1][1]
                        board.move(movePieceLoc[0], movePieceLoc[1],
                                   movePieceToLoc[0], movePieceToLoc[1])

                        chessSiteBoard.movePiece(movePieceLoc, movePieceToLoc)
                        # handle pawn promotion
                        if movePieceToLoc[0] == 0 and board.currBoard[movePieceToLoc[0]][movePieceToLoc[1]] == 1:
                            pyautogui.sleep(1)
                            print("Promoting Pawn")
                            chessSiteBoard.movePiece(
                                movePieceToLoc, movePieceToLoc)

                else:
                    diff = 0
                    while diff == 0:
                        diff = chessSiteBoard.findDifferences()
                        if chessSiteBoard.findNew10MinRatedChat() == 1:
                            endGameByNew10MinRated = True
                            print("Stopped by detecting - can create new game")
                            break
                        pyautogui.sleep(1)

                    if endGameByNew10MinRated:
                        break

                    board.currBoard = list(
                        np.array(chessSiteBoard.findPieces()) * -1)
                    board.currPlayerMove = 0
                    pyautogui.sleep(1)

                    if chessSiteBoard.checkGameOver() == 1:
                        print("Stopped by image recognition")
                        print("Good Game, white won")
                        board.printBoard()
                        break

                currMove = (currMove + 1) % 2

        if chessSiteBoard.findNew10MinGameBoard() == -1:
            if chessSiteBoard.findNew10MinRatedChat() == -1:
                if endGameByNew10MinRated:
                    endGameByNew10MinRated = False
                else:
                    print("Can't Find New Game, Stopping Execution")
                    break
        pyautogui.sleep(10)
    # '''


if __name__ == "__main__":
    main()

import copy
from email.mime import base
from random import random
from time import time
import numpy as np
import pyautogui
from matplotlib import pyplot as plt

from BoardDefiner import BoardDefiner
from ChessBoard import ChessBoard
from Util import playBO5, readGenerationFile, writeToGenerationFile
from agent2 import Agent2

from getkeys import key_check


def playGameOnChessDotCom():
    while True:
        keys = key_check()
        print("waiting press B to start")
        if keys == "B":
            print("Starting")
            break

    while(True):
        quitLooping = False
        endGameByNew10MinRated = False
        board = ChessBoard()
        chessSiteBoard = BoardDefiner()
        agent = Agent2()

        chessSiteBoard.takeScreenshotForFindingBoard()
        chessSiteBoard.findBoardBorders()
        chessSiteBoard.findBoardDimensions()
        chessSiteBoard.splitBoardIntoGrid()
        side = chessSiteBoard.determineSide()
        board.currBoard = chessSiteBoard.findPieces()
        gameOver = False

        # '''
        if side == 0:
            # new game - clear old stuff, reset values
            print("Playing as White")
            currMove = 0
            chessSiteBoard.resetAfterMoveScreenshot()
            board.currBoard = chessSiteBoard.findPieces()
            side = 0
            board.printBoard(board.currBoard)
            while not gameOver:
                # if white move
                if currMove == side:

                    # get all moves
                    moveList = board.getAllMoves(True)

                    # if no moves then GG
                    if len(moveList) == 0:
                        print("Good Game, black won")
                        board.printBoard(board.currBoard)
                        break
                    else:
                        # look for valid move
                        while(True):
                            print()
                            moveIndex = agent.pickMove(
                                moveList, True, board.currBoard)
                            move = moveList[moveIndex]
                            movePieceLoc = move[1][0]
                            movePieceToLoc = move[1][1]
                            moveReturnCode = board.move(
                                movePieceLoc[0], movePieceLoc[1], movePieceToLoc[0], movePieceToLoc[1])
                            # if not valid move remove it from list and loop again
                            if moveReturnCode == -1:
                                moveList.remove(move)
                            # if valid move - move piece on site then check if pawn promotion occurred
                            else:
                                chessSiteBoard.movePiece(
                                    movePieceLoc, movePieceToLoc)

                                # handle pawn promotion
                                if moveReturnCode == 2:
                                    pyautogui.sleep(1)
                                    print("Promoting Pawn")
                                    chessSiteBoard.movePiece(
                                        movePieceToLoc, movePieceToLoc)
                                break

                # if black move
                else:

                    # busy loop until black moves
                    diff = 0
                    while diff == 0:
                        # calc diff from current state and previous after move photo
                        diff = chessSiteBoard.findDifferences()

                        # if resignation or user won and new game pops up then end busy loop
                        if chessSiteBoard.findNew10MinRatedChat() == 1:
                            print("Stopped by detecting - can create new game")
                            keys = key_check()
                            if keys == "H":
                                quitLooping = True
                                break
                            else:
                                print("Creating New Game")
                                chessSiteBoard.clickMouse()
                                endGameByNew10MinRated = True
                                break

                        pyautogui.sleep(1)

                    # if resignation or user won and new game pops up then end busy loop
                    if endGameByNew10MinRated:
                        break

                    # set board to after black moved
                    board.currBoard = chessSiteBoard.findPieces()
                    pyautogui.sleep(1)

                    # stop game if game over sign indicating user lost appears
                    # if chessSiteBoard.checkGameOver() == 1:
                    #    print("Stopped by image recognition")
                    #    print("Good Game, black won")
                    #    board.printBoard()
                    #    break

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
            side = 0
            board.printBoard(board.currBoard)
            while not gameOver:
                # break
                if currMove == side:
                    moveList = board.getAllMoves()
                    if len(moveList) == 0:
                        print("Good Game, white won")
                        board.printBoard(board.currBoard)
                        break
                    else:
                        # look for valid move
                        while(True):
                            print()
                            moveIndex = agent.pickMove(moveList)
                            move = moveList[moveIndex]
                            movePieceLoc = move[1][0]
                            movePieceToLoc = move[1][1]
                            moveReturnCode = board.move(
                                movePieceLoc[0], movePieceLoc[1], movePieceToLoc[0], movePieceToLoc[1])
                            # if not valid move remove it from list and loop again
                            if moveReturnCode == -1:
                                moveList.remove(move)
                            # if valid move - move piece on site then check if pawn promotion occurred
                            else:
                                chessSiteBoard.movePiece(
                                    movePieceLoc, movePieceToLoc)

                                # handle pawn promotion
                                if moveReturnCode == 2:
                                    pyautogui.sleep(1)
                                    print("Promoting Pawn")
                                    chessSiteBoard.movePiece(
                                        movePieceToLoc, movePieceToLoc)
                                break

                else:
                    diff = 0
                    while diff == 0:
                        diff = chessSiteBoard.findDifferences()

                        if chessSiteBoard.findNew10MinRatedChat() == 1:
                            print("Stopped by detecting - can create new game")
                            keys = key_check()
                            if keys == "H":
                                quitLooping = True
                                break
                            else:
                                print("Creating New Game")
                                chessSiteBoard.clickMouse()
                                endGameByNew10MinRated = True
                                break
                        pyautogui.sleep(1)

                    if endGameByNew10MinRated:
                        break

                    board.currBoard = list(
                        np.array(chessSiteBoard.findPieces()) * -1)
                    pyautogui.sleep(1)

                currMove = (currMove + 1) % 2

        keys = key_check()
        if keys == "H" or quitLooping:
            break

        if chessSiteBoard.findNew10MinGameBoard() == -1:
            if chessSiteBoard.findNew10MinRatedChat() == -1:
                if endGameByNew10MinRated:
                    endGameByNew10MinRated = False
                else:
                    print("Can't Find New Game, Stopping Execution")
                    break
        pyautogui.sleep(10)


def createBaseGenerationFile(agent, generation):

    writeToGenerationFile(agent.returnWeightScores(), generation)


def runOneGeneration(generation):
    sampleAgent = Agent2(0, 0, 0)
    if generation == 1:
        createBaseGenerationFile(sampleAgent, generation - 1)

    baseParameters = readGenerationFile(
        generation - 1, len(sampleAgent.returnWeightScores()))

    mutationsInPop = int(random() * 10)
    # print("Mutations: " + str(mutationsInPop))
    numAgentsInGeneration = 64
    agentList = []
    mutationsCreated = 0
    baseAgent = 0
    for a in range(numAgentsInGeneration):
        if baseAgent == 0:
            # print("Creating Base")
            baseAgent = baseAgent + 1
            newAgent = Agent2(copy.deepcopy(baseParameters))
            agentList.append(copy.deepcopy(newAgent))
        elif mutationsCreated != mutationsInPop:
            # print("Creating Mutation")
            mutationsCreated = mutationsCreated + 1
            newAgent = Agent2(copy.deepcopy(baseParameters), True)
            agentList.append(copy.deepcopy(newAgent))
        else:
            # print("Creating Normal Pop")
            newAgent = Agent2(copy.deepcopy(baseParameters), False)
            agentList.append(copy.deepcopy(newAgent))

    '''
    with open('./generation/' + 'parameters_' + str(len(sampleAgent.returnWeightScores())) + '/' + 'generationAgents_' + str(generation) + '.txt', 'w') as file:
        count = 0
        for agent in agentList:
            count = count + 1
            file.write(str(count) + ') ' + str(agent))
            file.write(':\n')
            for item in agent.returnWeightScores().items():
                file.write(item[0] + ':' + str(item[1]) + '\n')
    # '''

    playTournament(agentList, generation)


def playTournament(agentList, generation):
    newRound = []

    while(len(newRound) != 1):
        newRound.clear()
        numContestants = len(agentList)
        print(str(numContestants) + " Contestants")
        for i in range(int(numContestants/2)):
            winner = playBO5(agentList[i], agentList[numContestants - 1 - i])
            newRound.append(winner)
        agentList = copy.deepcopy(newRound)
    print("Tournament Winner: " + str(newRound[0]))

    winnerParameters = newRound[0].returnWeightScores()
    writeToGenerationFile(winnerParameters, generation)


def testBoard():
    agent = Agent2()
    board = ChessBoard()

    board.SetSide(3)
    board.printBoard(board.currBoard)
    board.InvertBoard()
    board.printBoard(board.currBoard)
    board.InvertBoard()
    board.printBoard(board.currBoard)


if __name__ == "__main__":
    # playGame()
    # testBoard()
    begin = time()

    for generation in range(1, 101):
        runOneGeneration(generation)

    elapsed = time() - begin
    print("Total Runtime for 100 generations is " + str(elapsed))
    # break
    # playBO5()

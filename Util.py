from random import random
from ChessBoard import ChessBoard
import pyautogui


def TiedGameDecider(board):
    sumCurrPlayer = 0
    sumEnemyPlayer = 0
    for col in board:
        for row in col:
            if row > 0:
                sumCurrPlayer = sumCurrPlayer + row
            else:
                sumEnemyPlayer = sumEnemyPlayer + abs(row)
    return sumCurrPlayer, sumEnemyPlayer


def printStatistics(agent1Wins, agent2Wins, tied):
    print("STATS:---------------------")
    print("Agent 1:", agent1Wins)
    print("Agent 2:", agent2Wins)
    print("Tied:   ", tied)
    print("---------------------------")


def playGame(agent1, agent2):
    board = ChessBoard()

    board.SetSide(1)

    currMove = 0
    count = 0
    winner = ""
    while(True):
        if currMove == 0:
            moveList = board.getAllMoves(False)
            if len(moveList) == 0:
                print("Good Game, black won")
                winner = "Black"
                break
            else:
                while(True):
                    if len(moveList) == 0:
                        print("Good Game, black won")
                        winner = "Black"
                        break
                    moveIndex = agent1.pickMove(
                        moveList, False, board.currBoard)
                    move = moveList[moveIndex]
                    movePieceLoc = move[1][0]
                    movePieceToLoc = move[1][1]
                    moveReturnCode = board.move(
                        movePieceLoc[0], movePieceLoc[1], movePieceToLoc[0], movePieceToLoc[1])
                    if moveReturnCode == -1:
                        moveList.remove(move)
                    else:
                        break

        else:
            moveList = board.getAllMoves(False)
            if len(moveList) == 0:
                print("Good Game, white won")
                winner = "White"
                break
            else:
                while(True):
                    if len(moveList) == 0:
                        print("Good Game, white won")
                        winner = "White"
                        break
                    moveIndex = agent2.pickMove(
                        moveList, False, board.currBoard)
                    move = moveList[moveIndex]
                    movePieceLoc = move[1][0]
                    movePieceToLoc = move[1][1]
                    moveReturnCode = board.move(
                        movePieceLoc[0], movePieceLoc[1], movePieceToLoc[0], movePieceToLoc[1])
                    if moveReturnCode == -1:
                        moveList.remove(move)
                    else:
                        break

        if winner != "":
            break

        if count == 500:
            print("Ending Game: Too Many Moves")
            currPlayerScore, enemyPlayerScore = TiedGameDecider(
                board.currBoard)

            if currPlayerScore == enemyPlayerScore:
                print("True Tie")
                winner = "None"
            elif currMove == 0:
                if currPlayerScore > enemyPlayerScore:
                    print("White Won")
                    winner = "White"
                else:
                    print("Black Won")
                    winner = "Black"
                break
            else:
                if currPlayerScore > enemyPlayerScore:
                    print("Black Won")
                    winner = "Black"
                else:
                    print("White Won")
                    winner = "White"
                break

        board.InvertBoard()
        currMove = (currMove + 1) % 2
        count = count + 1

    # board.printBoard(board.currBoard)

    return winner


def playBO5(agent1, agent2):
    agent1Wins = 0
    agent2Wins = 0
    tied = 0
    side = 0
    for i in range(5):
        winner = ""
        if side == 0:
            winner = playGame(agent1, agent2)
            if winner == "White":
                agent1Wins = agent1Wins + 1
            elif winner == "Black":
                agent2Wins = agent2Wins + 1
            else:
                tied = tied + 1
        else:
            winner = playGame(agent2, agent1)
            if winner == "White":
                agent2Wins = agent2Wins + 1
            elif winner == "Black":
                agent1Wins = agent1Wins + 1
            else:
                tied = tied + 1
        side = (side + 1) % 2

    printStatistics(agent1Wins, agent2Wins, tied)
    returnVal = 0
    if agent1Wins > agent2Wins:
        returnVal = 1
    elif agent2Wins > agent1Wins:
        returnVal = 2
    else:
        decider = int(random() * 10)
        if decider <= 4:
            returnVal = 1
        else:
            returnVal = 2

    if returnVal == 1:
        return agent1
    else:
        return agent2


def writeToGenerationFile(parameters, generation):
    with open('./generation/' + 'parameters_' + str(len(parameters)) + '/' + 'generation_' + str(generation) + '.txt', 'w') as file:
        file.write('Generation ' + str(generation) +
                   ' best agent parameters:\n')
        for a in parameters.items():
            file.write(a[0] + ':' + str(a[1]) + '\n')


def readGenerationFile(generation, parametersLen):
    parameters = {}
    with open('./generation/' + 'parameters_' + str(parametersLen) + '/' + 'generation_' + str(generation) + '.txt', 'r') as file:
        count = 0
        for line in file:
            if count == 0:
                count = count + 1
            else:
                lineStr = line.strip()
                lineList = lineStr.split(':')
                parameters[lineList[0]] = int(lineList[1])

    return parameters

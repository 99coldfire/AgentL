import random


class Agent2:
    pieceDict = {
        "pawn": 1,
        "rook": 2,
        "knight": 3,
        "bishop": 4,
        "queen": 5,
        "king": 6
    }

    parameters = {
        'pieceValueScoreWeight': 0,
        # 'destLocScoreWeight': 0
    }

    def calcMoveScore(self, move, board):
        score = 0
        score = score + \
            self.parameters['pieceValueScoreWeight'] * \
            self.pieceValueScore(move)
        # score = score + \
        #    self.parameters['destLocScoreWeight'] * \
        #    self.destLocScore(move, board)
        return score

    def __init__(self, *args):
        if len(args) != 3:
            parametersPassedIn = args[0]
            self.parameters = parametersPassedIn
            if len(args) == 2:
                mutation = args[1]
                for item in self.parameters.items():
                    self.parameters[item[0]] = self.parameters[item[0]
                                                               ] + random.randint(-5, 5)

                # if mutationChance <= 10:
                if mutation:
                    items = list(self.parameters.items())
                    index = random.randint(0, len(items) - 1)
                    self.parameters[items[index][0]] = self.parameters[items[index][0]
                                                                       ] + random.randint(-100, 100)

# ------------------------------NEW POP---------------------------------------------------------

    def returnWeightScores(self):
        return self.parameters


# -------------------------------------SCORING-----------------------------------------------

    def pieceValueScore(self, move):
        return self.pieceDict.get(move[0])

    def destLocScore(self, move, board):
        return abs(board[move[1][1][0]][move[1][1][1]])

    def hozMiddleScore():
        print()

    def vertMiddleScore():
        print()

    def pickMove(self, moveList, verbose, board):
        maxScore = -99999
        maxScoreIndex = []
        for i in range(len(moveList)):
            moveScore = self.calcMoveScore(moveList[i], board)
            if moveScore > maxScore:
                maxScore = moveScore
                maxScoreIndex.clear()
                maxScoreIndex.append(i)
            elif moveScore == maxScore:
                maxScoreIndex.append(i)

        if len(maxScoreIndex) > 1:
            index = random.randint(0, len(maxScoreIndex) - 1)
        else:
            index = 0

        if verbose:
            print("PickMove: ", moveList[index])

        return index

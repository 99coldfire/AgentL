import random


class GeneticFreakAgent:
    pieceDict = {
        "pawn": 1,
        "rook": 2,
        "knight": 3,
        "bishop": 4,
        "queen": 5,
        "king": 6
    }

    def calcMoveScore(self):
        print("Calculate Move Score")

    def pieceValueScore(self, move):
        print(move)

    def pickMove(self, moveList, verbose):
        if len(moveList) == 0:
            print("Length", len(moveList))
            index = random.randint(0, len(moveList) - 1)
        else:
            index = random.randint(0, len(moveList) - 1)
        if verbose:
            print("PickMove: ", moveList[index])
        print("PickMove: ", moveList[index])
        return index

import copy


class ChessBoard:

    # user = 1, opponent = -1
    userSide = 0

    currBoard = []

    whiteBoard = [[-2, -3, -4, -5, -6, -4, -3, -2],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 3, 4, 5, 6, 4, 3, 2]]

    blackBoard = [[-2, -3, -4, -6, -5, -4, -3, -2],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [2, 3, 4, 6, 5, 4, 3, 2]]

    testingBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 5, 0, 0, 0, 0]]

    pieceDict = {
        1: "pawn",
        2: "rook",
        3: "knight",
        4: "bishop",
        5: "queen",
        6: "king"
    }

    def InvertBoard(self):
        invertedBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]
        for row in range(8):
            for col in range(8):
                invertedRow = 4 + 3 - row
                invertedCol = 4 + 3 - col
                invertedBoard[invertedRow][invertedCol] = self.currBoard[row][col] * -1
        self.currBoard = invertedBoard

    def SetSide(self, side):
        if side == 1:
            self.currBoard = copy.deepcopy(self.whiteBoard)
        elif side == 2:
            self.currBoard = copy.deepcopy(self.blackBoard)
        else:
            self.currBoard = copy.deepcopy(self.testingBoard)

    def move(self, row1, col1, row2, col2):
        currBoardCopy = copy.deepcopy(self.currBoard)
        self.currBoard[row2][col2] = self.currBoard[row1][col1]
        self.currBoard[row1][col1] = 0

        # check if move does not put king in check
        kingLoc = self.getKingLoc()
        if self.checkLocForCheck(kingLoc[0], kingLoc[1])[0]:
            #print("Move puts king in check")
            self.currBoard = currBoardCopy
            return -1

        if self.currBoard[row2][col2] == 1 and row2 == 0:
            #print("Promoting Pawn to Queen")
            self.currBoard[row2][col2] = 5
            return 2
        return 1

    def getAllMoves(self, verbose):
        moveList = self.getMoves()
        kingLoc = self.getKingLoc()
        check, checkingPieceLoc = self.checkLocForCheck(
            kingLoc[0], kingLoc[1])

        if verbose:
            print("\nKing at ", kingLoc[0], ":",
                  kingLoc[1], ", Check: ", check)
            if check:
                print("Checking Piece Loc at: ", checkingPieceLoc)

        pathToChecker = self.getPathFromCheckerToKing(
            checkingPieceLoc, kingLoc, verbose)

        if check:
            moveList = self.kingCheckMoves(moveList, pathToChecker)

        if verbose:
            self.printMoveList(moveList)
        return moveList

    def getPathFromCheckerToKing(self, checkingPieceLoc, kingLoc, verbose):
        pathToChecker = []
        if checkingPieceLoc[0] != -1 or checkingPieceLoc[1] != -1:
            pathToChecker.append(checkingPieceLoc)
            rowDiff = checkingPieceLoc[0] - kingLoc[0]
            colDiff = checkingPieceLoc[1] - kingLoc[1]
            # diag
            if rowDiff != 0 and colDiff != 0 and abs(rowDiff) == abs(colDiff):
                rowPosNeg = rowDiff/abs(rowDiff)
                colPosNeg = colDiff/abs(colDiff)
                for i in range(1, abs(rowDiff)):
                    pathToChecker.append(
                        (int(kingLoc[0] + i * rowPosNeg), int(kingLoc[1] + i * colPosNeg)))
            # vertical
            elif rowDiff != 0 and colDiff == 0:
                rowPosNeg = rowDiff/abs(rowDiff)
                for i in range(1, abs(rowDiff)):
                    pathToChecker.append(
                        (int(kingLoc[0] + i * rowPosNeg), kingLoc[1]))
            # horizontal
            elif rowDiff == 0 and colDiff != 0:
                colPosNeg = colDiff/abs(colDiff)
                for i in range(1, abs(colDiff)):
                    pathToChecker.append(
                        (kingLoc[0], int(kingLoc[1] + i * colPosNeg)))

        if verbose:
            print("\nPath to Checker Loc")
            print(pathToChecker)
        return pathToChecker

    def kingCheckMoves(self, moveList, pathToChecker):
        kingCheckMoveList = []
        for move in moveList:
            if move[1][1] in pathToChecker and move[0] != "king":
                kingCheckMoveList.append(move)
            elif move[0] == "king":
                kingCheckMoveList.append(move)

        return kingCheckMoveList

    def checkLocForCheck(self, row, col):
        check = False
        checkingUnitLoc = (-1, -1)
        locCheckDictLoc = self.searchAroundLoc(row, col)
        for pieceInfo in locCheckDictLoc.items():
            try:
                piece = pieceInfo[1][0]
                pieceLoc = pieceInfo[1][1]
                if piece < 0:
                    pawnCheck = False
                    kingCheck = False
                    if piece == -1 and pieceLoc[0] == row - 1:
                        pawnCheck = True

                    if piece == -6 and (pieceLoc[0] == row - 1 or pieceLoc[0] == row + 1 or pieceLoc[1] == col - 1 or pieceLoc[1] == col + 1):
                        kingCheck = True

                    if len(pieceInfo[0]) > 5 and ((abs(piece) == 4 or abs(piece) == 5) or pawnCheck or kingCheck):
                        check = True
                        checkingUnitLoc = pieceLoc
                    elif len(pieceInfo[0]) <= 5 and ((abs(piece) == 2 or abs(piece) == 5)) or kingCheck:
                        check = True
                        checkingUnitLoc = pieceLoc

            except TypeError:
                continue

        knightDirDict = {
            (-2, -1): "north1",
            (-2, 1): "north2",
            (2, -1): "south1",
            (2, 1): "south2",
            (1, 2): "east1",
            (-1, 2): "east2",
            (1, -2): "west1",
            (-1, -2): "west2",
        }

        for a in knightDirDict.keys():
            checkLoc = (row + a[0],
                        col + a[1])
            if checkLoc[0] >= 0 and checkLoc[1] >= 0:
                try:
                    piece = self.currBoard[checkLoc[0]][checkLoc[1]]
                    if piece == -3:
                        check = True
                        checkingUnitLoc = checkLoc

                except IndexError:
                    continue

        return check, checkingUnitLoc

    def searchAroundLoc(self, row, col):
        dirDict = {
            (0, 1): "east",
            (0, -1): "west",
            (1, 0): "south",
            (-1, 0): "north",
            (1, 1): "southeast",
            (-1, 1): "northeast",
            (1, -1): "southwest",
            (-1, -1): "northwest",
        }

        locCheckDictLoc = {
            "north": 0,
            "south": 0,
            "east": 0,
            "west": 0,
            "northeast": 0,
            "northwest": 0,
            "southeast": 0,
            "southwest": 0,
        }
        dirList = list(dirDict.keys())
        dirListCopy = dirList.copy()

        # max search dist = 7
        for i in range(8):
            # iterate through all dir
            for direction in dirList:
                checkLoc = (row + direction[0] * (i + 1),
                            col + direction[1] * (i + 1))

                if checkLoc[0] >= 0 and checkLoc[1] >= 0:
                    try:
                        piece = self.currBoard[checkLoc[0]][checkLoc[1]]
                        if piece != 0:
                            addToDict = True
                            if piece == 6:
                                addToDict = False
                            if addToDict:
                                locCheckDictLoc[dirDict[direction]] = (
                                    piece, checkLoc)
                                dirListCopy.remove(direction)
                    except IndexError:
                        dirListCopy.remove(direction)
                else:
                    dirListCopy.remove(direction)
            dirList = dirListCopy.copy()
            if len(dirList) == 0:
                break
        return locCheckDictLoc

    def getKingLoc(self):
        # row
        for i in range(8):
            # col
            for j in range(8):
                if self.currBoard[i][j] == 6:
                    return (i, j)
        return (-1, -1)

    def printMoveList(self, moveList):
        print("\nMove List")
        for move in moveList:
            print(move[0], ": ", move[1][0], " -> ", move[1][1])

    def getMoves(self):
        moveList = []
        # row
        for i in range(8):
            # col
            for j in range(8):
                if self.currBoard[i][j] > 0:
                    pieceMoveList = self.getMovesForPiece(i, j)
                    if len(pieceMoveList) > 0:
                        for move in pieceMoveList:
                            move = move.strip()
                            if move != "":
                                element = (
                                    self.pieceDict[self.currBoard[i][j]], ((i, j), (int(move[0]), int(move[2]))))
                                moveList.append(element)
        return moveList

    def getMovesForPiece(self, row, col):
        piece = self.currBoard[row][col]
        retVal = ""
        if piece == 1:
            # print("Found Pawn")
            retVal = self.pawnMoves(row, col, piece)
        elif piece == 2:
            # print("Found Rook")
            retVal = self.rookMoves(row, col, piece)
        elif piece == 3:
            # print("Found Knight")
            retVal = self.knightMoves(row, col, piece)
        elif piece == 4:
            # print("Found Bishop")
            retVal = self.bishopMoves(row, col, piece)
        elif piece == 5:
            # print("Found Queen")
            retVal = self.queenMoves(row, col, piece)
        elif piece == 6:
            # print("Found King")
            retVal = self.kingMoves(row, col, piece)

        pieceMoveList = retVal.strip().split(";")
        return pieceMoveList

    def checkValidMove(self, row, col, piece, overtake):
        if row < 0 or col < 0:
            return 0
        try:
            pieceAtLoc = self.currBoard[row][col]
            # nothing at loc then valid move
            # same piece at loc not valid move
            # move that can eat other piece and enemy at loc then valid
            # move that can't eat and enemy at loc then not valid
            # 0 = invalid, 1 = valid
            if abs(piece) == 1:
                if overtake:
                    if pieceAtLoc < 0:
                        return 1
                    return 0
                else:
                    if pieceAtLoc == 0:
                        return 1
                    return 0
            if abs(piece) == 2:
                if pieceAtLoc < 0:
                    return 2
                elif pieceAtLoc == 0:
                    return 1
                else:
                    return 0
            if abs(piece) == 3:
                if pieceAtLoc == 0 or pieceAtLoc < 0:
                    return 1
                else:
                    return 0
            if abs(piece) == 4:
                if pieceAtLoc < 0:
                    return 2
                elif pieceAtLoc == 0:
                    return 1
                else:
                    return 0
            if abs(piece) == 5:
                if pieceAtLoc < 0:
                    return 2
                elif pieceAtLoc == 0:
                    return 1
                else:
                    return 0
            if abs(piece) == 6:
                if pieceAtLoc == 0 or pieceAtLoc < 0:
                    return 1
                else:
                    return 0
        except IndexError:
            return 0

    def pawnMoves(self, row, col, piece):
        moves = ""
        if col + 1 <= 7 and self.checkValidMove(row - 1, col + 1, piece, True) == 1:
            moves += str(row - 1) + ',' + str(col + 1) + "; "
        if col - 1 >= 0 and self.checkValidMove(row - 1, col - 1, piece, True) == 1:
            moves += str(row - 1) + ',' + str(col - 1) + "; "
        if self.checkValidMove(row - 1, col, piece, False) == 1:
            moves += str(row - 1) + ',' + str(col) + "; "
            if row == 6 and self.checkValidMove(row - 2, col, piece, False) == 1:
                moves += str(row - 2) + ',' + str(col) + "; "
        return moves

    def rookMoves(self, row, col, piece):
        moves = ""
        # up
        for a in range(1, 8):
            if row - a >= 0 and self.checkValidMove(row - a, col, piece, True) != 0:
                moves += str(row - a) + ',' + str(col) + "; "
                if self.checkValidMove(row - a, col, piece, True) == 2:
                    break
            else:
                break
        # down
        for a in range(1, 8):
            if row + a <= 7 and self.checkValidMove(row + a, col, piece, True) != 0:
                moves += str(row + a) + ',' + str(col) + "; "
                if self.checkValidMove(row + a, col, piece, True) == 2:
                    break
            else:
                break
        # left
        for a in range(1, 8):
            if col - a >= 0 and self.checkValidMove(row, col - a, piece, True) != 0:
                moves += str(row) + ',' + str(col - a) + "; "
                if self.checkValidMove(row, col - a, piece, True) == 2:
                    break
            else:
                break
        # right
        for a in range(1, 8):
            if col + a <= 7 and self.checkValidMove(row, col + a, piece, True) != 0:
                moves += str(row) + ',' + str(col + a) + "; "
                if self.checkValidMove(row, col + a, piece, True) == 2:
                    break
            else:
                break
        return moves

    def knightMoves(self, row, col, piece):
        moves = ""
        if row - 1 >= 0 and col - 2 >= 0 and self.checkValidMove(row - 1, col - 2, piece, True):
            moves += str(row - 1) + ',' + str(col - 2) + "; "
        if row - 1 >= 0 and col + 2 <= 7 and self.checkValidMove(row - 1, col + 2, piece, True):
            moves += str(row - 1) + ',' + str(col + 2) + "; "
        if row + 1 <= 7 and col - 2 >= 0 and self.checkValidMove(row + 1, col - 2, piece, True):
            moves += str(row + 1) + ',' + str(col - 2) + "; "
        if row + 1 <= 7 and col + 2 <= 7 and self.checkValidMove(row + 1, col + 2, piece, True):
            moves += str(row + 1) + ',' + str(col + 2) + "; "
        if row - 2 >= 0 and col - 1 >= 0 and self.checkValidMove(row - 2, col - 1, piece, True):
            moves += str(row - 2) + ',' + str(col - 1) + "; "
        if row - 2 >= 0 and col + 1 <= 7 and self.checkValidMove(row - 2, col + 1, piece, True):
            moves += str(row - 2) + ',' + str(col + 1) + "; "
        if row + 2 <= 7 and col - 1 >= 0 and self.checkValidMove(row + 2, col - 1, piece, True):
            moves += str(row + 2) + ',' + str(col - 1) + "; "
        if row + 2 <= 7 and col + 1 <= 7 and self.checkValidMove(row + 2, col + 1, piece, True):
            moves += str(row + 2) + ',' + str(col + 1) + "; "
        return moves

    def bishopMoves(self, row, col, piece):
        moves = ""
        # up left
        for a in range(1, 8):
            if row - a >= 0 and col - a >= 0 and self.checkValidMove(row - a, col - a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row - a, col - a, piece, True) == 2:
                    break
            else:
                break

        # up right
        for a in range(1, 8):
            if row - a >= 0 and col + a <= 7 and self.checkValidMove(row - a, col + a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row - a, col + a, piece, True) == 2:
                    break
            else:
                break

        # down left
        for a in range(1, 8):
            if row + a <= 7 and col - a >= 0 and self.checkValidMove(row + a, col - a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row + a, col - a, piece, True) == 2:
                    break
            else:
                break

        # down right
        for a in range(1, 8):
            if row + a <= 7 and col + a <= 7 and self.checkValidMove(row + a, col + a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row + a, col + a, piece, True) == 2:
                    break
            else:
                break

        return moves

    def queenMoves(self, row, col, piece):
        moves = ""
        # up left
        for a in range(1, 8):
            if row - a >= 0 and col - a >= 0 and self.checkValidMove(row - a, col - a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row - a, col - a, piece, True) == 2:
                    break
            else:
                break

        # up right
        for a in range(1, 8):
            if row - a >= 0 and col + a <= 7 and self.checkValidMove(row - a, col + a, piece, True) != 0:
                moves += str(row - a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row - a, col + a, piece, True) == 2:
                    break
            else:
                break

        # down left
        for a in range(1, 8):
            if row + a <= 7 and col - a >= 0 and self.checkValidMove(row + a, col - a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col - a) + "; "
                if self.checkValidMove(row + a, col - a, piece, True) == 2:
                    break
            else:
                break

        # down right
        for a in range(1, 8):
            if row + a <= 7 and col + a <= 7 and self.checkValidMove(row + a, col + a, piece, True) != 0:
                moves += str(row + a) + ',' + str(col + a) + "; "
                if self.checkValidMove(row + a, col + a, piece, True) == 2:
                    break
            else:
                break

        # up
        for a in range(1, 8):
            if row - a >= 0 and self.checkValidMove(row - a, col, piece, True) != 0:
                moves += str(row - a) + ',' + str(col) + "; "
                if self.checkValidMove(row - a, col, piece, True) == 2:
                    break
            else:
                break
        # down
        for a in range(1, 8):
            if row + a <= 7 and self.checkValidMove(row + a, col, piece, True) != 0:
                moves += str(row + a) + ',' + str(col) + "; "
                if self.checkValidMove(row + a, col, piece, True) == 2:
                    break
            else:
                break
        # left
        for a in range(1, 8):
            if col - a >= 0 and self.checkValidMove(row, col - a, piece, True) != 0:
                moves += str(row) + ',' + str(col - a) + "; "
                if self.checkValidMove(row, col - a, piece, True) == 2:
                    break
            else:
                break
        # right
        for a in range(1, 8):
            if col + a <= 7 and self.checkValidMove(row, col + a, piece, True) != 0:
                moves += str(row) + ',' + str(col + a) + "; "
                if self.checkValidMove(row, col + a, piece, True) == 2:
                    break
            else:
                break
        return moves

    def kingMoves(self, row, col, piece):
        moves = ""
        if col + 1 <= 7 and self.checkValidMove(row, col + 1, piece, True) != 0 and not self.checkLocForCheck(row, col+1)[0]:
            moves += str(row) + ',' + str(col + 1) + "; "
        if col - 1 >= 0 and self.checkValidMove(row, col - 1, piece, True) != 0 and not self.checkLocForCheck(row, col-1)[0]:
            moves += str(row) + ',' + str(col - 1) + "; "
        if row + 1 <= 7 and self.checkValidMove(row + 1, col, piece, True) != 0 and not self.checkLocForCheck(row+1, col)[0]:
            moves += str(row + 1) + ',' + str(col) + "; "
        if row - 1 >= 0 and self.checkValidMove(row - 1, col, piece, True) != 0 and not self.checkLocForCheck(row-1, col)[0]:
            moves += str(row - 1) + ',' + str(col) + "; "
        if row + 1 <= 7 and col + 1 <= 7 and self.checkValidMove(row + 1, col + 1, piece, True) != 0 and not self.checkLocForCheck(row+1, col+1)[0]:
            moves += str(row + 1) + ',' + str(col + 1) + "; "
        if row + 1 <= 7 and col - 1 >= 0 and self.checkValidMove(row + 1, col - 1, piece, True) != 0 and not self.checkLocForCheck(row+1, col-1)[0]:
            moves += str(row + 1) + ',' + str(col - 1) + "; "
        if row - 1 >= 0 and col + 1 <= 7 and self.checkValidMove(row - 1, col + 1, piece, True) != 0 and not self.checkLocForCheck(row-1, col+1)[0]:
            moves += str(row - 1) + ',' + str(col + 1) + "; "
        if row - 1 >= 0 and col - 1 >= 0 and self.checkValidMove(row - 1, col - 1, piece, True) != 0 and not self.checkLocForCheck(row-1, col-1)[0]:
            moves += str(row - 1) + ',' + str(col - 1) + "; "
        return moves

    def printBoard(self, board):
        print()
        print("        0    1    2    3     4    5    6    7      Col ")
        print("      -----------------------------------------")
        count = 0
        for col in board:
            print(" ", str(count), "  |", end='')
            for row in col:
                if row >= 0:
                    print(" ", row, "|", end='')
                else:
                    print("-", -1*row, "|", end='')
            print()
            print("      -----------------------------------------")
            count = count + 1
        print()
        print(" Row")
        print()
        print()
        print()

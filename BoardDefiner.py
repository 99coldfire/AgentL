import numpy as np
import cv2 as cv
from numpy.lib import math
import pyautogui
import pytesseract
from matplotlib import pyplot as plt
from operator import itemgetter
from skimage.metrics import structural_similarity
from scipy.linalg import norm
from scipy import sum, average
from PIL import Image


class BoardDefiner:
    topLeftCorner = (0, 0)

    coordsOfRedRect = {
        'top': (0, 0),
        'left': (0, 0),
        'right': (0, 0),
        'bot': (0, 0),
    }

    borders = ['BottomBorder.png', 'RightBorder.png',
               'LeftBorder.png', 'TopBorder.png']

    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
               'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    boardTopLeftCorner = (0, 0)
    boardLengthHeight = (0, 0)

    gridCoords = {}

    beforeImage = ""
    afterImage = ""
    # 0 = white, 1 = black
    side = 0

    pieceDict = {
        "pawn": 1,
        "rook": 2,
        "knight": 3,
        "bishop": 4,
        "queen": 5,
        "king": 6
    }

    def findNew10MinRatedChat(self):
        img = pyautogui.screenshot()
        img = cv.cvtColor(np.array(img),
                          cv.COLOR_RGB2BGR)
        template = cv.imread("New10MinRatedChat.png")
        result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)

        MPx = -1
        MPy = -1

        w, h = template.shape[:-1]
        threshold = 0.90
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            print("Starting New Game from 10 Min Rated in Chat")
            MPx, MPy = pt

        if MPx == -1:
            return -1
        else:
            pyautogui.moveTo(MPx + h/2, MPy + w/2)
            pyautogui.click()
            return 1

    def findNew10MinGameBoard(self):
        img = pyautogui.screenshot()
        img = cv.cvtColor(np.array(img),
                          cv.COLOR_RGB2BGR)
        template = cv.imread("New10MinBoard.png")
        result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)

        MPx = -1
        MPy = -1

        w, h = template.shape[:-1]
        threshold = 0.90
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            print("Starting New Game: 10 Min Game")
            MPx, MPy = pt

        if MPx == -1:
            return -1
        else:
            pyautogui.moveTo(MPx + h/2, MPy + w/2)
            pyautogui.click()
            return 1

    def findPieces(self):
        blankBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]

        img_rgb = pyautogui.screenshot(region=(
            self.boardTopLeftCorner[0], self.boardTopLeftCorner[1], self.boardLengthHeight[0], self.boardLengthHeight[1]))
        img_rgb = cv.cvtColor(np.array(img_rgb),
                              cv.COLOR_RGB2BGR)
        cv.imwrite("board.png", img_rgb)

        pieces = ["Pawn", "Rook", "Knight", "Bishop", "Queen", "King"]
        sides = ["Black", "White"]
        boxSize = self.boardLengthHeight[0]/8
        for side in sides:
            for piece in pieces:
                template = cv.imread(side + piece + ".png")

                w, h = template.shape[:-1]

                res = cv.matchTemplate(img_rgb, template, cv.TM_CCOEFF_NORMED)
                threshold = .80
                loc = np.where(res >= threshold)
                count = 0

                pieceLocs = []

                for pt in zip(*loc[::-1]):  # Switch collumns and rows
                    if count == 0:
                        pieceLocs.append((int(pt[0] + w/2), int(pt[1] + h/2)))
                    else:
                        minDist = 99999999
                        for a in pieceLocs:
                            dist = ((pt[0] + w/2 - a[0])**2 +
                                    (pt[1] + h/2 - a[1])**2)**0.5
                            if dist < minDist:
                                minDist = dist

                        if minDist > 25:
                            pieceLocs.append(
                                (int(pt[0] + w/2), int(pt[1] + h/2)))

                    count = count + 1

                for pieceLoc in pieceLocs:
                    pieceCol = np.floor(pieceLoc[0]/boxSize)
                    pieceRow = np.floor(pieceLoc[1]/boxSize)
                    multiplier = 1
                    if side == "Black":
                        multiplier = -1
                    blankBoard[int(pieceRow)][int(pieceCol)
                                              ] = self.pieceDict[piece.lower()] * multiplier

        return blankBoard

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

    def takeScreenshotForFindingBoard(self):
        image = pyautogui.screenshot()
        image = cv.cvtColor(np.array(image),
                            cv.COLOR_RGB2BGR)
        cv.imwrite("chessImage.png", image)

    def takeScreenshotOfBoard(self, imageName):
        image = pyautogui.screenshot(region=(
            self.boardTopLeftCorner[0], self.boardTopLeftCorner[1], self.boardLengthHeight[0], self.boardLengthHeight[1]))
        image = cv.cvtColor(np.array(image),
                            cv.COLOR_RGB2BGR)
        cv.imwrite(imageName, image)

    def compare_images(self, img1, img2):
        # calculate the difference and its norms
        diff = img1 - img2  # elementwise for scipy arrays
        m_norm = sum(abs(diff))  # Manhattan norm
        z_norm = norm(diff.ravel(), 0)  # Zero norm
        return (m_norm, z_norm)

    def to_grayscale(self, arr):
        if len(arr.shape) == 3:
            # average over the last axis (color channels)
            return average(arr, -1)
        else:
            return arr

    def resetAfterMoveScreenshot(self):
        img = pyautogui.screenshot(region=(
            self.boardTopLeftCorner[0], self.boardTopLeftCorner[1], self.boardLengthHeight[0], self.boardLengthHeight[1]))
        img = cv.cvtColor(np.array(img),
                          cv.COLOR_RGB2BGR)
        cv.imwrite("afterMoveScreenshot.png", img)

    def findDifferences(self):
        before = cv.imread('afterMoveScreenshot.png')

        after = pyautogui.screenshot(region=(
            self.boardTopLeftCorner[0], self.boardTopLeftCorner[1], self.boardLengthHeight[0], self.boardLengthHeight[1]))
        after = cv.cvtColor(np.array(after),
                            cv.COLOR_RGB2BGR)
        cv.imwrite("comparingImage.png", after)

        # Convert images to grayscale
        before_gray = cv.cvtColor(before, cv.COLOR_BGR2GRAY)
        after_gray = cv.cvtColor(after, cv.COLOR_BGR2GRAY)

        before_gray = self.to_grayscale(
            cv.imread('afterMoveScreenshot.png').astype(float))
        after_gray = self.to_grayscale(after.astype(float))

        n_m, n_0 = self.compare_images(before_gray, after_gray)
        #print("Manhattan norm:", n_m, "/ per pixel:", n_m/before_gray.size)
        #print("Zero norm:", n_0, "/ per pixel:", n_0*1.0/before_gray.size)

        return n_m

    def findDiffMove(self):
        # load images
        before = cv.imread("afterMoveScreenshot.png")

        moveList = []

        # while(len(moveList) != 2):
        after = pyautogui.screenshot(region=(
            self.boardTopLeftCorner[0], self.boardTopLeftCorner[1], self.boardLengthHeight[0], self.boardLengthHeight[1]))
        after = cv.cvtColor(np.array(after),
                            cv.COLOR_RGB2BGR)
        cv.imwrite("comparingImage.png", after)

        # Convert images to grayscale
        before_gray = cv.cvtColor(before, cv.COLOR_BGR2GRAY)
        after_gray = cv.cvtColor(after, cv.COLOR_BGR2GRAY)

        # Compute SSIM between two images
        (score, diff) = structural_similarity(
            before_gray, after_gray, full=True)
        print("Image similarity", score)

        # The diff image contains the actual image differences between the two images
        # and is represented as a floating point data type in the range [0,1]
        # so we must convert the array to 8-bit unsigned integers in the range
        # [0,255] before we can use it with OpenCV
        diff = (diff * 255).astype("uint8")

        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv.threshold(
            diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        contours = cv.findContours(
            thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(before.shape, dtype='uint8')
        filled_after = after.copy()

        boxSize = self.boardLengthHeight[0]/8

        moveList = []
        for c in contours:
            area = cv.contourArea(c)
            if area > 40:
                x, y, w, h = cv.boundingRect(c)
                row = int(np.floor((y + h/2)/boxSize))
                col = int(np.floor((x + w/2)/boxSize))
                moveList.append((row, col))

        print("Move: ")
        print(moveList)

        cv.imwrite("after.png", after)

        return moveList

    def checkGameOver(self):
        img = pyautogui.screenshot()
        img = cv.cvtColor(np.array(img),
                          cv.COLOR_RGB2BGR)
        template = cv.imread("GameOverSign.png")
        result = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)

        MPx = -1
        MPy = -1

        w, h = template.shape[:-1]
        threshold = 0.99
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            print("Found GameOver")
            MPx, MPy = pt
            cv.rectangle(img, (MPx, MPy),
                         (MPx+h, MPy+w), (0, 0, 255), 2)

        print(MPx, ":", MPy)

        # Display the original image with the rectangle around the match.
        cv.imshow('output', img)

        # The image is only displayed if we call this
        cv.waitKey(0)

        if MPx == -1:
            return -1
        else:
            return 1

    def findBoardBorders(self):
        img = cv.imread('chessImage.png')

        for border in self.borders:
            print()
            print(border)
            method = eval(self.methods[4])
            template = cv.imread(border)
            result = cv.matchTemplate(template, img, method)

            # We want the minimum squared difference
            mn, _, mnLoc, _ = cv.minMaxLoc(result)

            # Draw the rectangle:
            # Extract the coordinates of our best match
            MPx, MPy = mnLoc

            # Step 2: Get the size of the template. This is the same size as the match.
            trows, tcols = template.shape[:2]

            loc = ''
            if border == 'BottomBorder.png':
                print("Bottom Y:", MPy+(trows/2))
                loc = 'bot'
            if border == 'TopBorder.png':
                print("Top Y:", MPy+(trows/2))
                loc = 'top'
            if border == 'LeftBorder.png':
                print("Left X:", MPx+(tcols/2))
                loc = 'left'
            if border == 'RightBorder.png':
                print("Right X:", MPx+(tcols/2))
                loc = 'right'

            self.coordsOfRedRect[loc] = (MPx, MPy)
            '''
            # Step 3: Draw the rectangle on large_image
            cv.rectangle(img, (MPx, MPy),
                         (MPx+tcols, MPy+trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv.imshow('output', img)

            # The image is only displayed if we call this
            cv.waitKey(0)
            '''

    def findBoardDimensions(self):
        img = cv.imread('chessImage.png')

        length = self.coordsOfRedRect['right'][0] - \
            self.coordsOfRedRect['left'][0]
        height = self.coordsOfRedRect['bot'][1] - \
            self.coordsOfRedRect['top'][1]

        print('Length: ', length)
        print('Height: ', height)
        self.boardLengthHeight = (length, height)

        x = 0
        xList = [item[0] for item in self.coordsOfRedRect.values()]
        xList = sorted(xList)
        minDist = 9999
        minPair = (0, 0)
        for i in range(len(xList)-1):
            dist = abs(xList[i] - xList[i+1])
            if dist < minDist:
                minDist = dist
                minPair = (xList[i], xList[i+1])

        x = (minPair[0] + minPair[1])/2

        y = 0
        yList = [item[1] for item in self.coordsOfRedRect.values()]
        yList = sorted(yList)
        minDist = 9999
        minPair = (0, 0)
        for i in range(len(yList)-1):
            dist = abs(yList[i] - yList[i+1])
            if dist < minDist:
                minDist = dist
                minPair = (yList[i], yList[i+1])
        y = (minPair[0] + minPair[1])/2

        print('Top Left Corner: ', (x, y))
        self.boardTopLeftCorner = (x, y)

    '''        
            cv.rectangle(img, (int(x), int(y)),
                        (int(x+length), int(y+height)), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv.imshow('output', img)

            # The image is only displayed if we call this
            cv.waitKey(0)
    '''

    def splitBoardIntoGrid(self):
        img = cv.imread('chessImage.png')
        boxSize = self.boardLengthHeight[0]/8

        x, y = self.boardTopLeftCorner

        for i in range(8):
            for j in range(8):
                self.gridCoords[(j, i)] = ((x + i*boxSize + boxSize/2),
                                           (y + j*boxSize + boxSize/2))

    '''
                    cv.rectangle(img, (int(x + i*boxSize), int(y + j*boxSize)),
                                (int(x + i*boxSize + boxSize), int(y + j*boxSize + boxSize)), (0, 0, 255), 2)

                    cv.rectangle(img, (int(x + i*boxSize + boxSize/2-1), int(y + j*boxSize + boxSize/2-1)),
                                (int(x + i*boxSize + boxSize/2+2), int(y + j*boxSize + boxSize/2 + 2)), (0, 0, 255), 2)

                    # Display the original image with the rectangle around the match.
                    cv.imshow('output', img)

                    # The image is only displayed if we call this
                    cv.waitKey(0)
    '''

    def moveMouseIntoGridCoords(self):
        for key, value in self.gridCoords.items():
            print('Grid Loc: ', key, ' = ', value)
            pyautogui.moveTo(value[0], value[1])
            pyautogui.sleep(0.5)

    def determineSide(self):
        img = cv.imread('chessImage.png')
        method = eval(self.methods[4])
        template = cv.imread('WhitePawn.png')
        result = cv.matchTemplate(template, img, method)

        mn, _, mnLoc, _ = cv.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = template.shape[:2]

        boxSize = self.boardLengthHeight[0]/8
        if MPy <= self.boardTopLeftCorner[1] + boxSize * 7 and MPy >= self.boardTopLeftCorner[1] + boxSize * 6:
            print("White Side")
            return 0
        else:
            print("Black Side")
            return 1

    def movePiece(self, origLoc, newLoc):
        coord = self.gridCoords[origLoc]
        pyautogui.moveTo(coord[0], coord[1])
        coord = self.gridCoords[newLoc]
        pyautogui.dragTo(coord[0], coord[1], button='left')
        self.takeScreenshotOfBoard("afterMoveScreenshot.png")
        pyautogui.sleep(1)

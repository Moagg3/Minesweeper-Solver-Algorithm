import numpy as np
import random

#Alg1

class AI1():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows"
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    # return the square (r, c) you want to open based on the given boardState
    # the boardState will contain the value (0-8 inclusive) of the square, or -1 if that square is unopened
    # an AI example that returns a random square (r, c) that you want to open
    def performAI(self, boardState):
        # find all the unopened squares
        unopenedSquares = set()
        bombsFoundSoFar = set()
        safeSquares = set()

        # Get list of bombs visible in current state
        for row in range(self.numRows):
            for col in range(self.numCols):
                if boardState[row][col] == 9:
                    bombsFoundSoFar.add((row, col))
        
        # Answer has been found
        if len(list(bombsFoundSoFar)) == self.numBombs:
            return self.submit_final_answer_format(bombsFoundSoFar)

        # find squares that we should / shouldn't choose as safe square
        # FOR EACH square in the grid:
        for row in range(self.numRows):
            for col in range(self.numCols):
                # if square unopened, add to unopenedSquares list
                if boardState[row][col] == -1:
                    unopenedSquares.add((row, col)) # 
                
                # if no bomb in proximity of current square, we can assume they are safe and we don't need to dig the 8 squares surrounding it
                elif boardState[row][col] == 0:
                    safeSquares.add((row, col))
                    for cur in self.getSurroundingSquares(row, col):
                        safeSquares.add(cur)   
                
                # check if there is some number of bombs in the neighborhood of the current square
    
                elif boardState[row][col] != 9:
                    numBombs = boardState[row][col]
                    surroundBombs = 0
                    uncover = 0
                    surroundingSquares = self.getSurroundingSquares(row, col)
										# count number of bombs nearby
                    for cur in surroundingSquares:
                        if cur in bombsFoundSoFar:
                            surroundBombs += 1
                    # now compare against actual number of bombs in the neighborhood.
                    # If surrouding bombs are equal to tile number then we just add rest of the tiles to safe squares.
                    if numBombs == surroundBombs:
                        safeSquares.add((row, col))
                        for cur in surroundingSquares:
                            if cur not in bombsFoundSoFar:
                                safeSquares.add(cur)

        # remove the safe squares from the list of unopened squares because we don't need to dig them
        unknownSquares = unopenedSquares.difference(safeSquares)
        squareToOpen = random.choice(list(unknownSquares))

        return self.open_square_format(squareToOpen)

    # Helper method to get a list of surrounding squares for a cell given by (row, col)
    def getSurroundingSquares(self, row, col):
        surrounding = set()
        surrounding.add((max(0, row - 1), col))
        # up down
        surrounding.add((max(0, row - 1), col))
        surrounding.add((min(self.numRows - 1, row + 1), (col)))
        # diaganols
        surrounding.add((min(self.numRows - 1, row + 1), max(0, col - 1)))
        surrounding.add((max(0, row - 1), max(0, col - 1)))

        surrounding.add((min(self.numRows - 1, row + 1), min(col + 1, self.numCols - 1)))
        surrounding.add((max(0, row - 1), min(col + 1, self.numCols - 1)))
        # left right
        surrounding.add((row, max(col - 1, 0)))
        surrounding.add((row, min(col + 1, self.numCols - 1)))
        # remove middle if in it
        if ((row, col)) in surrounding:
            surrounding.remove((row, col))
        return surrounding

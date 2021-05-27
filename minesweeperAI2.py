import numpy as np
import random

#Alg2

class AI2():

    # Define settings upon initialization. Here you can specify
    def __init__(self, numRows, numCols, numBombs, safeSquare):   

        # game variables that can be accessed in any method in the class. For example, to access the number of rows, use "self.numRows" 
        self.numRows = numRows
        self.numCols = numCols
        self.numBombs = numBombs
        self.safeSquare = safeSquare



        # 
        self.bombsList = set() #only 9s
        self.safeSquares = set() #0, 1, 2 not 9
        self.guesses = [] # records my guesses for squares
        self.unknownSquares = set() 
        self.squaresToCheck = set() # know the number 1 or 2 or 3 NOT 0, 9, -1

    def open_square_format(self, squareToOpen):
        return ("open_square", squareToOpen)

    def submit_final_answer_format(self, listOfBombs):
        return ("final_answer", listOfBombs)

    def performAI(self, boardState):
        # iniitalize variables for this single iteration
        probability = {}
        bestSquare = None
        highestProb = -1
        
        # Check what last guess was, update sets accordingly
        if len(self.guesses) > 0:
            numGuess = len(self.guesses)
            lastRes = self.guesses[numGuess-1]
            self.unknownSquares.remove(lastRes)
            if boardState[lastRes[0]][lastRes[1]] == 9:
                self.bombsList.add(lastRes)
            # All Free Neighbors (AFN)
            elif boardState[lastRes[0]][lastRes[1]] == 0:
                self.safeSquares.add(lastRes)
                for cur in self.getSurroundingSquares(lastRes[0], lastRes[1]):
                    self.safeSquares.add(cur)
            else:
                self.safeSquares.add(lastRes)
                self.squaresToCheck.add(lastRes)
            self.unknownSquares = self.unknownSquares.difference((self.bombsList.union(self.safeSquares)))
        # on first iteration guess "safe square" and initialize lists
        else:
            for row in range(self.numRows):
                for col in range(self.numCols):
                    self.unknownSquares.add((row, col))
            self.guesses.append(self.safeSquare)
            return self.open_square_format(self.safeSquare)
        # Answer has been found
        # print(len(self.bombsList))
        if len(list(self.bombsList)) == self.numBombs:
            return self.submit_final_answer_format(self.bombsList)

        #squaresToCheck = all the squares we have info on -- 1, 2, 3
        for point in list(self.squaresToCheck):
            row = point[0]
            col = point[1]
            numBombs = boardState[row][col] # number of the space
            surroundBombs = 0 # number of bombs we know for sure surrounding
            surroundingSquares = self.getSurroundingSquares(row, col)
            surroundUnknownsCount = 0 #number of '-1's we have surrounding
            surroundingUnknowns = set() #set of these '-1's

            # find/populate previous variables
            for cur in surroundingSquares:
                if cur in self.bombsList:
                    surroundBombs+=1
                if cur in self.unknownSquares:
                    surroundUnknownsCount += 1
                    surroundingUnknowns.add(cur)
            # All unknown neighbors must be bombs so add all to list (AMN)
            if numBombs - surroundBombs == surroundUnknownsCount:
                for res in list(surroundingUnknowns):
                    self.bombsList.add(res)
                    self.unknownSquares.remove(res)
                if len(list(self.bombsList)) == self.numBombs:
                    return self.submit_final_answer_format(self.bombsList)
                else:
                    continue
            # All other neighbors must be safe since the number of surrounding bombs==number of possible surrounding bombs (AFN)
            elif numBombs - surroundBombs == 0:
                for space in surroundingSquares:
                    self.safeSquares.add(space) #fix
            # Some mixture of neighbors are bombs or not. Find "pseudo-probability" to help determine which to pick. High prob=More likely a bomb
            else:                    
                remaining = numBombs - surroundBombs
                for cur in surroundingSquares:
                    if cur not in self.unknownSquares:
                        continue
                    index = cur[0]*self.numCols + cur[1]
                    currentProb = probability.get(index, 0)
                    currentProb += remaining
                    if currentProb > highestProb:
                        highestProb = currentProb
                        bestSquare = cur
                    probability[index] = currentProb
        # If we have that we think is likely to be a bomb, let's try it
        if highestProb > 0 and  bestSquare in self.unknownSquares:
            self.guesses.append((bestSquare))
            return self.open_square_format((bestSquare))
        #Otherwise, we can just pick randomly
        else:
            unknownSquares = self.unknownSquares.difference(self.safeSquares.union(self.bombsList))
            squareToOpen = random.choice(list(unknownSquares))
            self.guesses.append(squareToOpen)
            return self.open_square_format(squareToOpen)


    # Basic helper function to get the 8 surrounding squares
    def getSurroundingSquares(self, row, col):
        surrounding = set()
        surrounding.add((max(0, row-1), col))
        #up down
        surrounding.add((max(0, row-1), col))
        surrounding.add((min(self.numRows-1, row+1), (col)))
        #diaganols
        surrounding.add((min(self.numRows-1, row+1), max(0, col-1)) )
        surrounding.add((max(0, row-1), max(0, col-1)))

        surrounding.add((min(self.numRows-1, row+1), min(col+1, self.numCols-1)))
        surrounding.add((max(0, row-1), min(col+1, self.numCols-1)) )
        #left right
        surrounding.add((row, max(col-1, 0)) )
        surrounding.add((row, min(col+1, self.numCols-1)))
        #remove middle if in it
        if ((row,col)) in surrounding:
            surrounding.remove((row, col))
        return surrounding
# Shadman Quazi
# CSCI 35000/76100 Artificial Intelligence
# Homework #2

import random
import math
import time
from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):
    # terminal test
    def checkTerminal(self, grid):
        return not grid.canMove()

    # first heuristic function
    # number of empty trials
    def checkFreeTiles(self, grid):
        return len(grid.getAvailableCells())

    # heuristic for additional evaluation
    # basic idea for smoothness:
    # measuring the difference between adjacent score
    # and picking a move that minimizes that score.
    def checkSmoothness(self, grid):
        smoothness = 0
     #   print(grid.size)

        for x in range(grid.size):
            for y in range(grid.size):
                # iterating over the grid, getting the smoothness
                s = 1000000

                # checking over rows and column, taking the difference
                if x > 0:
                    s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x - 1][y] or 2)))
                if y > 0:
                    s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x][y - 1] or 2)))
                if x < 3:
                    s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x + 1][y] or 2)))
                if y < 3:
                    s = min(s, abs((grid.map[x][y] or 2) - (grid.map[x][y + 1] or 2)))
                smoothness -= s

        return smoothness

    # basic idea of monotonicity
    # checking if in any direction the board is either ascending or descending
    def checkMonotonicity(self, grid):
        return_score = 0

        # first checking across the horizontal, i.e. monotonicity over rows
        for x in range(grid.size):
            if ((all(grid.map[x][y] <= grid.map[x][y + 1] for y in range(grid.size - 1)) or
                 all(grid.map[x][y] >= grid.map[x][y + 1] for y in range(grid.size - 1)))):
                return_score += 2

         # then checking across the vertical, i.e. monotonicity over columns
        for y in range(grid.size):
            if ((all(grid.map[x][y] <= grid.map[x + 1][y] for x in range(grid.size - 1)) or
                 all(grid.map[x][y] >= grid.map[x + 1][y] for x in range(grid.size - 1)))):
                return_score += 2

        return return_score

    # 3 heuristics used,
    # smoothness, empty tiles, and monotonocity
    # each weight was obtained through a mixture of trial and error and the original 2048 codebase.
    def getScore(self, grid):
        return_value = grid.getMaxTile()
        return return_value + 0.1 * self.checkSmoothness(grid) + self.checkMonotonicity(grid) + 2.7 * self.checkFreeTiles(grid)

    # has three parameters, the current grid config
    # current depth of the tree
    # and if player is max or min
    def expectiminmax(self, grid, depth, alpha, beta, isMaxing, start):

        if self.checkTerminal(grid) or depth == 5 or (time.clock() - start) > 0.1:
            return self.getScore(grid)

        # max and min initially set as arbitrarily large
        else:
            if isMaxing:
                maxUtility = -1000000
                moveset = grid.getAvailableMoves()
                for child in moveset:
                    val = self.expectiminmax(child[1], depth + 1, alpha, beta, False, start)
                    maxUtility = max(maxUtility, val)
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break

                return maxUtility
            else:
                minUtility = 10000000

                empty = grid.getAvailableCells()

                # logic to account for chance moves
                moveset = []

                for pos in empty:
                    current_grid2 = grid.clone()
                    current_grid4 = grid.clone()

                    current_grid2.insertTile(pos, 2)
                    current_grid4.insertTile(pos, 4)

                    moveset.append(current_grid2)
                    moveset.append(current_grid4)

                for child in moveset:
                    val = self.expectiminmax(child, depth + 1, alpha, beta, True, start)
                    minUtility = min(val, minUtility)
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
                return minUtility

    def getMove(self, grid):
        start = time.clock()

        bestScore = -11000000
        direction = -1
        moveset = grid.getAvailableMoves()

        for move in moveset:
            val = self.expectiminmax(move[1], 0, -1000000, 10000000, False, start)
            if val > bestScore:
                bestScore = val
                direction = move[0]

        return direction

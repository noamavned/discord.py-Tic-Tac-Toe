import os
import time
from pydoc import cli
from tkinter.messagebox import NO

import discord
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands import CheckFailure, check, has_permissions
from discord.utils import get
from discord_components import Button, ButtonStyle, DiscordComponents


player, opponent = "o", "x"


def isMovesLeft(board):

    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                return True
    return False


def evaluate(b):
    for row in range(3):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == player:
                return 10
            elif b[row][0] == opponent:
                return -10

    for col in range(3):

        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:

            if b[0][col] == player:
                return 10
            elif b[0][col] == opponent:
                return -10

    # Checking for Diagonals for X or O victory.
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:

        if b[0][0] == player:
            return 10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:

        if b[0][2] == player:
            return 10
        elif b[0][2] == opponent:
            return -10

    return 0


def minimax(board, depth, isMax):
    score = evaluate(board)

    if score == 10:
        return score

    if score == -10:
        return score

    if isMovesLeft(board) == False:
        return 0

    if isMax:
        best = -1000

        for i in range(3):
            for j in range(3):

                if board[i][j] == "_":

                    board[i][j] = player

                    best = max(best, minimax(board, depth + 1, not isMax))

                    board[i][j] = "_"
        return best

    else:
        best = 1000

        for i in range(3):
            for j in range(3):

                if board[i][j] == "_":

                    board[i][j] = opponent

                    best = min(best, minimax(board, depth + 1, not isMax))

                    board[i][j] = "_"
        return best


def createboard(b):
    nb = [[], [], []]
    i = 0
    for line in b:
        for slot in line:
            if slot == 'x':
                nb[i].append('x')
            elif slot == 'o':
                nb[i].append('o')
            else:
                nb[i].append('_')
        i += 1
    return nb


def getIndex(id):
    id = str(id)
    if id == '0':
        return (0, 0)
    elif id == '1':
        return (0, 1)
    elif id == '2':
        return (0, 2)
    elif id == '3':
        return (1, 0)
    elif id == '4':
        return (1, 1)
    elif id == '5':
        return (1, 2)
    elif id == '6':
        return (2, 0)
    elif id == '7':
        return (2, 1)
    elif id == '8':
        return (2, 2)


def checkBestMove(bm):
    if(bm[0] == 0) and (bm[1] == 0):
        return 0
    elif(bm[0] == 0) and (bm[1] == 1):
        return 1
    elif(bm[0] == 0) and (bm[1] == 2):
        return 2
    elif(bm[0] == 1) and (bm[1] == 0):
        return 3
    elif(bm[0] == 1) and (bm[1] == 1):
        return 4
    elif(bm[0] == 1) and (bm[1] == 2):
        return 5
    elif(bm[0] == 2) and (bm[1] == 0):
        return 6
    elif(bm[0] == 2) and (bm[1] == 1):
        return 7
    elif(bm[0] == 2) and (bm[1] == 2):
        return 8


def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    for i in range(3):
        for j in range(3):

            if board[i][j] == "_":

                board[i][j] = player

                moveVal = minimax(board, 0, False)

                board[i][j] = "_"

                if moveVal > bestVal:
                    bestMove = (i, j)
                    bestVal = moveVal

    return bestMove


def isdraw(board):
    for line in board:
        for slot in line:
            if slot == '_':
                return False
    return True


def checkwin(board, ctx):
    if board[0][0] == board[0][1] == board[0][2] == 'x':
        return (False, 'x', (0, 1, 2))
    elif board[0][0] == board[0][1] == board[0][2] == 'o':
        return (False, 'o', (0, 1, 2))

    elif board[1][0] == board[1][1] == board[1][2] == 'x':
        return (False, 'x', (3, 4, 5))
    elif board[1][0] == board[1][1] == board[1][2] == 'o':
        return (False, 'o', (3, 4, 5))

    elif board[2][0] == board[2][1] == board[2][2] == 'x':
        return (False, 'x', (6, 7, 8))
    elif board[2][0] == board[2][1] == board[2][2] == 'o':
        return (False, 'o', (6, 7, 8))

    elif board[0][0] == board[1][0] == board[2][0] == 'x':
        return (False, 'x', (0, 3, 6))
    elif board[0][0] == board[1][0] == board[2][0] == 'o':
        return (False, 'o', (0, 3, 6))

    elif board[0][1] == board[1][1] == board[2][1] == 'x':
        return (False, 'x', (1, 4, 7))
    elif board[0][1] == board[1][1] == board[2][1] == 'o':
        return (False, 'o', (1, 4, 7))

    elif board[0][2] == board[1][2] == board[2][2] == 'x':
        return (False, 'x', (2, 5, 8))
    elif board[0][2] == board[1][2] == board[2][2] == 'o':
        return (False, 'o', (2, 5, 8))

    elif board[0][0] == board[1][1] == board[2][2] == 'x':
        return (False, 'x', (0, 4, 8))
    elif board[0][0] == board[1][1] == board[2][2] == 'o':
        return (False, 'o', (0, 4, 8))

    elif board[0][2] == board[1][1] == board[2][0] == 'x':
        return (False, 'x', (2, 4, 6))
    elif board[0][2] == board[1][1] == board[2][0] == 'o':
        return (False, 'o', (2, 4, 6))

    elif (isdraw(board)):
        return (False, 'tie', (0, 1, 2, 3, 4, 5, 6, 7, 8))

    else:
        return (True, None, None)


def start(b):
    return (findBestMove(b), True)

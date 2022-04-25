import os
import time
from pydoc import cli

import discord
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands import CheckFailure, check, has_permissions
from discord.utils import get
from discord_components import Button, ButtonStyle, DiscordComponents
from dpymenus import Page, PaginatedMenu

from src.ai import *


def addCommands(client):

    @client.command()
    async def help(ctx):
        page1 = Page(title='HELP', description='')

        page2 = Page(title='Help command',
                     description='Show the commands of the bot')

        page3 = Page(title='startgame',
                     description='Starting a game of Tic Tac Toe')

        menu = PaginatedMenu(ctx)
        menu.add_pages([page1, page2, page3])
        await menu.open()

    @client.command()
    async def startgame(ctx):
        isRunning = True
        board = [['1', '2', '3'],
                 ['4', '5', '6'],
                 ['7', '8', '9']]
        buttons = [
            [
                Button(label=' ', id='0', style=ButtonStyle.green),
                Button(label=' ', id='1', style=ButtonStyle.green),
                Button(label=' ', id='2', style=ButtonStyle.green)
            ],
            [
                Button(label=' ', id='3', style=ButtonStyle.green),
                Button(label=' ', id='4', style=ButtonStyle.green),
                Button(label=' ', id='5', style=ButtonStyle.green)
            ],
            [
                Button(label=' ', id='6', style=ButtonStyle.green),
                Button(label=' ', id='7', style=ButtonStyle.green),
                Button(label=' ', id='8', style=ButtonStyle.green)
            ]
        ]
        embed = discord.Embed(title="Tic Tac Toe", color=0xfee020)
        await ctx.send(embed=embed)
        message = await ctx.send(
            components=buttons
        )
        while(isRunning):
            for line in buttons:
                for btn in line:
                    if board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'x':
                        btn.style = ButtonStyle.blue
                        btn.disabled = True
                        btn.label = 'X'
                    elif board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'o':
                        btn.style = ButtonStyle.red
                        btn.disabled = True
                        btn.label = 'O'

            isEnd = checkwin(createboard(board), ctx)
            if isEnd[0] != True:
                for line in buttons:
                    for btn in line:
                        btn.disabled = True
                        if board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'x':
                            btn.style = ButtonStyle.blue
                            btn.disabled = True
                            btn.label = 'X'
                        elif board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'o':
                            btn.style = ButtonStyle.red
                            btn.disabled = True
                            btn.label = 'O'
                for ind in isEnd[2]:
                    buttons[getIndex(ind)[0]][getIndex(ind)[1]
                                              ].style = ButtonStyle.grey
                await message.edit(components=buttons)
                if isEnd[1] == 'x':
                    embed = discord.Embed(title="Human win!", color=0x5746dd)
                    await ctx.send(embed=embed)
                elif isEnd[1] == 'o':
                    embed = discord.Embed(title="Bot win!", color=0xff0000)
                    await ctx.send(embed=embed)
                elif isEnd[1] == 'tie':
                    embed = discord.Embed(title="Tie!", color=0xffffff)
                    await ctx.send(embed=embed)
                break

            await message.edit(components=buttons)

            res = await client.wait_for("button_click")
            try:
                await res.respond()
            except:
                pass
            if (res.channel == ctx.channel) and (res.user == ctx.author):
                indexes = getIndex(res.component.id)
                board[indexes[0]][indexes[1]] = 'x'
                isEnd = checkwin(createboard(board), ctx)
                if isEnd[0] != True:
                    for line in buttons:
                        for btn in line:
                            btn.disabled = True
                            if board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'x':
                                btn.style = ButtonStyle.blue
                                btn.disabled = True
                                btn.label = 'X'
                            elif board[getIndex(btn.id)[0]][getIndex(btn.id)[1]] == 'o':
                                btn.style = ButtonStyle.red
                                btn.disabled = True
                                btn.label = 'O'
                    for ind in isEnd[2]:
                        buttons[getIndex(ind)[0]][getIndex(
                            ind)[1]].style = ButtonStyle.grey
                    await message.edit(components=buttons)
                    if isEnd[1] == 'x':
                        embed = discord.Embed(
                            title="Human win!", color=0x5746dd)
                        await ctx.send(embed=embed)
                    elif isEnd[1] == 'o':
                        embed = discord.Embed(title="Bot win!", color=0xff0000)
                        await ctx.send(embed=embed)
                    elif isEnd[1] == 'tie':
                        embed = discord.Embed(title="Tie!", color=0xffffff)
                        await ctx.send(embed=embed)
                    break
            s = start(createboard(board))
            board[s[0][0]][s[0][1]] = 'o'
            isRunning = isEnd[0]

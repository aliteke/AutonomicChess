import os
import chess
import chess.engine
import chess.svg
from autonomicChessManager import autonomicChessManager
import random
import time
import matplotlib.pyplot as plt
import numpy as np
#these params are used to setup the test (can also be though of as high level policy for the autonomic system)
numIters = 50
moveTimeoutDuration = 0.1

#this script will be used in order to run tests on the autonomic chess system
#hardcode the "optimal" engine as well as the test engine's paths
dirname = os.path.dirname(__file__)
testEngineDirPath = os.path.join(dirname, 'chessEngineTestDirectory')
#TODO stockfish used as an optimal engine right now for testing because it is radically more reliable than others
optimalEnginePath = os.path.join(dirname, 'optimalEngineDirectory\stockfish-windows-x86-64-avx2.exe')

#for loop in which monte-carlos will be run
for iter in range(0,numIters):
    #initialize an empty board
    board = chess.Board()
    #initialiaze the autonomic manager
    manager = autonomicChessManager(optimalEnginePath,testEngineDirPath,moveTimeoutDuration)

    #draw an opponent from the test set
    opponentName = random.choice(os.listdir(testEngineDirPath))
    opponentPath = os.path.join(testEngineDirPath, opponentName)
    opponentEngine = chess.engine.SimpleEngine.popen_uci(opponentPath)

    #while the game is incomplete continue playing
    print("selected opponent",opponentName)
    while not board.is_game_over():
        #if it is white's turn let opponent play
        if(board.turn == chess.WHITE):
            #simply use the engine.play command
            result = opponentEngine.play(board, chess.engine.Limit(time=moveTimeoutDuration))
            board.push(result.move)
            print("opponent played",result.move)
        #else let manager play
        else:
            #use the makeNextMove command
            moveToMake = manager.makeNextMove(board)
            board.push(moveToMake)
        #log anything we'd want to keep on a turn-by-turn basis
        #boardsvg = chess.svg.board(board, size=350)

        #with open('temp.svg', 'w') as outputfile:
        #    outputfile.write(boardsvg)
        #time.sleep(0.1)
        #os.startfile('temp.svg')
    #log who won, and the state the autonomic manager was in
    print("outcome is",board.outcome())
    #use pyplot to show similarity scores over time
    fig, ax = plt.subplots()
    for count, y_vals in enumerate(manager.plot_y_lists):
        while(len(y_vals) < len(manager.plot_x)):
            y_vals.append(0)
        plt.plot(manager.plot_x,y_vals,label=manager.defeatorsList[count].botName)
        plt.xlabel("number of moves")
        plt.ylabel("similarity score")
        plt.title("Similarity over time for game played against " + opponentName)
        plt.figlegend()
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig('detectorTest/outputMapping'+opponentName+str(iter)+".png")

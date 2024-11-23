import os
import chess
import chess.engine
import chess.svg
from autonomicChessManager import autonomicChessManager
import random
import matplotlib.pyplot as plt
import pandas as pd
#these params are used to setup the test (can also be though of as high level policy for the autonomic system)
numIters = 1000
moveTimeoutDuration = 0.1

#this script will be used in order to run tests on the autonomic chess system
#hardcode the "optimal" engine as well as the test engine's paths
dirname = os.path.dirname(__file__)
testEngineDirPath = os.path.join(dirname, 'chessEngineTestReformed')
optimalEnginePath = os.path.join(dirname, 'optimalEngineDirectory\stockfish-windows-x86-64-avx2.exe')
#store the optimal opponent mapping, using the CCRL competition feature this will be the opponent each bot is weakest against
optimalMatch = { "stockfish-windows-x86-64-avx2.exe" : "stockfish-windows-x86-64-avx2.exe", "Clover.6.1-avx2.exe" : "igel-x64_popcnt_avx2_3_5_0.exe", "Alexandria-6.1.0-avx2.exe" : "stockfish-windows-x86-64-avx2.exe", "igel-x64_popcnt_avx2_3_5_0.exe": "stockfish-windows-x86-64-avx2.exe", "Uralochka3.40a-avx2.exe": "Uralochka3.40a-avx2.exe" }

#for loop in which monte-carlos will be run
for iter in range(0,numIters):
    df = pd.DataFrame(columns=['turn','move_made','player','winner','detected?'])
    #initialize an empty board
    board = chess.Board()    
    #initialiaze the autonomic manager
    manager = autonomicChessManager(optimalEnginePath,testEngineDirPath,moveTimeoutDuration,optimalMatch)

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
            df = df._append({'turn' : len(board.move_stack),'move_made': result.move.uci(),'player':'opponent,'+opponentName,"detected?":manager.engineDetected},ignore_index = True)
        #else let manager play
        else:
            #use the makeNextMove command
            moveToMake = manager.makeNextMove(board)
            board.push(moveToMake)
            df = df._append({'turn' : len(board.move_stack),'move_made': moveToMake.uci(),'player':'autonomic',"detected?":manager.engineDetected},ignore_index = True)
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
        plt.title("Game played against " + opponentName + " bot detected " + manager.engineDetected)
        #plt.figlegend()
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.savefig('detectorTest/outputMapping'+opponentName+str(iter)+".png")
    df.to_csv("GameAgainst"+opponentName+str(iter)+".csv")

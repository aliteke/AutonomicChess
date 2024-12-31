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
moveTimeoutDuration = 1
#numAttemptsPerEval = 10
lst_numAttemptsPerEval = [5, 10, 20, 50, 100]
plt.switch_backend('agg')       #TODO:  testing to fix error about RuntimeError: main thread is not in main loop
                                #       Tcl_AsyncDelete: async handler deleted by the wrong thread

#this script will be used in order to run tests on the autonomic chess system
#hardcode the "optimal" engine as well as the test engine's paths
dirname = os.path.dirname(__file__)
# NOTE: appende avx2 to Lizard and Viridithas engine .exe files, for easy tracking in Windows Task Manager.
testEngineDirPath = os.path.join(dirname, 'latest_engines') #'chessEngineTestReformed')
#testEngineDirPath = os.path.join(dirname, 'chessEngineTestDirectory')
optimalEnginePath = os.path.join(dirname, 'latest_engines\stockfish_24122214_x64_avx2.exe')
# Create if doesn't exist, the directory to save the resulting images, csv and raw values(.txt) files.
os.makedirs("detectorTest/top_ten_engines/", exist_ok=True)

#store the optimal opponent mapping, using the CCRL competition feature this will be the opponent each bot is weakest against
"""
optimalMatch = {"stockfish-windows-x86-64-avx2.exe" : "stockfish-windows-x86-64-avx2.exe", 
                "Clover.6.1-avx2.exe" : "igel-x64_popcnt_avx2_3_5_0.exe", 
                "Alexandria-6.1.0-avx2.exe" : "stockfish-windows-x86-64-avx2.exe", 
                "igel-x64_popcnt_avx2_3_5_0.exe": "stockfish-windows-x86-64-avx2.exe", 
                "Uralochka3.40a-avx2.exe": "Uralochka3.40a-avx2.exe" 
}
"""
optimalMatch = {'Alexandria-7.1-avx2.exe'                   : 'stockfish_24122214_x64_avx2.exe',
                'berserk-13-avx2.exe'                       : 'stockfish_24122214_x64_avx2.exe',
                'caissa-1.21-x64-avx2.exe'                  : 'stockfish_24122214_x64_avx2.exe',
                'integral_v5_avx2.exe'                      : 'stockfish_24122214_x64_avx2.exe',
                'Lizard-10_5-win_avx2.exe'                  : 'stockfish_24122214_x64_avx2.exe',
                'Obsidian140-avx2.exe'                      : 'stockfish_24122214_x64_avx2.exe',
                'PlentyChess-2.1.0-avx2.exe'                : 'stockfish_24122214_x64_avx2.exe',
                'Starzix-6.0-avx2.exe'                      : 'stockfish_24122214_x64_avx2.exe',
                'stockfish_24122214_x64_avx2.exe'           : 'stockfish_24122214_x64_avx2.exe',
                'viridithas-15.0.0-win-x86-64-v3_avx2.exe'  : 'stockfish_24122214_x64_avx2.exe'
                }

#for loop in which monte-carlos will be run
for iter, numAttemptsPerEval in enumerate(lst_numAttemptsPerEval):
    #draw an opponent from the test set
    #TODO we will iterate over all the engines in the test set numIters times
    for opponentName in os.listdir(testEngineDirPath):
        # TODO: Add the similarity scores to the dataframe too.
        df = pd.DataFrame(columns=['turn','move_made','player','winner','detected?'])
        #initialize an empty board
        board = chess.Board()
        #initialiaze the autonomic manager
        manager = autonomicChessManager(optimalEnginePath,testEngineDirPath,moveTimeoutDuration,optimalMatch,numAttemptsPerEval)
        #opponentName = random.choice(os.listdir(testEngineDirPath))
        opponentPath = os.path.join(testEngineDirPath, opponentName)
        if not os.path.isfile(opponentPath):
            print(f"[+] Skipping {opponentName} as it is not a file ({opponentPath})...")
            continue
        # Open the opponent engine
        opponentEngine = chess.engine.SimpleEngine.popen_uci(opponentPath)
        # Get PID of the opponent engine
        opponentEngine_pid = opponentEngine.transport.get_pid()

        #while the game is incomplete continue playing
        print(f"[+] selected opponent (PID={opponentEngine_pid}): ",opponentName)
        while not board.is_game_over():
            #if it is white's turn let opponent play
            if(board.turn == chess.WHITE):
                #simply use the engine.play command
                result = opponentEngine.play(board, chess.engine.Limit(time=moveTimeoutDuration))
                board.push(result.move)
                print(f"[+] opponent ({opponentName}) played: ",result.move)
                df = df._append({'turn' : len(board.move_stack),'move_made': result.move.uci(),'player':'opponent,'+opponentName,"detected?":manager.engineDetected},ignore_index = True)
            #else let manager play
            else:
                #use the makeNextMove command
                moveToMake = manager.makeNextMove(board, opponentName)
                board.push(moveToMake)
                df = df._append({'turn' : len(board.move_stack),'move_made': moveToMake.uci(),'player':'autonomic',"detected?":manager.engineDetected},ignore_index = True)
            #log anything we'd want to keep on a turn-by-turn basis
            #boardsvg = chess.svg.board(board, size=350)

            #with open('temp.svg', 'w') as outputfile:
            #    outputfile.write(boardsvg)
            #time.sleep(0.1)
            #os.startfile('temp.svg')
        #log who won, and the state the autonomic manager was in
        if board.outcome().winner is None:
            winner = "Draw"
        elif board.outcome().winner == True:
            winner = "Autonomic"
        else:
            winner = "Opponent"
        print(f"[+] Opponent: {opponentName}, Outcome is: {board.outcome()}, Winner: {winner}, Detected: {manager.engineDetected}")
        #use pyplot to show similarity scores over time
        fig, ax = plt.subplots(figsize=(12, 9))
        for count, y_vals in enumerate(manager.plot_y_lists):
            while(len(y_vals) < len(manager.plot_x)):
                y_vals.append(0)
            plt.plot(manager.plot_x,y_vals,label=manager.defeatorsList[count].botName)
            plt.xlabel("number of moves")
            plt.ylabel("similarity score")
            plt.title(f"Opponent: {opponentName}, Bot Detected: {manager.engineDetected}, Winner: {winner}")
            #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), prop={'size': 6})# TODO: Moving the legend under the plot to make it more readable
            plt.legend(loc='best', prop={'size': 6})
            plt.tight_layout()
            plt.savefig(f'detectorTest/top_ten_engines/{opponentName}_numAttempts{numAttemptsPerEval}_iter{str(iter)}.png', dpi=600)
        plt.close(fig)
        # Save the raw values of the similarity scores to a text file.
        with open(f"detectorTest/top_ten_engines/{opponentName}_numAttempts{numAttemptsPerEval}_iter{str(iter)}_raw_values.txt", 'w') as f:
            f.write(str(manager.plot_x) + "\n")
            f.write(str(manager.plot_y_lists))
        # Save the similarity scores to a csv file.
        df.to_csv(f"detectorTest/top_ten_engines/{opponentName}_numAttempts{numAttemptsPerEval}_iter{str(iter)}.csv")

        # Close the opponent engine
        print(f"[+] Closing opponent engine {opponentName} (PID={opponentEngine_pid})")
        opponentEngine.quit()

        # Close the autonomic manager's bot detectors and defeators
        for detector in manager.detectorsList:
            if detector.botOfInterest is not None:
                print(f"[+] Closing detector engine ({detector.botName}) (PID={detector.pid})")
                detector.botOfInterest.quit()
        for defeator in manager.defeatorsList:
            if defeator.optimalEngine is not None:
                print(f"[+] Closing defeator engine ({defeator.botName}) (PID={defeator.optimalEngine_pid})")
                defeator.optimalEngine.quit()
            
        # Close the autonomic manager's optimal move generator
        if manager.optimalMoveGenerator.optimalEngine is not None:
            print(f"[+] Closing optimal move generator engine ({manager.optimalMoveGenerator.optimalEngineName}) (PID={manager.optimalMoveGenerator.optimalEngine_pid})")
            manager.optimalMoveGenerator.optimalEngine.quit()
        
        print(f"\n[+] Done with {opponentName} iteration {iter}.")



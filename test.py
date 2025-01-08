import asyncio
import chess
import chess.engine
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
import re
import psutil
import os

def main(path) -> int:
   #as a test we will implement a very simple "Bot defeater" for the stockfish model
   
   #start by loading the relevant engines
   # r"C:\\Users\\agben\\Downloads\\stockfish-windows-x86-64-avx2\\stockfish\stockfish-windows-x86-64-avx2.exe"
   #transport, engine = chess.engine.SimpleEngine.popen_uci(path)
   engine = chess.engine.SimpleEngine.popen_uci(path)
   ## For CPU, comment if want to use GPU
   #engine.configure({"Context": "cpu"})

   move_count=0
   compBoard = chess.Board()
   while not compBoard.is_game_over(): 
       #let stockfish make the first move
       result = engine.play(compBoard, chess.engine.Limit(time=0.1))
       if result.move is None:
           engine_name = path.split('\\')[-1]
           print(f"{engine_name} has no legal moves... Trying again.")
           time.sleep(1)
           continue
       #print(f"[+{move_count}+] {result.move}")
       move_count+=1
       compBoard.push(result.move)
       #push stockfish's move to the board
       #get a list of all unique legal moves from this position
       #iterate over legal moves
           #for each legal move we create a test board in which that position is pushed
           #eval the engine's response from this point
           #
   engine.quit()

   return move_count

def getStats():
   df = pd.DataFrame(columns=['gameNo','opponent','detected','winner'])
   str_table_3 = \
   """
   1 & Clover      & n/a       & Autonomic     & & &\\ 
   2 & Clover      & n/a       & Opponent      &  & &\\
   3 & Stockfish   & Stockfish & Autonomic     &  & &\\
   4 & Uralochka   & Igel      & Opponent      & & &\\
   5 & Igel        & Stockfish & Autonomic     & & &\\ 
   6 & Igel        & n/a       & Autonomic     & & &\\
   7 & Clover      & n/a       & Autonomic     & & &\\ 
   9 & Igel        & n/a       & Opponent      & & &\\
   8 & Alexandria  & n/a       & Opponent      & & &\\ 
   10 & Clover     & Clover    & Opponent      & & &\\ 
   11 & Stockfish  & n/a       & Opponent      & & &\\ 
   12 & Igel       & n/a       & Autonomic     & & &\\ 
   13 & Igel       & n/a       & Autonomic     & & &\\ 
   14 & Clover     & n/a       & Opponent      & & &\\ 
   15 & Alexandria & Stockfish & Autonomic     & & &\\ 
   16 & Stockfish  & Alexandria & Opponent      & & &\\ 
   17 & Stockfish  & Stockfish & Opponent      & & &\\ 
   18 & Stockfish  & n/a       & Opponent      & & &\\ 
   19 & Clover     & Uralochka & Opponent      & & &\\ 
   20 & Igel       & Igel      & Autonomic     & & &\\ 
   21 & Alexandria & n/a       & Autonomic     & & &\\ 
   22 & Stockfish  & n/a       & Autonomic     & & &\\
   23 & Uralochka  & Uralochka & Autonomic     & & &\\ 
   24 & Alexandria & Stockfish & Autonomic     & & &\\
   25 & Clover     & n/a       & Autonomic     & & &\\
   26 & Uralochka  & Stockfish & Autonomic     & & &\\
   27 & Uralochka  & n/a       & Autonomic     & & &\\
   28 & Stockfish  & n/a       & Autonomic     & & &\\
   29 & Clover     & n/a       & Opponent      & & &\\
   30 & Clover     & Clover    & Autonomic     & & &\\
   31 & Stockfish  & n/a       & Autonomic     & & &\\
   32 & Igel       & Stockfish & Autonomic     & & &\\
   33 & Igel       & n/a       & Autonomic     & & &\\ [1ex]
   """ 

   lines = [ x.strip().lstrip() for x in str_table_3.split("\n") if len(x) > 5 ]

   for index, line in enumerate(lines):
       df.loc[index] = [line.split()[0], line.split()[2], line.split()[4], line.split()[6]]  
       #print(index, line.split()[2])
   
   #print(df.sort_values(by=['opponent']))

   # Group by opponent column
   grouped = df.groupby('opponent')
   for name, group in grouped:
       num_detected = len(group[ group['detected'] == name ] )
       num_wins = len(group[ group['winner'] == 'Autonomic' ] )
       print(f"name: {name}, #games: {len(group)}, detected: {num_detected}, detect_rate: {100* (num_detected / len(group))}%, win_rate: {100 *(num_wins / len(group))}%")       #\ngroup:\n{group}")
   

def process_a_game(game_df):
    """
        game_df has 51 columns for each row. 
        Each row is one turn of the game where 10 bots do simulations number of times to calculate similarity score to the opponent's move.
    """
    opponent = game_df.iloc[0].Opponent
    numAttempts = int(game_df.iloc[0].Alex_matching_score.split('/')[-1])
    print(f"[+] PROCESS GAME: opponent: {opponent}, conf: {game_df.iloc[0].Conf}, total_turns: {game_df.iloc[-1].Turn}")

    game_df = game_df[['Turn','Conf','Alex_RunningScore', 'berserk_RunningScore', 'caissa_RunningScore', 'integral_RunningScore', \
                       'Lizard_RunningScore', 'Obsidian_RunningScore', 'PlentyChess_RunningScore', 'Starzix_RunningScore', \
                       'stockfish_RunningScore', 'viridithas_RunningScore']]
    game_df['Conf'] = pd.to_numeric(game_df['Conf'], errors='coerce',downcast='float')
    game_df['Alex_RunningScore'] = pd.to_numeric(game_df['Alex_RunningScore'], errors='coerce',downcast='float')
    game_df['berserk_RunningScore'] = pd.to_numeric(game_df['berserk_RunningScore'], errors='coerce',downcast='float')
    game_df['caissa_RunningScore'] = pd.to_numeric(game_df['caissa_RunningScore'], errors='coerce',downcast='float')
    game_df['integral_RunningScore'] = pd.to_numeric(game_df['integral_RunningScore'], errors='coerce',downcast='float')
    game_df['Lizard_RunningScore'] = pd.to_numeric(game_df['Lizard_RunningScore'], errors='coerce',downcast='float')
    game_df['Obsidian_RunningScore'] = pd.to_numeric(game_df['Obsidian_RunningScore'], errors='coerce',downcast='float')
    game_df['PlentyChess_RunningScore'] = pd.to_numeric(game_df['PlentyChess_RunningScore'], errors='coerce',downcast='float')
    game_df['Starzix_RunningScore'] = pd.to_numeric(game_df['Starzix_RunningScore'], errors='coerce',downcast='float')
    game_df['stockfish_RunningScore'] = pd.to_numeric(game_df['stockfish_RunningScore'], errors='coerce',downcast='float')
    game_df['viridithas_RunningScore'] = pd.to_numeric(game_df['viridithas_RunningScore'], errors='coerce',downcast='float')
    game_df.set_index('Turn', inplace=True)
    
    plt.figure(figsize=(12, 9))
    score_columns = [col for col in game_df.columns if col not in ['Turn', 'Conf']]
    ax = game_df.plot(y=score_columns)
    # Add Conf column with dotted line style
    ax = game_df.plot(y='Conf', linestyle=':', color='black', ax=plt.gca())
    #ax = game_df.plot()
    ax.set_title(f"Opponent: {opponent}")
    ax.set_xlabel('Number of Moves')
    ax.set_ylabel('Similarity & Confidence Score')
    plt.legend(['Alex', 'Berserk', 'Caissa', 'Integral', 'Lizard', 'Obsidian', 'PlentyChess', 'Starzix', 'Stockfish', 'Viridithas', 'Confidence'],
               loc='best', prop={'size': 4})
    plt.savefig(f'detectorTest/top_ten_engines/{opponent}_numAttempts{numAttempts}_new.png', dpi=600)
    plt.close()

def getScores(fname):
    df = pd.DataFrame(columns=['Opponent', 'Turn', 'Conf', 'Highest', 'Second', 'Avg', 'Min', 'Max', 'Std', 'Threshold', 'above_threshold', \
                               'Alex_matching_score', 'Alex_PreScore', 'Alex_RunningScore', 'Alex_NumMovesEvaluated', \
                                'berserk_matching_score', 'berserk_PreScore', 'berserk_RunningScore', 'berserk_NumMovesEvaluated', \
                                    'caissa_matching_score', 'caissa_PreScore', 'caissa_RunningScore', 'caissa_NumMovesEvaluated', \
                                        'integral_matching_score', 'integral_PreScore', 'integral_RunningScore', 'integral_NumMovesEvaluated', \
                                            'Lizard_matching_score', 'Lizard_PreScore', 'Lizard_RunningScore', 'Lizard_NumMovesEvaluated', \
                                                'Obsidian_matching_score', 'Obsidian_PreScore', 'Obsidian_RunningScore', 'Obsidian_NumMovesEvaluated', \
                                                    'PlentyChess_matching_score', 'PlentyChess_PreScore', 'PlentyChess_RunningScore', 'PlentyChess_NumMovesEvaluated', \
                                                        'Starzix_matching_score', 'Starzix_PreScore', 'Starzix_RunningScore', 'Starzix_NumMovesEvaluated', \
                                                            'stockfish_matching_score', 'stockfish_PreScore', 'stockfish_RunningScore', 'stockfish_NumMovesEvaluated', \
                                                                'viridithas_matching_score', 'viridithas_PreScore', 'viridithas_RunningScore', 'viridithas_NumMovesEvaluated'])
    ptrn_matching = r"matching: (\d+\/\d+),\s+previous_matchingScore: (None|\d*\.\d+|d+),\s+running_matchingScore: (\d*\.\d+|d+),\s+numberOfMovesEvaluated: (\d+)"
    # DEBUG: on turn:  1  confidence_score:  0.0  highestBotDetectorScore (Alexandria-7.1-avx2.exe):  0.8  secondHighestBotDetectorScore(Alexandria-7.1-avx2.exe):  0.8  averageDetectorScore: 0.36000000000000004  min_score: 0.0  max_score: 0.8  std_dev: 0.3072458299147443  threshold: 0.7299999999999999  #above_threshold: 2
    ptr2_matching = r"on turn:\s+(\d+)\s+confidence_score:\s+(\d*\.\d+e?-?\d*)\s+highestBotDetectorScore\s+\((.*\.exe)\):\s+(\d*\.\d+)\s+secondHighestBotDetectorScore\((.*\.exe)\):\s+(\d*\.\d+)\s+averageDetectorScore:\s+(\d*\.\d+)\s+min_score:\s+(\d*\.\d+)\s+max_score:\s+(\d*\.\d+)\s+std_dev:\s+(\d*\.\d+)\s+threshold:\s+(\d*\.\d+)\s+#above_threshold:\s+(\d+)"
    with open(fname, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                print(f"[+] Reached end of {fname}...")
                break
            if re.search(r'\[\+\] opponent \(.*\) played:', line):
                cur_row = {}
                opponent = line.split()[2].replace('(', '').replace(')', '')
                cur_row['Opponent'] = opponent

                # Alexandria
                line = f.readline()
                if not line:
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #Alexandria
                    #print(f"[+] Alexandria: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['Alex_matching_score'] = match.group(1)
                    cur_row['Alex_PreScore'] = match.group(2)
                    cur_row['Alex_RunningScore'] = match.group(3)
                    cur_row['Alex_NumMovesEvaluated'] = match.group(4)
                else:
                    continue
               
                # berserk
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #berserk
                   #print(f"[+] berserk: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                   cur_row['berserk_matching_score'] = match.group(1)
                   cur_row['berserk_PreScore'] = match.group(2)
                   cur_row['berserk_RunningScore'] = match.group(3)
                   cur_row['berserk_NumMovesEvaluated'] = match.group(4)
               
                # caissa
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                # TODO: There are 3 lines in the first game with PlentyChess where Caissa times out.
                while "timed out on move" in line:
                    print(f"[+] TIME OUT CAISSA")
                    line = f.readline()

                match = re.search(ptrn_matching, line)
                if match:   #caissa
                    #print(f"[+] caissa: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['caissa_matching_score'] = match.group(1)
                    cur_row['caissa_PreScore'] = match.group(2)
                    cur_row['caissa_RunningScore'] = match.group(3)
                    cur_row['caissa_NumMovesEvaluated'] = match.group(4)
               
                # integral
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #integral
                    #print(f"[+] integral: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['integral_matching_score'] = match.group(1)
                    cur_row['integral_PreScore'] = match.group(2)
                    cur_row['integral_RunningScore'] = match.group(3)
                    cur_row['integral_NumMovesEvaluated'] = match.group(4)

                # Lizard
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #Lizard
                    #print(f"[+] Lizard: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['Lizard_matching_score'] = match.group(1)
                    cur_row['Lizard_PreScore'] = match.group(2)
                    cur_row['Lizard_RunningScore'] = match.group(3)
                    cur_row['Lizard_NumMovesEvaluated'] = match.group(4)
                
                # Obsidian
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #Obsidian
                    #print(f"[+] Obsidian: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['Obsidian_matching_score'] = match.group(1)
                    cur_row['Obsidian_PreScore'] = match.group(2)
                    cur_row['Obsidian_RunningScore'] = match.group(3)
                    cur_row['Obsidian_NumMovesEvaluated'] = match.group(4)
               
                # PlentyChess
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #PlentyChess
                    #print(f"[+] PlentyChess: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['PlentyChess_matching_score'] = match.group(1)
                    cur_row['PlentyChess_PreScore'] = match.group(2)
                    cur_row['PlentyChess_RunningScore'] = match.group(3)
                    cur_row['PlentyChess_NumMovesEvaluated'] = match.group(4)
               
                # Starzix
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #Starzix
                    #print(f"[+] Starzix: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['Starzix_matching_score'] = match.group(1)
                    cur_row['Starzix_PreScore'] = match.group(2)
                    cur_row['Starzix_RunningScore'] = match.group(3)
                    cur_row['Starzix_NumMovesEvaluated'] = match.group(4)
                
                 # stockfish
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #stockfish
                    #print(f"[+] stockfish: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['stockfish_matching_score'] = match.group(1)
                    cur_row['stockfish_PreScore'] = match.group(2)
                    cur_row['stockfish_RunningScore'] = match.group(3)
                    cur_row['stockfish_NumMovesEvaluated'] = match.group(4)
               
                # viridithas
                line = f.readline()
                if not line: 
                    print(f"[+] EOF...")
                    break
                match = re.search(ptrn_matching, line)
                if match:   #viridithas
                    #print(f"[+] viridithas: matching: {match.group(1)}, previous: {match.group(2)}, running_score: {match.group(3)}, num_move_evaled: {match.group(4)}")
                    cur_row['viridithas_matching_score'] = match.group(1)
                    cur_row['viridithas_PreScore'] = match.group(2)
                    cur_row['viridithas_RunningScore'] = match.group(3)
                    cur_row['viridithas_NumMovesEvaluated'] = match.group(4)
           
                # on turn XX: confidence_score: ....
                line = f.readline()
                if not line:
                    print(f"[+] EOF...")
                    break
                match = re.search(ptr2_matching, line)
                if match:
                    # print(f"[+] turn: {match.group(1)}, conf_score: {match.group(2)}, highest({match.group(3)}): {match.group(4)}, \
                    #       second({match.group(5)}): {match.group(6)}, avg: {match.group(7)}, min: {match.group(8)}, max: {match.group(9)}, \
                    #       std: {match.group(10)}, threshold: {match.group(11)}, above_threshold: {match.group(12)}")
                    #df.loc[len(df)] = [turn,conf,highest,second,avg,min,max,std,threshold]
                    cur_row['Turn'] = match.group(1)
                    cur_row['Conf'] = match.group(2)
                    cur_row['Highest'] = match.group(4)
                    cur_row['Second'] = match.group(6)
                    cur_row['Avg'] = match.group(7)
                    cur_row['Min'] = match.group(8)
                    cur_row['Max'] = match.group(9)
                    cur_row['Std'] = match.group(10)
                    cur_row['Threshold'] = match.group(11)
                    cur_row['above_threshold'] = match.group(12)

                # Append the cur_row dict to the dataframe
                df.loc[len(df)] = cur_row
                #print(df)

    # iterate through the rows of the DataFrame and plot confidence scores and similarity scores for each game.
    cur_turn = 0
    row_index = 0
    cur_game_starting_index = 0
    game_number = 0
    for row in df.itertuples():
        if row.Opponent == "Alexandria-7.1-avx2.exe" and int(row.Alex_matching_score.split('/')[-1]) == 100:
            #print(row)
            continue

        if cur_turn < int(row.Turn):
            cur_turn = int(row.Turn)
            row_index += 1
            
        else:
            # NOTE: Try to plot the current game here.
            cur_df = df.iloc[cur_game_starting_index:row_index]
            #print(f"[+] game_number: {game_number}, cur_turn: {cur_turn}, row_index: {row_index}, df_start: {cur_game_starting_index}, df_end: {row_index-1} first_row_turn: {cur_df.iloc[0].Turn}, lastrow_turn: {cur_df.iloc[0].Turn}")
            process_a_game(cur_df)

            # NOTE: At this point we have reached the end of the current game, current row is first row of the next game.
            cur_game_starting_index = row_index
            game_number += 1
            cur_turn = int(row.Turn)
            row_index += 1


if __name__ == "__main__":
   """
   path_to_engines=os.path.join( os.getcwd(), r"latest_engines" )
   for engine in reversed(os.listdir(path_to_engines)):
       start = time.time()
       if "Rubi" in engine:
           continue 
       print(f"[+] {engine} starting...")
       lst_moves = []
       for i in tqdm(range(0, 10)):
           #num_moves = asyncio.run( main( os.path.join(path_to_engines, engine)))
           num_moves = main( os.path.join(path_to_engines, engine))
           lst_moves.append(num_moves)
       
       print(f"[+{engine}+] lst_moves: {lst_moves}, avg_moves: {sum(lst_moves) / len(lst_moves)}, max_moves: {max(lst_moves)}, min_moves: {min(lst_moves)}, time: {time.time() - start} sec.")
   """
   #getStats()

   getScores(fname = 'output1.txt')
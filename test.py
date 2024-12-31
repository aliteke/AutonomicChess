import asyncio
import chess
import chess.engine
import os
import pandas as pd
import time
from tqdm import tqdm
import psutil

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
    

if __name__ == "__main__":
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

    #getStats()
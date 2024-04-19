import asyncio
import chess
import chess.engine

async def main() -> None:
    
    #as a test we will implement a very simple "Bot defeater" for the stockfish model
    
    #start by loading the relevant engines
    transport, engine = await chess.engine.popen_uci(r"C:\\Users\\agben\\Downloads\\stockfish-windows-x86-64-avx2\\stockfish\stockfish-windows-x86-64-avx2.exe")

    compBoard = chess.Board()
    while not compBoard.is_game_over(): 
        #let stockfish make the first move
        result = await engine.play(compBoard, chess.engine.Limit(time=0.1))
        compBoard.push(result.move)
        #push stockfish's move to the board
        #get a list of all unique legal moves from this position
        #iterate over legal moves
            #for each legal move we create a test board in which that position is pushed
            #eval the engine's response from this point
            #

        
    await engine.quit()

asyncio.run(main())




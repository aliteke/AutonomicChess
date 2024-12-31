from converter.pgn_data import PGNData
import os
#this simply scans the "train" directory for .pgn files which can be converted to PDFs
#please update the directory path to reflect the path containing all .pgn files you are interested in converting to csv format
directory = "C:\\Users\\agben\\AutonomicChess\\AutonomicChess\\train"
for path, folders, files in os.walk(directory):
    for file in files:
        pgn_data = PGNData(os.path.join(directory, file,file))
        result = pgn_data.export()
        result.print_summary()
from parse_debates import DebateParser
import ngrams
import os
import mallet
import build_graph
import networkx

'''
main entry point for generating mallet input files project
'''
if __name__ == "__main__":
    # first parse and load the debates and create the mallet raw input
    parser = DebateParser("./data/debates")
    parser.parse()
    parser.build_text_for_mallet('./data/mallet_raw_statements.txt')

    # now generate and save bigrams for mallet replacement files
    ngrams.save_bigrams_for_replacement_file_txt([item[0] for sublist in parser.statements.values() for item in sublist],
                                      os.path.join("./data/mallet_files", "replacements.txt"))

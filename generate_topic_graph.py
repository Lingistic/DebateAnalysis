import mallet
import build_graph
import networkx

'''
main entry point for generating topic graphs
'''
if __name__ == "__main__":

    # assumes mallet has been trained

    model = mallet.MalletLDA('./Data/mallet_files/doc_topics.tsv',
                             './Data/mallet_files/topic_counts.tsv')

    g = build_graph.build_interaction_graph(model, .33)
    networkx.write_graphml(g, "./data/mallet_files/interaction_graph.graphml")
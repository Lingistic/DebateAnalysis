import csv
import re
import os
from glob import glob

class DebateParser:
    '''
    this class parses the debates and creates two files: a file with one statement per line (for training mallet) and a
    TSV file which contains the columns ["Speaker", "Statement", "Democrat", "GOP", "Debate Number"]
    '''

    def __init__(self, path):
        '''
        The constructor setups a dictionary of all statements, as well as a list of the debate files
        :param path:
        :return:
        '''
        self.debates = self.__build_debate_list(path)
        self.statements = dict()
        print ""

    def __build_debate_list(self, path):
        '''
        builds a list of all of the possible debates to parse by walking the path and looking for .txt extensions
        :param path: the path of debates to walk, each debate in its own .txt file
        :return: list
        '''
        return [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.txt'))]

    def parse(self):
        '''
        Loads each transcript from self.debates list and splits statements by political party and
        debate number, indexed by speaker
        :return:
        '''
        for debate in self.debates:
            self.statements.update(self.__split_transcript_by_speaker(debate))

    def build_text_for_mallet(self, output_file_path):
        '''
        dumps the statements from the statement dictionary into a simple .txt file with one statement per line,
        to be fed into mallet
        :param output_file_path:
        :return:
        '''
        with open(output_file_path, 'wb+') as output_file:
            for speaker in self.statements.keys():
                for statement in self.statements[speaker]:
                    text = statement[0]
                    dem = statement[1]
                    gop = statement[2]
                    debate_number = statement[3]
                    output_file.write(text.replace('\n', ' ') + "\n")

    def get_statements_by_speaker(self, speaker, debate_number, csv_file="../resources/debates/gop/raw_text.tsv"):
        '''
        returns a list of statement tuples (Statement, party, and debate number) for a given speaker and debate number
        :param speaker:
        :param debate_number:
        :param csv_file:
        :return:
        '''
        statements = list()
        with open(csv_file, 'rb') as open_file:
            reader = csv.reader(open_file, delimiter="\t")
            for row in reader:
                if int(row[2]) == debate_number and row[0] == speaker:
                    statements.append(row[1])

        return statements

    def __split_transcript_by_speaker(self, transcript_path):
        '''
        opens a transcript file and generates a dictionary of statement, political party, and
        debate number -- indexed by speaker
        :param transcript_path:
        :return:
        '''
        with open(transcript_path, 'rb') as transcript_file:
            text = transcript_file.read()

        statements = dict()
        # assuming there is only one digit in the filename, and that is the corresponding debate #
        debate_number = re.findall("\d+", transcript_path)[0]
        dem = gop = False;
        if "gop" in transcript_path.lower():
            gop = True
        elif "dem" in transcript_path.lower():
            dem = True
        assert dem != gop

        # debate transcript follows <SPEAKER:> convention before each statement
        speaker_regex = re.compile("(^[A-Z]+:\s*)", re.MULTILINE)
        result = speaker_regex.split(text)
        current_speaker = None
        for chunk in result:
            if chunk != '':
                if speaker_regex.match(chunk):
                    current_speaker = chunk.replace(" ", "").replace(":", "")
                    if current_speaker not in statements.keys():
                        statements[current_speaker] = list()
                    continue
                elif current_speaker is not None:
                    statements[current_speaker].append([chunk, dem, gop, debate_number])
        return statements

    def save_to_tsv(self, output):
        '''
        saves the full transcript tuples to TSV in the format
        [speaker]\t[statement]\t[DEM]\t[GOP]\tDebate_number]
        :param output:
        :return:
        '''
        with open(output, 'wb+') as output_file:
            writer = csv.writer(output_file, delimiter="\t")
            writer.writerow(["Speaker", "Statement", "Democrat", "GOP", "Debate Number"])
            for speaker in self.statements.keys():
                for statement in self.statements[speaker]:
                    text = statement[0]
                    dem = statement[1]
                    gop = statement[2]
                    debate_number = statement[3]
                    writer.writerow([speaker, text.replace('\n', ' '), dem, gop, debate_number])

if __name__ == "__main__":
    parser = DebateParser("./data/debates")
    parser.parse()
    parser.build_text_for_mallet('./data/mallet_raw_statements.txt')
    parser.save_to_tsv('./data/raw_statements.tsv')

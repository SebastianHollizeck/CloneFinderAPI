from alignments.AncestralState import AncestralState
from alignments.AncestralStatesList import AncestralStatesList
import os.path
import traceback

class AncestralStatesParser(object):

    """
        Parses ancestral states text files that are generated by the MEGA/MEGA-CC
        software as a part of Maximum Parsimony tree construction
        
        On success, call get_ancestral_states to a list of AncestralState objects
        generated from the ancestral states text file
    """
    def __init__(self):
        self._input_file_name = ''
        self._ancestral_states = AncestralStatesList()
        self._messages = []
        
    @property
    def input_file_name(self):
        return self._input_file_name
    
    @input_file_name.setter
    def input_file_name(self, value):    
        self._input_file_name = value
        
    @property
    def messages(self):
        return self._messages
    
    def parse(self):
        try:
            print 'parsing ancestral states file...'
            result = False
            if os.path.isfile(self._input_file_name) == False:
                IOError('ancestral states file not found')
            input_file = open(self._input_file_name, 'r')
            lines = input_file.readlines()
            input_file.close()
            self._set_filename(lines[1])
            self._set_newick_string(lines[4])
            index = 7
            while index < len(lines):
                self._parse_line(lines[index])
                index += 1
            result = (self._ancestral_states.num_nodes > 3)    
            if result == True:
                print 'successfully parsed ancestral states file: ' + str(self._ancestral_states.num_nodes) + ' taxa'
            else:
                print 'failed to parse ancestral states file'
            return result
        except Exception as e:
            traceback.print_exc()           
            self._messages.append(str(e))
            return False            
        
            
    def _parse_line(self, line):
        tokens = line.split()
        if len(tokens) == 0:
            return # blank line
        state = AncestralState()
        state.index = int(tokens[0])
        state.label = tokens[1]
        if tokens[2] != '-':
            state.des1 = int(tokens[2])
        if tokens[3] != '-':
            state.des2 = int(tokens[3])        
        index = 4
        seq_data = ''
        while index < len(tokens):
            seq_data += tokens[index]
            index += 1
        state.seq_data = seq_data
        self._ancestral_states.add_state(state)
        
        
    def _set_filename(self, line):
        tokens = line.split(':')
        self._ancestral_states.filename = tokens[1].strip()
        
    def _set_newick_string(self, line):
        tokens = line.split(':')
        self._ancestral_states.newick_string = tokens[1].strip()
        
    def get_ancestral_states(self):
        return self._ancestral_states
    
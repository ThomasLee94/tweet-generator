from classes.dictogram import Dictogram
from weighted_sample import output_random_word 
from get_text_from_corpus import read_file
import random

class Markov_nth_order(dict):
    def __init__(self, word_list=None, order=2):
        super(Markov_nth_order, self).__init__() # Initialise empty dictionary
        self.types = 0
        self.tokens = 0
        self.order = order
        if word_list is not None:
            self.create_dict_of_dict(word_list)

    def create_dict_of_dict(self, word_list):
        """ 
        Creating a dictionary of {(current_tuple):{next_type: 1}} structure.
        """
        list_length = len(word_list)
        for i in range(0, list_length-self.order):
            if i + 1 + self.order < list_length:
                # Tuple of nth order as current_tuple
                current_tuple = tuple(word for word in word_list[i: i + self.order])
                next_type = word_list[i + 1 + self.order]
                print(current_tuple)
                self.add_word_to_dict_of_dict(current_tuple, next_type)
            else:
                current_type = (word_list[i], word_list[i+self.order])
                next_word = 'END'
                self.add_word_to_dict_of_dict(current_type, next_word)

    def add_word_to_dict_of_dict(self, current_type, next_type): 
        """ 
        Adding new tuple key-value pairs  or incrementing next_next_word frequency if
        they exist.
        """ 
        if current_type in self:
            dictogram = self[current_type]
            # Dictogram class incrementing frequency if current_type is found 
            # in initialised dictionary.
            dictogram.add_count(next_type)
        else:
            # New {(current_type, next_word): {next_next_word: 1}} pair being added if current_type
            # is not found. Dictogram used to make histogram. 
            self[current_type] = Dictogram(next_type)
            self.types += 1
            self.tokens += 1
    
    def generate_random_sentence(self, word_list, sentence_length=8):
        """ 
        Generating a random sentence from given corpus using markov chains,
        returning as a list. 
        """
        random_sentence_output = list()
        # I will use a completely random word as my first word.
        random_index = random.randint(0, len(self.keys())-1)
        random_type = list(self.keys())[random_index]
        random_word = random_type[0]
        next_words = list(random_type[1:self.order])
        random_sentence_output.extend((word for word in random_type))
        print('random word')
        
        output_count = 1
        # * Now using 2nd order markov chains to append the most likely "next_next_word"
        while output_count < sentence_length:
            try:
                random_word = output_random_word(self[random_word])
                if not random_word == 'END':
                    random_sentence_output.append(random_word)
                    output_count += 1
                    
                    next_words.append(random_word)
                    random_word = tuple(next_words)
                    next_words = next_words[1:self.order]
                # 'END' will be used to check if the random word picked is not at the
                # end of the given words_list. If it is, there can be no "next_next_word". 
                else:
                    new_index = random.randint(0, len(self.keys()) - 1)
                    random_word = list(self.keys())[new_index]
            except KeyError:
                 new_index = random.randint(0, len(self.keys()) - 1)
                 random_word = list(self.keys())[new_index]
                 next_word = random_word[1]

        return random_sentence_output



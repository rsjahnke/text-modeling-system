#
# Final Project
#
#
# Part I: Building an initial text model
# Part II: Saving and retrieving a text model
# Part III: Adding features to the model
# Part IV: Adding a Bayesian scoring algorithm
# Part V: Comparing Texts
#
#
# name: Rebecca Jahnke
# email: rsjahnke@bu.edu
#


import math 


def clean_text(txt): # regular function, not a method of the below TextModel class! 
    """ returns a list containing the words in txt after it has been 'cleaned.' function
        used when you need to process each word in a text individually, without havng to
        worry about punctuation or special characters.
        input -- txt, a string of text (str)
    """    
    # use string method lower to convert all characters to lowercase
    clean_txt = txt.lower()  

    # use string method replace to replace common punctuation symbols 
    clean_txt = clean_txt.replace('.', '')
    clean_txt = clean_txt.replace(',', '')
    clean_txt = clean_txt.replace('?', '')
    clean_txt = clean_txt.replace('!', '')
    clean_txt = clean_txt.replace('/', '')
    clean_txt = clean_txt.replace('(', '')
    clean_txt = clean_txt.replace(')', '')
    clean_txt = clean_txt.replace('--', '')
    clean_txt = clean_txt.replace("'", '')
    clean_txt = clean_txt.replace('"', '')
    clean_txt = clean_txt.replace('[', '')
    clean_txt = clean_txt.replace(']', '')
    clean_txt = clean_txt.replace(':', '')
    clean_txt = clean_txt.replace(';', '')
    clean_txt = clean_txt.replace('-', '')
    clean_txt = clean_txt.replace('é', 'e')
    
    # split string of text into list of words
    word_list = clean_txt.split()  

    # return list of words
    return word_list


def stem(s): # helper function, defined outside TextModel class!
    """ returns the stem of word s--the root part of the word, which excludes any prefixes and suffixes.
        input s -- str
    """
    # list handles special cases
    special_cases = ['my', 'guy', 'boy', 'toy', 'they', 'way', 'any']
    if s in special_cases:
        return s 

    # general rule for words ending in -thing
    elif s[-5:] == 'thing':
        if len(s) >= 8:
            s = s[:-5]

    # general rules for words ending in -ing
    elif s[-3:] == 'ing':
        if len(s[0:-3]) == 1 or len(s[0:-3]) == 2:
            s = s
        elif len(s[0:-3]) == 3:
            s = s[0:-3] + 'e'
        elif s[-4] == 'y':
            s = s[:-4] + 'i'
        elif s[-4] == s[-5] and len(s[:-5]) > 2: 
            s = s[:-4]    
        else:  
            s = s[:-3] 

    # general rules for words ending in -er
    elif s[-2:] == 'er':
        if len(s) >= 4:
            if s[-3] == s[-4]:
                s = s[:-3]
            else:
                s = s[:-2]

    # general rule for words ending in -ies
    elif s[-3:] == 'ies':
        s = s[:-2]

    # general rule for words ending in -ers
    elif s[-3:] == 'ers':
        s = s[:-3]

    # general rule for words ending in -s
    elif s[-1] == 's':
        s = s[:-1]
        stem(s)

    # general rule for words ending in -y 
    elif s[-1] == 'y':
        s = s[:-1] + 'i'
        stem(s)
        
    return s


def sample_file_write(filename): # sample write function 
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
       input -- filename, str representing a txt file
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.


def sample_file_read(filename): # sample read function
    """A function that demonstrates how to read a
       Python dictionary from a file.
       input -- filename, str representing a txt file
    """
    f = open(filename, 'r')    # Open for reading.
    dict_str = f.read()        # Read in a string that represents a dict.
    f.close()                  # Close the file. 

    dict = eval(dict_str)      # Evaluate the string to a dictionary.

    print("Inside the newly-read dictionary, dict, we have:")
    print(dict)


class TextModel: # create class for TextModel objects, a blueprint for objects modeling a body of text  
    """ a data type for a TextModel object.
    """
    
    def __init__(self, model_name): 
        """ a constructor for TextModel objects. function lets you build and name a TextModel
            and initialize its dictionaries.
            inputs -- self (TextModel object) and model_name (str)
        """
        # initialize its attributes 
        self.name = model_name      # string that is a label for TextModel
        self.words = {}             # dictionary for number of times each word appears
        self.word_lengths = {}      # dictionary for number of times each word length appears
        self.stems = {}             # dictionary for number of times each word stem appears
        self.sentence_lengths = {}  # dictionary for number of times each sentence length appears

    def __str__(self):
        """ returns a string representation of the TextModel that includes the name of
            the model as well as the sizes of the dictionaries for each feature of the
            text. function used for getting info on a specific TextModel's attributes.
            input -- self (TextModel object)
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'

        return s

    def __repr__(self):
        """ returns a string representing the called TextModel object. function lets us
            evaluate Textmodel object directly from the Shell.
            input -- self (TextModel object)
        """
        return str(self) # calls __str__ method

    def add_string(self, s):
        """ analyzes the string txt and adds its pieces to all of the dictionaries in this
            text model. function used when you want to add text to a model by augmenting
            the feature dictionaries defined in the constructor.
            inputs -- self (TextModel object) and s, a string of text (str)
        """
        # code for updating the sentence_lengths dictionary (done before cleaning string s of punctuation). 
        count = 0 # initialize counter variable
        split_text = s.split() # split s into words 

        for next_word in split_text:
            count += 1 # count words...
            if next_word[-1] in '.!?': # until you reach last word in a sentence! then, update dictionary.
                if count not in self.sentence_lengths:
                    self.sentence_lengths[count] = 1
                else: # elif count in self.sentence_lengths:
                    self.sentence_lengths[count] += 1
                count = 0 # reset counter for next sentence in split_text.

        # call clean_text to clean the text and split into a list of words
        words = clean_text(s) 

        # code for updating the words dictionary.
        for w in words:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        # code for updating the word_lengths dictionary.
        for w in words:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1

        # code for updating the word_stems dictionary.
        for w in words:
            word_stem = stem(w) # call stem function to get stem for each word 
            if word_stem not in self.stems:
                self.stems[word_stem] = 1
            else:
                self.stems[word_stem] += 1

    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model. function for
            when you want to read an entire file of text into a model (by first reading the
            text file into a string and then adding that string to the model with add_string
            method). 
            inputs -- self (TextModel object) and filename, a string representing a txt file (str)
        """
        file = open(filename, 'r') # open file
        text = file.read()         # read file into a string
        file.close()               # close file 

        self.add_string(text) # method call to add_string to add string of text, text, to the model

    def save_model(self):
        """ saves the TextModel object self by writing its various feature dictionaries to
            files. there will be one file written for each feature dictionary.
            input -- self (TextModel object)
        """
        # code for writing words dictionary to a file
        d = self.words
        f = open(self.name + '_words', 'w')
        f.write(str(d))
        f.close()

        # code for writing word_lengths dictionary to a file 
        d2 = self.word_lengths
        f = open(self.name + '_word_lengths', 'w')
        f.write(str(d2))
        f.close()

        # code for writing stems dictionary to a file 
        d3 = self.stems
        f = open(self.name + '_stems', 'w')
        f.write(str(d3))
        f.close()

        # code for writing sentence_lengths dictionary to a file 
        d4 = self.sentence_lengths
        f = open(self.name + '_sentence_lengths', 'w')
        f.write(str(d4))
        f.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their files
            and assigns them to the attributes of the called TextModel.
            input -- self (TextModel object)
        """
        # code for reading stored words dictionary from its file and assigning it to self.words
        f = open(self.name + '_words', 'r')
        dict_str = f.read()
        f.close()
        dict = eval(dict_str)
        self.words = dict 

        # code for reading stored word_lengths dictionary from its file and assigning it to self.word_lengths
        f = open(self.name + '_word_lengths', 'r')
        dict_str2 = f.read()
        f.close()
        dict = eval(dict_str2)
        self.word_lengths = dict

        # code for reading stored stems dictionary from its file and assigning it to self.stems
        f = open(self.name + '_stems', 'r')
        dict_str3 = f.read()
        f.close()
        dict = eval(dict_str3)
        self.stems = dict

        # code for reading stored sentence_lengths dictionary from its file and assigning it to self.sentence_lengths
        f = open(self.name + '_sentence_lengths', 'r')
        dict_str4 = f.read()
        f.close()
        dict = eval(dict_str4)
        self.sentence_lengths = dict

    def similarity_score(self, other):
        """ returns the log probability that the text from which the other model was derived
            is related to the text from which self's model was derived. method treats self as the
            original text model and the other model as a new 'mystery' text model, and returns the similarity
            score b/w them using logs.
            inputs -- self (TextModel object) and other (TextModel object)
        """
        # call dic_score to get similarity_score for self.words and other.words
        self_dic = self.words
        other_dic = other.words
        words_score = dic_score(self_dic, other_dic)

        # call dic_score to get similarity_score for self.word_lengths and other.word_lengths
        self_dic = self.word_lengths
        other_dic = other.word_lengths
        word_lengths_score = dic_score(self_dic, other_dic)

        # call dic_score to get similarity_score for self.stems and other.stems
        self_dic = self.stems
        other_dic = other.stems
        word_stems_score = dic_score(self_dic, other_dic)

        # call dic_score to get similarity_score for self.sentence_lengths and other.sentence_lengths
        self_dic = self.sentence_lengths
        other_dic = other.sentence_lengths
        sentence_lengths_score = dic_score(self_dic, other_dic) 


        # average above similarity scores together to get an overall score 
        overall_similarity_score = (words_score + word_lengths_score + word_stems_score + sentence_lengths_score) / 4
        return overall_similarity_score 


# helper function for similarity_score method of TextModel class
# defined outside TextModel class! 
def dic_score(self_dic, other_dic):
    """ returns the similarity score between a dictionary of self and the corresponding dictionary of
        other using logs. function used to find the similarity scores between individual attributes of two
        TextModels when computing the overall similarity score between the models! 
        inputs -- self_dic and other_dic (dictionaries)
    """
    dic_score = 0

    total = 0
    for item in self_dic:
        total += self_dic[item]

    for item in other_dic:
        if item in self_dic:
            num_appearances = self_dic[item]
            probability = num_appearances / total
            item_score = other_dic[item] * math.log(probability)
            dic_score += item_score
        else: # elif item not in self_dic
            default_probability = 1 / total
            item_score = other_dic[item] * math.log(default_probability)
            dic_score += item_score

    return dic_score 


# defined outside TextModel class!
def compare_texts():
    """A function to create text models and
       calculate similarity scores for bodies of text.
       function for when you want to use similarity scores and text models
       to determine which of two texts another text is more like!
       no inputs. 
    """
    # create model and add files for Cosmo magazine (orig1)
    cosmo_model = TextModel('Cosmopolitan Magazine')
    cosmo_model.add_file('cosmo_rough-sex.txt')
    cosmo_model.add_file('cosmo_model.txt')
    cosmo_model.add_file('cosmo_carrie.txt')
    cosmo_model.save_model()

    # create model and add files for GQ magazine (orig2)
    gq_model = TextModel('GQ Magazine')
    gq_model.add_file('gq_x-girl.txt')
    gq_model.add_file('gq_sex-trade.txt')
    gq_model.add_file('gq_brooklyn.txt')
    gq_model.add_file('gq_sports.txt')
    gq_model.save_model()

    # create model with extra file from Cosmo to test its similarity to Cosmo vs. GQ (new1)
    cosmo_test = TextModel('Cosmo Test')
    cosmo_test.add_file('cosmo_sex-positions.txt')
    score1 = cosmo_model.similarity_score(cosmo_test)
    print("The similarity between Cosmopolitan magazine and an additional Cosmo article is", score1)
    score2 = gq_model.similarity_score(cosmo_test)
    print("The similarity between GQ magazine and an additional Cosmo article is", score2)

    # create model with extra file from GQ to test its similarity to Cosmo vs. GQ (new2)
    gq_test = TextModel('GQ Test')
    gq_test.add_file('gq_mkerr.txt')
    score1 = cosmo_model.similarity_score(gq_test)
    print("The similarity between Cosmopolitan magazine and an additional GQ article is", score1)
    score2 = gq_model.similarity_score(gq_test)
    print("The similarity between GQ magazine and an additional GQ article is", score2)

    # create model with file from Rolling Stone to test its similarity with Cosmo vs. GQ (new3)
    rolling_stone_model = TextModel('Rolling Stone Magazine')
    rolling_stone_model.add_file('rolling_stone_berghain.txt')
    score1 = cosmo_model.similarity_score(rolling_stone_model)
    print("The similarity between Cosmopolitan magazine and Rolling Stone is", score1)
    score2 = gq_model.similarity_score(rolling_stone_model)
    print("The similarity between GQ magazine and Rolling Stone is", score2)

    # create model with file from Nylon to test its similarity with Cosmo vs. GQ (new4)
    nylon_model = TextModel('Nylon Magazine')
    nylon_model.add_file('nylon_emma.txt')
    score1 = cosmo_model.similarity_score(nylon_model)
    print("The similarity between Cosmopolitan magazine and Nylon is", score1)
    score2 = gq_model.similarity_score(nylon_model)
    print("The similarity between GQ magazine and Nylon is", score2)

    # create model with file from my writing to test its similarity with Cosmo vs. GQ (new5)
    my_model = TextModel("Rebecca's Writing")
    my_model.add_file('my_201.txt')
    score1 = cosmo_model.similarity_score(my_model)
    print("The similarity between Cosmopolitan magazine and my writing is", score1)
    score2 = gq_model.similarity_score(my_model)
    print("The similarity between GQ magazine and my writing is", score2)

    # create model with file from The New Yorker to test its similarity with Cosmo vs. GQ (new6)
    new_yorker_model = TextModel('The New Yorker Magazine')
    new_yorker_model.add_file('new_yorker_paris.txt')
    score1 = cosmo_model.similarity_score(new_yorker_model)
    print("The similarity between Cosmopolitan magazine and The New Yorker is", score1)
    score2 = gq_model.similarity_score(new_yorker_model)
    print("The similarity between GQ magazine and The New Yorker is", score2)
        

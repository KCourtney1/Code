"""
CMPSC 131 - Summer 2023 LEAP Section
Final Project
"""

# ==== START OF HELPER FUNCTIONS, DO NOT MODIFY ====

def intro():
    """
        Displays the header of the game
    """
    info="""     
         +---+
         O   |     HANGMAN 2.0
        /|\  |        Summer 2023
        / \  |          Developed by : <Kyle J Courtney>      
            ==="""
    print(info)

def sort_patterns(d):
    """
        Given a dictionary d, returns a list of (key,value) pairs that are sorted in ascending order based on the custom
        sorting function sort_priority

        >>> sort_patterns({'____': ['jazz', 'fork', 'cool', 'good', 'pond'], '___e': ['ache', 'blue', 'duke', 'hope'], 'e___': ['east', 'easy'], '_e__': ['deal', 'wear'], 'e__e': ['else'], '__e_': ['flew']})
        [('e__e', ['else']), ('__e_', ['flew']), ('_e__', ['deal', 'wear']), ('e___', ['east', 'easy']), ('___e', ['ache', 'blue', 'duke', 'hope']), ('____', ['jazz', 'fork', 'cool', 'good', 'pond'])]
    """
    sorted_patterns = list(d.items())
    sorted_patterns.sort(key=sort_priority)
    return sorted_patterns

def sort_priority(item):
    """
        Specifies the criteria for how the item should be sorted and returns:
        #1: The length of the value in the dictionary
        #2: The number of undercores in the key
        #3: The key itself

        >>> sort_priority(('____', ['jazz', 'fork', 'cool', 'good', 'pond'])) 
        (5, 4, '____')
        >>> sort_priority(('_e__', ['deal', 'wear'])) 
        (2, 3, '_e__')     
    """
    return (len_value(item), count_underscores(item), sort_keys_only(item))

# ==== END OF HELPER FUNCTIONS, DO NOT MODIFY ====

def len_value(item):
    """
        precondition: item is a tuple with a string[0] and an non-empty list of int[1]
        poscondition: returns an int of the total number of items in num_lst
    """
    return len(item[1])

def count_underscores(item):
    """
        precondition: item is a tuple with a string[0] and an non-empty list of int[1]
        poscondition: returns number of "_" in the string
    """
    count = 0
    for char in item[0]:
        if char == "_":
            count+=1
    return count

def sort_keys_only(item):
    """
        precondition: item is a tuple with a string[0] and an non-empty list of int[1]
        poscondition: returns the element at position 0 in the tuple item
    """
    return item[0]

# ==== MY FUNCTIONS ====

def get_words(filename,word_len):
    """
        precondition: filename is a string representing the name of the file you want to read, word_len is an int representing the lenght of the words you want to search for
        postcondition: returns a list of words with the len of word_len from the file given
    """
    import os
    target_path = os.path.join(os.path.dirname(__file__), filename)
    word_lst = []
    with open(target_path,"r") as the_file:
        contents = the_file.readlines()
        for line in contents:
            data = line.split()
            for word in data:
                if len(word) == word_len:
                    word_lst.append(word)
    return word_lst

def char_search(guess,word_lst):
    """
        postcondition: guess is a letter of the alphabet and word_lst is a non-list of strings
        postcondition: returns result which is a list of tuples with key[1] and words[2]
    """
    underscore_sort = {}
    for word in word_lst:
        key = ""
        for char in word:
            if char == guess:
                key += guess
            else:
                key+= "_"
        if key in underscore_sort:
            underscore_sort[key] += [word]
        else:
            underscore_sort[key] = [word]
    result = sort_patterns(underscore_sort)
    return result

def correct_letters(old_char,new_char):
    """
        precondition: both arguments are strings repersenting the correct letters guesssed
        prosconditionL returns a string of the combined letters in place of "_" if there.
        >>> missed_letters_s("___r","_o__")
        '_o_r'
    """
    result = ""
    for i in range(len(old_char)):
        if old_char[i] != "_":
            result += old_char[i]
        elif new_char[i] != "_":
            result += new_char[i]
        else:
            result += "_"
    return result

def game(attempts,word_lst,word_len):
    """
        precondtion: attempts is an positive int, word_lst is a list of strings, word_len in a int representing the length of the words you want to search for
        postcondition: prints the guessing section of the game hangman
    """
    assert 0<len(word_lst)>0, f"no words have {word_len} letters"
    count = 0
    old_char = "_"*word_len
    missed_letters = ""
    while count < attempts and "_" in old_char:
        print(f"{old_char}\nMissed letters: {missed_letters} ({attempts-count} chances left)")
        guess = input("Enter your guess: ")
        sorted_dic = char_search(guess,word_lst)
        new_char = correct_letters(old_char,sorted_dic[-1][0])
        word_lst = sorted_dic[-1][1]
        if new_char in old_char:
            missed_letters += guess+ " "
            count+=1
        else:
            old_char = new_char 
        print("")
    if not "_" in old_char:
        print(f"You guessed the word: {old_char}") 
    else:
        print(f"You lost after {attempts} wrong guesses.")  

def main():
    intro()
    filename = str(input("Enter the name of you words file: "))
    word_len = int(input("Enter the length of your word: "))
    attempts = int(input("Enter the number of attempts: "))
    word_lst = get_words(filename,word_len)
    print("Let's play!")
    game(attempts,word_lst,word_len)
   
def run_tests_b():
  import doctest
  doctest.run_docstring_examples(correct_letters, globals(), name="Final", verbose=True)

if __name__== "__main__":
    main()
    #run_tests_b()
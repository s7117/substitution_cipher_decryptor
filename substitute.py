#!/usr/bin/env python
"""
This file contains the functions which together lend to completing the task of
deciphering the substitution ciphertext.
"""
################################################################################
# Author: Peyton Chandarana
################################################################################
# Import Packages
import random
################################################################################
# (NOT USED) Get the frequencies of the letters in a string
def character_frequencies(in_str):
    """
    This function takes an instance of a string and returns the frequencies
    at which each character in the input string occurs.
    """
    # Remove the space and newline character
    stripped_str = in_str.replace(' ', '').strip()
    stripped_str_len = len(stripped_str)
    char_set = set(stripped_str)
    freqs = {}
    # Compute the frequencies.
    for char in char_set:
        freqs[char] = stripped_str.count(char) / stripped_str_len
    return freqs
################################################################################
# (NOT USED) Build a dictionary that maps word lengths to lists of words with
# that word length.
def build_dictionary(filename):
    """
    This function takes in a file of words each of arbitrary length. A
    dictionary is then created based on the length of the words with the
    key as the length and the values as words with that corresponding length.
    """
    len_dictionary = {}
    # File IO
    dict_file = open(filename)
    dict_lines = dict_file.readlines()
    dict_file.close()
    # For each line in the file.
    for line in dict_lines:
        # Remove punctuations and newlines
        dict_word = line.strip('\n').replace('\'', '').replace('.', '')
        # If the word length does not exist in the dictionary yet create it.
        if len(dict_word) not in len_dictionary.keys():
            len_dictionary[len(dict_word)] = []
        # Store the word in the dictionary
        len_dictionary[len(dict_word)].append(dict_word)
    return len_dictionary
################################################################################
def get_dict_words(filename):
    """
    Takes in the filename corresponding to the words in the dictionary, gets
    the words from the dictionary file, and then returns a list of the words
    found in the dictionary.
    """
    dict_words_list = []
    # File IO
    dict_file = open(filename)
    dict_lines = dict_file.readlines()
    dict_file.close()
    # For each line get the word and then append it to the list of words.
    for line in dict_lines:
        # Remove punctuations and newlines
        dict_word = line.strip('\n').replace('\'', '').replace('.', '')
        dict_words_list.append(dict_word)
    return dict_words_list
################################################################################
def get_similarity_key(word):
    """
    Takes in a word and then returns a list of lists to represent the indices
    of the letters that are repeated in a word. (i.e. 'all' would return
    [[1,2]] and 'floof' would return [[0,4],[2,3]])
    """
    parent_list = []
    temp_child_list = []
    # For each letter in the set of letters in a word check if the
    # letter is repeated in the word. If it is then store the index.
    for letter in set(word):
        for i in range(0, len(word)):
            # If letters are equal
            if letter == word[i]:
                temp_child_list.append(i)
        # If the letter was found more than once.
        if len(temp_child_list) > 1:
            parent_list.append(temp_child_list)
        # Clear the list for the next letter in sequence.
        temp_child_list = []
    return parent_list
################################################################################
def get_word_similarity_dictionary(word_list):
    """
    This function generates a dictionary which maps the word length to a key
    which is generated based on the indices of duplicate letters in a word.
    """
    ret_dict = {}
    # For each word in the word list from the dictionary.
    for word in word_list:
        # Create the dictionary entry if it DNE
        if len(word) not in ret_dict.keys():
            ret_dict[len(word)] = {}
        # Get the similarity key of the word
        sim_key = str(get_similarity_key(word))
        # Check if similarity key exists in dictionary.
        if sim_key not in ret_dict[len(word)].keys():
            ret_dict[len(word)][str(get_similarity_key(word))] = []
        # Add the word to the dictionary based on length and similarity key.
        ret_dict[len(word)][str(get_similarity_key(word))].append(word)
    return ret_dict
################################################################################
def update_putative_dictionary(putative_dict, mapping):
    """
    Takes in a putative dicitonary which maps the cipherwords as keys to lists
    of putative plainwords and a mapping which updates the keys in the
    dictionary as well as the lists in the value.
    """
    # Copy the putative dictionary.
    putative_dict_copy = putative_dict.copy()
    # For each key and value pair in the putative dictioanry.
    for key, value in putative_dict.items():
        # Check if there are any letters that can be updated in the key.
        # value[0] is a running version of the plaintext. Each time the mapping
        # is updated this is updated to reduce the size of the putative word
        # list.
        plain_key = value[0]
        # value[1] is the putative word list
        new_list = value[1].copy()
        # Update the plain word in the put dicitonary value[0]
        for i in range(0, len(key)):
            if key[i] in mapping.keys():
                plain_key = plain_key[:i] + mapping[key[i]] + plain_key[i+1:]
            else:
                plain_key = plain_key[:i] + '.' + plain_key[i+1:]
        # Update the list in the putative dictionary value[1]
        for put_word in value[1]:
            # If the intersection is empty then remove the word from the list.
            if len(set(plain_key).intersection(set(put_word))) == 0:
                new_list.remove(put_word)
        # Format data to return.
        new_value = (plain_key, new_list)
        putative_dict_copy[key] = new_value
    return putative_dict_copy

################################################################################
def query_similarity_dictionary(cipher_word, sim_dict):
    """
    This function queries the similarity dictionary for a cipher word's
    possible matches based on the similarity schema gotten in the
    get_similarity_key funciton.
    """
    ret_list = []
    # Get the similarity key of the cipher word
    cipher_word_key = str(get_similarity_key(cipher_word))
    # Check that the cipher word's length key is in the dict
    if len(cipher_word) in sim_dict.keys():
        # Check that the cipher word similarity key is in the dict
        if cipher_word_key in sim_dict[len(cipher_word)].keys():
            # The cipher word key was found.
            # Return the words in the dict.
            ret_list = sim_dict[len(cipher_word)][cipher_word_key]
    return ret_list
################################################################################
# (NOT USED)
def get_dict_vs_sim_dict(reg_dict, sim_dict, word_len, cipherword):
    """
    This function just gets the sizes of the possible words in the similarity
    dictionary vs. the length based dictionary and prints them out.
    """
    # Get length of putative word list from similarity dictionary.
    sim_dict_len = len(query_similarity_dictionary(cipherword, sim_dict))
    # Get length of putative word list of the length dictionary.
    reg_dict_len = len(reg_dict[word_len])
    print("SIMILARITY DICT LEN: "+str(sim_dict_len))
    print("REGULAR DICT LEN: "+str(reg_dict_len))
################################################################################
# (NOT USED)
def get_ciphertext_fragment(ciphertext):
    """
    This function gets only a portion of the cipher text and returns it
    as a list of cipherwords sorted by their lengths. The range can be random
    or it can be the first n words of the set of words in the ciphertext.
    """
    # Specify the number of words in a fragment and if the fragment start index
    # should be random.
    use_random = False
    frag_size = 30
    random_seed = 0
    random.seed(random_seed)
    # Split the cipher text into words, remove duplicates, and sort.
    ciphertext_set = sorted(list(set(ciphertext.split(' '))), key=len)
    # Get a random number in the range of the ciphertext_list
    # We set the upper bound as len(list) - fragment_size to prevent OOB errors.
    # If use_random is false then the index is set to zero.
    if len(ciphertext_set) > frag_size and use_random:
        frag_index = random.randint(0, len(ciphertext_set) - frag_size)
    else:
        frag_index = 0
    fragment = ciphertext_set[frag_index:frag_index+frag_size:1]
    fragment_str = ' '.join(fragment)
    return [fragment_str, fragment]
################################################################################
def print_plain_text(cipher_str, mappings):
    """
    This function takes in the ciphertext string and the cipher to plain letter
    mappings and then produces a plaintext using the mappings.
    """
    # For all letters in the cipher string
    for i in range(0, len(cipher_str)):
        # If a space is encounterd print space.
        if cipher_str[i] == ' ':
            print(' ', end='')
        # If a letter then check to see if it has been mapped.
        elif cipher_str[i] in mappings.keys():
            print(mappings[cipher_str[i]], end='')
        # Else just print a period as a place hold.
        else:
            print('.', end='')
    print('\n')
################################################################################
def decipher(ciphertext, sim_dict):
    """
    This function performs all the deciphering with a big loop which attempts
    to retrieve the plaintext from using the similarity dictionary to narrow
    down the putative words.
    """
    keep_running = True
    # Get a copy of the ciphertext
    cipher_str = ciphertext
    # Get a unique set of the cipher words
    cipher_list = list(set(ciphertext.split(' ')))
    # Print the ciphertext.
    print('CIPHERTEXT\t'+str(cipher_str))

    # The putative dictionary maps cipherwords ->
    # (copy of cipherword, list of possible plainwords)
    # The copy of the cipher word is for converting it to plain text and
    # updating the putative list.
    putative_dict = {}
    # The known mappings are the mappings which the user chooses are
    # appropriate letter mappings.
    known_mappings = {}

    # We first fill up the putative word list.
    for cipher_word in cipher_list:
        # Get the list of putative words from similarity dict
        put_list = query_similarity_dictionary(cipher_word, sim_dict)
        # Map the cipher word to a tuple with a copy of the
        # cipher word and the putative word list.
        putative_dict[cipher_word] = (cipher_word, put_list)

    # This is the main loop of the program which loops through the
    # putative words. This loop asks the user to inspect the possible
    # plaintext to see if it makes sense.
    ##### ENTER BIG LOOP #####
    while keep_running:
        # First we find the cipherwords that have the least
        # putative words.
        least = ''
        # For each cipher word in the putative dict
        for cipher_word in putative_dict.keys():
            if len(putative_dict[cipher_word][1]) != 0:
                # If the first time running we need to initialize the
                # the least variable as a valid cipher word.
                if least == '' and cipher_word != '':
                    least = cipher_word
                # Else check that the variable is not the empty string and
                # that the current cipher word has less putative words than the
                # current least and check that the putative word list not empty.
                if len(putative_dict[cipher_word][1]) < \
                len(putative_dict[least][1]):
                    # New cipherword with less putative words found.
                    least = cipher_word
        # Print the cipherword with the least putative words.

        # Print the putative word in the list
        # Recall that [0] is the running copy of the plain word.

        # Get the letters from the cipherword and map them
        # to the putative word.

        for put_word in putative_dict[least][1]:
            try_mappings = {}
            try_mappings.update(known_mappings)
            for i in range(0, len(put_word)):
                try_mappings[least[i]] = put_word[i]
            # If the intersection of plain letters between the put_word
            # and the already mapped plain letter are equal to the
            # set of put word letters then skip putative word.
            if not set(known_mappings.values()).intersection(set(put_word)) == \
                set(put_word):
                print(least)
                print(put_word)
                # Print new mappings.
                print('-----TRYING NEW MAP!-----')
                print_plain_text(cipher_str, try_mappings)
                # Print all mappings
                print('-----KNOWN MAPPINGS!-----')
                print_plain_text(cipher_str, known_mappings)
                # Get user input
                to_continue = input('\nEnter "keep" to save the mapping, ' +
                                    'or exit to exit. Hit return to remove ' +
                                    'the word and continue.\n')
                # Exit
                if to_continue == 'exit':
                    keep_running = False
                    break
                # Keep running and keep the mapping
                elif to_continue == 'keep':
                    # Merge letter mappings
                    known_mappings.update(try_mappings)

        # Now we update the putative list with the new mapping which
        # will reduce the set of putative words per cipher word due to
        # the new mappings being found.
        putative_dict = update_putative_dictionary(putative_dict, try_mappings)
        # Remove the word
        putative_dict.pop(least, None)
    ##### END OF BIG LOOP #####

    # Now we ask the user to do some cribbing if possible.
    continue_cribbing = True
    while continue_cribbing:
        # Print ciphertext and plaintext
        print('-----CIPHERTEXT-----')
        print(cipher_str+'\n')
        print('-----PLAINTEXT-----')
        print_plain_text(cipher_str, known_mappings)
        # Get input from user.
        crib_string = input('\nPlease enter a cipher letter and plain letter ' +
                            'with a space between them.\nEnter exit to exit.\n')
        # Check if the format of the input was correct
        if len(crib_string) == 3 and crib_string[1] == ' ':
            crib_mapping = {crib_string[0]:crib_string[2]}
            known_mappings.update(crib_mapping)
        # Exit
        elif crib_string == 'exit':
            break
        else:
            print('ERROR: Incorrect input. Enter a letter then a space and' +
                  'then another letter\n')

# Could add brute force down here.
################################################################################

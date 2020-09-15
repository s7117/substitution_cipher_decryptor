#!/usr/bin/env python
"""This program acts as the main driver program of the entire substitution
cipher decryptor."""
################################################################################
# Author: Peyton Chandarana
################################################################################
# Import packages
from utilities import arg_handler, file_to_string
from substitute import decipher, get_word_similarity_dictionary, \
                       get_dict_words
################################################################################
# Main driving part of program
def main():
    """
    The main driver of the program that calls upon the other supporting
    functions to complete a specific task.
    """
    filename, dictionary = arg_handler()
    print("--------------------------------------------------")
    print("USING DICTIONARY FILE:\n"+dictionary[0])
    print("USING CIPHERTEXT FILE:\n"+str(filename[0]))
    print("--------------------------------------------------")
    # Get a word length based dictioanry (Not used)
    # len_dict = build_dictionary(dictionary[0])
    # Get and the ciphertext as a string
    ciphertext = file_to_string(filename[0])
    # Generate the similarity dictionary
    sim_dict = get_word_similarity_dictionary(get_dict_words(dictionary[0]))
    # Call the deciphering program
    decipher(ciphertext, sim_dict)

# Call main function
if __name__ == "__main__":
    main()
################################################################################
# Unused code for future implementations
# For loop for doing several files
#     for file in filenames:
#         file_string = file_to_string(file)
#         char_freqs = character_frequencies(file_string)
#         for key, val in char_freqs.items():
#             print(str(key) + '---' + str(val))

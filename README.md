# Substitution Cipher Decryptor
Author: Peyton Chandarna

*** Note: This program's methodology of finding the possible words that fit does not always work on the first try. If you encount a ciphertext where you cannot get substitutions that make sense then run the program again. ***

*** Note: For an example of the output of the program see sample_plaintext.txt ***

## File Structure:
- main.py       - the main driver function of the entire program
- substitute.py - the functions that are used to decipher the ciphertext
- utilities.py  - some boilerplate-ish functions


# Running Instructions:
Run ```python3 main.py -h``` for the input schema:

For Example:  
```python3 main.py -f sample_ciphertext.txt -d list_of_words.txt```

```
usage: main.py [-h] -f filename -d dictionary

Decipher a substitution ciphertext.

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -f filename, --filename filename
                        Substitution ciphertext filename
  -d dictionary, --dictionary dictionary
                        File of unique words on each line
```

## Once the program has started:

When the program is started a dictionary is generated from the words in the dictionary file passed in as an argument. This takes a few seconds.

The cipher text will be displayed. Next, a cipherword with a guess will appear above their mappings into a plaintext string.  

For example:
```
laflvlfjnr 
['individual']
-----TRYING NEW MAP!-----
.. ..un.....n ..i. ...a.i.n i. n.. al.n. ... ad.ini...a.i.n

-----KNOWN MAPPINGS!-----
.. .......... .... ........ .. ... ..... ... ..............
```

Look at the '-----TRYING NEW MAP!-----' section in the terminal and inspect if the plain letters make any sense. Specifically look to see if any new words were formed.

Now do one of the following when prompted:
- If the plaintext appears to make sense in the 'TRYING NEW MAP!' section (i.e. new words were formed, there are lots of duplicates, or contains 'a' and 'i' as single letter words) type 'keep' and press enter to keep the mappings.
- If the plaintext does not make any sense, press return/enter.
- Enter the word 'exit' and press enter to exit the programattic guessing.

For example:
```
Enter "keep" to save the mapping, or exit to exit. Hit return to remove the word and continue.
keep
```
This keeps the letter mappings for future use in the '-----KNOWN MAPPINGS!-----' section.

This process repeats itself for many putative words that could be encrypted in the ciphertext as long as you wish. However, when more than one plainwords begin to map to the single cipherword you may need to stop soon.

After exiting the guessing part, cribs can be entered to fill in the rest manually. When prompted enter a cipher letter followed by a space followed by a plain letter can be entered to map the cipher letter to the plain letter manually.

For example:
```
Please enter a cipher letter and plain letter with a space between them.
Enter exit to exit.
a b
```
This replaces all 'a' characters in the ciphertext with 'b'.

After all letters have been filled in and the plaintext has been solved enter 'exit' to exit the program.

# Explanation:

### Definition of Similarity Key:
- A key (list of lists) which is generate based on the indices of duplicate letters throughout a word. (i.e. the key for the word 'similarity' is [[1,3,7]])

### The Similarity Dictionary:
When you run the Python 3 script with the ciphertext filename and the dictionary of words as arguments the program first takes few seconds to generate a dictionary which does the following:

- Maps lengths of dictionary words (as the parent key) to similarity keys (child key) with a list of word(s) as the similarity keys' value. 

For example for the words hello and jello:
  
5 --> [[2,3]] --> ['hello', 'jello', ...]

Notice that 5 is the length of the word, [2,3] are the indices of the letter 'l' in both words.

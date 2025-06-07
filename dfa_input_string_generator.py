from DFA import parseFile, runDfa
import random
import os
import sys

class DFAFileNotFoundError(Exception):
    pass

# cross-platform friendly - works with backslashes and slashes depending on OS or distro
validFile = os.path.join("Generated Files", "valid_inputs.txt")
invalidFile = os.path.join("Generated Files", "invalid_inputs.txt")


validInputsFile = open(validFile, "w")
invalidInputsFile = open(invalidFile, "w")

if len(sys.argv) == 1:

    fileName = input("Give DFA Definition file name: ")

elif len(sys.argv) >= 2:

    fileName = sys.argv[1]

try:
    dfaDefinitionFile = os.path.join("DFA Definition Files", fileName)
    inputDfaFile = open(dfaDefinitionFile, "r")
except FileNotFoundError:
    raise DFAFileNotFoundError(f"DFA file not found") 

stringSeparator = " " # what separator do the symbols in the input string need, usually space or empty character
DFA = parseFile(inputDfaFile)
sigma = DFA[1]
NUMBER_OF_INPUT_LENGTHS = 100 # not to use magic numbers, kind of consts
MIN_LENGTH = 5 # minimum length 1 may cause a lot of duplicate input strings
MAX_LENGTH = 6 * len(sigma) # should be changed depending on the length of the alphabet
                            # for binary alphabet a 20 * len is okay, but for bigger ones it's not that recommended
NUMBER_OF_GENERATED_INPUTS = 1000
lengths = [random.choice(range(MIN_LENGTH, MAX_LENGTH)) for length in range(NUMBER_OF_INPUT_LENGTHS)] 
                                                                              # generating a number of possible input lengths from
                                                                              # 1 to 10 times the length of the 
seenInputs = set() # used to not show duplicate input strings

for generatedInputIndex in range(NUMBER_OF_GENERATED_INPUTS): # generating inputs strings
    length = random.choice(lengths) # getting their length randomly from the lengths list
    inputString = "" # initialising our randomly generated string with an empty string
    
    for symbolIndex in range(length):
        inputString += random.choice(sigma) # concatenating with the randomly generated symbol
        inputString += stringSeparator # adding the separator

    if inputString not in seenInputs:
        seenInputs.add(inputString)
    
generatedInputs = list(seenInputs)
generatedInputs.sort(key = lambda x: len(x)) # sorting generated non duplicate strings after their length

for generatedInput in generatedInputs:
    if runDfa(DFA, generatedInput, stringSeparator, False) == True:
        validInputsFile.write(generatedInput + "\n") # adding valid strings to their respective file
    else:
        invalidInputsFile.write(generatedInput + "\n") # adding invalid strings to their respective file

inputDfaFile.close()        
validInputsFile.close()
invalidInputsFile.close()
    

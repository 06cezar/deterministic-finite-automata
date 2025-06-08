from DFA import parseFile, runDfa
import random
import os
import sys

class DFAFileNotFoundError(Exception):
    pass

class InvalidArgumentError(Exception):
    pass # never trust user input:)

# cross-platform friendly - works with backslashes and slashes depending on OS or distro
validFile = os.path.join("Generated Files", "valid_inputs.txt")
invalidFile = os.path.join("Generated Files", "invalid_inputs.txt")


# default values for arguments 
stringSeparator = " " # what separator do the symbols in the input string need, usually space or empty character
NUMBER_OF_INPUT_LENGTHS = 100 # not to use magic numbers, kind of consts
MIN_LENGTH = 5 # minimum length 1 may cause a lot of duplicate input strings
MAX_LENGTH = 0 # we will parse the DFA file later => if not given another value it's default value will be 6 * |sigma|
NUMBER_OF_GENERATED_INPUTS = 1000
# end

validInputsFile = open(validFile, "w")
invalidInputsFile = open(invalidFile, "w")

if len(sys.argv) == 1:
    fileName = input("Give DFA Definition file name: ").strip()
    print("Press ENTER to keep the default value for any argument.")
    separatorInput = input("Give string separator (SPACE for ' ' / NOSEPARATOR for '' / custom, default: SPACE): ").strip()
    if separatorInput.upper() == "SPACE" or separatorInput == "": # also gives default
        stringSeparator = " "
    elif separatorInput.upper() == "NOSEPARATOR":
        stringSeparator = ""
    else:
        stringSeparator = separatorInput

    try:
        min_input = input(f"Minimum length (default: {MIN_LENGTH}): ").strip()
        if min_input: # keeps default value if empty string is given
            MIN_LENGTH = int(min_input)
            if MIN_LENGTH < 0:
                raise InvalidArgumentError("Minimum length must be non-negative.")
    except ValueError:
        raise InvalidArgumentError("Minimum length must be a valid integer.")

    try:
        max_input = input(f"Maximum length (default: 6 × |Σ|, where Σ is the alphabet of the DFA): ").strip()
        if max_input: # keeps default value if empty string is given
            MAX_LENGTH = int(max_input)
            if MAX_LENGTH < 0:
                raise InvalidArgumentError("Maximum length must be non-negative.")
    except ValueError:
        raise InvalidArgumentError("Maximum length must be a valid integer.")

    try:
        input_count = input(f"Number of inputs to generate (default: {NUMBER_OF_GENERATED_INPUTS}): ").strip()
        if input_count: # keeps default value if empty string is given
            NUMBER_OF_GENERATED_INPUTS = int(input_count)
            if NUMBER_OF_GENERATED_INPUTS < 0:
                raise InvalidArgumentError("Input count must be non-negative.")
    except ValueError:
        raise InvalidArgumentError("Input count must be a valid integer.")

    try:
        len_count = input(f"How many different lengths to generate (default: {NUMBER_OF_INPUT_LENGTHS}): ").strip()
        if len_count: # keeps default value if empty string is given
            NUMBER_OF_INPUT_LENGTHS = int(len_count)
            if NUMBER_OF_INPUT_LENGTHS < 0:
                raise InvalidArgumentError("Length count must be non-negative.")
    except ValueError:
        raise InvalidArgumentError("Length count must be a valid integer.")


elif len(sys.argv) >= 2:

    fileName = sys.argv[1]
    if fileName.lower() in ["--help", "-h"]: # bash-like help for CLI
        print("""
        Usage:
            python3 dfa_input_string_generator.py <dfa_filename> [separator] [min_len] [max_len] [input_count] [length_count]

        Arguments:
            dfa_filename     - Name of DFA file in 'DFA Definition Files/'
            separator        - SPACE / NOSEPARATOR / custom delimiter
            min_len          - Minimum length of generated input strings
            max_len          - Maximum length of input strings
            input_count      - Total number of inputs to generate
            length_count     - How many different lengths to generate

        Example:
            python3 dfa_input_string_generator.py game.dfa SPACE 5 30 1000 100
            """)
        sys.exit(0)

    # the following if statements are nested because if len(sys.argv) is not >= n => len(len(sys.argv)) is not >= n+1
    # even though not nesting 5 if statements may mean more readable code
    if len(sys.argv) >= 3:

        if (sys.argv[2]).upper() == "SPACE":
            stringSeparator = " "
        elif (sys.argv[2]).upper() == "NOSEPARATOR":
            stringSeparator = ""
        else:
            stringSeparator = sys.argv[2] 

        if len(sys.argv) >= 4:
            try:
                MIN_LENGTH = int(sys.argv[3])
            except ValueError:
                raise InvalidArgumentError("The MIN_LENGTH argument (the third one) needs to be a positive integer!")
            if MIN_LENGTH < 0: # for negative inputs 
                raise InvalidArgumentError("The MIN_LENGTH argument (the third one) needs to be a positive integer! Lengths can't be negative!")
            if len(sys.argv) >= 5:
                try:
                    MAX_LENGTH = int(sys.argv[4])
                except ValueError:
                    raise InvalidArgumentError("The MAX_LENGTH argument (the fourth one) needs to be a positive integer!")
                if MAX_LENGTH < 0: # for negative inputs 
                    raise InvalidArgumentError("The MAX_LENGTH argument (the fourth one) needs to be a positive integer! Lengths can't be negative!")
                if len(sys.argv) >= 6:
                    try:
                        NUMBER_OF_GENERATED_INPUTS = int(sys.argv[5])
                    except ValueError:
                        raise InvalidArgumentError("The NUMBER_OF_GENERATED_INPUTS argument (the fifth one) needs to be a positive integer!")
                    if NUMBER_OF_GENERATED_INPUTS < 0: # for negative inputs 
                        raise InvalidArgumentError("The NUMBER_OF_GENERATED_INPUTS argument (the fifth one) needs to be a positive integer! We can not generate negative numbers of strings!")    
                    if len(sys.argv) >= 7:
                        try:
                            NUMBER_OF_INPUT_LENGTHS = int(sys.argv[6])
                        except ValueError:
                            raise InvalidArgumentError("The NUMBER_OF_INPUT_LENGTHS argument (the sixth one) needs to be a positive integer!")
                        if NUMBER_OF_INPUT_LENGTHS < 0: # for negative inputs 
                            raise InvalidArgumentError("The NUMBER_OF_INPUT_LENGTHS argument (the sixth one) needs to be a positive integer! We can not generate negative numbers of lengths!")    
                        

try:
    dfaDefinitionFile = os.path.join("DFA Definition Files", fileName)
    inputDfaFile = open(dfaDefinitionFile, "r")
except FileNotFoundError:
    raise DFAFileNotFoundError(f"DFA file not found") 

DFA = parseFile(inputDfaFile)
sigma = DFA[1]
# changing the max_length default value if needed
if MAX_LENGTH == 0: # it wasn't given a value
    MAX_LENGTH = 6 * len(sigma) # should be changed depending on the length of the alphabet
                                # for binary alphabet a 20 * len is okay, but for bigger ones it's not that recommended

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

    if stringSeparator != "":
        inputString = inputString[:-1] # removes the last separator
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
    
print(f"{len(generatedInputs)} inputs generated.")
print(f"Results written to {validFile} and {invalidFile}")
# DFA stands for deterministic finite automaton M is a 5-tuple, (Q, Σ, δ, q0, F), consisting of
# a finite set of states Q
# a finite set of input symbols called the alphabet Σ
# a transition function δ : Q × Σ → Q
# an initial (or start) state q0∈Q
# a set of accepting (or final) states F⊆Q

class DFAError(Exception): # exception is a class that all built-in Python errors (like ValueError, TypeError) inherit from.
    pass                   # defining a custom error that behaves like a normal Python exception with subclasses that 
                           # help categorize different types of DFA errors

class UndefinedRuleError(DFAError):
    # raised when a rule for a source state, symbol tuple is missing
    # not used anymore - by convention when this error used to be raised the DFA just stays in it's current state
    pass

class DuplicateRuleError(DFAError):
    # raised when while parsing we find two rules that have the same source state and symbol, but different destination states
    pass

class UndefinedStartStateError(DFAError):
    # raised when the DFA doesn't have a start state
    pass

class UndefinedAcceptStatesError(DFAError):
    # raised when the DFA doesn't have any accept states
    pass

class UndefinedAlphabetError(DFAError):
    # raised when the DFA doesn't have an alphabet
    pass
class InvalidStateError(DFAError):
    # raised when an invalid/undefined state is encountered.
    pass

class InvalidSymbolError(DFAError):
    # raised when an invalid/undefined symbol is encountered.
    pass


class InputStringError(Exception):
    # raised when there isn't an error with the DFA, but with the input string fed into it (it contains characters not present in the DFA's alphabet)
    pass


def isComment(string):
    return string.startswith("#")
    # return string[0] == "#" would raise an IndexError for an empty string ""

def stringWithoutComments(string):
    return string[0 : string.index("#")] # does not raise an exception, as function is only called 
                                         # when character "#" exists in the string, and everything after
                                         # the first "#" shouldn't be processed
def isEmptyLine(string):
    return string == ""
        
def parseFile(inputDfaFile):
    lines = inputDfaFile.readlines()
    currentSection = "None"
    states = []
    sigma = [] # sigma = alphabet
    rules = {} # rules[sourceState] = {symbol : destinationState}
               # tules[sourceState][symbol] = destinationState
    start = "None" # a dfa can only have one start state
    accept = [] # a dfa can have multiple accept states
    inMultipleLineComment = False # boolean variable to allow multiple line comments starting with /* and ending with */
                               # is true if we are currently inside a multi line comment and we need to skip all lines until */
    for line in lines:
        line = line.strip() # eliminating whitespace
        
        # continue statements go to next iteration (next line) and are used for readability purposes,
        # could be replaced by elif statements
        
        if isComment(line) or isEmptyLine(line):
            continue # skipping lines that are comments
            
        if "#" in line: # filtering lines that contain comments
            line = stringWithoutComments(line) # only text before the comment is processed 
            line = line.strip() # eliminating possible whitespace before first "#" character
            
        if not inMultipleLineComment:
            
            if "/*" in line:
                
                inMultipleLineComment = True # we are inside a multiple line comment
                # even though we are now in a multiple line comment, it can still be used as a one-liner
                # and this needs to be checked
                multipleLineCommentStartIndex = line.find("/*") # gives the position of the first comment opener
                
                if "*/" in line:

                    multipleLineCommentLastStartIndex = line.rfind("/*") # more /* can be used in a line, checks for the last one
                    multipleLineCommentLastEndIndex = line.rfind("*/") # gives the position of the last ending comment symbol
                    
                    if multipleLineCommentLastStartIndex < multipleLineCommentLastEndIndex:
                        # then this is actually a one liner comment
                        inMultipleLineComment = False
                        line = line[:multipleLineCommentStartIndex] + line[multipleLineCommentLastEndIndex + 2:] # concatenates string before the comment and after the comment
                        line = line.strip()
                        # checks if there is anything to parse before and after the comment
                        
                else:   # not a one-liner comment - only need to check before the /* 
                    
                    line = line[:multipleLineCommentStartIndex] # checks if there is anything to parse before the comment
                    line = line.strip()
                    
                if isEmptyLine(line):
                    continue
            
            
            
        elif inMultipleLineComment: # this means that it's not the first line in the comment
                                    # elif statement ensures that the parser won't skip lines that are before the start of a multiple line comment
                                    # for example, q1, 1, q0 /* some text - would be skipped by the continue statement if not for the elif statement
            if "*/" in line:
                
                multipleLineCommentEndIndex = line.rfind("*/")
                line = line[multipleLineCommentEndIndex + 2:] # the string after the */ (is not a comment)
                inMultipleLineComment = False
                line = line.strip()
                if isEmptyLine(line):
                    continue
                
            else:
                continue # skip line that is completely within the multiple line comment
        
        if line[0] == "[": # new section starts here, filtering opening and closing pharantesis
            currentSection = line[1:-1]
            continue
        if line == "End":
            currentSection = "None" # searching for new section tag ([SectionName])
            continue
        
        if currentSection == "None":
            continue # skipping line, still searching for section tags ([SectionName])
        if currentSection == "States":
            states.append(line) 
            continue
        if currentSection == "Sigma":
            sigma.append(line)
            continue 
        if currentSection == "Rules":
            sourceState, symbol, destinationState = line.split(",")
            sourceState = sourceState.strip()
            symbol = symbol.strip()
            destinationState = destinationState.strip()
            if sourceState in rules:                             
                if symbol in rules[sourceState]:
                    if destinationState != rules[sourceState][symbol]:
                        raise DuplicateRuleError("We have 2 rules with same source state and symbols and different outcomes (destination states)")
                        return False # DFA is not valid; it would not know which of the two rules to follow for the specific input state and symbol
                else: # symbol not in rules[sourceState], this rule was not yet defined but we have another rule with same source state (not a problem)
                    rules[sourceState][symbol] = destinationState
            else: # we don't have any rules with this source state yet, so we initialise the dictionary with this first rule
                rules[sourceState] = {symbol : destinationState}
                
                                                                  # a transition function 
                                                                  # δ  :  Q    ×   Σ    →   Q
                                                                  #     srcSt    symbol   destSt
        if currentSection == "Start":
            start = line
            continue
        if currentSection == "Accept":
            accept.append(line)
            continue

    inputDfaFile.close()
    
    DFA = states, sigma, rules, start, accept
    if not isDfaValid(DFA):
        return False 
    else:
        # returning 5-tuple of lists
        return DFA


def isDfaValid(DFA):

    states, sigma, rules, start, accept = DFA # getting values from 5-tuple
    if len(sigma) == 0:
        raise UndefinedAlphabetError("Alphabet is not defined")
        return False
    
    if start == "None":
        raise UndefinedStartStateError("Start state is not defined")
        return False 
    
    elif start not in states:
        raise InvalidStateError(f"Start state {start} is not defined")
        return False
    
    if accept == []:
        raise UndefinedAcceptStatesError("Accept state is not defined")
        return False 
    
    else:
        for acceptState in accept:
            if acceptState not in states:
                raise InvalidStateError(f"Accept state {acceptState} is not defined")
                return False
            
            
    for sourceState in rules: # rules dict key is the source state of the rule
    
        if sourceState not in states:
            raise InvalidStateError(f"Source state {sourceState} is not defined in the states list for the DFA")
            return False
        
        for symbol in rules[sourceState]:
            if symbol not in sigma:
                raise InvalidSymbolError(f"Symbol {symbol} is not defined in the alphabet for the DFA")
                return False
            
            # for destinationState in rules[sourceState][symbol]: not for, as there is only one destinationState, this for would split the destinationState
            # string character by character
            destinationState = rules[sourceState][symbol]
            if destinationState not in states:
                raise InvalidStateError(f"Destination state {destinationState} is not defined in the states list for the DFA")
                # print(sourceState, symbol, destinationState)
                return False
                # traverses all rules in the dictionary, looking for source states, destination states and symbols
    return True
             
def printDfaDataStructures(DFA):
    states, sigma, rules, start, accept = DFA # getting values from 5-tuple

    print(f"States : {states}")
    print(f"Alphabet : {sigma}")
    print(f"Rules : {rules}")
    print(f"Start state : {start}")

    if len(accept) != 1:
        print(f"Accept states : {accept}") 
    else:
        print(f"Accept state: {accept[0]}") # to show singular form if needed and not a list with only one element


def isStringValid(string, stringSeparator, sigma):
    # searches if any element in the string is not included in the alphabet
    for symbol in splitIncludingNoSeparator(string, stringSeparator):
        if symbol not in sigma:
            return False
    return True
'''
def searchRuleAndReturnState(currentState, currentSymbol, rules):
    # removes redudant code (would be used twice, depending if separator is "" or not)
    if currentState in rules:
        if currentSymbol in rules[currentState]:
            currentState = rules[currentState][currentSymbol] # destination state of the existing rule
            return currentState
        else:
            return currentState # considered by default for every state, 
                                # if not specified a rule for the current symbol
                                # 
    else:
        return currentState
    
    # if there isn't any rule with the source state we have, or with the source state and the symbol we got from the sequence
    raise UndefinedRuleError(f"Rule {currentState}, {currentSymbol}, destination state not existent")
'''
def getNextState(currentState, currentSymbol, rules):
    if currentState not in rules:
        return currentState # considered by default for every state, if a rule is not specified, the DFA stays in the same state
                            # here we have no rule with the source state = the current state of the DFA
    elif currentSymbol not in rules[currentState]:
        return currentState # same case, but in the DFA we have a rule defined with the current state as the source state
                            # but no rule with the corresponding symbol, so we stay in the same state (by convention)
    else:
        return rules[currentState][currentSymbol] # the DFA goes to the state specified by the rule
    
def splitIncludingNoSeparator(string, separator):
    if separator == "" : # if not for this function, ValueError: empty separator
        return string  # would need an if-else statement within the runDfa function
    else:                # removes redudant code, by calling getNextState only once
        return string.split(separator)
            
def runDfa(DFA, inputString, stringSeparator, printDFASteps = True):

    states, sigma, rules, start, accept = DFA # getting values from 5-tuple

    # could check if the DFA is valid before running it, but the runDfa function should return an error
    # string instead of just False, because False might be misinterpreted as last state of the DFA is not
    # an accept state
    # but DFA validity is also looked upon when processing the file
    # if the functions are arranged in different files/modules, code like this is preferrable
    if not isDfaValid(DFA):
        raise DFAError("DFA not valid")
    
    inputString = inputString.strip() # removes whitespace, \n, from left and right
    if not isStringValid(inputString, stringSeparator, sigma):
        raise InputStringError("Input string contains symbols not in the given alphabet of the DFA. Possible problem: wrong string separator used when running the file.")
    
    
    currentState = start # first state is the start state of the DFA
    if printDFASteps == True: 
        # printDFASteps - boolean parameter - if it is true all the states and symbols the DFA encounters
        # will be printed to the screen - if not, only if the input string is valid will be printed to the screen
        print(currentState) # printing starting state
    
    for currentSymbol in splitIncludingNoSeparator(inputString, stringSeparator):
            if printDFASteps == True:
                print(currentSymbol) # printing every symbol in the string
            
            currentState = getNextState(currentState, currentSymbol, rules) 
            # function searches through the rules and finds the correct one 
            # improved time efficiency wise by using two hashmaps - dictionaries, for O(1) search time
 
            if printDFASteps == True:
                print(currentState)  # printing the new state of the DFA after every symbol
        
    if currentState in accept: # after the for loop exits the currentState variable stores the last state 
        return True            # of the DFA, if it is valid return true
    else:
        return False
    
        
        
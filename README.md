# deterministic-finite-automata
DFA stands for deterministic finite automaton M and is a 5-tuple, (Q, Σ, δ, q0, F), consisting of
- a finite set of states Q
- a finite set of input symbols called the alphabet Σ
- a transition function δ : Q × Σ → Q
- an initial (or start) state q0∈Q
- a set of accepting (or final) states F⊆Q

# Table of Contents
- [Definition Format](#clearly-defined-sections)
- [Example Definition](#example-definition-file)
- [Error Handling](#error-handling)
- [DFA Emulator](#dfa-emulator)
- [Folder Structure](#folder-structure)
- [Usage: DFA Emulator](#usage-dfa-emulator)
- [Random Input Generator](#random-input-string-generator)
- [Folder Structure: Generated Files](#folder-structure-generated-files)
- [Usage: Input Generator](#usage-input-generator)
- [Bonus: DFA-Based Game - "Escape the Room"](#bonus-dfa-based-game---escape-the-room)
- [How to Play (Run) the DFA Game](#-how-to-play-the-game-using-emulatedfapy)


# Clearly Defined Sections

- `[States]` lists all states, ensuring each state is explicitly declared.
- `[Sigma]` defines the input alphabet, making it clear what symbols are valid.
- `[Rules]` lists all transitions in a consistent format (currentState, inputSymbol, nextState).
- `[Start]` clearly identifies the initial state.
- `[Accept]` specifies accepting states.

   + Minimal but Sufficient Detail
   + It provides only necessary information, avoiding unnecessary syntax or clutter.
   + Easy to read and manually debug.
   + Consistent Structure
   + The format ensures predictability - each section starts with a header, and values are listed line-by-line.
   "End" markers make it clear where each section stops, which can prevent parsing errors.

- Comments are also allowed. One liner comments should start with a "#" character. (everything on the same line after the "#" is only for readability purposes and will not be interpreted by the parser. Comments that consist of multiple lines will start with `/*` and end with `*/`.
    + Improves readability by documenting states and transitions.
    + Makes debugging easier by explaining tricky parts.
    + Keeps the DFA understandable when revisiting later.

# Example definition file:


 DFA that checks if input string ends in a 1 - `machine.txt` file
```
# DFA that checks if input string ends in a 1
[States] 
q0 # Initial state
q1 # Accept state
End
[Sigma]
0
1
End
[Rules]
/* transition function 
starts here */
q0, 1, q1 
q0, 0, q0
q1, 1, q1
q1, 0, q0
End
[Start]
q0
End
[Accept]
q1 
End
```

# Error handling
- Added error classes and subclasses to give Python-like exceptions instead of returning "Error: ..." strings.
- Error Examples:
```
UndefinedAlphabetError: Alphabet is not defined
UndefinedRuleError: Rule q0, 0, destination state not existent
InvalidStateError: Accept state q1 is not defined
UndefinedStartStateError: Start state is not defined
InvalidStateError: Destination state q2 is not defined in the states list for the DFA
DuplicateRuleError: We have 2 rules with same source state and symbols and different outcomes (destination states)
InvalidSymbolError: Symbol 2 is not defined in the alphabet for the DFA

```
# DFA Emulator
It consists of the *emulateDFA.py* file - and it can be used in the Command Line Interface and in IDE's.
This Python script emulates a Deterministic Finite Automaton (DFA) by reading a `.dfa` file (written in the format specified above, the file extension can also be `.txt` or anything else, but the format needs to be correct - as the parser will give out errors) and an input string file, then running the DFA on the input.
## Features
- Runs a DFA simulation from a definition file.
- Reads input strings from a separate file.
- Optional verbose output of all intermediate steps.
- Outputs if the input string is accepted or rejected.
## Folder Structure
```
project/
│
├── DFA.py
├── emulateDFA.py
├── DFA Definition Files/
│ └── your_automaton.dfa
├── Input Files/
  └── your_input.txt
```
- can be easily changeable, but it seems more organised to me to have all definition files in their respective subdirectory - and the same for input files
- the script in its current state uses the python OS module and chdir function to dynamically move back and forth through directories - so it can avoid hardcoded file paths - and also be cross-platform friendly, as file paths may be different between operating systems
- On Linux/macOS, paths look like:
```
DFA Definition Files/your_automaton.dfa
```
- On Windows, paths look like:
```
DFA Definition Files\your_automaton.dfa
```
I also check if the directory exists and give out exceptions if not.
- May be changed later, because changing directories like this is not always recommended - can lead to unexpected behaviours in multithreaded or larger programs
- Though, I think this folder structure is pretty organised and can do its job really well, while still maintaining cross-platform advantages.
## Requirements
With this folder structure, you need to have the DFA module as well as the emulateDFA function in the same folder, and the DFA definition files and input files in their respective subfolders. You also need to change directory to the project/ folder (or any other name) - the folder that contains all the other subfolders, before running the script.
## Usage: DFA Emulator
After making the folder structure and placing each file in the correct subfolder, you can run the script:
### Option 1: Run interactively
```
python3 emulateDFA.py
```
OR press the run button on an IDE:)

You will be prompted to:

Enter the DFA definition file name (from `DFA Definition Files/`)

Enter the input string file name (from `Input Files/`)

Choose verbosity (1 = show steps, 0 = just Accepted/Rejected)

Specify input symbol separator:

`SPACE` → separator is a space (' ')

`NOSEPARATOR` → no separator (e.g., abba)

Any other string (e.g., ';') will be used as-is

### Option 2: Run via CLI
```
python3 emulateDFA.py <dfa_filename> <input_filename> [verbosity] [separator]
```
`<dfa_filename>`: file in DFA Definition Files/

`<input_filename>`: file in Input Files/

`[verbosity]`: Optional. Use 1 to print intermediate steps, 0 to print only the final result. The default value is no verbosity.

`[separator]`: Optional (default ''); use:

`SPACE` for ' '

`NOSEPARATOR` for no separator

or any custom delimiter like ';'

> ⚠️ If your separator is a shell-special character like ;, &, |, etc., wrap it in single quotes (';') to prevent shell misinterpretation.
```
python3 emulateDFA.py example.dfa test_input.txt 1 NoSeparator
python3 emulateDFA.py example.dfa test_input.txt 1 ';' 
```

## Custom exceptions 
Custom exceptions are raised for:

- Missing DFA/input files

- Not enough CLI arguments

- Invalid working directories

# Random input string generator
- When seeing a DFA and trying to find what it actually does, a really good practice is giving some input examples and running them, while watching every state change the DFA makes carefully. That's what the  `dfa_input_string_generator.py`  file does.
- It generates an interval from which it takes some random integers that determine the input string lengths. Then it generates a number of input strings with different lengths out of the list and generates random symbols from the alphabet.
- It runs the DFA for each input string (of course it still gives out exceptions if the DFA is not valid) and it filters the valid inputs and puts them in the `valid_inputs.txt` file and the invalid ones in the `invalid_inputs.txt` file.
- Seeing a lot of valid and invalid input string for any DFA can help in finding patterns and determining what the DFA may do.
- After seeing the patterns, it is still recommended to look on the actual transition function of the DFA (it's rules) to validate if that is actually what the DFA does, or it may have been a coincidence. If you are not sure, trying to find counterexamples is the best option.
- The script generates random input strings, but if their lengths are small, there is a high chance of finding duplicates (and seeing the exact same input twice does not help, even if it is valid or it is not valid) - an idea to solve this problem would be using a hashset to memorise the input strings before traversing it and seeing which inputs are valid and which are not. This would use more memory (for the hash set) and take more time to run (as whenever it finds a duplicate string it would need to generate another string, and also every single string would need to be checked not to be in the hashset (or just be added to the hashset, same thing)). A problem that would possibly arise is that if the MIN_LENGTH to MAX_LENGTH interval is pretty small, and their values are also small (also the alphabet), we would try to **randomly** get every single possible input value for it (even brute force would be a better approach). - Possible solution: having bigger MIN_LENGTH and MAX_LENGTH values (even though bigger inputs are harder to read -> harder to find patterns within them).
- Added hashmap to input generator - new results: for a simple DFA that accepts all strings that end with 0 (and with an alphabet of 1 and 0), with string lengths between 5 and 20:
   + 1000 strings were generated
   + 419 strings were valid
   + 456 strings were invalid
   + 125 strings were duplicates
- Same DFA, with string lengths between 10 and 20
   + 1000 strings were generated
   + 505 strings were valid
   + 487 strings were invalid
   + 8 strings were duplicates
- Same DFA, with string lengths between 10 and 40
   + 1000 strings were generated
   + 500 strings were valid
   + 499 strings were invalid
   + 1 string was a duplicate
- So, the larger the MIN_LENGTH and MAX_LENGTH values, the fewer duplicates we get, and less need for a hash set (look up time is O(1)) so still pretty efficient for only 1000 input strings to generate
## Folder Structure: Generated Files
Folder: Generated Files

All generated outputs are automatically saved in the `Generated Files` subdirectory. This includes:

- `valid_inputs.txt`: All input strings accepted by the DFA.

- `invalid_inputs.txt`: All input strings rejected by the DFA.

This folder keeps results organized and separate from source files, making it easier to review input coverage and patterns.

```
project/
│
├── DFA.py
├── emulateDFA.py
├── dfa_input_string_generator.py
├── DFA Definition Files/
│ └── your_automaton.dfa
├── Input Files/ # not needed for the input string generator
  └── your_input.txt
├── Generated Files/
  └── invalid_inputs.txt
  └── valid_inputs.txt
```
## Usage: Input Generator
### Option 1: Run interactively
```
python3 dfa_input_string_generator.py
```
or run it on an IDE:) 
You will be prompted for:

- **DFA Definition file name** (from `DFA Definition Files/`)

**Example:**
```
Give DFA Definition file name: evenLength.txt
```
### Option 2: Can be run from the CLI.
```
python3 dfa_input_string_generator.py <dfa_filename>
```
`<dfa_filename>`: Name of the DFA file located in the `DFA Definition Files/` folder (ex: `evenLength.txt`).

# Bonus: DFA-Based Game - "Escape the Room"

This DFA simulates a simple *adventure puzzle* game. The player navigates a house, must **pick up a spoon**, and reach the **Exit**. But you can only exit if you’re holding the spoon!

It shows how DFAs can model **state + inventory mechanics** - but also reveals a limitation of DFAs: to track whether the spoon was picked up, we had to **duplicate the entire state set** into "With Spoon" and "No Spoon" versions (they don't have any "memory").


### 🧩 Inventory Mechanic via State Doubling

To simulate an inventory (spoon possession), we **doubled every state**:

- `Kitchen No Spoon` → `Kitchen With Spoon`  
- `Library No Spoon` → `Library With Spoon`  
- and so on...

Each transition had to be duplicated to preserve correct movement with or without the spoon.

This allows the DFA to "remember" whether the player has the spoon by encoding it into the state name.

### This Seems Tedious...

Having to manually double the number of states for every inventory item or memory condition becomes **inefficient and hard to maintain**.

This limitation brings up an important question:

> ❓ What if we had a “memory” component to track this kind of info?

A Pushdown Automaton (PDA) would solve this more elegantly - with a *stack memory* that stores whether you've picked up the spoon or not.

A PDA extends DFAs by adding a **stack** - a type of memory you can read and write to, and you can do different transitions depending on it.

With a PDA:

- You could `PUSH SPOON` onto the stack when picking it up
- Later, `CHECK` if "SPOON" is on the top of the stack before allowing transition to the Exit

This makes the game logic **cleaner and more powerful**, without needing to duplicate all states.
You can check this game implementation in my PDA repository - link here later :)

## 🕹️ Game Map
```
            Secret Room
                |
                |
 Kitchen-----Hallway-----Library
  Spoon         |           |
                |           |
            Entrance       Exit SPOON NEEDED
```

### ✅ Objective:
- Start at **Entrance No Spoon**
- Use `UP`, `DOWN`, `LEFT`, `RIGHT`, and `PICK` as input symbols
- Pick up the spoon from the **Kitchen**
- Reach the **Exit With Spoon** state to win

### 🏁 Example winning input:
```
UP LEFT PICK RIGHT RIGHT DOWN
```

This path:
1. Goes to Kitchen
2. Picks up the spoon
3. Goes to Library
4. Reaches Exit while having Spoon

### 🔧 DFA Definition:
The full DFA definition file for this game is available in: `DFA Definition Files/updatedgame.dfa`.

You can also play the game without the spoon mechanic - available in `DFA Definition Files/game.dfa`.

### 🎮 How to Play the Game Using `emulateDFA.py`

To try out the game, use the DFA emulator script and follow these steps:

#### ▶️ Run in the IDE

Run the emulator:
```
python3 emulateDFA.py
```
or press the run button :)

When prompted:

- **DFA Definition file name**:  
  Enter one of the following:
  - `game.dfa` - for the basic version (no spoon mechanic)
  - `updatedgame.dfa` - for the version with the spoon inventory mechanic

- **Input string file name**:  
  Enter the name of a `.txt` file from the `Input Files/` folder that contains your sequence of moves.

Example content of `my_input.txt`:
```
UP LEFT PICK RIGHT RIGHT DOWN
```

- **Verbosity**:  
  Enter `1` to see each step, or `0` to only see the result.

- **Input separator**:  
  Enter `SPACE` (without quotes) to treat moves as space-separated.

#### ⚙️ CLI Mode

You can also run the game directly from the command line:
```
python3 emulateDFA.py updatedgame.dfa my_input.txt 1 SPACE
```
(1 - for verbosity, 0 - just shows result)

Make sure:

- `updatedgame.dfa` or `game.dfa` is located in the `DFA Definition Files/` directory
- `my_input.txt` is located in the `Input Files/` directory
- The input file contains a valid sequence of moves


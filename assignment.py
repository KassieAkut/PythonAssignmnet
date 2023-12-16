import re
from itertools import combinations

# Function to load letter values from a file
def file_loading(file_path='trees.txt'):
    words_split = {}
    with open(file_path, 'r') as text_file:
        for line in text_file:
            line = line.strip()
            if ',' in line:
                letter, value = line.split(',')
                words_split[letter] = int(value)
    return words_split

# Function to calculate scores based on letter position
def scores(letter, position, words_split):
    first_score_positions = {'first': 0, 'last': 5}
    remaining_score_position = {'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
                     'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15,
                     'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35}

    if position == 'first':
        return first_score_positions[position]
    elif position == 'last':
        return 20 if letter == 'E' else 5
    else:
# If position is neither first nor last, calculate score based on position and letter 
        first_score_positions = 1 if position == 'second' else 2
        remaining_score_position = remaining_score_position.get(letter, 0)
        return first_score_positions + remaining_score_position

# Function to generate abbreviations 
def generate_abbreviations(line, words_split):
# Splitting the line into words
    words = re.findall(r'\b\w+\b', line.upper())
    abbreviations = set()

    for word in words:
        if len(word) >= 3:
# Extracting the first, second and third letters
            first_letter = word[0]
            second_and_third_letters = word[1:3]

# Creating the abbreviation and calculating the score
            abbreviation = f"{first_letter}{second_and_third_letters}"
            score = (
                scores(first_letter, 'first', words_split) +
                scores(second_and_third_letters[0], 'second', words_split) +
                scores(second_and_third_letters[1], 'third', words_split)
            )
            abbreviations.add((abbreviation, score))

    if len(words) > 1:
# If there are more than one word in a name, create abbreviations using combination function
        first_letter = words[0][0]
        remaining_letters = ''.join(word[1:] for word in words[1:])
        
        for combo in combinations(remaining_letters, 2):
            second_and_third_letters = ''.join(combo)
            abbreviation = f"{first_letter}{second_and_third_letters}"
            score = (
                scores(first_letter, 'first', words_split) +
                scores(second_and_third_letters[0], 'second', words_split) +
                scores(second_and_third_letters[1], 'third', words_split)
            )
            abbreviations.add((abbreviation, score))

    return abbreviations

# Function to generate score 
def generate_score(first_letter, remaining_letters, words_split):
    abbreviation = first_letter
    score = 0

    for i, letter in enumerate(remaining_letters, start=1):
# Determining the position of the letter in the abbreviation
        position = 'first' if i == 1 else 'last' if i == len(remaining_letters) else 'third'
        letter_score = scores(letter, position, words_split)
        score += letter_score
        abbreviation += letter

    return abbreviation, score

# Main function to execute the code
def main():
# Taking input file name and surname from the user
    input_file = input("Enter the input file name (with .txt extension): ")
    surname = input("Enter your surname: ")

# Loading letter values from the specified file
    words_split = file_loading()

# Reading lines from the input file
    with open(input_file, 'r') as names_file:
        lines = names_file.readlines()

# Generating the output file name based on surname and file name
    output_file_name = f"{surname}_{input_file.replace('.txt', '')}_abbrevs.txt"

# Writing to the output file
    with open(output_file_name, 'w') as output_file:
        for line in lines:
            name = line.strip()
            abbreviations = generate_abbreviations(name, words_split)
            if not abbreviations:
# Writing a newline if no abbreviations are generated
                output_file.write('\n')
                continue

# Sorting the abbreviations based on score and selecting the lowest one
            sorted_abbreviations = sorted(abbreviations, key=lambda x: x[1])  
            best_abbreviation, best_score = sorted_abbreviations[0]  
# Writing the result to the output file
            output_file.write(f"{name}\t{best_abbreviation}({best_score})\n")


if __name__ == "__main__":
    # Calling the main function
    main()

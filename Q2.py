"""
The dictionary was modified to insert a case that has
the same starting phonemas with the test case
""" 
pronunciation_dict = [
    ("ABACUS", ["AE","B","AH","K","AH","S"]),
    ("BOOK", ["B", "UH", "K"]),
    ("THEIR", ["DH", "EH", "R"]),
    ("THEIRTH", ["DH", "EH", "R", "DH"]),
    ("EIR", ["EH", "R"]),
    ("THERE", ["DH", "EH", "R"]),
    ("TOMATO", ["T", "AH", "M", "AA", "T", "OW"]),
    ("TOMATO", ["T", "AH", "M", "EY", "T", "OW"])
]

def find_word_combos_with_pronunciation(phonemes):
    # Preprocess the dictionary to map the phonemas to the list of words
    processed_dict = preprocess_phenom_dict()
    substrings = list(processed_dict.keys())
    target = ','.join(phonemes)
    """
    Finding all the phenomas combinations of the dict
    that create the given sequence of phonemas
    """
    pron_combos = find_combinations(substrings, target)
    result = []
    
    for combo in pron_combos:
        combo_words = [[]]
        for pron in combo:
            # Adding all the words of the phenoma to the current combination
            pron_words = processed_dict[pron]
            combo_words = [word_list + [word] for word_list in combo_words for word in pron_words]
        result.extend(combo_words)
    return result
    

def preprocess_phenom_dict():
    processed_dict = {}
    for word, pron in pronunciation_dict:
        processed_pron = ','.join(pron)
        if processed_pron in processed_dict.keys():
            processed_dict[processed_pron].append(word)
            continue
        processed_dict[processed_pron] = [word]
    
    return processed_dict

def find_combinations(substrings, target):
    def backtrack(start, current_combination):
        # If we've used substrings to exactly form the target
        if start == len(target):
            result.append(current_combination[:])
            return

        # Try each substring
        for substring in substrings:
            end = start + len(substring)
            # Check if the substring can match the part of target starting at `start`
            if target.startswith(substring, start):
                # Check if we are at the end of the string or a comma follows
                if end == len(target) or target[end] == ',':
                    # Choose the substring and move forward
                    current_combination.append(substring)
                    # Move past the comma, if present
                    if end < len(target) and target[end] == ',':
                        end += 1
                    backtrack(end, current_combination)
                    # Backtrack
                    current_combination.pop()

    result = []
    backtrack(0, [])
    return result

if __name__ == '__main__':
    phonemes =  ["DH", "EH", "R", "DH", "EH", "R"]
    combinations = find_word_combos_with_pronunciation(phonemes)
    print("All the combinations of the words that can produce",
          f"the sequence\n {phonemes} \n are \n {combinations}")

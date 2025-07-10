text = input("Enter text: ")

import re
def readability_score(text):
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', text)
    num_words = len(words)

    # Count sentences by looking for end punctuation
    sentences = re.split(r'[.!?]+', text)
    num_sentences = len([s for s in sentences if s.strip()])  # Filter out empty strings

    # Count syllables in each word
    def count_syllables(word):
        word = word.lower()
        syllable_count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            syllable_count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i-1] not in vowels:
                syllable_count += 1
        if word.endswith("e"):
            syllable_count -= 1
        if syllable_count == 0:
            syllable_count = 1
        return syllable_count

    num_syllables = sum(count_syllables(word) for word in words)

    # Calculate the Flesch Reading Ease score
    if num_sentences == 0 or num_words == 0:
        return "Insufficient data to calculate readability score."

    score = 206.835 - (1.015 * (num_words / num_sentences)) - (84.6 * (num_syllables / num_words))

    return f"Readability Score: {score:.2f}"
print(readability_score(text))
# Example usage
# text = "This is an example sentence. It has several words and some punctuation!"
# print(readability_score(text))
# Example usage
# text = "This is an example sentence. It has several words and some punctuation!"
# print(readability_score(text))
# Example usage
# text = "This is an example sentence. It has several words and some punctuation!"


# Prompt the user for some texts

text = input("Text: ")


def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count

def count_words(text):
    count = 0
    for word in text:
        if word.isspace() or word == ' ':
            count += 1
    return count + 1  # Add one for the last word

def count_sentences(text):
    count = 0
    for char in text:
        if char == '.' or char == '!' or char == '?':
            count += 1
    return count

sum = 0

letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)

L = letters / words * 100
S = sentences / words * 100
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")



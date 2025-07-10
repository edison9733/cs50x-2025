# Prompt the user for some texts

text = input("Text: ")

sum = 0

letters = count_letters(text)
words = count_words(text)
sentences = count_sentences(text)


def count_letters(text):
    count = 0
    for char in range(text):
        if char.isalpha():
            count += 1
    return count

print({letters})


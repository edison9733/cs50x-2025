# Prompt the user for some texts

text = input("Text: ")


def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1
    return count

sum = 0

letters = count_letters(text)



print({count_letters(text)}, letters)


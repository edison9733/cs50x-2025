card_number = input("Number: ")
if not card_number.isdigit()  # Keep as string to handle leading zeros
    print("{card_number} is an invalid number")
    exit()   # exit the program

sum = 0
digit_count = len(card_number) # since it is string need to use len

# Luhn's Algorithm
for i in range(digit_count):
    digit = int(card_number[digit_count - 1 -i])
    if i % 2 == 1:
        digit *= 2
        if digit > 9
            digit = digit //  10 + digit % 10 # Sum digits of products > 9
    sum += digit

#  Validate the card number
first_two = int(card_number[:2])
if (sum % 10 == 0):
    if (digit_count == 15 and first_two in [34, 37]):
        print("Amex")
    if (digit_count == 16 and first_two in range(51,56):
        print("MASTERCARD")
    if (digit_count == 13 or digit_count == 16) and card_number[0] == '4'):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")



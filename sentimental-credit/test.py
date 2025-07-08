card_number = input("Number: ")  # Keep as string to handle leading zeros
if not card_number.isdigit():
    print("INVALID")
    exit()

sum = 0
digit_count = len(card_number)

# Luhn's Algorithm
for i in range(digit_count):
    digit = int(card_number[digit_count - 1 - i])
    if i % 2 == 1:  # Every second digit from the end
        digit *= 2
        if digit > 9:
            digit = digit // 10 + digit % 10  # Sum digits of products > 9
    sum += digit

# Check card type and validity
first_two = int(card_number[:2])
if (sum % 10 == 0):
    if (digit_count == 15 and first_two in [34, 37]):
        print("AMEX")
    elif (digit_count == 16 and first_two in range(51, 56)):
        print("MASTERCARD")
    elif ((digit_count == 13 or digit_count == 16) and card_number[0] == '4'):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")

from cs50 import get_int

while True:
    card = get_int("Card: ")
    if card > 0:
        break

def luhn_checksum(card):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

# Convert card number to string for easy handling
card_str = str(card)
length = len(card_str)

# Check starting digits for type
first_digit = int(card_str[0])
first_two_digits = int(card_str[:2])

# Verify with Luhn Algorithm
if luhn_checksum(card) == 0:
    if first_digit == 4 and (length == 13 or length == 16):
        print("VISA")
    elif length == 15 and (first_two_digits == 34 or first_two_digits == 37):
        print("AMEX")
    elif length == 16 and (51 <= first_two_digits <= 55):
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")

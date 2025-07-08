height = int(input("Height: "))

if 0 < height < 9:
    for row in range(height):

        print(" " * (height - row - 1), end ="")

        print("#" * (row + 1), end = "")

        print("  " , end= "")

        print("#" * (row + 1))

else:
    print(f"{height} is not a valid input")


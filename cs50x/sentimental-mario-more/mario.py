from cs50 import get_int

# Ask for height; integer between 1 and 8 inclusive
while True:
    height = get_int("Height: ")
    if 1 <= height <= 8:
        break

# Print pyramid
for i in range(1, height + 1):
    print((height - i) * " ", end="")
    print(i * "#" + "  " + i * "#")

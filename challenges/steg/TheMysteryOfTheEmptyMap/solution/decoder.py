input_file = "message.txt"
output_file = "binary.txt"

with open(input_file, "r", newline="") as f:
    lines = f.readlines()

groups = []

for line in lines:
    line = line.rstrip("\r\n")
    
    binary = "".join(
        "0" if char == " " else "1"
        for char in line
    )

    groups.append(binary)

result = " ".join(groups)

with open(output_file, "w") as f:
    f.write(result)

print("Decoded binary:")
print(result)

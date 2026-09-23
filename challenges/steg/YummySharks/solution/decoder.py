from scapy.all import rdpcap, TCP, UDP

input_file = "pirates_vs_sharks.pcap"
output_file = "decoded.txt"

packets = rdpcap(input_file)

bits = []

for packet in packets:
    if packet.haslayer(TCP):
        bits.append("0")
    elif packet.haslayer(UDP):
        bits.append("1")

binary = "".join(bits)

with open(output_file, "w") as f:
    f.write(binary)

print("Binary:", binary)
print("Saved to:", output_file)

ChipList = open("/Users/michaelruggiero/Desktop/002/ChipNameList.txt")
MistakenChip = open("/Users/michaelruggiero/Desktop/002/MistakenChip.txt", "a")

for line in ChipList:
    try:
        if line[0] == "N":
            a = line.split("GH")[0]
            b = line.split("GH")[1]
            b = b.strip("\n")
            b = "GH" + b
            MistakenChip.write(a + "\n")
            MistakenChip.write(b + "\n")
        else:
            line = line.strip("\n")
            MistakenChip.write(line + "\n")
    except:
        pass

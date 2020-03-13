import os
Complete = open("/Users/michaelruggiero/Desktop/" + "Complete.txt", "r")
CompleteFileList = open("/Users/michaelruggiero/Desktop/" + "CompleteFileList.txt", "w")

for line in Complete:
    if line[0] == "*":
        line = line.strip("***"+".txt"+"\n")
        print(line)
        CompleteFileList.write(line + "\n")
        # os.makedirs("/Users/michaelruggiero/Desktop/Samples/" + line)

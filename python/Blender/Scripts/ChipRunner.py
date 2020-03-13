import os
Complete = open("/Users/michaelruggiero/Desktop/" + "Complete.txt", "w")

Simulation_list = os.listdir("/Users/michaelruggiero/Desktop/Samples")
print(Simulation_list)

for x in range(len(Simulation_list)):
    file = Simulation_list[x]
    Complete.write("***" + Simulation_list[x].strip("\n") + "\n")
    file = open("/Users/michaelruggiero/Desktop/Samples/" + file, "r")
    for line in file:
        line = line.replace("_", "")
        Complete.write(line.strip("\n") + "\n")

Complete.close()

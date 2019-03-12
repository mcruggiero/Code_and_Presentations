# This is a fun little script I wrote to memorize the major system and the Stephen
# Mitchell translation Tao. Please do not use this code without my consent.
#All rights reserved.

# 2019
# michael@mcruggiero.com



import pandas as pd
import numpy as np
import os
os.system('cls' if os.name == 'nt' else 'clear')

Tao = pd.read_csv("Tao3.csv")
Tao["SessionSeen"] = 0
Letter = "A. B. C. D. E. F. G. H. I. J. K. L.".split()

def Choice(a,b):
    while True:
        try:
            print("\n")
            choice = int(input("Please choose a number from " +str(a)+" to " +str(b)+ ": "))
            if int(a) <= choice <= int(b):
                print("\n")
                return choice
                break
            else: print("Stick to the numbers, Sam.")
        except: print("Stick to the numbers, Sam.")

def Settings(Size, QTypes, CutOff):
    a = 1
    while a == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nSetting Panel \n")
        print("\nWhat would you like?\n")
        print("\t1. Reset Scores\n")
        print("\t2. Current Multiple Choice List Size is " + str(Size) + "\n")
        print("\t3. Current Question Types is # " +str(QTypes + 1)+ "\n")
        print("\t4. Fill In The blank vs Multiple Choice is " + str(int(100 * CutOff)) +"%"+ " correct\n")
        print("\t5. View Tao with scores\n")
        print("\t6. Back to Main Menu\n")
        print("What would you like to change?")

        setchoice = Choice(1,6)

        if setchoice == 1:
            Re = str(input("Are you sure you want to reset your scores? \n Type 'yes' to reset "))
            if Re == "yes":
                ResetScore(Tao)
                input("Scores reset. Hit return to continue")
            else: input("OK. scores not reset. Hit return to continue")
        elif setchoice == 2:
            print("How many choices for the multiple choice lists? ")
            Size = Choice(1,12)
        elif setchoice == 3:
            print("\t1. 'TaoLine' \n")
            print("\t2. 'MemoryFileSmall' \n")
            print("\t3. 'MemoryFileSmall' & 'TaoLine' \n")
            print("\t4. 'TaoLine' & 'MemoryFileSmall' & 'LineNumber' \n")
            QTypes = Choice(1,4) - 1
        elif setchoice == 4:
            print("What is the percent threshold for fill in the blank vs. multiple choice? ")
            CutOff = (Choice(0,100)/100)
        elif setchoice == 5:
            pd.set_option('display.max_rows', len(Tao))
            A = Tao[["TaoLine", "MemoryFileSmall", "Points"]]
            print(A.set_index('TaoLine'))
            input("Hit return to continue")
        if setchoice == 6:
            a += 1

    return Size, QTypes, CutOff

def Main():
    Size = 6
    quit = 1
    QTypes = 2
    CutOff = .5
    while quit == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nWelcome to TaoLearner v.1 \n")
        print("\nWhat would you like?\n")
        print("\t1. Lookup Chapter\n")
        print("\t2. Learn unshuffled lines in an interval\n")
        print("\t3. Learn shuffled lines in an interval\n")
        print("\t4. Learn an entire chapter\n")
        print("\t5. Settngs\n")
        print("\t6. Quit\n")

        choice = Choice(1,6)

        if choice == 1:
            print("\nWhat Chapter? ")
            N = Choice(1,81)
            LookupChapter(Tao, N)
        elif choice ==2:
            print("\nWhat is the lowest line?")
            Lower = Choice(0,len(Tao)-1)
            print("\nWhat is the highest line?")
            Upper = Choice(0,len(Tao)-1)
            Sequence(Tao, Lower, Upper, CutOff, QTypes, Size)
        elif choice == 3:
            print("\nWhat is the lowest line?")
            Lower = Choice(0,len(Tao)-1)
            print("\nWhat is the highest line?")
            Upper = Choice(0,len(Tao)-1)
            Random(Tao, Lower, Upper, CutOff, QTypes, Size)
        elif choice == 4:
            print("\nWhat Chapter? ")
            N = Choice(1,81)
            ReviewChapter(Tao,N,CutOff, QTypes, Size)
        elif choice == 5:
            SettingSet = Settings(Size, QTypes, CutOff)
            Size, QTypes, CutOff = SettingSet[0], SettingSet[1], SettingSet[2]
        elif choice == 6:
            quit = 0

def ListBuilder(List,N,Size):
    while True: #This while is something of a compromise to handle repeating values
        if len(List) < Size: Size = len(List)
        if Size > 12: Size = 12
        answer_list = []
        while len(answer_list) < Size:
            A = np.random.randint(len(List))
            if A not in answer_list: answer_list.append(A)
        if ((N%100,N%3) not in [(x%100,x%3) for x in answer_list]) or (N not in answer_list): #Checks to see if answer in list
            real_choice = np.random.randint(0,Size)
            answer_list[real_choice] = N
        else: real_choice = answer_list.index(N)

        #Build list of choices
        complete_list = []
        for i in range(len(answer_list)):
            a = int(answer_list[i])
            complete_list.append(List.iat[a,2])

        if len(complete_list) == len(set(complete_list)):
            complete_list = []
            for i in range(len(answer_list)):
                a = int(answer_list[i])
                complete_list.append([Letter[i],
                                      List.iat[a,0],
                                      List.iat[a,2],
                                      List.iat[a,4]])
            return complete_list, complete_list[int(real_choice)][0]
            break

def Tester(List, N, Size, Show, Score, QType):

    Answer = ListBuilder(List, N, Size)
    complete_list, real_choice = Answer[0], Answer[1]

    Words = QType

    if QType != "LineNumber": A = str(List.iat[int(N),4])
    else: A = ""


    if QType == "MemoryFileSmall": QType = int(2)
    elif QType == "TaoLine": QType = int(0)
    elif QType == "LineNumber": QType = int(4)

    if Show == 1:
        print("\n")
        for i in range(len(complete_list)):
            print(complete_list[i][0],complete_list[i][1+int(QType/2)])

    Choice = input("\nType " + str(Words) + " # " + str(List.iat[int(N),9]) + " from Tao: " + A +  " (q to quit): ")

    if Choice == List.iat[N,QType]  or \
    ((Show == 1) and (Choice == real_choice[0])):
        Score += 2
        print("\nPoints! \nTotal Score: " + str(Score) + "\n")
        List.iat[N,6] += .5
    elif Choice == "q":
        quit()
    else:
        Score -= 3
        print("\nWrong! The answer was: " + str(List.iat[N,QType]) + " \nTotal Score: " + str(Score) + "\n")
        List.iat[N,6] -= .75

    return Score

def Mul_Choice(List, N, Size, Show, Score, QTypes):
    # N: real answer
    # Size: size of choice list, max 12 or len(List)
    # Show: printer

    #Test if line number is new
    if List.iat[N,5] == 0:
        print("\nMemorize line # " + str(N) +" from "+ str(List.iat[N,4]) +":\n"+ str(List.iat[N,0]) +",\nFile: "+ str(List.iat[N,2]) + "\n")
        List.iat[N,5] += 1
        input("Press return continue")
    else:
        List.iat[N,5] += .1*QTypes + .33
        List.iat[N,7] += 1
        if QTypes == 0: Score = Tester(List, N, Size, Show, Score, "TaoLine")
        elif QTypes == 1: Score = Tester(List, N, Size, Show, Score, "MemoryFileSmall")
        elif QTypes == 2:
            Score = Tester(List, N, Size, Show, Score, "MemoryFileSmall")
            Score = Tester(List, N, Size, Show, Score, "TaoLine")
        elif QTypes == 3:
            Score = Tester(List, N, Size, Show, Score, "TaoLine")
            Score = Tester(List, N, Size, Show, Score, "MemoryFileSmall")
            Score = Tester(List, N, Size, Show, Score, "LineNumber")

    if len(List) != len(Tao):
        List = List[List["TaoLine"] == List.iat[N,0]]
        Tao[Tao["TaoLine"] == List.iat[0,0]] = List

    return Score

#User Callable

def LookupChapter(List, N):
    #Prints out Chapters from Tao
    List = List[List["Chapter"] == N]
    print(List[["MemoryFileSmall", "TaoLine"]])
    input("\nPress return when done")

def ResetScore(List):
    List["TimesSeen"] = 0.0
    List["SessionSeen"] = 0.0
    List["Points"] = 0.0
    Tao.to_csv("Tao3.csv", index=False)

def Random(List, Lower, Upper, CutOff, QTypes, Size):
    #Limit: List stop value
    #CutOff: % View
    #Random: %Chance to see anyway
    Score, i, Pic = 0, 0, []

    while i < len(range(Lower,Upper + 1)):
        a = np.random.randint(Lower,Upper + 1)
        if a not in Pic:
            Pic.append(a)
            i += 1

    for N in Pic:
        if List.iat[N,6]/(List.iat[N,5] + 1) < CutOff:
            A = Score
            Score = Mul_Choice(List, N, Size, 1, Score, QTypes)
            if Score - A < 2: Pic.append(N)
        else:
            A = Score
            Score = Mul_Choice(List, N, Size, 0, Score, QTypes)
            if Score - A < 2: Pic.append(N)

    Tao.to_csv("Tao3.csv", index=False)
    pd.set_option('display.max_rows', len(Tao))
    A = Tao[Tao["SessionSeen"] > 0]
    print(A[["TaoLine","TimesSeen","Points"]])
    input("Press return")

    return Score

def Sequence(List, Lower, Upper, CutOff, QTypes, Size):
    #Limit: List stop value
    #CutOff: % View
    #Random: %Chance to see anyway
    Score, Pic = 0, list(range(Lower,Upper + 1))

    for N in Pic:
        if List.iat[N,6]/(List.iat[N,5] + 1) < CutOff:
            A = Score
            Score = Mul_Choice(List, N, Size, 1, Score, QTypes)
            if Score - A < 2: Pic.append(N)
        else:
            A = Score
            Score = Mul_Choice(List, N, Size, 0, Score, QTypes)
            if Score - A < 2: Pic.append(N)

    Tao.to_csv("Tao3.csv", index=False)
    pd.set_option('display.max_rows', len(Tao))
    A = Tao[Tao["SessionSeen"] > 0]
    print(A[["TaoLine","TimesSeen","Points"]])
    input("\nPress return when done")

    return Score

def ReviewChapter(List,N,CutOff, QTypes, Size):
    List = List[List["Chapter"] == N]
    return Sequence(List, 0, len(List) - 1, CutOff, QTypes, Size)

Main()

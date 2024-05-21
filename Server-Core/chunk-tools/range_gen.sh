#X1 = 870
#Y1 = 576
#X2 = 880
#Y2 = 586
#outputFile = "/home/apathabove/Zomboid/Lua/chunk_lists/bill.txt"

for i in range(X1, X2+1):
    for y in range (Y1, Y2+1):
        print(str(i)+"_"+str(y), file=open(outputFile, 'a'))

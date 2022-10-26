#!/usr/bin/env python3

#import treelib
#import sys
from treelib import Node, Tree
#Functions used to draw tree:

def writeTree(listOfAllPrev):
    tree = Tree()
    treeDict = {}
    #initialize root node:
    tree.create_node(listOfAllPrev[0][0], listOfAllPrev[0][0] + str(0))
    nodeDict = {}
    for prevList in listOfAllPrev:
        for i in range(1, len(prevList)):
            #print("node public name: " + prevList[i])
            #print(("node identifier: " + prevList[i] + str(i)))
            #print("parent: " + prevList[i-1] + str(i-1))
            if i >= 2:
                if prevList[i] + str(i) + prevList[i-1] not in nodeDict:
                    nodeDict[prevList[i] + str(i) + prevList[i-1]] = set()
                    if prevList[i-1] + str(i-1) + prevList[i-2] not in nodeDict[prevList[i] + str(i) + prevList[i-1]]:
                        #print("creating node")
                        tree.create_node(prevList[i], (prevList[i] + str(i) + prevList[i-1]), parent=(prevList[i-1] + str(i-1)) + prevList[i-2])
                        nodeDict[prevList[i] + str(i) + prevList[i-1]].add(prevList[i-1] + str(i-1) + prevList[i-2])

            else:
                if prevList[i] + str(i) + prevList[i-1] not in nodeDict:
                    nodeDict[prevList[i] + str(i) + prevList[i-1]] = set()
                    if prevList[i-1] + str(i-1) not in nodeDict[prevList[i] + str(i) + prevList[i-1]]:
                        #print("creating node")
                        tree.create_node(prevList[i], (prevList[i] + str(i) + prevList[i-1]), parent=(prevList[i-1] + str(i-1)))
                        #parent must be root node, only identified by root
                        nodeDict[prevList[i] + str(i) + prevList[i-1]].add(prevList[i-1] + str(i-1))



    tree.show()
    #if nid is None, root is used
    tree.remove_subtree(None)

# this file is for the trace NFA
#Team: Makenna Gall (team of 1)

import time
import sys
import csv


#main execution:
def main():
    filename = sys.argv[1]
    transDict = {}
    #open output file:
    name = filename.split(sep='.')[0]
    writeFile = open(name + "Output", 'w')
    with open(filename) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        lineNumber = 0
        startState = []
        for line in csvReader:
            if lineNumber == 0:
                title = line[0]
                writeFile.write("File: " + title + "\n")
            elif lineNumber == 3:
                #create a list of start state so it can be used as initial prevStates in traceNFA
                startState.append(line[0])
            elif lineNumber > 4:
                #rows that give transitions
                if (line[0] + "/" + str(line[1])) not in transDict:
                    #if key is not already in dictionary, initiallize an empty list
                    #print("initializing value with empty list for " + line[0] + str(line[1]))
                    transDict[line[0] + "/" + str(line[1])] = []
                #add the result to the result list
                transDict[line[0] + "/" + str(line[1])].append(line[2])
            lineNumber += 1
    #create a variable to store the string
    '''
    #test values created in main:
    print(theString)
    print("dictionary: ")
    print(type(transDict))
    for key in transDict.keys():
        print("--KEY--: " + key)
        print("value: ", end='')
        print(transDict[key])
    '''
    #Call traceNFA in main:
    #create loop that allows you to input multiple strings:
    for string in sys.argv[2:]:
        writeFile.write("Testing String: " + string + "\n")
        accPrevList = []
        traceNFA(transDict, startState, string, writeFile, accPrevList)
        writeFile.write("\n")
        #print(accPrevList)
        writeTree(accPrevList)

def traceNFA(transDict, prevStates, theString, writeFile, accPrevList):

    #print("type of prevStates: " + str(type(prevStates)))
    '''
    #Can be used to trace entire tree:
    print("Previous states ", end="")
    print(prevStates)
    print("remaining string: " + theString)
    '''
#inputs:
    #1: dictionary containing transitions:
        #key: start+changeChar #value: list of resulting states
    #2: list containing previous states passed through, originally contains start state
    #3: current string without the letters that have been accounted for
    #4: writeFile (does not change when recursive calls are made)
    if not theString:
        accPrevList.append(prevStates)
        if (prevStates[-1])[0] == '*':
            writeFile.write("ends in accepting state: ")
            writeFile.write(", ".join(prevStates))
            writeFile.write("\n")
        else:
            writeFile.write("does not end in accepting state: ")
            writeFile.write(", ".join(prevStates))
            writeFile.write("\n")

        return
    else:
        if (str(prevStates[-1]) + "/" + theString[0]) in transDict:
            for value in transDict[prevStates[-1] + "/" + theString[0]]:
                #create a copy of the list object prevList:
                newPrev = prevStates.copy()
                alphaPrev = newPrev
                alphaPrev.append(value)
                traceNFA(transDict, alphaPrev, theString[1:], writeFile, accPrevList)
            return
#account for epsilon:
        if(str(prevStates[-1]) + "/" + "~") in transDict:
            key = (str(prevStates[-1]) + "/" + "~")
            for value in transDict[key]:
                #create a copy of the list object prevList:
                newPrev = prevStates.copy()
                epsilonPrev = newPrev
                epsilonPrev.append(value)
                traceNFA(transDict, epsilonPrev, theString, writeFile, accPrevList)
            return
        else:
            #stuck:
            accPrevList.append(prevStates)
            return
    return


#run main:
if __name__ == "__main__":
    main()

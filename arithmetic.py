# lossless data compression
import collections
import math
import sys

class Node:
    def __init__(self,val,left=None,right=None):
        self.left = left
        self.right = right
        self.val = val

# Message represented by an interval of real numbers between 0 and 1
# Bigger message, interval to represent becomes smaller
# Continuously magnifying fraction of values from range(0,1)
# Take range of nothing (0,1), then magnify to range of character a=(0,0.2) -> 1/5 of original nothing space
# Take character a=[0,0.2], then magnify to range of next character i=[0.5,0.6] -> 1/10 of original nothin
# New range = [0.2/(1/0.5),0.2/(1/0.6)] = [.1,.12]
# formula = [current_range/(original_range/original_char_lower),current_range/(original_range/original_char_upper)]
class Arithmetic:
    def __init__(self, eD, inputString):
        self.sumP = sum(eD)
        self.inputString = inputString
        self.pMap= {}
        inputCount = collections.Counter(inputString)
        count = 0
        for x,y in inputCount.items():
            probabilityRange = (count,count+(y/len(inputString)))
            self.pMap[x] = probabilityRange
            count += y/len(inputString)

    def aencode(self ):
        encoded = []
        currPMap = dict(self.pMap)
        lower,upper = (0,1)
        currSum = upper-lower
        def magnify(currSum, currPMap, lower, upper, inputString):
            if not inputString:
                return

            char = inputString[0]
            lower,upper = tuple(currPMap[char])
            print(self.pMap)
            print("Current Char: {}\nCurr Range: {}".format(char,(lower,upper)))
            prevUpper = lower
            for c in currPMap:
                currPMap[c] = (prevUpper,prevUpper+((upper-lower)/(1/(self.pMap[c][1]-self.pMap[c][0]))))
                print(c,currPMap[c])
                prevUpper = prevUpper+((upper-lower)/(1/(self.pMap[c][1]-self.pMap[c][0])))

            print(prevUpper,upper)
            print()
            magnify(upper-lower, currPMap, lower, upper, inputString[1:])

            return

        return magnify(currSum, currPMap, lower, upper, inputString)

inputString = 'abbbaacdcaaa'
frequency = collections.Counter(inputString)
eD = [x/len(inputString) for x in frequency.values()] # distribution of probabilities
eS = [-math.log2(y) for y in eD]
eH = sum([eD[z]*eS[z] for z in range(len(eD))])
#print(frequency, eD, eS, eH)

arithmetic = Arithmetic(eD, inputString)
arithmetic.aencode()

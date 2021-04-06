# lossless data compression
import collections
import heapq
import math
import sys

class Node:
    def __init__(self,val,left=None,right=None):
        self.left = left
        self.right = right
        self.val = val

# most freq = smalles codes, least freq = longer codes
# greedy approach - merge 2 subtrees with least weight at each iteration
#                   new subtree into the priority queue 
class Huffman:
    def __init__(self,inputString):
        self.inputString = inputString
        self.lookup = collections.Counter(inputString).most_common()
        self.pq = collections.deque([])
        for node,nodeCount in self.lookup:
            print(node,nodeCount)
            self.pq.append((nodeCount,Node(node)))

    def build(self):
        # creating tree from bottom up
        while len(self.pq) > 1:
            # get 2 lowest weights, then join these two 2 trees
            least = self.pq.pop()
            secondLeast = self.pq.pop()
            currRootVal = least[0] + secondLeast[0]
            currRoot = Node(currRootVal)
            currRoot.left, currRoot.right = least[1], secondLeast[1]
            self.pq.append((currRootVal,currRoot))
            #print(currRoot.val,currRoot.left.val,currRoot.right.val)

        return self.pq[0] if len(self.pq) == 1 else collections.deque([])

    def printTreeArray(self):
        if len(self.pq) < 1:
            print("")
            return

        treeArr = []
        q = collections.deque([self.pq[0][1]])
        count = 0
        while q:
            layer = list(q)
            q = collections.deque([])
            for parent in layer:
                if parent is None:
                    treeArr.append(parent)
                    continue

                treeArr.append(parent.val)
                q.append(parent.left)
                q.append(parent.right)

        print(treeArr)

    def huffEncode(self):
        # Assuming we have huffman tree
        if len(self.pq) != 1:
            print("Must Build Huffman Tree Before Encoding")
            return None

        encodedString = []
        def traverseHuffman(char, node=self.pq[0][1],encode=""):
            if not node:
                return False

            if str(node.val) == char:
                encodedString.append(encode)
                return True

            if traverseHuffman(char, node.left, encode+"0"):
                return True
            if traverseHuffman(char, node.right, encode+"1"):
                return True

            return False

        for char in self.inputString:
            traverseHuffman(char)
            print(char, str(encodedString))

        return ''.join(encodedString)

    
    def huffDecode(self,encodedString):
        pass

inputString = sys.argv[1] if len(sys.arv[1]) > 1 else ""

huffman = Huffman(inputString)
huffman.build()
#huffman.printTreeArray()
print()
print()
print()
print("Encoded String: {}".format(huffman.huffEncode()))
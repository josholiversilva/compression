# lossless data compression
import collections
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
        nodeCount = len(self.lookup)
        treeRuns = math.log2(nodeCount)
        done = collections.deque([2,1])
        f = collections.deque([1,3])
        print('Number of chars: {}'.format(nodeCount))
        # After forming subtrees, continue until we have 1 root node of all subtrees
        # O(t)*(O(logq)+O(q)) = O(t*qlogq)
        for treeRun in range(math.ceil(treeRuns)):
            done = collections.deque([])
            print('----------------- {} ----------------'.format(treeRun))
            print(self.pq)
            # Form subtrees of nodes
            while len(self.pq) > 1:
                # get 2 lowest weights, then join these two 2 trees
                least = self.pq.pop()
                secondLeast = self.pq.pop()
                currRootVal = least[0] + secondLeast[0]
                currRoot = Node(currRootVal)
                currRoot.left, currRoot.right = least[1], secondLeast[1]
                #self.pq.append((currRootVal,currRoot))
                done.appendleft((currRootVal,currRoot))
                print(currRoot.val,currRoot.left.val,currRoot.right.val)
            self.pq += done

            # Missed a value (when odd nodes), must put in correct spot for next queue subtree execution
            x = 0
            if len(self.pq) > x+1:
                while self.pq[x][0] < self.pq[x+1][0]:
                    self.pq[x], self.pq[x+1] = self.pq[x+1], self.pq[x]
                    x += 1
                    if len(self.pq) == x+1:
                        break

        print()
        print("End Node: {}".format(self.pq[0]))
        return self.pq[0] 

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
            print(char, str(encodedString[-1]))
        return ''.join(encodedString)

    def huffDecode(self,encodedString):
        if len(self.pq) != 1:
            print("Must Build Huffman Tree Before Encoding")
            return None

        decodedString = []
        def traverseHuffman(encodedString,node=self.pq[0][1]):
            if not node.left and not node.right:
                decodedString.append(node.val)
                return 0

            if encodedString[0] == "0":
                return traverseHuffman(encodedString[1:],node.left)+1
            else:
                return traverseHuffman(encodedString[1:],node.right)+1

        # required inputs: encodedString, self.lookup, self.pq
        while encodedString:
            depth = traverseHuffman(encodedString,self.pq[0][1])
            encodedString = encodedString[depth:]
            print(encodedString, decodedString)

        return ''.join(decodedString)

encode = sys.argv[1] if len(sys.argv) > 1 else ""
inputString = sys.argv[2] if len(sys.argv) > 2 else ""
decode = sys.argv[3] if len(sys.argv) > 3 else ""

if encode and inputString:
    huffman = Huffman(inputString)
    print()
    print()
    huffman.build()
    print()
    print()
    encoded = huffman.huffEncode()
    print("Encoded String: {}".format(encoded))
    print()
    print()
    if decode:
        decoded = huffman.huffDecode(encoded)
        print("Decoded String: {}".format(decoded))
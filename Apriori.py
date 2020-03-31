

    #Apriori Algorithm Implementation using Python

''' How to Run this code snippet in your termianl;
    >python Apriori.py -f TRANSACTION-DATASET.csv -s minSupport  -c minConfidence
    >python Apriori.py -f TRANSACTION-DATASET.csv -s 0.15 -c 0.6 '''
    


import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

#Used to return the non empty subsets of array
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

 #Used to calculate the support for items in the itemSet and returns the subset
def returnItemsWithMinSupport(itemSet, txnList, minSupport, freqSet):

        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in txnList:
                      if item.issubset(transaction):
                              freqSet[item] += 1
                              localSet[item] += 1

        
        for item, count in localSet.items():
                support = float(count)/len(txnList)
                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSettxnList(data_iterator):
    txnList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        txnList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, txnList

# Method for Apriori Algorithm
def runApriori(data_iter, minSupport, minConfidence):

    itemSet, txnList = getItemSettxnList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,txnList,minSupport,freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,txnList,minSupport,freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
           return float(freqSet[item])/len(txnList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    #print 'confidence: ' + repr(confidence)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
                        #print 'confidence: ' + repr(confidence)


    return toRetItems, toRetRules

#prints the itemsets sorted by support and Lift
def printResults(items, rules):

    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
    print "\n----List of Lift items which is greater than 1----"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        #print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)
        lift = confidence/support
        if lift > 1.09999:
            print "Lift: %s ==> %s , %.3f" % (str(pre), str(post), lift)


def dataFromFile(fname):
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')
                record = frozenset(line.split(','))
                yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = dataFromFile(options.input)
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)


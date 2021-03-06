from random import randint
from core.util.data import StockHistory, Featurizer
from core.rl.portfolio import evalLinUCB

def policyGradient(T=5, maxStaticRewards=10, maxShift=5, maxIterations=1000, alpha=0.1, dataSet='nasdaq100') :
    done = False
    stockHistory = StockHistory(dataSet)
    currentArgs = [5, 5, 5, 0, 1.5, -1.5]
    argEpsilons = [1, 1, 1, 0.01, 0.1, 0.1]
    CAGRs = evalLinUCB(stockHistory, Featurizer(stockHistory, *currentArgs), alpha=alpha)
    currentMax = sum(CAGRs) / len(CAGRs)
    print
    print 'Initial CAGRs:', CAGRs
    print 'Initial max:  ', currentMax
    f = open('maxArg.txt', 'a')
    f.write('Begin again! Excited!!!\n')
    f.close()
    numStaticRewards = 0
    iteration = 0
    while numStaticRewards < maxStaticRewards and iteration < maxIterations :
        iteration += 1
        randomPerturbations = [[randint(-maxShift, maxShift)*epsilon+arg for (arg,epsilon) in zip(currentArgs, argEpsilons)] for t in range(T)]
        for perturbation in randomPerturbations :
            print 'Trying args:', perturbation
        #changes = [[-1 if arg1 < arg2 else 1 if arg1 > arg2 else 0 for (arg1, arg2) in zip(randomArgs, currentArgs)] for randomArgs in randomPerturbations]
        featurizers = [Featurizer(stockHistory, *args) for args in randomPerturbations]
        results = [evalLinUCB(stockHistory, featurizer, alpha=alpha) for featurizer in featurizers]

        """
        less = [[] for i in range(T)]
        zero = [[] for i in range(T)]
        more = [[] for i in range(T)]
        for i in range(T) :
            for change in changes[i] :
                if change == -1 :
                    less[i].append(results[i])
                elif change == 0 :
                    zero[i].append(results[i])
                else :
                    more[i].append(results[i])

        avgLess = [sum(l)/float(len(l)) for l in less]
        avgZero = [sum(z)/float(len(z)) for z in zero]
        avgMore = [sum(m)/float(len(m)) for m in more]

        for i in range(T) :
            l = less[i]
            z = zero[i]
            m = more[i]
            greatestReward = max(l, z, m)
            if greatestReward == l :
                currentArgs[i] -= argEpsilons[i]
            elif greatestReward == m :
                currentArgs[i] += argEpsilons[i]
        """
        numStaticRewards += 1
        for (args, cagrs) in zip(randomPerturbations, results) :
            print 'Args:  ', args
            print 'CAGRs: ', cagrs
            result = sum(cagrs) / len(cagrs)
            if result > currentMax :
                currentMax = result
                currentArgs = args
                numStaticRewards = 0

        resultString = 'Iteration: ' + str(iteration) + ', Static Rewards: ' + str(numStaticRewards) + ', Current Max: ' + str(currentMax) + ', Args: ' + str(currentArgs)
        print
        print resultString
        f = open('maxArg_' + str(alpha) + '.txt', 'a')
        f.write(resultString + '\n')
        f.close()

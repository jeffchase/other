# Tennis - Aggregate Scoring
# State : (x,y)
# (x,y) = game score

# NextState() ignores the win-by-two requirements. GetPointOdds() instead takes
# it into account

from random import random

prob = dict()
ex = dict()
p1 = 0.6
p2 = 0.6

# Length of game (first to N wins, win by two)
N = 88

def IsDeuce(state):
    return (state == (N-1,N-1))

def GameWon(state):
    return state[0] >= N

def GameLost(state):
    return state[1] >= N

def NextState(state, PointWon, PnotE):
    if GameWon(state) or GameLost(state):
        return state
    
    g = list(state)
    if not PnotE and IsDeuce(state):
        if PointWon:
            g[1] -= 1
        else:
            g[0] -= 1
    else:
        if PointWon:
            g[0] += 1
        else:
            g[1] += 1
    return tuple(g)

def TestNextState(p=0.6):
    s = (0,0)
    print s
    while not GameWon(s) and not GameLost(s):
        w = random() < p
        s = NextState(s, w, True)
        print s, w

def GetServe(state):
    return ((state[0] + state[1] + 1)/2) % 2

def GetPointOdds(state):
    global p1, p2

    if IsDeuce(state):
        return (p1*(1-p2))/(1-p1*p2-(1-p1)*(1-p2))

    serve = GetServe(state)
    return p1 if (serve == 0) else (1-p2)

def TraverseP(s):
    global prob
    if GameWon(s):
        prob[s] = 1.0
        return 1.0
    if GameLost(s):
        prob[s] = 0.0
        return 0.0
    if s in prob:
        return prob[s]
    p = GetPointOdds(s)
    t = p*TraverseP(NextState(s, True, True)) + (1-p)*TraverseP(NextState(s, False, True))
    prob[s] = t
    return t

def Compute(p=0.6, q=0.6):
    global p1, p2, prob, ex
    s = (0,0)
    p1 = p
    p2 = q
    prob.clear()
    ex.clear()
    TraverseP(s)
    TraverseE(s)
    
def TraverseE(s):
    global prob, ex
    PnotE = False
    if GameWon(s) or GameLost(s):
        ex[s] = 0.0
        return
    if s in ex:
        return
    ex[s] = abs(prob[NextState(s, True, PnotE)] - prob[NextState(s, False, PnotE)])
    TraverseE(NextState(s, True, PnotE))
    TraverseE(NextState(s, False, PnotE))
    return

def Simulate():
    global p1, p2
    state = (0,0)
    trail = [state]
    while not (GameWon(state) or GameLost(state)):
        serve = GetServe(state)
        p = p1 if (serve == 0) else (1-p2)
        w = random() < p
        state = NextState(state, w, False)
        trail.append(state)
    return trail

def SimulateList(p, q):
    # p and q are lists of serve outcomes for Players 1 and 2
    state = (0,0)
    trail = [state]
    while not (GameWon(state) or GameLost(state)):
        serve = GetServe(state)
        w = p.pop() if (serve == 0) else not q.pop()
        state = NextState(state, w, False)
        trail.append(state)
    return trail

def PrintState(state):
    print '%d-%d' % state

def GetAverageMatchLength(N=100):
    s = 0.0
    for i in range(N):
        s += len(Simulate())
    return s/N

def GetAverageImportance(trail):
    global ex
    return sum(map(ex.__getitem__, trail)) / float(len(trail))
    

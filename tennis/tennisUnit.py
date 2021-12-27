# State : ((x,y,z),(m,n),(a,b))
# (x,y) = match score
# z = (0 for even # of games played) or (1 for odd # of games played)
#    [not counting current set]
# (m,n) = current set score
# (a,b) = current game score

# NextState() ignores the win-by-two requirements. GetPointOdds() instead takes
# it into account

from random import random

prob = dict()
ex = dict()
p1 = 0.6
p2 = 0.6

def UnpackState(state):
    return map(list, state)

def PackState(m,s,g):
    return tuple(map(tuple,(m,s,g)))

def IsTiebreaker(state):
    (m,s,g) = UnpackState(state)
    return (s == [6,6])

def IsDeuce(state):
    (m,s,g) = UnpackState(state)
    if IsTiebreaker(state):
        return (g == [6,6])
    else:
        return (g == [3,3])

def GameWon(state):
    assert not IsTiebreaker(state)
    (m,s,g) = UnpackState(state)
    return g[0] >= 4

def GameLost(state):
    assert not IsTiebreaker(state)
    (m,s,g) = UnpackState(state)
    return g[1] >= 4

def TiebreakerWon(state):
    assert IsTiebreaker(state)
    (m,s,g) = UnpackState(state)
    return (g[0] >= 7)

def TiebreakerLost(state):
    assert IsTiebreaker(state)
    (m,s,g) = UnpackState(state)
    return (g[1] >= 7)

def SetWon(state):
    (m,s,g) = UnpackState(state)
    return (s[0] == 6 and s[1] <= 4) or (s[0] == 7)

def SetLost(state):
    (m,s,g) = UnpackState(state)
    return (s[1] == 6 and s[0] <= 4) or (s[1] == 7)

def MatchWon(state):
    return state[0][0] >= 2

def MatchLost(state):
    return state[0][1] >= 2

def UpdateGame(state, PointWon, PnotE):
    (m,s,g) = UnpackState(state)
    if not PnotE and IsDeuce(state):
        # Move back to the state equivalent to ad in/out
        # Same for normal game and tiebreaker
        if PointWon:
            g[1] -= 1
        else:
            g[0] -= 1
    else:
        if PointWon:
            g[0] += 1
        else:
            g[1] += 1
    return PackState(m,s,g)

def UpdateSet(state):
    (m,s,g) = UnpackState(state)
    if IsTiebreaker(state):
        if TiebreakerWon(state):
            g = [0,0]
            s[0] += 1
        elif TiebreakerLost(state):
            g = [0,0]
            s[1] += 1
    else:
        if GameWon(state):
            g = [0,0]
            s[0] += 1
        elif GameLost(state):
            g = [0,0]
            s[1] += 1
    return PackState(m,s,g)

def UpdateMatch(state):
    (m,s,g) = UnpackState(state)
    if SetWon(state):
        m[2] = (m[2] + s[0] + s[1]) % 2
        s = [0,0]
        m[0] += 1
    elif SetLost(state):
        m[2] = (m[2] + s[0] + s[1]) % 2
        s = [0,0]
        m[1] += 1
    return PackState(m,s,g)

def NextState(state, PointWon, PnotE):
    if MatchWon(state) or MatchLost(state):
        return state

    state = UpdateGame(state, PointWon, PnotE)
    state = UpdateSet(state)
    state = UpdateMatch(state)

    return state

def TestNextState(p):
    s = ((0,0,0),(0,0),(0,0))
    print s
    while not MatchWon(s) and not MatchLost(s):
        w = random() < p
        s = NextState(s, w, True)
        print s, w

def GetServe(state):
    (m,s,g) = UnpackState(state)
    serve = (m[2] + s[0] + s[1]) % 2
    if IsTiebreaker(state):
        serve = (serve + (g[0] + g[1] + 1)/2) % 2
    return serve

def GetPointOdds(state):
    global p1, p2
    serve = GetServe(state)

    if IsDeuce(state):
        if not IsTiebreaker(state):
            if serve == 0:
                return p1*p1/(1-2*p1*(1-p1))
            else:
                return (1-p2)*(1-p2)/(1-2*p2*(1-p2))
        else:
            return (p1*(1-p2))/(1-p1*p2-(1-p1)*(1-p2))

    return p1 if (serve == 0) else (1-p2)

def TraverseP(s):
    global prob
    if MatchWon(s):
        prob[s] = 1.0
        return 1.0
    if MatchLost(s):
        prob[s] = 0.0
        return 0.0
    if s in prob:
        return prob[s]
    p = GetPointOdds(s)
    t = p*TraverseP(NextState(s, True, True)) + (1-p)*TraverseP(NextState(s, False, True))
    prob[s] = t
    return t

def Compute(p,q):
    global p1, p2, prob, ex
    s = ((0,0,0),(0,0),(0,0))
    p1 = p
    p2 = q
    prob.clear()
    ex.clear()
    TraverseP(s)
    TraverseE(s)
    
def TraverseE(s):
    global prob, ex
    PnotE = False
    if MatchWon(s) or MatchLost(s):
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
    state = ((0,0,0),(0,0),(0,0))
    trail = [state]
    while not (MatchWon(state) or MatchLost(state)):
        serve = GetServe(state)
        p = p1 if (serve == 0) else (1-p2)
        w = random() < p
        state = NextState(state, w, False)
        trail.append(state)
    return trail

def SimulateList(p, q):
    # p and q are lists of serve outcomes for Players 1 and 2
    state = ((0,0,0),(0,0),(0,0))
    trail = [state]
    while not (MatchWon(state) or MatchLost(state)):
        serve = GetServe(state)
        w = p.pop() if (serve == 0) else not q.pop()
        state = NextState(state, w, False)
        trail.append(state)
    return trail    

def PrintState(state):
    (m,s,g) = UnpackState(state)
    if IsTiebreaker(state):
        gp = range(8)
    else:
        gp = [0, 15, 30, 40]
    print '%d-%d %d-%d %d-%d' % (m[0], m[1], s[0], s[1], gp[g[0]], gp[g[1]])

def GetAverageMatchLength(N=100):
    s = 0.0
    for i in range(N):
        s += len(Simulate())
    return s/N
   

def GetAverageImportance(trail):
    global ex
    return sum(map(ex.__getitem__, trail)) / float(len(trail))
    

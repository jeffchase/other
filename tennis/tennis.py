# tennis.py

import tennisUnit
import tennisAgg
from random import random
from numpy import array
from datetime import datetime
# from scipy import io
import pickle

def setup(p=0.6, q=0.6):
    global p1, p2
    p1,p2 = p,q
    tennisUnit.Compute(p1, p2)
    tennisAgg.Compute(p1, p2)

def simulate():
    s1 = [random() < p1 for i in range(400)]
    s2 = [random() < p2 for i in range(400)]

    t_unit = tennisUnit.SimulateList(s1, s2)
    t_agg = tennisAgg.SimulateList(s1, s2)

    return t_unit, t_agg

def map_to_importance(t_unit, t_agg):
    e_unit = unit_importance(t_unit)
    e_agg = agg_importance(t_agg)
    return e_unit, e_agg

def unit_probabilities(t_unit):
    return map(tennisUnit.prob.__getitem__, t_unit)

def unit_importance(t_unit):
    return map(tennisUnit.ex.__getitem__, t_unit)

def agg_importance(t_agg):
    return map(tennisAgg.ex.__getitem__, t_agg)

def agg_probabilities(t_agg):
    return map(tennisAgg.prob.__getitem__, t_agg)

def run(T=1):
    m_u, m_a = ([0]*T, [0]*T)
    for i in range(T):
        m_u[i], m_a[i] = simulate()
    return m_u, m_a

def create_data(N, p=0.6, q=0.6):
    setup(p, q)
    m_u, m_a = run(N)
    #f_u = lambda(x): map(tennisUnit.ex.__getitem__, x)
    #f_a = lambda(x): map(tennisAgg.ex.__getitem__, x)
    #e_u, e_a = map(f_u, m_u), map(f_a, m_a)
    filename = 'raw-' + datetime.today().strftime('%b%d-%H%M%S')
    fout = open(filename, 'wb')
    #varsdict= {'Trials':N, 'p':p, 'q':q, 'matches_unit':m_u, 'matches_agg':m_a, 'ex_unit':e_u, 'ex_agg':e_a}
    varsdict= {'Trials':N, 'p':p, 'q':q, 'matches_unit':m_u, 'matches_agg':m_a}
    pickle.dump(varsdict, fout)
    fout.close()

def load_data():
    f = open('data/matches', 'rb')
    v = pickle.load(f)
    f.close()
    return v

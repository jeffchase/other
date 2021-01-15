# Threshold Plot

import numpy as np
import matplotlib
from matplotlib import pyplot as plt

import tennis

tennis.setup()
v = tennis.load_data()

m_u = v['matches_unit'][:1000]
m_a = v['matches_agg'][:1000]

i_u, i_a = [],[]

for m,n in zip(m_u, m_a):
    t_u, t_a = tennis.map_to_importance(m,n)
    i_u.extend(t_u)
    i_a.extend(t_a)

i_u = np.array(i_u)
i_a = np.array(i_a)

p_u, p_a = [],[]
ts = np.linspace(0, 0.3)
for t in ts:
    p_u.append(sum(i_u > t))
    p_a.append(sum(i_a > t))

p_u = np.array(p_u) / float(len(i_u))
p_a = np.array(p_a) / float(len(i_a))

plt.figure()
plt.plot(ts, p_u, ts, p_a)
plt.xlabel('Point Importance Threshold')
plt.ylabel('Percentage of Points')
plt.title('Percentage of Points vs. Threshold')
plt.legend(('Unit Scoring', 'Aggregate Scoring'))
plt.savefig('plots/percentage_threshold')

ps = np.linspace(0,1)
t_u = np.interp(ps, p_u[::-1], ts[::-1])
t_a = np.interp(ps, p_a[::-1], ts[::-1])

plt.figure()
plt.plot(ps, t_u, ps, t_a)
plt.xlabel('Percentage of points')
plt.ylabel('Point Importance')
plt.title('Minimum Point Importance vs. Percentage of Points')
plt.legend(('Unit Scoring', 'Aggregate Scoring'))
plt.savefig('plots/threshold_percentage')

plt.figure()
plt.plot(ps, t_u - t_a)
plt.xlabel('Percentage of points')
plt.ylabel('Difference in Point Importance')
plt.title('Difference in Minimum Point Importance vs. Percentage of Points')
plt.savefig('plots/threshold_perecentage_diff')

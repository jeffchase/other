# Game Lengths

import tennis
import matplotlib
from matplotlib import pyplot as plt

v = tennis.load_data()
m_u = v['matches_unit']
m_a = v['matches_agg']

l_u = map(len, m_u)
l_a = map(len, m_a)

plt.figure(1)
plt.hist(l_u, (max(l_u)-min(l_u)+1)/2)
plt.title('Distribution of match length - unit scoring')
plt.xlabel('Number of points'); plt.ylabel('Frequency')
plt.savefig('plots/lengthdist_unit')

plt.figure(2)
plt.hist(l_a, (max(l_a)-min(l_a)+1)/2)
plt.title('Distribution of match length - aggregate scoring')
plt.xlabel('Number of points'); plt.ylabel('Frequency')
plt.savefig('plots/lengthdist_agg')

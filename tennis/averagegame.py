import tennis
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

tennis.setup()
v = tennis.load_data()

m_u = v['matches_unit']
m_a = v['matches_agg']
N = v['Trials']

l_u = np.array(map(len, m_u))
l_a = np.array(map(len, m_a))

e_u = np.zeros([N, max(l_u)])
e_a = np.zeros([N, max(l_a)])

for i in range(N):
    i_u, i_a = tennis.map_to_importance(m_u[i], m_a[i])
    e_u[i][0:l_u[i]] = i_u
    e_a[i][0:l_a[i]] = i_a

# e[x][y]: x is match index, y is point index
mean_e_u = sum(e_u)/sum(e_u!=0)
mean_e_a = sum(e_a)/sum(e_a!=0)

for l in [125, 175, 225]:
    l_u_i = (l_u >= l) & (l_u <= l+5)
    e_u_i = e_u[l_u_i]
    mean_e_u_i = sum(e_u_i)/sum(e_u_i!=0)
    plt.figure()
    plt.plot(mean_e_u_i)
    plt.title('Average point importance (unit scoring) (match length ' + str(l) + '-' + str(l+5) + ')')
    plt.xlabel('Point in match')
    plt.ylabel('Average point importance')
    plt.ylim(0, 0.5)
    plt.savefig('plots/averagematch_unit_' + str(l))

for l in [150, 160, 170]:
    l_a_i = (l_a >= l) & (l_a <= l+5)
    e_a_i = e_a[l_a_i]
    mean_e_a_i = sum(e_a_i)/sum(e_a_i!=0)
    plt.figure()
    plt.plot(mean_e_a_i)
    plt.title('Average point importance (aggregate scoring) (match length ' + str(l) + '-' + str(l+5) + ')')
    plt.xlabel('Point in match')
    plt.ylabel('Average point importance')
    plt.ylim(0, 0.5)
    plt.savefig('plots/averagematch_agg_' + str(l))

plt.figure()
plt.plot(mean_e_u)
plt.xlabel('Point in match')
plt.ylabel('Average point importance')
plt.title('Average point importance (unit scoring)')
plt.ylim(0, 0.5)
plt.savefig('plots/averagematch_unit')

plt.figure()
plt.plot(mean_e_a)
plt.xlabel('Point in match')
plt.ylabel('Average point importance')
plt.title('Average point importance (aggregate scoring)')
plt.ylim(0, 0.5)
plt.savefig('plots/averagematch_agg')

# Single Game

import matplotlib
from matplotlib import pyplot as plt

import tennis

tennis.setup()

v = tennis.load_data()

m_u = v['matches_unit']
m_a = v['matches_agg']

t = m_u[0]
p = tennis.unit_probabilities(t)
i = tennis.unit_importance(t)

# Interesting scores: 42 (4-2 break), 60 (5-4 break), 79 (6-6 (2-0)),
# 88 (6-7 (7-4)), 145 (6-7 6-4), 210 (6-7 6-4 6-6), 219 (6-7 6-4 7-6 (7-2))
plt.figure()
plt.ylim([0,1.1])
plt.plot(p)
plt.annotate('4-2', xy=(42, p[42]), xytext=(20, 0.75),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('5-4', xy=(60, p[60]), xytext=(40, 0.45),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('6-6 (2-0)', xy=(79, p[79]), xytext=(60, 0.75),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('6-7 (7-4)', xy=(88, p[88]), xytext=(50, 0.2),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('6-7 6-4', xy=(145, p[145]), xytext=(130, 0.55),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('6-7 6-4 6-6 (0-0)', xy=(210, p[210]), xytext=(145, 0.65),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('6-7 6-4 7-6 (7-2)', xy=(219, p[219]), xytext=(145, 0.85),
             arrowprops=dict(width=1, frac=0.1))
plt.hold(True)
plt.plot(i)
plt.legend(('Probability of Player 1 Winning','Point Importance'), loc=2)
plt.xlabel('Match Progress')
plt.ylabel('Probability/Importance')
plt.title('Match Progress (Unit Scoring)')
plt.savefig('plots/singlematch_unit')

t = m_a[0]
p = tennis.agg_probabilities(t)
i = tennis.agg_importance(t)

plt.figure()
plt.ylim([0,1.1])
plt.plot(p)
plt.annotate('62-38', xy=(100, p[100]), xytext=(90, 0.9),
             arrowprops=dict(width=1, frac=0.1))
plt.annotate('88-60', xy=(148, p[148]), xytext=(130, 0.9),
             arrowprops=dict(width=1, frac=0.1))
plt.hold(True)
plt.plot(i)
plt.legend(('Probability of Player 1 Winning','Point Importance'), loc=7)
plt.xlabel('Match Progress')
plt.ylabel('Probability/Importance')
plt.title('Match Progress (Aggregate Scoring)')
plt.savefig('plots/singlematch_agg')

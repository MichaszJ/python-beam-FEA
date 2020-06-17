import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from beam import Beam

endpoints = ['fixed', 'none']
forces = [
    ['distributed', 1000, [0, 1]],
    ['distributed', 1500, [1, 2]]
]

#b1 = Beam(80, endpoints, forces, 2, 82.74e9, 0.00001956)
#print(b1.get_max_deflect())

# TESTING
start = time.time()
elems = list(np.linspace(1, 150, 150))
maxes = []
for element in elems:
    beam = Beam(int(element), endpoints, forces, 2, 82.74e9, 0.00001956)
    maxes.append(beam.get_max_deflect())

print('Elapsed time for {0} beams: {1}'.format(len(elems), time.time() - start))

sns.set()
plt.figure(dpi=230)
plt.plot(elems, maxes)
plt.xlabel('Number of elements')
plt.ylabel('Maximum displacement of beam')
plt.show()
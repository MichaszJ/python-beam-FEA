import numpy as np
import matplotlib.pyplot as plt
from element import Element
plt.style.use('classic')

class Beam():
    def __init__(self, num_elements, endpoints, forces, length, elastic_mod, moment_inertia):
        self.num_elements = num_elements
        self.endpoints = endpoints
        self.forces = forces
        self.length = length
        self.elastic_mod = elastic_mod
        self.moment_inertia = moment_inertia

        num_nodes = self.num_elements + 1
        num_removed = 0

        if self.endpoints[0] == 'fixed':
            num_removed += 2

        elif self.endpoints[0] == 'pin':
            num_removed += 1

        if self.endpoints[1] == 'fixed':
            num_removed += 2

        elif self.endpoints[1] == 'pin':
            num_removed += 1

        num_columns = 2*num_nodes - num_removed

        row = [0] * num_columns
        temp_list = [row] * 2*num_nodes
        temp_list = [sublist[:] for sublist in temp_list]

        # x = 0
        if self.endpoints[0] == 'fixed':
            for x in range(0, 2*num_nodes - 4):
                temp_list[x+2][x] = 1
            
        elif self.endpoints[0] == 'pin':
            for x in range(0, 2*num_nodes - 4):
                temp_list[x+1][x] = 1

        elif self.endpoints[0] == 'none':
            for x in range(0, 2*num_nodes - 4):
                temp_list[x][x] = 1

        # x = L
        if self.endpoints[1] == 'pin':
            temp_list[2*num_nodes-1][-1] = 1

        elif self.endpoints[1] == 'none':
            temp_list[2*num_nodes-2][-2] = 1
            temp_list[2*num_nodes-1][-1] = 1

        self.boundary_conditions = np.matrix(temp_list)

        # todo: revamp elements declaration to implement different force types and magnitudes
        elements = [Element(x+1, self.num_elements, self.forces[0], self.forces[1], self.length/self.num_elements, self.elastic_mod, self.moment_inertia) for x in range(self.num_elements)]

        global_stiffness = sum([element.global_stiffness_part for element in elements])
        global_force = sum([element.global_force_part for element in elements])

        global_stiffness_BC = self.boundary_conditions.T * global_stiffness * self.boundary_conditions
        global_force_BC = self.boundary_conditions.T * global_force

        u_matrix = np.linalg.inv(global_stiffness_BC) * global_force_BC
        self.u_matrix_list = list(np.array(u_matrix).reshape(-1,))

    def plot(self):
        displacements = [0] + [self.u_matrix_list[x*2] for x in range(int(len(self.u_matrix_list)/2))]
        x = np.linspace(0, 2, self.num_elements+1)

        plt.figure(dpi=180)
        plt.title('Beam displacement n = ' + str(self.num_elements))
        plt.plot(x, displacements, 'o-')
        plt.show()
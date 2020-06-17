import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from element import Element

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
        # elements = [Element(x+1, self.num_elements, self.forces[0], self.forces[1], self.length/self.num_elements, self.elastic_mod, self.moment_inertia) for x in range(self.num_elements)]

        # todo: create point forces at distributed force intersections
        # check for distributed load intersections
        #if len(self.forces) != 1:
        #    for x in range(len(self.forces)-1):
        #        if self.forces[x][0] == 'distributed' and self.forces[x+1][0] == 'distributed':
        #            if self.forces[x][2][1] == self.forces[x+1][2][0]:
        #                self.forces.append(['point', self.forces[x][1] + self.forces[x+1][1], [self.forces[x][2][1], self.forces[x][2][1]]])

        elements = []
        for i in range(self.num_elements):
            distance = i * (self.length / self.num_elements)

            force_magnitude = 0
            for force in self.forces:
                if force[2][0] <= distance <= force[2][1]:
                    force_magnitude += force[1]
                    force_type = force[0]

            elements.append(Element(i+1, self.num_elements, force_type, force_magnitude, self.length/self.num_elements, self.elastic_mod, self.moment_inertia))
            

        global_stiffness = sum([element.global_stiffness_part for element in elements])
        global_force = sum([element.global_force_part for element in elements])

        global_stiffness_BC = self.boundary_conditions.T * global_stiffness * self.boundary_conditions
        global_force_BC = self.boundary_conditions.T * global_force

        u_matrix = np.linalg.inv(global_stiffness_BC) * global_force_BC
        self.u_matrix_list = list(np.array(u_matrix).reshape(-1,))

        # adding boundary conditions to u matrix
        if self.endpoints[0] == 'fixed':
            self.u_matrix_list.insert(0, 0)
            self.u_matrix_list.insert(0, 0)

        elif self.endpoints[0] == 'pin':
            self.u_matrix_list.insert(0, 0)

        if self.endpoints[1] == 'fixed':
            self.u_matrix_list.append(0)
            self.u_matrix_list.append(0)

        elif self.endpoints[1] == 'pin':
            self.u_matrix_list.insert(-1, 0)

        self.displacements = [self.u_matrix_list[x*2] for x in range(int(len(self.u_matrix_list)/2))]

    def plot(self, dpi):
        # scaling displacement graph
        #self.displacements = [self.u_matrix_list[x*2] for x in range(int(len(self.u_matrix_list)/2))]

        #scale_factor = 1
        #scaled_displacements = [element*scale_factor for element in displacements]

        #while min(scaled_displacements) > -0.25:
        #    scale_factor = scale_factor*5
        #    scaled_displacements = [element*5 for element in scaled_displacements]

        x = np.linspace(0, 2, self.num_elements + 1)

        sns.set()
        plt.figure(dpi=dpi)

        plt.title('Beam Displacement - # Elements = {0}'.format(self.num_elements))
        plt.plot([0, self.length], [0, 0], '--', label='Original Beam')
        plt.plot(x, self.displacements, '.-', label='Loaded Beam')
        plt.legend()

        plt.show()

    def get_max_deflect(self):
        return min(self.displacements)
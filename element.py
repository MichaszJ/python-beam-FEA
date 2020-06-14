import numpy as np

class Element():
    def __init__(self, elem_num, total_num, force_type, force_magnitude, length, elastic_mod, moment_inertia):
        self.elem_num = elem_num
        self.total_num = total_num
        self.force_type = force_type
        self.force_magnitude = force_magnitude
        self.length = length
        self.elastic_mod = elastic_mod
        self.moment_inertia = moment_inertia

        # stiffness matrix
        const = (self.elastic_mod * self.moment_inertia) / (self.length**3)
        matrix = np.matrix([
            [12, 6*self.length, -12, 6*self.length],
            [6*self.length, 4*self.length**2, -6*self.length, 2*self.length**2],
            [-12, -6*self.length, 12, -6*self.length],
            [6*self.length, 2*self.length**2, -6*self.length, 4*self.length**2]
        ])

        self.stiffness_matrix = const * matrix

        # translation matrix
        list = []

        if self.elem_num != 1:
            for x in range(self.elem_num-1):
                list.append([0, 0, 0, 0])
                list.append([0, 0, 0, 0])

        list.append([1, 0, 0, 0])
        list.append([0, 1, 0, 0])
        list.append([0, 0, 1, 0])
        list.append([0, 0, 0, 1])

        if self.elem_num != self.total_num:
            for x in range(self.elem_num, self.total_num):
                list.append([0, 0, 0, 0])
                list.append([0, 0, 0, 0])

        self.translation_matrix = np.matrix(list)

        # element part of global stiffness matrix
        self.global_stiffness_part = self.translation_matrix * self.stiffness_matrix * self.translation_matrix.T

        # force matrix
        if self.force_type == 'distributed':
            self.force_matrix = np.matrix([
                [-self.force_magnitude*(self.length)/2],
                [-self.force_magnitude*((self.length)**2)/12],
                [-self.force_magnitude*(self.length)/2],
                [self.force_magnitude*((self.length)**2)/12]
            ])

        elif self.force_type == 'point':
            self.force_matrix = np.matrix([
                [-self.force_magnitude/2],
                [-self.force_magnitude*self.length/8],
                [-self.force_magnitude/2],
                [self.force_magnitude*self.length/8]
            ])

        #elif self.force_type == 'linear':

        # element part of global force matrix
        self.global_force_part = self.translation_matrix * self.force_matrix
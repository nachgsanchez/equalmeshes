import bpy
import mathutils
import numpy as np

import bpy

#Main solver for rigid transforms
#For now, a mixture of NumPy/Mathutils data structures and utilities
#is chosen, without much criteria or regards to performance, and mainly
#prioritizing simplicity of code. This is likely to change in the future.
class Solver:
    def __init__(self, obj_from, obj_to, treshold):
        #Mean of distances between each point pair is used to test
        #against treshold. It's pretty unamazing, and once other features are added, it
        #won't work, but for now it will do.
        self.treshold = treshold

        #points_{}_abs just stores the absolute positions of the points in the mesh, as you 
        #see them in the viewport (so, with transforms applied)
        self.points_from_abs = [obj_from.matrix_world @ v.co for v in obj_from.data.vertices]
        self.points_to_abs = [obj_to.matrix_world @ v.co for v in obj_to.data.vertices]
        self.count = len(self.points_to_abs)

        #Centroids are just averages of points
        self.centroid_from = np.sum(self.points_from_abs, axis = 0) / self.count
        self.centroid_to = np.sum(self.points_to_abs, axis = 0) / self.count

        #These are just the point cloud's points relative to their respective centroids
        self.points_to_rel = np.array(self.points_to_abs) - self.centroid_to
        self.points_from_rel = np.array(self.points_from_abs) - self.centroid_from

    def solve(self):
        scale = self.solve_scale()
        rotation = self.solve_rotation()
        translation = self.solve_translation(scale, rotation)

        transform = translation @ (scale * rotation)
        
        #These are the transformed absolute points of the 'from mesh' 
        tp_abs = [transform @ v for v in self.points_from_abs]
        mean_distance = sum([(tp_abs[x] - self.points_to_abs[x]).magnitude for x in range(self.count)]) / self.count
        return mean_distance < self.treshold


    def solve_scale(self):
        num = np.sum(np.square(self.points_to_rel))
        den = np.sum(np.square(self.points_from_rel))
        return ((num / den) ** (1 / 2)).item()

    def solve_rotation(self):
        #The rotation matrix
        matrix = np.zeros((4,4))

        #Matrix representations of both relative point clouds
        from_matrices = np.array([Solver.from_vert_to_matrix(v) for v in self.points_from_rel])
        to_matrices = np.array([Solver.to_vert_to_matrix(v) for v in self.points_to_rel])
        matrix = np.sum(np.matmul(from_matrices, to_matrices), axis=0)


        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        #Eigenvectors are returned by numpy as column vectors, so we transpose
        eigenvectors = np.transpose(eigenvectors)
        max_eigval_idx = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[max_eigval_idx]
        
        #A quaternion representation of our max eigenvector
        eig_qr = mathutils.Quaternion(max_eigenvector)

        return eig_qr.to_matrix().to_4x4()

    def solve_translation(self, scale, rotation):
        #We convert our centroids to mathutils vectors
        to_centroid = mathutils.Vector(self.centroid_to)
        from_centroid = mathutils.Vector(self.centroid_from)

        t_vector = to_centroid - scale * (rotation @ from_centroid)
        return mathutils.Matrix.Translation(t_vector)

    @staticmethod
    def from_vert_to_matrix(fv):
        fvm = np.array([
            [0     ,-fv[0] ,-fv[1] ,-fv[2]],
            [fv[0] ,0      ,fv[2]  ,-fv[1]],
            [fv[1] ,-fv[2] ,0      ,fv[0] ],
            [fv[2] ,fv[1]  ,-fv[0] ,0     ]
        ])
        return np.transpose(fvm)

    @staticmethod
    def to_vert_to_matrix(tv):
        tvm = np.array([
            [0     ,-tv[0] ,-tv[1] ,-tv[2]],
            [tv[0] ,0      ,-tv[2] ,tv[1] ],
            [tv[1] ,tv[2]  ,0      ,-tv[0]],
            [tv[2] ,-tv[1] ,tv[0]  ,0     ]
        ])
        return tvm

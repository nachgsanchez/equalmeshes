import bpy
import mathutils
import numpy as np

class Solver:
    @staticmethod
    def Solve(cloud_from, cloud_to):
        pass

    @staticmethod
    def solve_scale(cloud_from, cloud_to):
        num = np.sum(np.square(cloud_to.points_rel))
        den = np.sum(np.square(cloud_from.points_rel))
        return (num / den) ** (1 / 2)

    @staticmethod
    def solve_rotation(cloud_from, cloud_to):
        matrix = np.zeros((4,4))

        #fv is as in 'From Vertex'
        #tv is as in 'To Vertex'
        #mfv and mtv are their respective matrix representations
        for x in range(cloud_from.count):
            fv = cloud_from.points_rel[x]
            fvm = np.array([
                [0     ,-fv[0] ,-fv[1] ,-fv[2]],
                [fv[0] ,0      ,fv[2]  ,-fv[1]],
                [fv[1] ,-fv[2] ,0      ,fv[0] ],
                [fv[2] ,fv[1]  ,-fv[0] ,0     ]
            ])

            tv = cloud_to.points_rel[x]
            tvm = np.array([
                [0     ,-tv[0] ,-tv[1] ,-tv[2]],
                [tv[0] ,0      ,-tv[2] ,tv[1] ],
                [tv[1] ,tv[2]  ,0      ,-tv[0]],
                [tv[2] ,-tv[1] ,tv[0]  ,0     ]
            ])

            matrix += np.transpose(fvm) @ tvm
        
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        #Eigenvectors are returned by numpy as column vectors, so we transpose
        eigenvectors = np.transpose(eigenvectors)
        max_eigval_idx = np.argmax(eigenvalues)
        max_eigenvector = eigenvectors[max_eigval_idx]
        
        #A quaternion representation of our max eigenvector
        eig_qr = mathutils.Quaternion(max_eigenvector)
        return eig_qr.to_matrix().to_4x4()


    @staticmethod
    def solve_translation(cloud_from, cloud_to, scale, rotation):
        return cloud_to.centroid - scale * (rotation @ cloud_from.centroid)


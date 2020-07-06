import bpy
import numpy as np

class PointCloud:
    def __init__(self, obj):
        points_abs = [obj.matrix_world @ v.co for v in obj.data.vertices]

        #points_abs just stores the absolute positions of the points in the mesh, as you 
        #see them in the viewport (so, with transforms applied)
        self.points_abs = [np.array([v.x, v.y, v.z]) for v in points_abs]

        #centroid is just an average of those points
        self.centroid = np.sum(self.points_abs, axis = 0) / self.points_abs.size

        #these are just the mesh's points relative to the centroid
        self.points_rel = self.points_abs - self.centroid
import bpy
import numpy as np
import core.utils.conversions as conv

#Class to represent meshes as objects
class PointCloud:
    def __init__(self, obj):
        self.wm = np.array(obj.matrix_world)

        #These are the absolute positions of the mesh's vertices (as you see them in the viewport), so,
        #with object transforms 'applied'
        self.abs_points = self.wm.dot(np.array([conv.Vector3D_4D(v.co) for v in obj.data.vertices]).T).T

        #centroid is just the average of those points, and rel_points are the points relative to the centroid
        self.centroid = np.mean(self.abs_points, axis=0)
        self.rel_points = self.abs_points - self.centroid
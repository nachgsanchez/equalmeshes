# :hammer: Equal Meshes
Equal meshes is a blender addon intended to provide useful tools when dealing with sets of unorganized meshes that are equal in shape.
Although it is at a very early stage, and the set of features intended to be added in the future is quite large, the little that it can do right now seemed to be useful enough to share the code as it is. Moreover, what it brings to the table is still not heavily tested (and will probably be implemented differently in the future), so use with caution.

# Installation
Just download the source files as a Zip file, and install from within Blender's preferences menu. Enable the addon, and voilá.

# Supported features (so far)
* Selection of meshes equal in shape (exactly the same geometry) to the active selected mesh. It does not matter wether object transforms were applied or not.  
  Limitations of this feature:
  * Right now, this only works if the meshes being compared have **the same vertex ordering** (this tends to be the case), so, keep that in mind. Adding support for point matching will fix this and is the next priority, but it may take some time since it's not a trivial task.
  * Currently, meshes are treated as point clouds, so, meshes that share the same shape, but don't share the same set of polygons will be trated as equal. This, however, is very rare, and should not matter.

# Usage
Right now, after installing the addon, a menu entry gets added to the 'Select' menu in the 3D view, when in object mode. You can perform the selection via that menu entry, or you can use the default shortcut keyboard SHIFT+E, or set your own in the preferences menu.
  
![alt text](https://github.com/nachgsanchez/equalmeshes/blob/master/images/menu_entry.png?raw=true)

# Sources
Works that helped implement this software so far:
  * **B.K.P Horn**, Closed Form Solution of Absolute Orientation Using Unit Quaternions
  * **Besl, A Method** for Registration of 3D Shapes

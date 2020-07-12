# :hammer: Equal Meshes
Equal meshes is a Blender addon intended to provide useful tools when dealing with sets of unorganized meshes that are equal in shape.
Although it is at a very early stage, and the set of features intended to be added in the future is quite large, the little that it can do right now seemed to be useful enough to share the code as it is. Moreover, what it brings to the table is still not heavily tested (and will probably be implemented differently in the future), so use with caution.

# Installation
Just download the source files as a Zip file, and install from within Blender's preferences menu. Enable the addon, and voilá.

# Supported features (so far)
* Selection of all meshes equal or almost similar in shape to the active selected mesh. It does not matter wether object transforms were applied or not.  
  Limitations of this feature:
  * Right now, this only works if the meshes being compared have **the same vertex ordering** (this tends to be the case), so, keep that in mind. Adding support for point matching will fix this and is the next priority, but it may take some time since it's not a trivial task.
  * Currently, meshes are treated as point clouds, so, meshes that share the same set of vertices, but don't share the same set of polygons will be treated as equal. This, however, is very rare, and should not get in the way of basic selection functionality. It may or may not be changed in the future.
# Usage
Right now, after installing the addon, a menu entry gets added to the 'Select' menu in the 3D view, when in object mode. You can perform the selection via that menu entry, or you can use the default shortcut keyboard SHIFT+E, or set your own in the preferences menu.  
After selection, a redo panel is displayed at the bottom left of the 3D Viewport, along with a 'Distance Treshold' property that the user can modify. This treshold is used to decide 'how similar' a mesh must be to be considered a match. It is used to specify the maximum distance that there can be between pairs of corresponding vertices after alignment. Small values might have to be used when working on very small scale scenes (since, say, the default value of 0.001 might actually be a big relative difference at such scales). Bigger values will accept meshes that are less and less equal to the one being compared, but **it will also help avoid errors caused by floating point arithmetic, which tends to get inaccurate at big scale scenes**. This is something to be looked at in the future, but it's not clear now if there's a way to optimize code to mitigate these errors, or if it's just a limitation of hardware + Blender using single precision FP representation/ not handling things that well. So right now (at big scales), a compromise between shape similarity and precision must be made.
  
![alt text](https://github.com/nachgsanchez/equalmeshes/blob/master/images/menu_entry.png?raw=true)

# Sources
Works that helped implement this software so far:
  * **B.K.P Horn**, Closed Form Solution of Absolute Orientation Using Unit Quaternions.
  * **Besl**, A Method for Registration of 3D Shapes.

# Equal Meshes
Equal meshes is a blender addon intended to provide useful tools when dealing with sets of unorganized meshes that are equal in shape.
Although it is at a very early stage, and the set of features intended to be added in the future is quite large, the little that it can do right now seemed to be useful enough to share the code as it is. Moreover, what it brings to the table was still not heavily tested (and will probably be implemented differently in the future), so use with caution.

# Installation
Just download the source files as a Zip file, and install from within Blender's preferences menu. Enable the addon, and voilá.

# Supported features (so far)
Selection of meshes equal in shape to the active selected mesh.
Limitations of this feature:
*Right now, this only works if the meshes being compared has the same vertex ordering (this tends to be the case), so, keep that in mind. Adding support for point matching will fix this and is the next priority, but it may take some time since it's not a trivial task.

# Usage
Right now, after installing the addon, a menu entry gets added to the 'Select' menu in the 3D view, when in object mode. You can perform the selection via that menu entry, or you can use the default shortcut keyboard SHIFT+E, or set your own in the preferences menu.

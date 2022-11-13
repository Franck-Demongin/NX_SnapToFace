![hero](https://user-images.githubusercontent.com/54265936/201523374-aac64fa8-f943-4e46-b0ac-41ce27eca51b.png)

# NX_SnapToFace
Snap source object to active face of  target object or duplicate source to selected faces of target.

<img src="https://img.shields.io/badge/Blender-2.8.0-green" /> <img src="https://img.shields.io/badge/Python-3.10-blue" /> <img src="https://img.shields.io/badge/Addon-1.0.0.Stable-orange" /> 
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

## Installation
Download ZIP file on your system.

In Blender, install addon from _Preferences > Add-ons > Install_...  
Activate the addon

## Usage

![snap_to_face](https://user-images.githubusercontent.com/54265936/201523909-e9b5422e-a6b5-49e7-8a8b-54594f551219.png)

In order, select one or more faces of target object. In Object Mode, select source object first then target object.

In Object Mode, the commands are available in the menu _Object > Snap_  
and in the _contextual menu > Snap_ (right clic in the viewport)  
In Edit Mode, the commands are available in the menu _Mesh > Snap_

> _Both objects, source and target **must have their scale applyed!**  
> Don't apply the rotation and keep top of the source object oriented on Z axis._

### Snap to Face
The source object is snapped to the center of the selected face (the last selected) of the target object.

### Duplicate and Snap to Faces
The source object is duplicated and the copys are snapped on each selected face.

### Duplicate Linker and Snap to Face
Like _Duplicate and Snap to Face_ but uses some linked copys of the source object.




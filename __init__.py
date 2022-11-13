# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NX_SnapToFace",
    "author" : "Franck Demongin",
    "description" : "Snap source object to active face of target object or duplicate source to selected faces of target.",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "View3D > Object > Snap",
    "warning" : "",
    "category" : "Object"
}

import bpy
from mathutils import Matrix

def snap_to_face(obj, face, mw):
    """Sbap obj on face"""
    
    normal = face.normal
    center = face.center    
    up = normal.to_track_quat('Z', 'Y')
    matrix_rot = mw.to_3x3() @ up.to_matrix()
    matrix_translation = Matrix.Translation(mw @ center)
        
    obj.matrix_world = matrix_translation @ matrix_rot.to_4x4()
    
class NXSTF_OT_snap_to_face(bpy.types.Operator):    
    """Snap source object on active face in target object."""    
    bl_idname = 'nxstf.snap_to_face'
    bl_label = 'Snap to Face'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if (
            context.object is None or 
            len(context.selected_objects) != 2 or
            context.object.data.polygons.active is None or
            context.object.data.polygons[context.object.data.polygons.active].select == False
        ):
            return False
        return True
    
    def execute(self, context):
        target = context.object
        selected = context.selected_objects
    
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    
        src = [obj for obj in selected if obj is not target][0]    
        mw = target.matrix_world.copy()
        face = target.data.polygons[target.data.polygons.active]    
        
        snap_to_face(src, face, mw)
        
        return {'FINISHED'}
    
class NXSTF_OT_duplicate_and_snap_to_face(bpy.types.Operator):    
    """Snap a copy of source object on each faces selected in target object."""
    bl_idname = 'nxstf.duplicate_and_snap_to_face'
    bl_label = 'Duplicate and Snap to Face'
    bl_options = {'REGISTER', 'UNDO'}
    
    linked: bpy.props.BoolProperty(default=False)        
    
    @classmethod
    def poll(cls, context):
        if (
            context.object is None or 
            len(context.selected_objects) != 2 or
            len([f for f in context.object.data.polygons if f.select]) == 0
        ):
            return False
        return True
    
    def execute(self, context):
        target = context.object
        selected = context.selected_objects    
        
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        src = [obj for obj in selected if obj is not target][0]        
        mw = target.matrix_world.copy()
        faces = [f for f in target.data.polygons if f.select]
    
        for f in faces:
            if self.linked:
                copy = src.copy()        
            else:
                copy = bpy.data.objects.new(src.name, src.data.copy())
            
            context.collection.objects.link(copy)
            
            snap_to_face(copy, f, mw)

        return {'FINISHED'}
    
        
def draw_menu(self, context):    
    layout = self.layout
    layout.separator()
    layout.operator('nxstf.snap_to_face', text="Snap to Face")
    layout.operator('nxstf.duplicate_and_snap_to_face', text="Duplicate and Snap to Face")
    layout.operator('nxstf.duplicate_and_snap_to_face', text="Duplicate Linked and Snap to Face").linked = True

classes = (
   NXSTF_OT_snap_to_face,
   NXSTF_OT_duplicate_and_snap_to_face,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_snap.append(draw_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
          
    bpy.types.VIEW3D_MT_snap.remove(draw_menu)
  
if __name__ == "__main__":
    register()
"""No desc.

:copyright: (c) 2018, Serge Emond
:license: BSD

"""

import os

import bpy
from bpy.app.handlers import persistent
from bpy.props import StringProperty

bl_info = {
    'name': 'System Path',
    'author': 'Serge Émond',
    'version': (0, 2),
    'blender': (2, 79, 0),
    'description': "Add paths to the system's path",
    'category': 'System',
}


class State(object):
    """Temporary buffer to remember the original path."""

    original_path = None


class SystemPathApply(bpy.types.Operator):
    """Apply the path."""

    bl_idname = "systempath.apply"
    bl_label = "Apply the system's path"
    bp_options = {"REGISTER", 'UNDO'}
    bl_description = "Apply the system path's configuration"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        if State.original_path:
            os.environ['PATH'] = State.original_path
        else:
            State.original_path = os.environ.get('PATH', '')

        if addon_prefs.prepath:
            os.environ['PATH'] = (
                addon_prefs.prepath + os.pathsep + os.environ['PATH'])
        if addon_prefs.postpath:
            os.environ['PATH'] += os.pathsep + addon_prefs.postpath

        return {"FINISHED"}


class SystemPathReset(bpy.types.Operator):
    """Reset the path."""

    bl_idname = "systempath.reset"
    bl_label = "Reset the system's path"
    bp_options = {"REGISTER", 'UNDO'}
    bl_description = "Reset the original system path"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences

        if State.original_path:
            os.environ['PATH'] = State.original_path
            State.original_path = None

        return {"FINISHED"}


class SystemPathPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    prepath = StringProperty(
        name="Path prefix",
        subtype="FILE_PATH",
    )
    postpath = StringProperty(
        name="Path suffix",
        subtype="FILE_PATH",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(
            text="Separate items with semi-colon (':'). "
            "Example: /usr/local/bin:/usr/local/sbin")
        layout.prop(self, "prepath")
        layout.prop(self, "postpath")

        # col = layout.column(align=True)
        layout.operator("systempath.apply", text="Apply changes")


@persistent
def _init(context):
    # bpy.app.handlers.scene_update_pre.remove(_init_scene)
    # bpy.app.handlers.load_post.remove(_init)

    bpy.ops.systempath.apply()


def register():
    bpy.utils.register_class(SystemPathPreferences)
    bpy.utils.register_class(SystemPathApply)
    bpy.utils.register_class(SystemPathReset)
    bpy.app.handlers.load_post.append(_init)


def unregister():
    bpy.ops.systempath.reset()
    bpy.utils.unregister_class(SystemPathPreferences)
    bpy.utils.unregister_class(SystemPathApply)
    bpy.utils.unregister_class(SystemPathReset)

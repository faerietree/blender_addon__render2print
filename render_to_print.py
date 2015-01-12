# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    'name': 'Render to Print to Scale',
    'author': 'Marco Crippa <thekrypt77@tiscali.it>, Dealga McArdle, J.R.B.-Wein <Radagast@DragonTale.DE>, faerietree',
    'version': (0, 3),
    'blender': (2, 6, 8),
    'location': 'Render > Render to Print',
    'description': 'Set the size of the render for a print',
    'wiki_url': 'http://wiki.blender.org/index.php/Extensions:2.6/Py/'\
        'Scripts/Render/Render to Print',
    'tracker_url': 'https://projects.blender.org/tracker/index.php?'\
        'func=detail&aid=24219',
    'category': 'Render'}


import math
import bpy
from bpy.types import Panel, Operator, Scene, PropertyGroup
from bpy.props import (IntProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       PointerProperty,
                       BoolProperty
                       )


paper_presets = (
    ("custom_1_1", "custom", ""),
    ("A0_84.1_118.9", "A0 (84.1x118.9 cm)", ""),
    ("A1_59.4_84.1", "A1 (59.4x84.1 cm)", ""),
    ("A2_42.0_59.4", "A2 (42.0x59.4 cm)", ""),
    ("A3_29.7_42.0", "A3 (29.7 42.0 cm)", ""),
    ("A4_21.0_29.7", "A4 (21.0x29.7 cm)", ""),
    ("A5_14.8_21.0", "A5 (14.8x21.0 cm)", ""),
    ("A6_10.5_14.8", "A6 (10.5x14.8 cm)", ""),
    ("A7_7.4_10.5", "A7 (7.4x10.5 cm)", ""),
    ("A8_5.2_7.4", "A8 (5.2x7.4 cm)", ""),
    ("A9_3.7_5.2", "A9 (3.7x5.2 cm)", ""),
    ("A10_2.6_3.7", "A10 (2.6x3.7 cm)", ""),

    ("B0_100.0_141.4", "B0 (100.0x141.4 cm)", ""),
    ("B1_70.7_100.0", "B1 (70.7x100.0 cm)", ""),
    ("B2_50.0_70.7", "B2 (50.0x70.7 cm)", ""),
    ("B3_35.3_50.0", "B3 (35.3x50.0 cm)", ""),
    ("B4_25.0_35.3", "B4 (25.0x35.3 cm)", ""),
    ("B5_17.6_25.0", "B5 (17.6x25.0 cm)", ""),
    ("B6_12.5_17.6", "B6 (12.5x17.6 cm)", ""),
    ("B7_8.8_12.5", "B7 (8.8x12.5 cm)", ""),
    ("B8_6.2_8.8", "B8 (6.2x8.8 cm)", ""),
    ("B9_4.4_6.2", "B9 (4.4x6.2 cm)", ""),
    ("B10_3.1_4.4", "B10 (3.1x4.4 cm)", ""),

    ("C0_91.7_129.7", "C0 (91.7x129.7 cm)", ""),
    ("C1_64.8_91.7", "C1 (64.8x91.7 cm)", ""),
    ("C2_45.8_64.8", "C2 (45.8x64.8 cm)", ""),
    ("C3_32.4_45.8", "C3 (32.4x45.8 cm)", ""),
    ("C4_22.9_32.4", "C4 (22.9x32.4 cm)", ""),
    ("C5_16.2_22.9", "C5 (16.2x22.9 cm)", ""),
    ("C6_11.4_16.2", "C6 (11.4x16.2 cm)", ""),
    ("C7_8.1_11.4", "C7 (8.1x11.4 cm)", ""),
    ("C8_5.7_8.1", "C8 (5.7x8.1 cm)", ""),
    ("C9_4.0_5.7", "C9 (4.0x5.7 cm)", ""),
    ("C10_2.8_4.0", "C10 (2.8x4.0 cm)", ""),

    ("Letter_21.6_27.9", "Letter (21.6x27.9 cm)", ""),
    ("Legal_21.6_35.6", "Legal (21.6x35.6 cm)", ""),
    ("Legal junior_20.3_12.7", "Legal junior (20.3x12.7 cm)", ""),
    ("Ledger_43.2_27.9", "Ledger (43.2x27.9 cm)", ""),
    ("Tabloid_27.9_43.2", "Tabloid (27.9x43.2 cm)", ""),

    ("ANSI C_43.2_55.9", "ANSI C (43.2x55.9 cm)", ""),
    ("ANSI D_55.9_86.4", "ANSI D (55.9x86.4 cm)", ""),
    ("ANSI E_86.4_111.8", "ANSI E (86.4x111.8 cm)", ""),

    ("Arch A_22.9_30.5", "Arch A (22.9x30.5 cm)", ""),
    ("Arch B_30.5_45.7", "Arch B (30.5x45.7 cm)", ""),
    ("Arch C_45.7_61.0", "Arch C (45.7x61.0 cm)", ""),
    ("Arch D_61.0_91.4", "Arch D (61.0x91.4 cm)", ""),
    ("Arch E_91.4_121.9", "Arch E (91.4x121.9 cm)", ""),
    ("Arch E1_76.2_106.7", "Arch E1 (76.2x106.7 cm)", ""),
    ("Arch E2_66.0_96.5", "Arch E2 (66.0x96.5 cm)", ""),
    ("Arch E3_68.6_99.1", "Arch E3 (68.6x99.1 cm)", ""),
    )


def paper_enum_parse(idname):
    tipo, dim_w, dim_h = idname.split("_")
    return tipo, float(dim_w), float(dim_h)


paper_presets_data = {idname: paper_enum_parse(idname)
                      for idname, name, descr in paper_presets}


def update_settings_cb(self, context):
    # annoying workaround for recursive call
    if update_settings_cb.level == False:
        update_settings_cb.level = True
        pixels_from_print(self)
        update_settings_cb.level = False

update_settings_cb.level = False




print2scale_scale_factor_previous = 1
def print2scale_recalculate_camera_focal_length_or_orthographic_scale(self, context):
   
    # annoying workaround for recursive call
    if print2scale_recalculate_camera_focal_length_or_orthographic_scale.level == False:
        print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = True
        print2scale_processInput(self, context)
        print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = False

print2scale_recalculate_camera_focal_length_or_orthographic_scale.level = False



def print2scale_processInput(self, context):
    global print2scale_scale_factor_previous
    
    ps = self
    
    if (print2scale_scale_factor_previous == ps.in_print2scale_scale_factor):
        return {'FINISHED'}
    
    if (ps.in_print2scale_scale_factor < 1):
        #ps.in_print2scale_scale_factor = round(ps.in_print2scale_scale_factor, 1)
        print2scale_scale_factor_previous = ps.in_print2scale_scale_factor
        return {'FINISHED'}
    

    #if the scale factor is changed by an amount less than 1 it has to be either incremented or
    # decremented and NOT rounded as this will result in the old result.
    # This special case is treated for convenience only.
    if ps.in_print2scale_scale_factor > print2scale_scale_factor_previous:
        #then round up:
        ps.in_print2scale_scale_factor = math.ceil(ps.in_print2scale_scale_factor)
        
    elif ps.in_print2scale_scale_factor < print2scale_scale_factor_previous:
       ps.in_print2scale_scale_factor = math.floor(ps.in_print2scale_scale_factor)

    #else: equal! nothing to change!
    
    #store the current value for next time:
    print2scale_scale_factor_previous = ps.in_print2scale_scale_factor




class RenderPrintSertings(PropertyGroup):
    unit_from = EnumProperty(
            name="Set from",
            description="Set from",
            items=(
                ("CM_TO_PIXELS", "CM -> Pixel", "Centermeters to Pixels"),
                ("PIXELS_TO_CM", "Pixel -> CM", "Pixels to Centermeters")
                ),
            default="CM_TO_PIXELS",
            )
    orientation = EnumProperty(
            name="Page Orientation",
            description="Set orientation",
            items=(
                ("Portrait", "Portrait", "Portrait"),
                ("Landscape", "Landscape", "Landscape")
            ),
            default="Portrait",
            update=update_settings_cb,
            )
    preset = EnumProperty(
            name="Select Preset",
            description="Select from preset",
            items=paper_presets,
            default="custom_1_1",
            update=update_settings_cb,
            )
    dpi = IntProperty(
            name="DPI",
            description="Dots per Inch",
            default=300,
            min=72, max=1800,
            update=update_settings_cb,
            )
    width_cm = FloatProperty(
            name="Width",
            description="Width in CM",
            default=5.0,
            min=1.0, max=100000.0,
            update=update_settings_cb,
            )
    height_cm = FloatProperty(
            name="Height",
            description="Height in CM",
            default=3.0,
            min=1.0, max=100000.0,
            update=update_settings_cb,
            )
    width_px = IntProperty(
            name="Pixel Width",
            description="Pixel Width",
            default=900,
            min=4, max=10000,
            update=update_settings_cb,
            )
    height_px = IntProperty(
            name="Pixel Height",
            description="Pixel Height",
            default=600,
            min=4, max=10000,
            update=update_settings_cb,
            )
    #PRINT TO SCALE
    in_print2scale = BoolProperty(
            name="Print to scale"
            ,description="Print to scale by automatically calculate the correct distance of the camera to the object or the center of scene."
            ,default=True
            #,update=print2scale_reset_camera_focal_length_or_orthographic_scale
    )
    #Remapping probably will lead to much confusion. e.g. model 10 -> 1 on the plan means the output will be a model copy 10 times smaller.
    # Many architects will accidentally fill in 1:10 instead because they forget that here the ratio is (model:plan) and not (plan:model) like printed
    # on the plan. So unfortunately this will cost a lot of trees as the prints in that a size will be rendered useless.
    # => SO NOW WE USE SCALE FACTOR ONLY! THAT'S MUCH MORE INTUITIVE AND IS NOTHING ELSE than print ratio but without the confusion.
    #in_print2scale_scale_remap_source_model = IntProperty(
    #        name="Model - Print ratio denominator (Model, Map source)"
    #        ,description="If the model value is greater than the real world value (e.g. 2:1) then the printed output will be scaled down to 1/2 the model size. is e.g. 10 and the real world value 1, then we have a print ratio of 10:1, that is 10 model units print to 1 real world unit. So a 10m model becomes 1m. Thus the printed plan is to scale in a ratio of 1:10 (while the model is in the opposite ratio of 10:1)."
    #        ,default=1
    #        ,min=1
    #        ,max=10000
    #        ,update=print2scale_recalculate_camera_focal_length_or_orthographic_scale
    #)
    #in_print2scale_scale_remap_target_printed = IntProperty(
    
    #NOTE:
    #The print ratio is nothing else than a scale factor. E.g. 1:10 on a plan means the original real measurements are scaled down by factor 10.
    #ATTENTION:
    #Precondition is that the 3D model must be modelled to scale. Only then printing a plan to scale, scaled down or up, gives meaningful dimensions.
    # E.g. if a 1m long wing is modelled with 1mm length in blender instead, then it has to be printed with a 1000:1 for a 1:1 scale on a 1m sheet
    # or 100:1 on a 1/10m sheet, resulting in a factor of 1:10. Unfortunately the program can't know if the model now really is that small (1mm) or
    # not and labels the plan as 100:1 in scale - obviously confusing all engineers and architects involved.
    # Either scaling the model up or changing the unit settings scale can solve this. From experience the first approach can prove difficult
    # as this can lead to strange behaviour of modifiers and any kind of relationsships of objects of the model - often messing up the complete model.
    # The latter - changing the unit settings - is okay, but results in modularity problems if this setting is different in each scene,
    # so when finally importing one model into another scene, a lot of new problems arise. Also problematic are discrepancies in the grid and blender's
    # buildin-measurement functionality (N panel, e.g. edge info) as well as the bullet engine or other features that rely on physically accurate units
    # (and from what reason ever (there are plenty!) don't take the unit scale into account correctly).
    # The loss of modularity is such a big problem that it's good to know that all this trouble can be avoided by simply modelling to scale.
    # (While model accuracy might prove inaccurate if modelling to scale without scaling up the model as the grids resolution is limited! So there is no silverbullet.)

    in_print2scale_scale_factor = FloatProperty(
            name="Print scale factor"
            ,description="Scale big models down (scale factor <1) or tiny models up (scale facot >1). E.g. 10 results in scaling up tenfold, a 1meter model will fill 10m on a giant sheet of papyrus when printed out with this setting. On the other hand 0.1 = 1/10 results in a 1:10 plan being printed."
            ,default=1
            ,min=0.00000001 #If zero is possible, problems will arise due to division by zero!
            ,max=10000
            ,update=print2scale_recalculate_camera_focal_length_or_orthographic_scale
    )

            
def print2scale(ps, context):
        #--------------------------------------------------------
        #print2scale
        #--------------------------------------------------------
        if (ps.in_print2scale):
            if (context.scene.camera is None):
                #create a camera
                bpy.ops.object.add('CAMERA', layers=(True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True))
                ##the added object keeps the short name, while the others are renamed
                #context.scene.selected_object['Camera']
                
            #
            #At this point the scene must have a camera.
            #
        
            ########
            # ADD SCALE FACTOR FOR PRINTING
            ########
            #add a text for the scale factor e.g. 1:10 on the print.
#            bpy.ops.object.text_add(view_align=True, enter_editmode=True)
            
            #print scale factor
            #TODO
            
            #leave editmode to objectmode
#            bpy.ops.object.editmode_toggle()
            
            #both of the following results in the just added text object:
            #getLastObjectInSelection(context)
            #text_object = context.active_object
            
            #make sure nothing is selected
 #           bpy.ops.object.select_all(mode='DESELECT')
            
            #select the camera
#            context.scene.camera.select = True
            
            #make the text object active
#            text_object.select = True
#            context.scene.objects.active = text_object
            
            #add a constraint to the active object with the selected object(s) as target(s)
#            bpy.ops.object.constraint_add_with_targets('TRACK_TO')


            
            #######
            # SET THE CAMERA's ZOOM OR ORTHOGRAPHIC SCALE
            #######
            aspect_ratio = ps.height_cm / ps.width_cm #as it's a ratio converting to meter or not does not matter here!
            print(context.scene.camera.type)
            if (not context.scene.camera.type == 'CAMERA'):
                return {'CANCELLED'}
            
            
            longer_side = ps.height_cm / float(m2cm)
            if (ps.width_cm > ps.height_cm): #if (ps.orientation == 'Landscape'):
                longer_side = ps.width_cm / float(m2cm)

            #print('old ortho scale: ', context.scene.camera.data.ortho_scale)                
            if not context.scene.camera.data.type == 'ORTHO':
                context.scene.camera.data.type = 'ORTHO'
            if context.scene.camera.data.type == 'ORTHO':    #ORTHO, PANO, PERSP
                #blenderartists.org/forum/showthread.php?257556-Render-to-Scale-in-Blender-using-the-Render-to-Print-addon-!
                #They use the magic number 1.3648 - wonder why, its origin needs to be determined.
                #     Orthographic_scale                = 1.3648 x L_format_real x L_virtual / L_real
                # <=> Orthographic_scale * scale_factor = 1.3648 x L_format_real 
                # <=> Orthographic_scale * scale_factor = H_format_real
                #                                                       where L_real = scale factor * L_virtual
                #And as the orthographic scale does not take the Scene.unit_settings scale_length into account (for some reason?):
                # The H_format_real now in the model has to be 'unscaled' too for consistency as the model is scaled with the scale_length setting
                # too while strangely the orthographic is not scaled, so the right hand side will also be divided by the scale to make it equal again:
                # <=> Orthographic_scale * scale_factor = H_format_real / unit_settings_scale_length
                # <=> Orthographic_scale = H_format_real / unit_settings_scale_length / scale_factor
                #
                #print('unit setting: ', context.scene.unit_settings.scale_length, ' longer_side in meters: ', longer_side)
                context.scene.camera.data.ortho_scale = (1.3648 / float(context.scene.unit_settings.scale_length)) / float(ps.in_print2scale_scale_factor)
                
                
            elif (context.scene.camera.data.type == 'PERSP'):
                #TODO: somehow involve the location and the field of view!
                context.scene.camera.data.focal_length = (longer_side / context.scene.unit_settings.scale_length) / ps.in_print2scale_scale_factor

            #else:
                #PANO
                #TODO
                
            #print('new ortho scale: ', context.scene.camera.data.ortho_scale)








    

def pixels_from_print(ps):
    tipo, dim_w, dim_h = paper_presets_data[ps.preset]

    if ps.unit_from == "CM_TO_PIXELS":
        if tipo == "custom":
            dim_w = ps.width_cm
            dim_h = ps.height_cm
            ps.width_cm = dim_w
            ps.height_cm = dim_h
        elif tipo != "custom" and ps.orientation == "Landscape":
            ps.width_cm = dim_h
            ps.height_cm = dim_w
        elif tipo != "custom" and ps.orientation == "Portrait":
            ps.width_cm = dim_w
            ps.height_cm = dim_h

        ps.width_px = math.ceil((ps.width_cm * ps.dpi) / 2.54)
        ps.height_px = math.ceil((ps.height_cm * ps.dpi) / 2.54)
    else:
        if tipo != "custom" and ps.orientation == "Landscape":
            ps.width_cm = dim_h
            ps.height_cm = dim_w
            ps.width_px = math.ceil((ps.width_cm * ps.dpi) / 2.54)
            ps.height_px = math.ceil((ps.height_cm * ps.dpi) / 2.54)
        elif tipo != "custom" and ps.orientation == "Portrait":
            ps.width_cm = dim_w
            ps.height_cm = dim_h
            ps.width_px = math.ceil((ps.width_cm * ps.dpi) / 2.54)
            ps.height_px = math.ceil((ps.height_cm * ps.dpi) / 2.54)

        ps.width_cm = (ps.width_px / ps.dpi) * 2.54
        ps.height_cm = (ps.height_px / ps.dpi) * 2.54


class RENDER_PT_print(Panel):
    bl_label = "Render to Print"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        ps = scene.print_settings


        #PRINT2SCALE
        row00 = layout.row(align=True)
        text = "Print to scale "
        if (ps.in_print2scale_scale_factor < 1):
            num = ps.in_print2scale_scale_factor
            #while str(num).find('.') != -1:
            #denominator = 1
            #while round(num * denominator, 0) != num * denominator:
            #    denominator = denominator * 10
            if (num != 0):
                text = text + ' 1:' + str(round(1 / num, 2))
                
            
        else:
            text = text + str(int(ps.in_print2scale_scale_factor)) + ':1'






            
        row00.prop(ps, "in_print2scale", text=text)
        
        row01 = layout.row(align=True)
        row01.active = ps.in_print2scale
        
        row01.prop(ps, "in_print2scale_scale_factor", text="Scale factor")
        #PRINT2SCALE -END


        row = layout.row(align=True)
        row1 = layout.row(align=True)
        row2 = layout.row(align=True)
        row3 = layout.row(align=True)
        row4 = layout.row(align=True)
        row5 = layout.row(align=True)
        row6 = layout.row(align=True)
        row7 = layout.row(align=True)
        col = layout.column(align=True)

        row.prop(ps, "unit_from")
        row1.prop(ps, "orientation")
        row2.prop(ps, "preset")

        col.separator()
        row3.prop(ps, "width_cm")
        row3.separator()
        row3.prop(ps, "height_cm")
        col.separator()
        row4.prop(ps, "dpi")
        col.separator()
        row5.prop(ps, "width_px")
        row5.separator()
        row5.prop(ps, "height_px")

        col.separator()
        row6.label("Inch Width: %.2f" % (ps.width_cm / 2.54))
        row6.label("Inch Height: %.2f" % (ps.height_cm / 2.54))
        col.separator()

        row7.operator("render.apply_size", icon="RENDER_STILL")

        #  this if else deals with hiding UI elements when logic demands it.
        tipo = paper_presets_data[ps.preset][0]

        if tipo != "custom":
            row.active = False
            row.enabled = False

        if ps.unit_from == "CM_TO_PIXELS":
            row5.active = False
            row5.enabled = False

            if tipo == "custom":
                row3.active = True
                row3.enabled = True
                row1.active = False
                row1.enabled = False
            elif tipo != "custom" and ps.orientation == "Landscape":
                row3.active = False
                row3.enabled = False
                row1.active = True
                row1.enabled = True
            elif tipo != "custom" and ps.orientation == "Portrait":
                row3.active = False
                row3.enabled = False
                row1.active = True
                row1.enabled = True
        else:
            row3.active = False
            row3.enabled = False

            if tipo == "custom":
                row1.active = False
                row1.enabled = False
            elif tipo != "custom" and ps.orientation == "Landscape":
                row1.active = True
                row1.enabled = True
                row5.active = False
                row5.enabled = False
            elif tipo != "custom" and ps.orientation == "Portrait":
                row1.active = True
                row1.enabled = True
                row5.active = False
                row5.enabled = False


m2cm = 100

class RENDER_OT_apply_size(Operator):
    bl_idname = "render.apply_size"
    bl_label = "Apply Print to Render"
    bl_description = "Set the render dimension"

    def execute(self, context):

        scene = context.scene
        ps = scene.print_settings

        pixels_from_print(ps)

        render = scene.render
        render.resolution_x = ps.width_px
        render.resolution_y = ps.height_px
        

        print2scale(ps, context)




        return {'FINISHED'}
    
    
    
    
    
    
def getLastObjectInSelection(context):
    return context.scene.selected_objects[len(context.scene.selected_objects) - 1]




def register():
    bpy.utils.register_class(RENDER_OT_apply_size)
    bpy.utils.register_class(RENDER_PT_print)
    bpy.utils.register_class(RenderPrintSertings)

    Scene.print_settings = PointerProperty(type=RenderPrintSertings)


def unregister():
    bpy.utils.unregister_class(RENDER_OT_apply_size)
    bpy.utils.unregister_class(RENDER_PT_print)
    bpy.utils.unregister_class(RenderPrintSertings)
    del Scene.print_settings


if __name__ == "__main__":
    register()

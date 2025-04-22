#!/usr/bin/python3
import os
import math
from GCodeLib import gcode_lib

# ------------------------------------------------------------------------------
                                                               # things to drill
show_bounding_box = True
drill_fixing_holes = True
drill_power_supply_hole = True
    
# ------------------------------------------------------------------------------
                                                           # drilling parameters
board_thickness = 6
board_drill_depth = board_thickness + 3
drill_diameter = 4
fast_displacement_speed = 1000
drill_displacement_speed = 250

machining_parameters = {
    'displacement_height'      : 10,
    'drill_depth'              : board_drill_depth,
    'pass_depth'               : 1,
    'drill_diameter'           : drill_diameter,
    'fast_displacement_speed'  : fast_displacement_speed,
    'drill_displacement_speed' : drill_displacement_speed,
    'drill_bore_speed'         : 100
}

# ------------------------------------------------------------------------------
                                                                      # geometry
box_length = 297
box_width  = 210
box_height  = 80

board_length = box_length
board_width  = box_height - 2*board_thickness

fixing_holes_x_offset = board_thickness/2
fixing_holes_y_offset = 16
fixing_holes_length = board_length - 2*fixing_holes_x_offset
fixing_holes_width = board_width - 2*fixing_holes_y_offset

supply_hole_x_offset = 23
supply_hole_y_offset = 4
supply_hole_width = 28
supply_hole_length = 60

# ------------------------------------------------------------------------------
                                                                     # file spec
(g_code_file_path, g_code_file_name) = os.path.split(__file__)
g_code_file_path = g_code_file_path.rstrip('./')
design_name = g_code_file_name.replace('.py', '')
g_code_file_name = g_code_file_path + os.sep + design_name + '.gcode'

# ------------------------------------------------------------------------------
                                                                       # display
INDENT = 2 * ' '

# ==============================================================================
                                                                   # main script
print('Building g-codes for the A4 box top plate')

# ------------------------------------------------------------------------------
                                                           # write g-code header
print(INDENT + "Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))

comment = "A4 top plate"
g_code_file.write(";\n; %s\n" % comment)
print(INDENT + comment)

# ------------------------------------------------------------------------------
                                                                   # board shape
if show_bounding_box :
    comment = "shape"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n;\n" % comment)
    g_code_file.write(gcode_lib.rectangle_gcode(
        board_length, board_width, fast_displacement_speed
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                  # fixing holes
if drill_fixing_holes :
    comment = "fixing holes"
    print(2*INDENT + comment)
                                                                       # 4 holes
    g_code_file.write(gcode_lib.build_hole_set(
        gcode_lib.build_retangle(
            fixing_holes_x_offset, fixing_holes_y_offset,
            fixing_holes_length, fixing_holes_width
        ),
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                             # power supply hole
if drill_power_supply_hole :
    comment = "power supply hole"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n;\n" % comment)
                                                           # top clearance holes
    comment = "top clearances"
    print(3*INDENT + comment)
    g_code_file.write(gcode_lib.build_hole_set(
        [[
            board_length - supply_hole_x_offset - supply_hole_width,
            board_width - supply_hole_y_offset - drill_diameter/2
        ],[
            board_length - supply_hole_x_offset,
            board_width - supply_hole_y_offset - drill_diameter/2
        ]],
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                   # outlet hole
    comment = "outlet"
    print(3*INDENT + comment)
    g_code_file.write(gcode_lib.build_drawing_element(
        gcode_lib.rectangle_gcode(
            supply_hole_width - drill_diameter,
            supply_hole_length - drill_diameter,
            drill_displacement_speed
        ),
        -supply_hole_width + drill_diameter/2,
        -supply_hole_length + drill_diameter,
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()

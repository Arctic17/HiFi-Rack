#!/usr/bin/python3
import os
import math
from GCodeLib import gcode_lib
    
    
# ------------------------------------------------------------------------------
                                                               # things to drill
show_board           = True
drill_fixing_holes   = True
drill_stacking_holes = True
drill_RPi_holes      = True
drill_supply_holes   = True

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

board_length   = box_length
board_width    = box_width - board_thickness

fixing_holes_x_offset = board_thickness/2
fixing_holes_y_offset = 19
fixing_holes_length = board_length - 2*fixing_holes_x_offset
fixing_holes_width = board_width - 2*fixing_holes_y_offset

stacking_holes_x_offset = 28.5
stacking_holes_y_offset = 16
stacking_holes_length = board_length - 2*stacking_holes_x_offset
stacking_holes_width = board_width - 2*stacking_holes_y_offset

rpi_board_length = 49.25
rpi_board_width = 58.25
rpi_board_x_offset = 16
rpi_board_y_offset = board_width - rpi_board_width - 12

supply_board_length = 55
supply_board_x_offset = 244
supply_board_y_offset = 44

# ------------------------------------------------------------------------------
                                                           # input polygons spec
current_dir = os.path.dirname(os.path.abspath(__file__))
fablab_logo_polygon1_name = 'gear'
fablab_logo_polygon2_name = 'star'
polygon_file_name = 'case.svg'
polygon_file_name = current_dir + os.sep + polygon_file_name

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
print('Building g-codes for the switch back plate')

# ------------------------------------------------------------------------------
                                                           # write g-code header
print(INDENT + "Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))

# ------------------------------------------------------------------------------
                                                                         # board
comment = "back plate"
g_code_file.write(";\n; %s\n" % comment)
print(INDENT + comment)

# ==============================================================================
                                                                   # board shape
if show_board :
    comment = "shape"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n;\n" % comment)
    g_code_file.write(gcode_lib.move_fast(
        0, 0, 0, fast_displacement_speed
    ))
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
    g_code_file.write(";\n; %s\n" % comment)
                                                                      # hole set
    fixing_holes = gcode_lib.build_retangle(
        fixing_holes_x_offset, fixing_holes_y_offset,
        fixing_holes_length, fixing_holes_width
    )
                                                                  # holes g-code
    g_code_file.write(gcode_lib.build_hole_set(
        fixing_holes,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                # stacking holes
if drill_stacking_holes :
    comment = "stacking holes"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n" % comment)
                                                                      # hole set
    stacking_holes = gcode_lib.build_retangle(
        stacking_holes_x_offset, stacking_holes_y_offset,
        stacking_holes_length, stacking_holes_width
    )
                                                                  # holes g-code
    g_code_file.write(gcode_lib.build_hole_set(
        stacking_holes,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                              # RPi fixing holes
if drill_RPi_holes :
    comment = "RPi fixing holes"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n" % comment)
                                                                      # hole set
    fixing_holes = gcode_lib.build_retangle(
        rpi_board_x_offset, rpi_board_y_offset,
        rpi_board_length, rpi_board_width
    )
                                                                  # holes g-code
    g_code_file.write(gcode_lib.build_hole_set(
        fixing_holes,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                     # power supply fixing holes
if drill_supply_holes :
    comment = "RPi fixing holes"
    print(2*INDENT + comment)
    g_code_file.write(";\n; %s\n" % comment)
                                                                      # hole set
    fixing_holes = [
        [supply_board_x_offset, supply_board_y_offset],
        [supply_board_x_offset, supply_board_y_offset + supply_board_length]
    ]
                                                                  # holes g-code
    g_code_file.write(gcode_lib.build_hole_set(
        fixing_holes,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ==============================================================================
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()

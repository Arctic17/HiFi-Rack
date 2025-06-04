#!/usr/bin/python3
import os
import math
from GCodeLib import gcode_lib

# ------------------------------------------------------------------------------
                                                               # things to drill
show_board = True
drill_slits = True
cut_holder_slits = True

cut_left_holder_slits = True
cut_right_holder_slits = True
cut_bottom_holder_slits = True
cut_top_holder_slits = True

# ------------------------------------------------------------------------------
                                                           # drilling parameters
board_thickness = 6
board_drill_depth = board_thickness + 2
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
box_length = 210
box_width  = 148
box_height  = 80

board_length = box_width - 2*board_thickness
board_width = box_height - 2*board_thickness

slits_x_offset = 12
slits_y_offset = 10
slits_length = 35
slits_width = machining_parameters['drill_diameter']
slits_spacing = 2*slits_width
slit_nb = 15

screw_slits_x_offset = 16
screw_slits_y_offset = 16
screw_slits_width = 4.5
screw_slits_end_width = screw_slits_width + 2
screw_slits_length = 6

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
print('Building g-codes for the roomAmp side plates')

# ------------------------------------------------------------------------------
                                                                 # write to file
print("Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))

# ------------------------------------------------------------------------------
                                                                   # board shape
if show_board :
    comment = "board shape"
    print(INDENT + comment)
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
                                                             # ventilation slits
if drill_slits :
    comment = 'ventilation slits'
    print(INDENT + comment)
    g_code_file.write(gcode_lib.build_slit_set(
		slits_x_offset, slits_y_offset + drill_diameter/2,
		0, slits_length - drill_diameter, slits_spacing, 0, slit_nb,
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                           # screws fixing slits
if cut_holder_slits :
    drill_diamater = machining_parameters['drill_diameter']
    drill_speed = machining_parameters['drill_displacement_speed']
    left_side_polygons = [
        [0                 , -screw_slits_width/2     + drill_diamater/2],
        [screw_slits_length, -screw_slits_width/2     + drill_diamater/2],
        [screw_slits_length, -screw_slits_end_width/2 + drill_diamater/2],
        [screw_slits_length,  screw_slits_end_width/2 - drill_diamater/2],
        [screw_slits_length,  screw_slits_width/2     - drill_diamater/2],
        [0                 ,  screw_slits_width/2     - drill_diamater/2],
    ]
    right_side_polygons = gcode_lib.flip_horizontal(left_side_polygons)
    top_side_polygons = gcode_lib.rotate_polygon(left_side_polygons, -math.pi/2)
    bottom_side_polygons = gcode_lib.rotate_polygon(
        left_side_polygons, math.pi/2
    )
    deeper_machining_parameters = machining_parameters.copy()
    deeper_machining_parameters['drill_depth'] = board_drill_depth + 1
                                                                # left side slit 
    if cut_left_holder_slits :
                                                         # left side bottom slit
        comment = 'left side bottom screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(left_side_polygons, speed=drill_speed),
            0, screw_slits_y_offset,
            deeper_machining_parameters, comment
        ))
                                                            # left side top slit
        comment = 'left side top screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(left_side_polygons, speed=drill_speed),
            0, board_width - 2*screw_slits_y_offset,
            deeper_machining_parameters, comment
        ))
                                                                # top side slits
    if cut_top_holder_slits :
        g_code_file.write(gcode_lib.set_absolute_coordinates())
        g_code_file.write(gcode_lib.move_fast(
            screw_slits_x_offset, board_width
        ))
        g_code_file.write(gcode_lib.set_relative_coordinates())
                                                            # top side left slit
        comment = 'top side left screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(top_side_polygons, speed=drill_speed),
            0, 0,
            deeper_machining_parameters, comment
        ))
                                                           # top side right slit
        comment = 'top side right screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(top_side_polygons, speed=drill_speed),
            board_length - 2*screw_slits_x_offset, 0,
            deeper_machining_parameters, comment
        ))
                                                              # right side slits
    if cut_right_holder_slits :
        g_code_file.write(gcode_lib.set_absolute_coordinates())
        g_code_file.write(gcode_lib.move_fast(
            board_length, board_width - screw_slits_y_offset
        ))
        g_code_file.write(gcode_lib.set_relative_coordinates())
                                                           # right side top slit
        comment = 'right side top screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(right_side_polygons, speed=drill_speed),
            0, 0,
            deeper_machining_parameters, comment
        ))
                                                        # right side bottom slit
        comment = 'right side bottom screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(right_side_polygons, speed=drill_speed),
            0, -board_width + 2*screw_slits_y_offset,
            deeper_machining_parameters, comment
        ))
                                                             # bottom side slits
    if cut_bottom_holder_slits :
        g_code_file.write(gcode_lib.set_absolute_coordinates())
        g_code_file.write(gcode_lib.move_fast(
            board_length - screw_slits_x_offset, 0, absolute=True
        ))
        g_code_file.write(gcode_lib.set_relative_coordinates())
                                                       # bottom side right slit
        comment = 'bottom side right screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(bottom_side_polygons, speed=drill_speed),
            0, 0,
            deeper_machining_parameters, comment
        ))
                                                          # bottom side left slit
        comment = 'bottom side left screw fixing slit'
        print(INDENT + comment)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(bottom_side_polygons, speed=drill_speed),
            -board_length + 2*screw_slits_x_offset, 0,
            deeper_machining_parameters, comment
        ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------

g_code_file.close()

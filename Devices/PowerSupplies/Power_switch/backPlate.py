#!/usr/bin/python3
import os
import math
from GCodeLib import gcode_lib
    
# ------------------------------------------------------------------------------
                                                               # things to drill
show_board          = True
drill_fixing_holes  = True
drill_power_plug    = True
drill_RPi_slit      = True
drill_power_outlets = True
drill_logo          = True
    
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
board_width    = box_height - 2*board_thickness

fixing_holes_x_offset = board_thickness/2
fixing_holes_y_offset = 16
fixing_holes_length = box_length - 2*fixing_holes_x_offset
fixing_holes_width = box_height - 2*board_thickness \
    - 2*fixing_holes_y_offset

power_supply_slit_length = 28
power_supply_slit_width = 58.5
power_supply_slit_x_offset = 19
power_supply_slit_y_offset = 4

rpi_slit_length = 58
rpi_slit_width = 18.5
rpi_slit_x_offset = board_length - rpi_slit_length - 11.5
rpi_slit_y_offset = board_width - rpi_slit_width - 10

power_outlets_nb = 3
power_outlets_spacing = 53
power_outlets_hole_width = 32
power_outlets_hole_height = 26
power_outlets_45 = 7
power_outlets_x_offset = 72
power_outlets_y_offset = board_width - 47
power_outlets_holes_y_offset = 13
power_outlets_holes_spacing = 40

back_logo_x_offset = 240
back_logo_y_offset = 8
back_logo_scale = 1/2.9

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
comment = 'back plate'
g_code_file.write(";\n; %s\n" % comment)
print(INDENT + comment)

# ------------------------------------------------------------------------------
                                                                   # board shape
if show_board :
    comment = 'shape'
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
    comment = 'fixing holes'
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
                                                             # power supply slit
if drill_power_plug :
                                                       # power supply slit holes
    comment = 'power supply slit holes'
    power_supply_holes = [
        [
            power_supply_slit_x_offset,
            power_supply_slit_y_offset + power_supply_slit_width
        ],
        [
            power_supply_slit_x_offset + power_supply_slit_length,
            power_supply_slit_y_offset + power_supply_slit_width
        ]
    ]
    g_code_file.write(gcode_lib.build_hole_set(
        power_supply_holes,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())
                                                             # power supply slit
    comment = 'power supply slit'
    print(2*INDENT + comment)
    g_code_file.write(gcode_lib.build_drawing_element(
        gcode_lib.rectangle_gcode(
            power_supply_slit_length - drill_diameter,
            power_supply_slit_width - drill_diameter,
            drill_displacement_speed
        ),
        power_supply_slit_x_offset + drill_diameter/2,
        power_supply_slit_y_offset + drill_diameter/2,
        machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                           # back board RPi slit
if drill_RPi_slit :
                                                                      # RPi slit
    comment = 'RPi slit'
    print(2*INDENT + comment)
    g_code_file.write(gcode_lib.build_drawing_element(
        gcode_lib.rectangle_gcode(
            rpi_slit_length - drill_diameter,
            rpi_slit_width - drill_diameter,
            drill_displacement_speed
        ),
        rpi_slit_x_offset + drill_diameter/2,
        rpi_slit_y_offset + drill_diameter/2,
        machining_parameters,
        "\n; %s\n;" % comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                 # power outlets
if drill_power_outlets :
    comment = 'power outlets'
    print(2*INDENT + comment)

    g_code_file.write(gcode_lib.move_fast(
        power_outlets_x_offset,
        power_outlets_y_offset + power_outlets_holes_y_offset,
        0
    ))
    power_outlets_hole_to_body = \
        (power_outlets_holes_spacing - power_outlets_hole_width)/2
    body_width_internal = power_outlets_hole_width - drill_diameter
    body_height_internal = power_outlets_hole_height - drill_diameter
    power_outlet_shape = [
        [0, 0],
        [-body_width_internal, 0],
        [-body_width_internal, body_height_internal - power_outlets_45],
        [-body_width_internal + power_outlets_45, body_height_internal],
        [-power_outlets_45, body_height_internal],
        [0, body_height_internal - power_outlets_45]
    ]

    for index in range(power_outlets_nb):
                                                                  # fixing holes
        comment = "outlet %d holes" % index
        print(3*INDENT + comment)
        g_code_file.write(gcode_lib.build_hole_set(
            [[0, 0]],
            machining_parameters,
            comment
        ))
        g_code_file.write(gcode_lib.move_fast(
            power_outlets_holes_spacing, 0, 0
        ))
        g_code_file.write(gcode_lib.build_hole_set(
            [[0, 0]],
            machining_parameters,
            comment
        ))
                                                                   # outlet hole
        comment = "outlet %d body" % index
        print(3*INDENT + comment)
        g_code_file.write(gcode_lib.move_fast(
            -power_outlets_hole_to_body - drill_diameter/2,
            -power_outlets_holes_y_offset + drill_diameter/2,
            0
        ))
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.polygon_gcode(
                power_outlet_shape, True, drill_displacement_speed
            ),
            0, 0, machining_parameters, comment
        ))
        if index < power_outlets_nb - 1 :
            g_code_file.write(gcode_lib.move_fast(
                power_outlets_spacing - power_outlets_holes_spacing +
                    power_outlets_hole_to_body + drill_diameter/2,
                power_outlets_holes_y_offset - drill_diameter/2,
                0
            ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                               # back board logo
if drill_logo :
    print(INDENT + 'reading from %s' % polygon_file_name)

    comment = "polygon \"%s\"" % fablab_logo_polygon1_name
    print(INDENT + comment)
    polygon = gcode_lib.flip_vertical(gcode_lib.scale_polygon(
        gcode_lib.import_polygon(polygon_file_name, fablab_logo_polygon1_name),
        back_logo_scale
    ))
    (x_min, y_min, x_max, y_max) = gcode_lib.min_max(polygon)
    polygon = gcode_lib.offset_polygon(polygon, -x_min, -y_min)
    (x_offset, y_offset, polygon) = gcode_lib.extract_offset(polygon)
    x_offset = x_offset + back_logo_x_offset
    y_offset = y_offset + back_logo_y_offset
    logo_drill_depth = machining_parameters['pass_depth']
    logo_machining_parameters = machining_parameters
    logo_machining_parameters['drill_depth'] = logo_drill_depth
    g_code_file.write(gcode_lib.build_drawing_element(
        gcode_lib.polygon_gcode(polygon), x_offset, y_offset,
        logo_machining_parameters,
        comment
    ))
                                                                # back to origin
    g_code_file.write(gcode_lib.move_back_to_origin())


# ==============================================================================
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()

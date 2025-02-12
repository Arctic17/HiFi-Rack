;
; initialization
;
G21 (set units to millimeters)
G92 Z0 (set Z position to zero)
G91 (set to relative positioning)
; move up to displacement height, set steady pace
G1 Z10.000 f250
; move to start position, set fast pace
G92 X0 Y0 (set X,Y position to zero)
;
; A4 top plate
;
; shape
;
G1 X297.000 f1000
G1 Y204.000 f1000
G1 X-297.000 f1000
G1 Y-204.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)
; 
; fixing holes
;
T4 (drill diameter for the following operations)
G0 X3.000 Y19.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X291.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 Y160.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X-291.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)
; 
; fixing holes
;
T4 (drill diameter for the following operations)
G0 X28.500 Y16.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X240.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 Y166.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X-240.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)


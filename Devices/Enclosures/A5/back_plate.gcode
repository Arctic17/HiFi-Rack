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
G1 X210.000 f1000
G1 Y68.000 f1000
G1 X-210.000 f1000
G1 Y-68.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)
; 
; fixing holes
;
T4 (drill diameter for the following operations)
G0 X3.000 Y16.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X204.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 Y36.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X-204.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)
;
; power supply hole
;
; 
; top clearances
;
T4 (drill diameter for the following operations)
G0 X159.000 Y62.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
G0 X28.000 f1000
G1 Z-19.000 f100
G0 Z19.000 f1000
; 
; outlet
;
T4 (drill diameter for the following operations)
G0 X-26.000 Y-56.000 f1000
G1 Z-10.000 f100
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G1 Z-1.000 f100
G1 X24.000 f250
G1 Y56.000 f250
G1 X-24.000 f250
G1 Y-56.000 f250
G0 Z19.000 f1000
; move back to origin
G90 (set to absolute positioning)
G0 X0 Y0
G91 (set to relative positioning)


#!/usr/bin/bash

# ------------------------------------------------------------------------------
                                                                     # constants
plateList=('bottom_plate' 'top_plate' 'side_plate' 'back_plate' 'front_plate')
platesX=(297 297 198 297 297)
platesY=(204 204 68 68 80)
platesZ=6

workDirectory=$(dirname "$0")
gCodeDirectory="$workDirectory/GCodeLib"

verbose=false
#verbose=true
INDENT='  '

# ------------------------------------------------------------------------------
                                                                # loop on plates
for index in ${!plateList[@]} ; do
  plate=${plateList[$index]}
  scriptFile="$workDirectory/$plate.py"
  gcodeFile="$workDirectory/$plate.gcode"
  svgFile="$workDirectory/$plate.svg"
  svgArguments="-x ${platesX[$index]} -y ${platesY[$index]} -t $platesZ"
  if [ $verbose = true ] ; then
    echo $plate
  fi
                                                                      # generate
  if [ ! -f "$gcodeFile" ] ; then
    if [ $verbose = true ] ; then
      echo -e "${INDENT}generating g-code\n"
    fi
    $scriptFile || exit 1
    if [ $verbose = true ] ; then
      echo
    fi
                                                                        # update
  elif [ "$scriptFile" -nt "$gcodeFile" ] ; then
    if [ "$verbose" = true ] ; then
      echo "${INDENT}updating g-code"
    fi
    $scriptFile || exit 1
    if [ $verbose = true ] ; then
      echo
    fi
  fi
                                                                  # generate SVG
  if [ ! -f $svgFile ] ; then
    if [ $verbose = true ] ; then
      echo -e "${INDENT}generating svg\n"
    fi
    $gCodeDirectory/gcodeToSvg.py $svgArguments $gcodeFile || exit 1
    if [ $verbose = true ] ; then
      echo
    fi
                                                                    # update SVG
  elif [ "$gcodeFile" -nt "$svgFile" ] ; then
    if [ $verbose = true ] ; then
      echo -e "${INDENT}updating svg"
    fi
    $gCodeDirectory/gcodeToSvg.py $svgArguments $gcodeFile || exit 1
    windowId=`xdotool search --name $plate`
    #echo $windowId
    if [ -n "$windowId" ] ; then
      windowId=`echo $windowId | cut -d ' ' -f 1`
      xdotool windowfocus $windowId
      xdotool key ctrl+alt+r
      sleep 1
      xdotool key Tab
      xdotool key Return
    fi
    if [ $verbose = true ] ; then
      echo
    fi
  fi
done

# ------------------------------------------------------------------------------
# For Inkscape, Edit > Preferences... > Interface > Keyboard Shortcuts > File
# import /usr/share/inkscape/keys/default.xml, add Ctrl+Alt+R for FileRevert
# and export
# this creates .config/inkscape/keys/default.xml

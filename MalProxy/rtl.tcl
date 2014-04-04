## Cadence Encounter SOC RTL compiler script
## Groundworks Technologies 2014

##rtl.tcl file adapted from http://ece.colorado.edu/~ecen5007/cadence/
##this tells the compiler where to look for the libraries

#set_attribute lib_search_path /home/alfred/techlibs/osu27/cadence/lib/tsmc018/signalstorm
set_attribute lib_search_path /home/alfred/techlibs/Nangate-OpenCell-45nm/NangateOpenCellLibrary_PDKv1_3_v2010_12/Front_End/Liberty/CCS
## This defines the libraries to use

#set_attribute library {osu018_stdcells.lib}
set_attribute library {NangateOpenCellLibrary_typical_ccs.lib}

set_attribute gui_sv_threshold 50000
##This must point to your VHDL/verilog file
##it is recommended that you put your VHDL/verilog in a folder called HDL in
##the directory that you are running RC out of

## CHANGE THIS LINE to your VHDL/verilog file name, if you follow the tutorial
## you do not need to change anything

##read_hdl ../HDL/accu.v
read_hdl cortexm0ds_logic.v
read_hdl -v2001 CORTEXM0DS.v 

## This buils the general block
elaborate

##this allows you to define a clock and the maximum allowable delays
## READ MORE ABOUT THIS SO THAT YOU CAN PROPERLY CREATE A TIMING FILE
#set clock [define_clock -period 300 -name clk]
#external delay -input 300 -edge rise clk
#external delay -output 2000 -edge rise p1

##This synthesizes your code
synthesize -to_mapped

## This writes all your files
## change the tst to the name of your top level verilog
## CHANGE THIS LINE: CHANGE THE "accu" PART REMEMBER THIS
## FILENAME YOU WILL NEED IT WHEN SETTING UP THE PLACE & ROUTE
write -mapped > CORTEXM0DS_synth.v

## THESE FILES ARE NOT REQUIRED, THE SDC FILE IS A TIMING FILE
write_script > script

##write sdc > tst.sdc

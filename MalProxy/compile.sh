cd ./ChibiOS_2.6.1/demos/ARMCM0-LPC1114-LPCXPRESSO
source arm.sh
make
cd ../../../
cp ./ChibiOS_2.6.1/demos/ARMCM0-LPC1114-LPCXPRESSO/build/ch.bin ram.bin
iverilog CORTEXM0DS.v cortexm0ds_logic.v armtb.v

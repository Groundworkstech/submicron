Submicron
=========

Repository of resources and documentation to build and experiment with deep-submicron VLSI backdoors and other malicious hardware modifications.

This code was used for the talk "Deep-Submicron Backdoors" in Syscan 2014

Structure
---------

* docs: Latest version of slides and articles
* MalProxy: Contains sources of the MalProxy backdoor
* MalProxy/software: ChibiOS demo example
* MalProxy/hardware: Patch against ARM Cortex M0 designstart
* RiFt: Contains modulator and RF exfiltrator patch against the Zet 16-bit x86 CPU version 1.2.0 (zet.aluzina.org)
* NEC : Contains simulation files for the Numerical Electromagnetic Codes package. Tested with xnec2c 2.3-beta.
* GDS : Contains technology files needed to display correct NANGate 45nm and TSMC 180nm metal layers on GDS3D package.

See a visualization of the Backdoor here: http://www.youtube.com/watch?v=yHYMIvmMrH0

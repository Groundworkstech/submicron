#!/usr/bin/env python
#
# Copyright (c) 2014 Groundworks Technologies
#
# This code is part of the Deep-Submicron backdoor talk
#
# Demodulator for 700 MHz exfiltrated ASK signal using any RTL-SDR dongle
#

from multiprocessing import Process, Queue
import sys

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

SAMPLE_RATE = 1e6
FREQ = 699.5e6


def AsyncWelchProcess( queue ):

    import numpy as np
    from scipy import signal

    one_pwr_threshold  = 50
    one_ct_threshold = 8
    one_ct = 0

    zero_ct_threshold = 8
    zero_ct = 0

    state=0

    last_ = 0

    bit=0
    demodScanCode=0
    bitCount=0
    totalCount=0
    demodCount=0
    BITSIZE=12
    AVGBITSIZE=0
    FINALBITSIZE=0
    FINALBITSIZE2=0
    BITSIZEMIN=5 #smallest bit
    BITSIZEMAX=10 #MAX bit
    bitValue=0
    scancode=0

    str=""
    bitstr=""
    powerValues=[]
    while True:
   	try:
	        samples = queue.get()

	        f, p  = signal.welch( samples, fs= SAMPLE_RATE / 1e6,nperseg=512,return_onesided=True)


		slots=16
		barsPerSlots=len(p)/slots
		psum=[0]*slots
		for i in range(slots):
			psum[i]=0
			for q in range(barsPerSlots):
				psum[i]+=p[i*barsPerSlots+q]
		powerValues.append((psum[7],psum[6])) # append powers
		maxColumns=120
		powerValues=powerValues[-maxColumns:] # get last maxColumns
		row=""
		for r in range(10,0,-1):
			row+="\n"
			for i in range(maxColumns):
				if len(powerValues)>i:
					if (powerValues[i][0]>(powerValues[i][1]*r*10)):
						row+="*"
					else:	row+=" "
		row+="\n"
					
		sys.stdout.write("\x1b[2J\x1b[H") # clear screen
		sys.stdout.write(row)
			

		#if (psum[3]>psum[2]*3): # detection 8 groups
		if (psum[7]>psum[6]*50): # detection 16 groups
			bit=1
		else:	bit=0

		key_lookup = scancodes.get(scancode) or u'UNKNOWN:{}'.format(scancode)  # Lookup or return UNKNOWN:XX
	        key_str = bcolors.WARNING+ u'You Pressed the {} key!'.format(key_lookup)  +bcolors.ENDC

		print "Bitcount: %d state: %d BITSIZE: %f BITSIZE2: %d (%s) Scancode: %d " % (bitCount,state,FINALBITSIZE,FINALBITSIZE2,bitstr,scancode)
		print key_str
		
		totalCount+=1 # received bit counter
		if (state==0): # wating for start bits
			if bit==1:
				state=1
				demodScanCode=[]
				demodCount=1
				if (bitCount==0): totalCount=0
		elif (state==1): 
			if (bitCount==0): totalCount=0
			if bit==0:
				BITSIZE=demodCount
				demodCount=0
				if (BITSIZE<BITSIZEMIN): # too small
					continue
				if (BITSIZE>BITSIZEMAX): # too big a bit
					bitCount=0
					AVGBITSIZE=0
					state=0
				else:
					bitCount+=1 #Only increment if valid bit received
					AVGBITSIZE+=BITSIZE
					if (bitCount<3):
						state=0 # still reading header
					else:	
						FINALBITSIZE=AVGBITSIZE/4.0
						FINALBITSIZE2=totalCount/6
						AVGBITSIZE=0
						bitCount=0
						demodCount=0
						bitstr=""
						bitValue=0
						scancode=0
						state=2 # header finished
			else: demodCount+=1
		elif (state==2): #additional zero
			demodCount+=1
			if (demodCount>=FINALBITSIZE*2.5):
				demodCount=0
				state=3
		elif (state==3):
			demodCount+=1
			if (demodCount<=FINALBITSIZE):
				bitValue+=bit+0.001
			else:	
				demodCount=0
				bitValue/=FINALBITSIZE
				if (bitValue>0.5): # detectado 1
					bitstr+="0"
				else:	
					bitstr+="1"
					if (bitCount<6):
						scancode+=(1<<bitCount)
				bitCount+=1
				bitValue=0
				if (bitCount>10):
					bitCount=0
					state=0 # fin demod
	except: exit(0)
	

		
if __name__ == "__main__":
    q = Queue()
    p = Process(target=AsyncWelchProcess, args=(q,) )
    p.start()

    def on_sample(buf, queue):
        queue.put( list(buf) )
    from rtlsdr import RtlSdr

    sdr = RtlSdr()
    # configure device
    sdr.sample_rate = SAMPLE_RATE # sample rate
    sdr.center_freq = FREQ
    sdr.gain = 'auto'
    sdr.read_samples_async( on_sample, 2048, context = q)



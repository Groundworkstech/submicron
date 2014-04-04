/*
    ChibiOS/RT - Copyright (C) 2006-2013 Giovanni Di Sirio

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    MalProxy Demo by Groundworks Technologies    
*/

#include "ch.h"
#include "hal.h"
#include "test.h"
#include <string.h>
char *ttyout = (char *)0x40000000;

void putchar(const char c) {
    *ttyout=c;
}

int puts(const char *s)
{
    while(*s)
    {
      putchar(*s++); 
    }
    putchar('\n');
    return 0;
}

/*
 * Red LED blinker thread, times are in milliseconds.
 */
static WORKING_AREA(waThread1, 128);
static msg_t Thread1(void *arg) {

  (void)arg;
  chRegSetThreadName("blinker1");
  while (TRUE) {
    puts("This is Thread 1");
    chSchDoRescheduleBehind();
  }
 return 0;
}

/*
 * RGB LED blinker thread, times are in milliseconds.
 */
static WORKING_AREA(waThread2, 128);
static msg_t Thread2(void *arg) {

  (void)arg;
  chRegSetThreadName("blinker2");
  while (TRUE) {
    puts("This is Thread 2");
   chSchDoRescheduleBehind();
    }
 return 0;
}


/*
 * Application entry point.
 */
int main(void) {
  /*
   * System initializations.
   * - HAL initialization, this also initializes the configured device drivers
   *   and performs the board-specific initializations.
   * - Kernel initialization, the main() function becomes a thread and the
   *   RTOS is active.
   */
  halInit();
  chSysInit();

  /*
   * Creates the blinker threads.
   */
  chThdCreateStatic(waThread1, sizeof(waThread1), NORMALPRIO, Thread1, NULL);
  chThdCreateStatic(waThread2, sizeof(waThread2), NORMALPRIO, Thread2, NULL);

  /*
   * MalProxy activation memcpy() example:
   * 
   */
  char buf[40];
  char *str="\x78\x56\x34\x12WABCK---C---A---H---\x00---\x00---\x0a---\x1D---";
  while (TRUE) {
    puts("Main thread: hello world");
    memcpy(buf,str,40);
    chSchDoRescheduleBehind();
  }
}

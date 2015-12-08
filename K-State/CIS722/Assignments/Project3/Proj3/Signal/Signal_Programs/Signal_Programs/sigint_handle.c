#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

int sig_captured = 0;

void catch_ctrl_c(int signo)
{
  sig_captured = 1;
  printf("In Handler : I captured ^c (signal number: %d)\n", signo);
}

void main(void) {

  struct sigaction act;
  act.sa_handler = catch_ctrl_c;
  sigemptyset(&act.sa_mask);
  act.sa_flags = 0;
  if (sigaction(SIGINT, &act, NULL) < 0) {
    printf("I could not set a signal handler for SIGINT\n");
    exit(-1);
  };

  while (!sig_captured);
  printf("In Main : Yes, you captured SIGINT\n");
}



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
  sigset_t original_mask;
  sigset_t before_suspend_mask;
  sigset_t in_suspend_mask;

  /*  can have some code above this line  */
  sigprocmask(SIG_SETMASK, NULL, &original_mask);
  sigprocmask(SIG_SETMASK, NULL, &before_suspend_mask);
  sigprocmask(SIG_SETMASK, NULL, &in_suspend_mask);
  sigaddset(&before_suspend_mask, SIGINT);
  sigdelset(&in_suspend_mask, SIGINT);
  sigprocmask(SIG_SETMASK, &before_suspend_mask, NULL);

  /* Is this the best place to set the handler (I am not sure) ??? */
  act.sa_handler = catch_ctrl_c;
  sigemptyset(&act.sa_mask);
  act.sa_flags = 0;
  if (sigaction(SIGINT, &act, NULL) < 0) {
    printf("I could not set a signal handler for SIGINT\n");
    exit(-1);
  };

  printf("Now, the user can type ^C\n");


  while (!sig_captured)
    sigsuspend(&in_suspend_mask);
  sigprocmask(SIG_SETMASK, &original_mask, NULL);
  printf("In Main : Yes, you captured SIGINT\n");
}



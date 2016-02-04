//This file was generated from (Academic) UPPAAL 4.0.10 (rev. 4417), September 2009

/*

*/
//NO_QUERY

/*
When philospher 0 is eating both of his adjacent forks are picked up (by him)

NOTE: expects to pass
*/
E<> Philo0.isEating and (forks[0] == 0 or forks[0] == 0)

/*
Exists a path where philospher zero is eating with out one of his adjacent forks
safety property
NOTE: expects to fail
*/
E<> Philo0.isEating and ((forks[0] == 0 and forks[1] == 1) or (forks[0] == 1 and forks[1] == 0))

/*
Exists a path where philospher 0 is eating and forks at location 0 and 1 (his adjacent forks are not layed down)

NOTE: excepting to fail
*/
E<> Philo0.isEating and (forks[0] == 1 or forks[1] == 1)

/*
exists a path if Philo 0 wants to eat and hasn't eaten yet, and philo 1 wants to eat and has already eaten, and philo 0 checks the guard checkFork with his adjacent forks it returns true because Philo0 has priority because Philo1 has already eaten
liveness property
NOTE: expected to pass
*/
E<> Philo0.wantsToEat and eaten[0] == 0 and Philo1.wantsToEat and eaten[1] == 1 and checkFork(0,1)

/*
exists a path if Philo 0 wants to eat and hasn't eaten yet, and philo 1 wants to eat and has already eaten, and philo 1 checks the guard checkFork with his adjacent forks it returns false because Philo0 has priority
liveness property
NOTE: expected to fail
*/
E<> Philo0.wantsToEat and eaten[0] == 0 and Philo1.wantsToEat and eaten[1] == 1 and checkFork(1,2)

/*
there doesn't exist a path where the number of philosphers eating is greater than 2

NOTE: expecting to fail
*/
E<> numEating > 2

/*
All paths number of philsophers eating is always less than or equal to 2

NOTE: expecting to pass
*/
A<> numEating <= 2

/*
All locations, there is no deadlock

Note: expecting to pass
*/
A[] not deadlock

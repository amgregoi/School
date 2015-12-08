//This file was generated from (Academic) UPPAAL 4.0.10 (rev. 4417), September 2009

/*

*/
//NO_QUERY

/*
The system is deadlock free.
*/
A[] not deadlock

/*
Viking 1 can cross the bridge.
*/
E<> Viking1.safe

/*

*/
E<> Viking2.safe

/*

*/
E<> Viking3.safe

/*

*/
A[] not (Viking4.safe and time<slowest)

/*

*/
E<> Viking4.safe imply time>=slowest

/*
Scheduling problem reformulated as reachability property. Use
'Diagnostic Trace:Fastest' option to find fastest solution.
*/
E<> Viking1.safe and Viking2.safe and Viking3.safe and Viking4.safe

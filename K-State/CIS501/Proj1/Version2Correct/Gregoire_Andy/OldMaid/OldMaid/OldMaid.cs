using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OldMaidLib;

namespace OldMaid
{
    class OldMaid       //I/O class
    {
        cardDeck deck;                                                      //intialize new deck
        List<player> currentPlayers;                                        //list of current players
        List<computerPlayer> compPlayers;                                   //list of computer players
        humanPlayer humanPlayers;                                           //user
        int numPlayers;                                                     // number of players
        Random r = new Random();                                            // initialize random number gen

        /// <summary>
        /// execute game
        /// </summary>
        public void game()
        {
            bool playAgain;     //var to check if player wants to play again
            do                  //loop simulates game
            {
                start();                                                     //calls start
                while(currentPlayers.Count > 2 )                             //loop to play game until winner
                    fullRound();
                while (true)
                {
                    Console.Write("Would you like to play again? (y or n): ");  //play again message
                    try
                    {
                        string s = Console.ReadLine();

                        if (s[0].Equals('y') || s[0].Equals('Y'))           // tests input for 'y' or 'Y'
                        {
                            playAgain = true;                               //sets playAgain to true if test is true
                            break;
                        }
                        else if (s[0].Equals('n') || s[0].Equals('N'))      // tests input for 'n' or 'N'
                        {
                            playAgain = false;                              //sets playAgain to false if test is true
                            break;
                        }
                    }
                    catch { }
                }
                
            } while (playAgain) ;                                           //end do while - until user is finished playing
        }

        /// <summary>
        /// initialize players and shuffle/deal deck
        /// </summary>
        public void start()
        {
            deck = new cardDeck();
            currentPlayers = new List<player>();
            compPlayers = new List<computerPlayer>();
            Console.Write("Enter number of computer players (2 to 5): ");   //message, asks how many computer players
            numPlayers = Convert.ToInt32(Console.ReadLine());               //message input

            // initialize players
            int rand = r.Next()%numPlayers;                                 //random number for spot in player list
            int ind = 1;                                                    //indicie used for adding computer players to appropriate list
            for (int i = 0; i <= numPlayers; i++)                           //initialize players
            {
                if (i == rand)
                {

                    humanPlayers = new humanPlayer(numPlayers, "User   ");  //initialize user
                    currentPlayers.Add(humanPlayers);                       // add user to current player list
                }
                else
                {
                    compPlayers.Add(new computerPlayer(numPlayers, "Player" + ind.ToString()));     //initialize computer players in computer player list
                    currentPlayers.Add(compPlayers[ind-1]);                                         //add computer players to currentPlayers list
                    ind++;                                                                          //increment ind
        
                }
            }// end initialize players

            deck.shuffle(); // shuffle deck
            int x = 0;      // indicie for each player
            for (int i = 0; i < 53; i++)    //deals cards to current players
            {
                currentPlayers[x % (numPlayers+1)].deal(deck.draw());   
                x++;
            }
            for (int i = 0; i <= numPlayers; i++)   // discards pairs - start of game
            {
                currentPlayers[i].getTopIndex -= 1;
                currentPlayers[i].discardAllPairs();
                
            }
        }

        /// <summary>
        /// simulate a players round
        /// </summary>
        public void round()
        {
            
            currentPlayers.Add(currentPlayers[0]);          //copies first player in list to end of list
            currentPlayers.RemoveAt(0);                     //deletes first player (rotates list)

            int cpNum = 0;                                  //initialize cpNum (computerPlayer number)
            int index;
            try
            {
                index = r.Next() % (currentPlayers[0].getTopIndex);     //random number generated for computers pickCardAt
            }
            catch (DivideByZeroException) { index = r.Next() % 1; }
            if (currentPlayers[numPlayers].getName.Contains("P"))   //tests if its a computers turn
            {
                try
                {
                    //prints what the drawer took from the drawee
                    Console.WriteLine("\n" + currentPlayers[numPlayers].getName + " draws " + currentPlayers[0].getHand[index].ToString() + " from " + currentPlayers[0].getName + "\n");
                }
                catch { return; }
                currentPlayers[numPlayers].addCard(currentPlayers[0].pickCardAt(index));                //pickCard from drawee, places card in drawers hand
                for (int i = 0; i < currentPlayers.Count; i++)
                    Console.WriteLine(currentPlayers[i].getName + " " + currentPlayers[i].ToString());  //prints players hand
                try
                {
                    cpNum = (cpNum + 1) % numPlayers;                                                           //update cpNums
                }
                catch (DivideByZeroException) { cpNum = (cpNum + 1) % 1; }
                Console.Write("Enter to continue: "); 
                Console.ReadLine(); Console.WriteLine();
            }
            else
            {
                Console.WriteLine(currentPlayers[numPlayers].getName + " " +currentPlayers[numPlayers].ToString());     //prints users hand
                Console.WriteLine(currentPlayers[0].getName + " " + currentPlayers[0].ToString());                      //prints players hand
                Console.Write(compPlayers[cpNum].MakeCardIndicies());                                                   //print indicie choices of computer for user
                string line; int x;
                while(true)             //tests for correct input type
                {
                    line = Console.ReadLine();
                    if (Int32.TryParse(line, out x) && x <= currentPlayers[0].getTopIndex)
                    {
                        try
                        {
                            //prints what user took from drawee
                            Console.WriteLine(currentPlayers[numPlayers].getName + " draws " + currentPlayers[0].getHand[x].ToString() + " from " + currentPlayers[0].getName + "\n");
                
                        }
                        catch (NullReferenceException) { }
                        break;
                    }

                    else
                        Console.WriteLine("invalid input");                                 //prints invalid input
                }
                currentPlayers[numPlayers].addCard(currentPlayers[0].pickCardAt(x));        //pickCard from computer, places card in users hand
                for (int i = 0; i < currentPlayers.Count; i++)
                    Console.WriteLine(currentPlayers[i].getName + " " + currentPlayers[i].ToString());  //prints players hand
                Console.Write("Enter to continue: ");                                       //Enter to continue line after players turn
                Console.ReadLine(); Console.WriteLine();                                    //waits for readline
            }
        }

        /// <summary>
        /// simulate one play through for each player
        /// </summary>
        public void fullRound()
        {
            for (int i = 0; i <= numPlayers; i++)
            {
                isDone();
                if (currentPlayers.Count < 2)
                    break;
                round();
            }
            Console.WriteLine("#### End of round ####\n");
        }

        private void isDone()
        {
            for (int i = 0; i < currentPlayers.Count; i++)
                if (currentPlayers[i].getTopIndex == -1)
                {
                    numPlayers--;
                    currentPlayers.RemoveAt(i);
                }
        }
        

    }
}

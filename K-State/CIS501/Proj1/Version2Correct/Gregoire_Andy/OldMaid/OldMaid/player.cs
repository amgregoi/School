using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OldMaidLib;

namespace OldMaid
{
    class player
    {
        playingCard[] hand;             //player hand
        int[] simp;                     //player hand2 to help discard pairs ( sorted by rank )
        int topIndex=0, numPlayers;     //top card in hand & number of players
        string Name;                    //player name
        cardDeck deck = new cardDeck(); //initialize new deck of cards

        /// <summary>
        /// gets topIndex of hand
        /// </summary>
        public int getTopIndex
        {
            get
            {
                return topIndex;
            }
            set
            {
                topIndex = value;
            }
        }
        /// <summary>
        /// gets player name
        /// </summary>
        public string getName
        {
            get
            {
                return Name;
            }
        }
        /// <summary>
        /// gets player hand
        /// </summary>
        public playingCard[] getHand
        {
            get
            {
                return hand;
            }
        }

        /// <summary>
        /// player constructor 
        /// </summary>
        /// <param name="numPlayers"> number of players</param>
        /// <param name="n">name of player</param>
        public player(int numPlayers, string n)
        {
            this.numPlayers = numPlayers+1;                     //initialize number of players
            hand = new playingCard[(53/this.numPlayers)+2];     //initialize hand size
            Name = n;                                           //initialize player name
        }

        /// <summary>
        /// shuffle players hand
        /// </summary>
        public void shuffle()
        {
            System.Random random = new System.Random();
            for (int i = 0; i < hand.Length; i++)
            {
                int j = random.Next(hand.Length);
                playingCard temp = hand[i]; hand[i] = hand[j]; hand[j] = temp;
            }
        }

        /// <summary>
        /// Discards all pairs from players hand
        /// </summary>
        public void discardAllPairs()
        {            
            simp = new int[16];
            for(int i=0; i<simp.Length; i++)
                simp[i] = -1;
            for (int i = 0; i < hand.Length; i++)
            {
                try
                {
                    if (simp[hand[i].getRank] > -1 && simp[hand[i].getRank] != i)
                    {
                        int x = simp[hand[i].getRank];                      //temp var - holds index for card getting replaced
                        hand[simp[hand[i].getRank]] = hand[topIndex];       //replaces 1st occurrence of pair with last card in hand (topIndex)
                        simp[hand[topIndex].getRank] = x;                   //updates location in simp[] of the last card in hand ( that was just moved)
                        hand[topIndex] = null;                              //after moving last card, sets that index to null
                        topIndex--;                                         //decrement topIndex (removed card from hand) 
                        simp[hand[i].getRank] = -1;                         //updates simp[] - card is no longer in hand so its location is set to -1 (chosen default value)
                        hand[i] = hand[topIndex];                           //replaces 2nd occurrence of pair with new last card in hand (topindex)
                        simp[hand[topIndex].getRank] = simp[hand[i].getRank];//updates location in simp[] of last card in hand               
                        hand[topIndex] = null;                              //after moving last card, sets that index to null
                        topIndex--;                                         //decrememtn topIndex ( removed card from hand)
                        returnHandToDeck();                                 //incrememnt deck topIndex
                        returnHandToDeck();                                 //incrememnt deck topIndex
                        this.discardAllPairs();                             //recursive call of this method
                        }
                    else
                    {
                        simp[hand[i].getRank] = i;                          //places card in hand ( if there isnt another occurrence of its 'rank' )   
                    }
                }
                catch { }
            }   
        }

        public virtual void deal(playingCard card)
        {
            hand[topIndex] = card;          //places card in hand at topIndex
            topIndex++;                     //increment topIndex
        }

        /// <summary>
        /// pick card at location i in hand
        /// </summary>
        /// <param name="i">location in hand</param>
        /// <returns></returns>
        public playingCard pickCardAt(int i)
        {
            playingCard temp = hand[i];     //places copy of card in temp
            simp[temp.getRank] = -1;
            hand[i] = hand[topIndex];       //copy last card to chosen indicie
            simp[hand[topIndex].getRank] = i; //updates position of hand[topindex] since it was moved
            hand[topIndex] = null;          //deletes last card ( since its been moved )
            topIndex--;                     //decrement top index ( deleted above card )
            return temp;                    //returns copy of card that was deleted from hand
        }

        /// <summary>
        /// Add card to hand
        /// </summary>
        /// <param name="card"></param>
        public void addCard(playingCard card)
        {
            if (simp[card.getRank] == -1)             //if no pa ir to drawn card, places in hand
            {
                topIndex++;
                hand[topIndex] = card;
                simp[card.getRank] = topIndex;
                
            }
            else                                        //deletes paired card inhand
            {
                hand[simp[card.getRank]] = hand[topIndex];
                simp[hand[topIndex].getRank] = simp[card.getRank];
                hand[topIndex] = null;
                simp[card.getRank] = -1;
                topIndex--;
                returnHandToDeck();
                returnHandToDeck();
            }
        }

        /// <summary>
        /// increment decks topIndex
        /// </summary>
        public void returnHandToDeck()
        {
            deck.returnCard();
        }

        /// <summary>
        /// override players toString method
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < hand.Length; i++)
            {
                try
                {
                    sb.Append(hand[i].ToString());
                }
                catch (NullReferenceException) { }
            }
            return sb.ToString();
        }
        
    }
}

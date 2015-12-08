using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OldMaidLib
{
    public class cardDeck
    {
        playingCard[] deck = new playingCard[53];
        int topIndex = 52;

        /// <summary>
        /// create deck
        /// </summary>
        public cardDeck()
        {
            int x = 0;
            for (int i = 1; i <= 4; i++)                           //1-4 used to seperate suit
                for (int j = 0; j < 13; j++)                    //0-13 ranks for each card 2-ace
                {
                    deck[x] = new playingCard(j + 2, true, i);    //creates card
                    x++;                                        //increment x - travels through deck array
                }
            deck[52] = new playingCard(0, true, 5);             //creates last card (old maid)
        }

        /// <summary>
        /// draw from deck
        /// </summary>
        /// <returns></returns>
        public playingCard draw()
        {
            return deck[topIndex--];
        }

        /// <summary>
        /// shuffle deck
        /// </summary>
        /// <returns></returns>
        public cardDeck shuffle()   //knuths shuffle algorithm    
        {
            System.Random random = new System.Random();
            for (int i = 0; i < deck.Length; i++)
            {
                int j = random.Next(deck.Length);
                playingCard temp = deck[i]; deck[i] = deck[j]; deck[j] = temp;
            }
            return this;
        }

        /// <summary>
        /// returnscardto deck - increments deck topIndex
        /// </summary>
        public void returnCard()
        {
            topIndex++;
        }


    }
}

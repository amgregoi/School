using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OldMaidLib
{
    public class playingCard
    {
        public enum CardVal
        {
            T = 10,
            J = 11,
            Q = 12,
            K = 13,
            A = 14
        }
        public enum Suit
        {
            H = 1,
            C = 2,
            D = 3,
            S = 4,
            M = 5
        }


        CardVal cv = new CardVal();
        int rank;
        bool faceUp;
        Suit test = new Suit();

        public int getRank
        {
            get
            {
                return rank;
            }
        }

        public bool getFaceUp
        {
            get
            {
                return faceUp;
            }
            set
            {
                faceUp = value;
            }
        }


        public playingCard(int r, bool t, int suit)
        {
            rank = r;
            faceUp = t;
            test = (Suit)suit;
            cv = (CardVal)r;

        }
        public playingCard()
        {
            rank = -1;
            faceUp = true;
        }

        public override string ToString()
        {
            if (faceUp)
                return cv.ToString() + test + " ";
            else
                return "XX ";
        }
    }
}

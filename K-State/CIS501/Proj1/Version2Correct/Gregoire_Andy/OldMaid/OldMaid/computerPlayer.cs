using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using OldMaidLib;

namespace OldMaid
{
    class computerPlayer : player
    {
        public computerPlayer(int num, string n)    // constructor
            : base(num, n)
        {}
        static bool test;       
        [Conditional("DEBUG")]  // You need "using System.Diagnostics;"
        static void DebugTest(bool debug)
        {
            test = debug;
        }
        public override void deal(playingCard card)
        {
            DebugTest(true);               // false - show XX's   --> true - show JS (rank + suit)
            card.getFaceUp = test;
            base.deal(card);
        }

        public string MakeCardIndicies()
        {
            string index = "index:  ";
            for (int i = 0; i <= this.getTopIndex; ++i)
            {
                if (i < 10)
                    index += i.ToString() + "  ";       // correct spacing for indicies 0-9
                else
                    index += i.ToString() + " ";        // correct spacing for indicies >= 10
            }
            return index + "\n";
        }
        
    }
}

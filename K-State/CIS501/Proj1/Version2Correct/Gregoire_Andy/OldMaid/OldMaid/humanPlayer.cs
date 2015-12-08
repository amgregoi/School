using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OldMaidLib;

namespace OldMaid
{
    class humanPlayer : player
    {
        public humanPlayer(int num, string s)           // constructor
            : base(num, s) { }

        public override void deal(playingCard card)     // deal override (humanPlayer)
        {
            card.getFaceUp = true;
            base.deal(card);
        }
    }
}

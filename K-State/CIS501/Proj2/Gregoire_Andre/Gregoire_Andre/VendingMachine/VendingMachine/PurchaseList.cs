using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VendingMachine
{
    public class PurchaseList
    {
        string name;
        int amount;
        DateTime dt;

        public PurchaseList(string n, int amt, DateTime d)
        {
            name = n;
            amount = amt;
            dt = d;
        }

        public override string ToString()
        {
            return (name + " (" + amount.ToString() + ") " + dt.ToString());
        }
    }
}

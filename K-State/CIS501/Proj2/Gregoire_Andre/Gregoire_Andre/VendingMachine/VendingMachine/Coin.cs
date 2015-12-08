using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VendingMachine
{
    public class Coin
    {
        int stock, num = 0, coinVal, temp;
        CoinDispenser coinD;

        public Coin(int stock, int val, CoinDispenser coinD)
        {
            this.stock = temp = stock;
            coinVal = val;
            this.coinD = coinD;
        }

        public int getStock { get { return stock; } set { stock = value; } }
        public int getNum { get { return num; } set { num = value; } }
        public int getTemp { get { return temp; } set { temp = value; } }
        public int getVal { get { return coinVal; } set { coinVal = value; } }
        public CoinDispenser getCD { get { return coinD; } set { coinD = value; } }

        public int addOneCoin()
        {
            stock++;
            num++;
            temp++;
            return coinVal;
        }

        public int decrementTemp()
        {
            temp--;
            return coinVal;
        }

        public int setValuesAfterPurchase(int change)
        {
            coinD.Actuate(change); //update value for change in display
            change = 0;  //resets change array back to 0 (default)
            num = 0;    //resets num of inserted coins to 0
            stock = temp;//sets stock equal to temp
            return change;
        }

        public void coinReturn()
        {
            coinD.Actuate(num);
            stock -= num;
            num = 0;
        }


    }
}

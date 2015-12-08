using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VendingMachine
{
    public class Total
    {
        TimerLight noChange;
        AmountDisplay amount;
        CanDispenser cd;
        int[] change = { 0, 0, 0, 0 };
        List<PurchaseList> ListPurchases = new List<PurchaseList>();
        Can[] Cans;
        Coin[] Coins;
        int total = 0;

        /// <summary>
        /// Total Constructor
        /// </summary>
        /// <param name="noChangeLight"></param>
        /// <param name="amount"></param>
        /// <param name="CD"></param>
        /// <param name="Cans"></param>
        /// <param name="Coins"></param>
        public Total(TimerLight noChangeLight, AmountDisplay amount, CanDispenser CD, Can[] Cans, Coin[] Coins)
        {
            noChange = noChangeLight;
            this.amount = amount;
            this.cd = CD;
            this.Cans = Cans;
            this.Coins = Coins;
        }
        public int getTotal { get { return total; } set { total = value; } }


        /// <summary>
        /// adds coin to counter, updates amount display, turns on purchasable lights if total > can price
        /// I put this in Total rather than the coin to be able to check & turn on purchase lights
        /// </summary>
        /// <param name="c"></param>
        public void addOne(int i)
        {
            total += Coins[i].addOneCoin();         //increment coin stock, num, temp and return coinval to increment total
            amount.DisplayAmount(total);            //Displays new total
            foreach (Can can in Cans)               //iterates through Cans
            {
                can.updateLightsAfterCoinInsert(total); //updates purchaseLight if total > canPrice & not soldout
                
            }
        }

        /// <summary>
        /// returns true if we have enough coins to return adequate change
        /// </summary>
        /// <param name="curr"></param>
        /// <returns></returns>
        private bool _haveChange(Can curr)
        {
            int temp = total;                            //set temp to total
            temp -= curr.getPrice;                       //decrement temp by price of can
            for (int i = 3; i >= 0; i--)                 //Calculate if we have enough for change, and if so how much to return
            {
                if (temp >= Coins[i].getVal)             //checks if we can still use more of this type of coin
                {
                    if (Coins[i].getTemp > 0)            //checks if we still have coins to use
                    {
                        temp -= Coins[i].decrementTemp(); // decrement change we need to give back by coin value |  decrement 1 from temp of coin[i]
                        change[i]++;                     // increment 1 of type coin[i] to return as change
                        i++;                             // increment to go through again in case of multiple coin types
                    }
                }
            }
            if (temp == 0 && curr.getStock >= 0) return true; // if we have change return true
            else return false;
        }

        /// <summary>
        /// simulates the pruchase of a can, IF its not sold out and IF we have change
        /// </summary>
        /// <param name="i"></param>
        public void purchaseButton(int i)
        {
            if (!Cans[i].checkSoldOutLight())              //tests if selected can is not sold out
            {
                //You mentioned taking this out, wasnt quite sure how to check for change if we did
                if (_haveChange(Cans[i]))                                     
                {
                    Cans[i].getStock--;                       //decrements can stock
                    ListPurchases.Add(new PurchaseList(Cans[i].getName, Cans[i].getPrice, DateTime.Now ));  //Add to entry to purchase list (dialog)
                    amount.DisplayAmount(0);                 // changes amt display to 0 after purchase    
                    cd.Actuate(Cans[i].getName);             //adds name of can to display

                    for (int j = 0; j < 4; j++)             //initialize change back to 0, update change display
                    {
                        change[j] = Coins[j].setValuesAfterPurchase(change[j]);     //updates values in coin class and returns change reset value
                    }
                    foreach (Can c in Cans)
                    {
                        c.updateLightsAfterPurchase();              //updates purchase light/soldout light after purchase
                    }
                    total = 0;         // reset total to 0
                }
                else
                {
                    noChange.TurnOn3Sec();               // if we do not have change turn on no change light
                }
            }
        }

        /// <summary>
        /// simulates coinReturn button, returns all coins inserted by user
        /// </summary>
        public void coinReturn()
        {
            amount.DisplayAmount(0);
            foreach (Coin coin in Coins)
            {
                coin.coinReturn();      //updates values after coin return button 
            }
        }

        /// <summary>
        /// adds list of can purchases to list dialog
        /// </summary>
        public void salesButton()
        {
            object[] temp = ListPurchases.ToArray();
            ListDialog ld = new ListDialog();
            ld.AddDisplayItems(temp);
            ld.ShowDialog();
        }

        /// <summary>
        /// clears list dialog of all previous purchases
        /// </summary>
        public void clearSalesButton()
        {
            ListPurchases.Clear();
        }


    }
}

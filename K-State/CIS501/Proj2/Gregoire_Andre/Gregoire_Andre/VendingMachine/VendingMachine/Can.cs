using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VendingMachine
{
    public class Can
    {
        string name;
        int price, stock;
        Light purchaseLight;
        Light soldOutLight;

        public Can(string name, int price, int stock, Light purchase, Light soldOut)
        {
            this.name = name;
            this.price = price;
            purchaseLight = purchase;
            soldOutLight = soldOut;
            this.stock = stock;
        }
        public string getName{get { return name; }set { name = value; }}
        public int getPrice{get { return price; }set { price = value; }}
        public int getStock { get { return stock; } set { stock = value; } }
        public Light getPurchaseLight{get { return purchaseLight; }set { purchaseLight = value; }}
        public Light getSoldOutLight{get { return soldOutLight; }set { soldOutLight = value; }}

        public void updateLightsAfterCoinInsert(int total)
        {
            if (total >= price && !soldOutLight.IsOn())
                purchaseLight.TurnOn();

        }

        public void updateLightsAfterPurchase()
        {
            if (stock == 0)                //checks if stock is 0
                soldOutLight.TurnOn();     //turns on soldoutlight
            purchaseLight.TurnOff();       //turns of purchasable lights after purchase
        }

        public bool checkSoldOutLight()
        {
            if (soldOutLight.IsOn())
                return true;
            return false;
        }
    }


}

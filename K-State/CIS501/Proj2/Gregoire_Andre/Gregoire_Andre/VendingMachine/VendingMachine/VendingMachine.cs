//////////////////////////////////////////////////////////////////////
//      Vending Machine (Form1.cs)                                  //
//      Written by Masaaki Mizuno, (c) 2006, 2007, 2008, 2010       //
//                      for Learning Tree Course 123P, 252J, 230Y   //
//                 also for KSU Course CIS501                       //  
//////////////////////////////////////////////////////////////////////
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace VendingMachine
{
    public partial class VendingMachine : Form
    {
        // Static Constants
        public const int NUMCANTYPES = 4;
        public const int NUMCOINTYPES = 4;
        public static readonly int[] NUMCANS = { 4, 4, 4, 4 };
        public static readonly int[] CANPRICES = { 120, 170, 130, 110 };
        public static readonly string[] CANNAMES = { "Coca-Cola", "Pepsi", "Dr. Pepper", "Sprite" };

        public static readonly int[] COINVALUES = { 10, 50, 100, 500 };
        public static readonly int[] NUMCOINS = { 15, 10, 5, 2 };
        // 10Yen, 50Yen, 100Yen, 500Yen

        // Boundary Objects
        private AmountDisplay amountDisplay;
        private DebugDisplay displayPrice0, displayPrice1, displayPrice2, displayPrice3;
        private DebugDisplay displayNum10Yen, displayNum50Yen, displayNum100Yen, displayNum500Yen;
        private DebugDisplay displayName0, displayName1, displayName2, displayName3;
        private DebugDisplay displayNumCans0, displayNumCans1, displayNumCans2, displayNumCans3;
        private Light soldOutLight0, soldOutLight1, soldOutLight2, soldOutLight3;
        private TimerLight noChangeLight;
        private Light purchasableLight0, purchasableLight1, purchasableLight2, purchasableLight3;
        private CoinDispenser coinDispenser10Yen, coinDispenser50Yen, coinDispenser100Yen, coinDispenser500Yen;
        private CanDispenser canDispenser;
        private CoinInserter[] coinInserters;
        private VMButton[] purchaseButtons;
        private VMButton coinReturnButton;
        private VMButton salesRecordListButton;
        private VMButton salesRecordClearButton;

        // Declare fields for your entity and control objects
        Total total;
        Can[] cans = new Can[4];
        Coin[] coins = new Coin[4];


        public VendingMachine()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            amountDisplay = new AmountDisplay(txtAmount);
            displayNum10Yen = new DebugDisplay(txtNum10Yen);
            displayNum50Yen = new DebugDisplay(txtNum50Yen);
            displayNum100Yen = new DebugDisplay(txtNum100Yen);
            displayNum500Yen = new DebugDisplay(txtNum500Yen);
            displayPrice0 = new DebugDisplay(txtPrice0);
            displayPrice1 = new DebugDisplay(txtPrice1);
            displayPrice2 = new DebugDisplay(txtPrice2);
            displayPrice3 = new DebugDisplay(txtPrice3);
            displayName0 = new DebugDisplay(txtName0);
            displayName1 = new DebugDisplay(txtName1);
            displayName2 = new DebugDisplay(txtName2);
            displayName3 = new DebugDisplay(txtName3);
            displayNumCans0 = new DebugDisplay(txtNumCan0);
            displayNumCans1 = new DebugDisplay(txtNumCan1);
            displayNumCans2 = new DebugDisplay(txtNumCan2);
            displayNumCans3 = new DebugDisplay(txtNumCan3);
            soldOutLight0 = new Light(pbxSOLight0, Color.Orange);
            soldOutLight1 = new Light(pbxSOLight1, Color.Orange);
            soldOutLight2 = new Light(pbxSOLight2, Color.Orange);
            soldOutLight3 = new Light(pbxSOLight3, Color.Orange);
            noChangeLight = new TimerLight(pbxNoChange, Color.Red, timer1);
            purchasableLight0 = new Light(pbxPurLight0, Color.Aqua);
            purchasableLight1 = new Light(pbxPurLight1, Color.Aqua);
            purchasableLight2 = new Light(pbxPurLight2, Color.Aqua);
            purchasableLight3 = new Light(pbxPurLight3, Color.Aqua);
            coinDispenser10Yen = new CoinDispenser(txtChange10Yen);
            coinDispenser50Yen = new CoinDispenser(txtChange50Yen);
            coinDispenser100Yen = new CoinDispenser(txtChange100Yen);
            coinDispenser500Yen = new CoinDispenser(txtChange500Yen);
            canDispenser = new CanDispenser(txtCanDispenser);

            // Instantiate your entity and control objects
            // Connect these objects
            cans[0] = new Can(CANNAMES[0], CANPRICES[0], NUMCANS[0], purchasableLight0, soldOutLight0);
            cans[1] = new Can(CANNAMES[1], CANPRICES[1], NUMCANS[1], purchasableLight1, soldOutLight1);
            cans[2] = new Can(CANNAMES[2], CANPRICES[2], NUMCANS[2], purchasableLight2, soldOutLight2);
            cans[3] = new Can(CANNAMES[3], CANPRICES[3], NUMCANS[3], purchasableLight3, soldOutLight3);
            coins[0] = new Coin(NUMCOINS[0], COINVALUES[0], coinDispenser10Yen);
            coins[1] = new Coin(NUMCOINS[1], COINVALUES[1], coinDispenser50Yen);
            coins[2] = new Coin(NUMCOINS[2], COINVALUES[2], coinDispenser100Yen);
            coins[3] = new Coin(NUMCOINS[3], COINVALUES[3], coinDispenser500Yen);
            total = new Total(noChangeLight, amountDisplay, canDispenser, cans, coins);
            

            // You must replace the following default constructors with 
            // constructors with arguments (non-default constructors)
            purchaseButtons = new PurchaseButton[NUMCANTYPES];
            for (int i = 0; i < NUMCANTYPES; i++)
                purchaseButtons[i] = new PurchaseButton(total, i);


            coinInserters = new CoinInserter[NUMCOINTYPES];
            for (int i = 0; i < NUMCOINTYPES; i++)
                coinInserters[i] = new CoinInserter(total, i);

            coinReturnButton = new CoinReturnButton(total);

            salesRecordListButton = new SalesRecordListButton(total);

            salesRecordClearButton = new SalesRecordClearButton(total);

            

            // Display debug information
            displayCanPricesAndNames();
            updateDebugDisplays();
        }


        private void btnCoinInserter10Yen_Click(object sender, EventArgs e)
        {
            // Do not change the body
            coinInserters[0].CoinInserted();
            updateDebugDisplays();
        }

        private void btnCoinInserter50Yen_Click(object sender, EventArgs e)
        {
            // Do not change the body
            coinInserters[1].CoinInserted();
            updateDebugDisplays();
        }

        private void btnCoinInserter100Yen_Click(object sender, EventArgs e)
        {
            // Do not change the body
            coinInserters[2].CoinInserted();
            updateDebugDisplays();
        }

        private void btnCoinInserter500Yen_Click(object sender, EventArgs e)
        {
            // Do not change the body
            coinInserters[3].CoinInserted();
            updateDebugDisplays();
        }

        private void btnPurButtn0_Click(object sender, EventArgs e)
        {
            // Do not change the body
            purchaseButtons[0].ButtonPressed();
            updateDebugDisplays();
        }

        private void btnPurButton1_Click(object sender, EventArgs e)
        {
            // Do not change the body
            purchaseButtons[1].ButtonPressed();
            updateDebugDisplays();
        }

        private void btnPurButton2_Click(object sender, EventArgs e)
        {
            // Do not change the body
            purchaseButtons[2].ButtonPressed();
            updateDebugDisplays();
        }

        private void btnPurButton3_Click(object sender, EventArgs e)
        {
            // Do not change the body
            purchaseButtons[3].ButtonPressed();
            updateDebugDisplays();
        }

        private void btnCoinReturn_Click(object sender, EventArgs e)
        {
            // Do not change the body
            coinReturnButton.ButtonPressed();
            updateDebugDisplays();
        }

        private void btnListSalesRecord_Click(object sender, EventArgs e)
        {
            // Do not change the body
            salesRecordListButton.ButtonPressed();
        }

        private void btnClearSalesRecord_Click(object sender, EventArgs e)
        {
            // Do not change the body
            salesRecordClearButton.ButtonPressed();
        }

        private void btnChangePickedUp_Click(object sender, EventArgs e)
        {
            // This is just for a simulation
            coinDispenser10Yen.Clear();
            coinDispenser50Yen.Clear();
            coinDispenser100Yen.Clear();
            coinDispenser500Yen.Clear();
            amountDisplay.DisplayAmount(0);
        }

        private void btnCanPickedUp_Click(object sender, EventArgs e)
        {
            // This is just for a simulation
            canDispenser.Clear();
        }

        private void btnReset_Click(object sender, EventArgs e)
        {
            int i = 0;
            foreach (Can c in cans)
            {
                c.getPurchaseLight.TurnOff();
                c.getSoldOutLight.TurnOff();
                c.getStock = NUMCANS[i];
                i++;
            }
            i = 0;
            foreach (Coin c in coins)
            {
                c.getStock = c.getTemp = NUMCOINS[i];
                c.getNum = 0;
                i++;
            }
            noChangeLight.TurnOff();
            displayNum10Yen.Display(NUMCOINS[0]);
            displayNum50Yen.Display(NUMCOINS[1]);
            displayNum100Yen.Display(NUMCOINS[2]);
            displayNum500Yen.Display(NUMCOINS[3]);
            displayNumCans0.Display(NUMCANS[0]);
            displayNumCans1.Display(NUMCANS[1]);
            displayNumCans2.Display(NUMCANS[2]);
            displayNumCans3.Display(NUMCANS[3]);
            amountDisplay.DisplayAmount(0);
            coinDispenser10Yen.Clear();
            coinDispenser50Yen.Clear();
            coinDispenser100Yen.Clear();
            coinDispenser500Yen.Clear();
            canDispenser.Clear();
            total.clearSalesButton();
            total.getTotal = 0;

        }

        private void displayCanPricesAndNames()
        {
            displayPrice0.Display("\\" + CANPRICES[0]);
            displayPrice1.Display("\\" + CANPRICES[1]);
            displayPrice2.Display("\\" + CANPRICES[2]);
            displayPrice3.Display("\\" + CANPRICES[3]);
            displayName0.Display(CANNAMES[0]);
            displayName1.Display(CANNAMES[1]);
            displayName2.Display(CANNAMES[2]);
            displayName3.Display(CANNAMES[3]);
        }

        private void updateDebugDisplays()
        {
            // You need to change XXX to appropriate "object.property"

            displayNum10Yen.Display(coins[0].getStock);
            displayNum50Yen.Display(coins[1].getStock);
            displayNum100Yen.Display(coins[2].getStock);
            displayNum500Yen.Display(coins[3].getStock);
            displayNumCans0.Display(cans[0].getStock);
            displayNumCans1.Display(cans[1].getStock);
            displayNumCans2.Display(cans[2].getStock);
            displayNumCans3.Display(cans[3].getStock);
             
        }




    }
}
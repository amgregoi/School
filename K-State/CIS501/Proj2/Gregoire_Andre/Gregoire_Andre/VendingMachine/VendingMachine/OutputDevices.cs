//////////////////////////////////////////////////////////////////////
//      Vending Machine (Actuators.cs)                              //
//      Written by Masaaki Mizuno, (c) 2006, 2007, 2008, 2010, 2011 //
//                      for Learning Tree Course 123P, 252J, 230Y   //
//                 also for KSU Course CIS501                       //  
//////////////////////////////////////////////////////////////////////
using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Text;
using System.Drawing;

namespace VendingMachine
{
    // Do not change anything in if file
    public class AmountDisplay
    {
        TextBox tbx;
        public AmountDisplay(TextBox tbx)
        {
            this.tbx = tbx;
        }

        public void DisplayAmount(int amount)
        {
            this.tbx.Text = "\\" + amount;
        }
    }

    public class DebugDisplay
    {
        TextBox tbx;
        public DebugDisplay(TextBox tbx)
        {
            this.tbx = tbx;
        }

        public void Display(int amount)
        {
            this.tbx.Text = "" + amount;
        }

        public void Display(string st)
        {
            this.tbx.Text = st;
        }
    }

    public class Light
    {
        PictureBox pbx;
        Color onColor;
        static Color offColor = SystemColors.Control;

        public Light(PictureBox pbx, Color onColor)
        {
            this.pbx = pbx;
            this.onColor = onColor;
        }
        public void TurnOn()
        {
            pbx.BackColor = onColor;
        }
        public void TurnOff()
        {
            pbx.BackColor = offColor;
        }

        public Boolean IsOn()
        {
            return (pbx.BackColor == onColor);
        }
    }

    public class TimerLight : Light
    {
        Timer timer;
        public TimerLight(PictureBox pbx, Color onColor, Timer timer)
            : base(pbx, onColor)
        {
            this.timer = timer;
            timer.Tick += new EventHandler(timerTick);
        }

        public void TurnOn3Sec()
        {
            timer.Interval = 3000;
            timer.Start();
            TurnOn();
        }

        private void timerTick(object sender, EventArgs ea)
        {
            TurnOff();
            timer.Stop();
        }
    }

    public class CoinDispenser
    {
        TextBox txbChange;
        public CoinDispenser(TextBox txbChange)
        {
            this.txbChange = txbChange;
        }

        public void Actuate(int numCoins)
        {
            if (numCoins > 0)
                txbChange.Text = "" + numCoins;
            else
                txbChange.Text = "";
        }

        public void Clear()
        {
            txbChange.Text = "";
        }
    }

    public class CanDispenser
    {
        TextBox txbCan;
        public CanDispenser(TextBox txbCan)
        {
            this.txbCan = txbCan;
        }

        public void Actuate(string canType)
        {
            this.txbCan.Text = canType;
        }

        public void Clear()
        {
            this.txbCan.Text = "";
        }
    }
}

//////////////////////////////////////////////////////////////////////
//      Vending Machine (Actuators.cs)                              //
//      Written by Masaaki Mizuno, (c) 2006, 2007, 2008, 2010, 2011 //
//                      for Learning Tree Course 123P, 252J, 230Y   //
//                 also for KSU Course CIS501                       //  
//////////////////////////////////////////////////////////////////////
using System;
using System.Collections.Generic;
using System.Text;

namespace VendingMachine
{
    // For each class, you can (must) add fields and overriding constructors

    public class CoinInserter
    {
        int index;
        Total t;
        public CoinInserter(Total t, int i)
        {
            index = i;
            this.t = t;
        }
        public void CoinInserted()
        {
            t.addOne(index);
        }
    }

    public interface VMButton
    {
        void ButtonPressed();
    }

    public class PurchaseButton : VMButton
    {
        Total total;
        int index;
        public PurchaseButton(Total t, int i)
        {
            total = t;
            index = i;
        }
        public void ButtonPressed()
        {
            total.purchaseButton(index);
        }
    }

    public class CoinReturnButton : VMButton
    {
        Total total;
        public CoinReturnButton(Total t)
        {
            total = t;
        }
        public void ButtonPressed()
        {
            total.coinReturn();
        }
    }

    public class SalesRecordListButton : VMButton
    {
        Total total;
        public SalesRecordListButton(Total t)
        {
            total = t;
        }
        public void ButtonPressed()
        {
            total.salesButton();
        }
    }

    public class SalesRecordClearButton : VMButton
    {
        Total total;
        public SalesRecordClearButton(Total t)
        {
            total = t;
        }

        public void ButtonPressed()
        {
            total.clearSalesButton();
        }
    }
}

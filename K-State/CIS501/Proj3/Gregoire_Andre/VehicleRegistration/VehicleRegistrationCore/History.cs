using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VehicleRegistrationCore
{
    [Serializable()]
    public class History
    {
        Owner o;
        string date;
        string price;
        string license;

        public History(Owner o, string d, string p, string l)
        {
            this.o = o;
            date = d;
            price = p;
            license = l;
        }

        public Owner getOwner
        {
            get { return o; }
        }
        public string getDate
        {
            get { return date; }
        }
        public string getPrice
        {
            get { return price; }
        }
        public string getLicense
        {
            get { return license; }
        }

        public override string ToString()
        {
            if (license.Equals(null))
                return (date + ", " + price);
            else

                return (o.ToString()+", Date:"+date + ", Price:" + price + ", License:" + license);
        }
    }
}

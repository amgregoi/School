using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VehicleRegistrationCore
{
    [Serializable()] 
    public class Vehicle
    {
        string VIN, Make, Model, Color, DID, Year;
        List<History> Hist = new List<History>();

        /// <summary>
        /// Vehicle Construcot
        /// </summary>
        /// <param name="V">VIN</param>
        /// <param name="Ma">Make</param>
        /// <param name="Mo">Model</param>
        /// <param name="C">Color</param>
        /// <param name="ID">InitialDealer ID</param>
        /// <param name="yr">Year</param>
        public Vehicle(string V, string Ma, string Mo, string C, string ID, string yr)
        {
            VIN = V;
            Make = Ma;
            Model = Mo;
            Color = C;
            DID = ID;
            Year = yr;
        }

        /// <summary>
        /// updates new owner (transfers)
        /// </summary>
        /// <param name="O"></param>
        public void newOwner(Owner O, string date, string price, string license)
        {
            //Hist.Add(new History(O, date, price, license));
            Hist.Insert(0, new History(O, date, price, license));
        }

        //Get Properties
        public string getVIN
        {
            get { return VIN; }
            set { VIN = value; }
        }
        public string getMake
        {
            get { return Make; }
            set { Make = value; }
        }
        public string getModel
        {
            get { return Model; }
            set { Model = value; }
        }
        public string getColor
        {
            get { return Color; }
            set { Color = value; }
        }
        public string getDID
        {
            get { return DID; }
            set { DID = value; }
        }
        public string getYear
        {
            get { return Year; }
            set { Year = value; }
        }
        public List<History> getHistory
        {
            get { return Hist; }
        }
        //End Get Properties
        // display VIN, make, model, year, color 
        /// <summary>
        /// overrides ToString()
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            return ("VIN: "+VIN +", Make: "+ Make+", Model: "+ Model +", Year: "+ Year+ ", Color "+ Color+".");
        }
    }
}

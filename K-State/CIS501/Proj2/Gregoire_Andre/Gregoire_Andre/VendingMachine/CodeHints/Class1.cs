using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VendingMachine
{
    public class Nation
    {
        string name;
        int population;
        DateTime dateTime;
        public Nation(string name, int population)
        {
            this.name = name;
            this.population = population;
            dateTime = DateTime.Now;
        }

        public override string ToString()
        {
            return name + " (" + population + ") : " + dateTime.ToString();
        }
    }
    public class UnitedNations
    {
        List<Nation> nations = new List<Nation>();

        public List<Nation> MakeList()
        {
            nations.Add(new Nation("USA", 300000000));
            nations.Add(new Nation("Japan", 120000000));
            nations.Add(new Nation("China", 900000000));
            return nations;
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VehicleRegistrationCore
{
    [Serializable()] 
    public class Dealer
    {
        string DID, Name, City, State;
        List<Vehicle> LoV = new List<Vehicle>();

        /// <summary>
        /// Dealer Constructor
        /// </summary>
        /// <param name="ID">Dealer ID</param>
        /// <param name="N">Name</param>
        /// <param name="C">City</param>
        /// <param name="S">State</param>
        public Dealer(string ID, string N, string C, string S)
        {
            DID = ID;
            Name = N;
            City = C;
            State = S;
        }
        
        /// <summary>
        /// Add vehicle to dealers list of vehicles
        /// </summary>
        /// <param name="V"></param>
        public void AddVehicle(Vehicle V)
        {
            LoV.Add(V);
        }

        /// <summary>
        /// Remove vehicle from dealers list of vehicles
        /// </summary>
        /// <param name="V"></param>
        /// <returns></returns>
        public bool RemoveVehicle(Vehicle V)
        {
            for (int i = 0; i < LoV.Count; i++)
                if (LoV[i] == V)
                {
                    LoV.RemoveAt(i);
                    return true;
                }
            return false;
        }

        //Get properties
        public string getDID
        {
            get{return DID;}
            set{DID = value;}
        }
        public string getName
        {
            get { return Name; }
            set { Name = value; }
        }
        public string getCity
        {
            get { return City; }
            set { City = value; }
        }
        public string getState
        {
            get { return State; }
            set { State = value; }
        }
        public List<Vehicle> getLoV
        {
            get { return LoV; }
        }
        //end Get properties
        //display DIN, Dealer Name, City, State, and a list of vehicles that the dealer currently possesses
        /// <summary>
        /// overrides ToString()
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            string str = ("Dealer ID: "+DID + ", Name: " + Name + ", City: " + City + ", State: " + State + ", \n Vehicles Owned \n");
            foreach (Vehicle v in LoV)
                str += v.ToString();
            return str;
        }
        

    }
}

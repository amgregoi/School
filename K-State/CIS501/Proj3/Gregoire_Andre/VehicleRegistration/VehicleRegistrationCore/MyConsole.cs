using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VehicleRegistrationCore
{
    public class MyConsole
    {
        //int i;  //for loops
        List<Vehicle> LoV = new List<Vehicle>();    //list of vehicles
        List<Owner> LoO = new List<Owner>();        //list of owners
        List<Dealer> LoD = new List<Dealer>();      //list of dealers

        public List<Vehicle> getLoV
        {
            get { return LoV; }
        }
        public List<Owner> getLoO
        {
            get { return LoO; }
        }
        public List<Dealer> getLoD
        {
            get { return LoD; }
        }

        /// <summary>
        /// returns dealer based on dealer id
        /// </summary>
        /// <param name="did"></param>
        /// <returns></returns>
        public Dealer findDealer(string did)
        {
            Dealer T = LoD.Find(temp => temp.getDID == did);
            return T;
        }
        /*
        public Dealer findDealer(string did)
        {
            for (i = 0; i < LoD.Count; i++)
                if (LoD[i].getDID.Equals(did))
                    return LoD[i];
            return null;
        }*/

        /// <summary>
        /// returns owner based on SSN
        /// </summary>
        /// <param name="ssn"></param>
        /// <returns></returns>
        /// 
        public Owner findOwner(string ssn)
        {
            Owner T = LoO.Find(temp => temp.getSSN == ssn);
            return T;
        }
        /*
        public Owner findOwner(string ssn)
        {
            for (i = 0; i < LoO.Count; i++)
                if (LoO[i].getSSN.Equals(ssn))
                    return LoO[i];
            return null;
        } */

        /// <summary>
        /// returns vehicle based on VIN
        /// </summary>
        /// <param name="vin"></param>
        /// <returns></returns>
        /// 
        public Vehicle findVehicle(string vin)
        {
            Vehicle T = LoV.Find(temp => temp.getVIN == vin);
            return T;
        }
        /*
        public Vehicle findVehicle(string vin)
        {
            for (i = 0; i < LoV.Count; i++)
                if (LoV[i].getVIN.Equals(vin))
                    return LoV[i];
            return null;
        }*/

        /// <summary>
        /// Add vehicle to list
        /// </summary>
        /// <param name="V">Vehicle</param>
        /// <param name="d">Dealer</param>
        public void AddVehicle(Vehicle V, Dealer d)
        {
            LoV.Add(V);
            M2D(d, V);
        }

        /// <summary>
        /// Add deadler to list
        /// </summary>
        /// <param name="D"></param>
        public void addDealer(Dealer D)
        {
            LoD.Add(D);
        }

        /// <summary>
        /// Add owner to list
        /// </summary>
        /// <param name="O"></param>
        public void addOwner(Owner O)
        {
            LoO.Add(O);
        }

        /// <summary>
        /// Removes vehicle from list based on VIN
        /// </summary>
        /// <param name="vin">Vehicle VIN</param>
        /// 

        public void removeVehicle(string vin)
        {
            Vehicle T = LoV.Find(temp => temp.getVIN == vin);
            LoV.Remove(T);    
        }
        /*
        public void removeVehicle(string vin)   //######################################## need to find a way to test if has owner before deleting
        {
            for (i = 0; i < LoV.Count; i++)
                if (LoV[i].getVIN.Equals(vin))
                    LoV.RemoveAt(i);
        }*/

        /// <summary>
        /// Removes owner from list based on SSN
        /// </summary>
        /// <param name="ssn">Owners SSN</param>
        /// 

        public bool removeOwner(string ssn)
        {
            Owner T = LoO.Find(temp => temp.getSSN == ssn);
            if (LoO.Contains(T) && T.getLoV.Count == 0)
            {
                LoO.Remove(T);
                return true;
            }
            return false;
        }
        /*
        public bool removeOwner(string ssn)
        {
            for (i = 0; i < LoO.Count; i++)
                if (LoO[i].getSSN.Equals(ssn))
                    if (LoO[i].getLoV.Count == 0)
                    {
                        LoO.RemoveAt(i);
                        return true;
                    }
            return false;
        } */

        /// <summary>
        /// Removes dealer from list base don DID
        /// </summary>
        /// <param name="did">Dealer ID</param>
        /// 

        public bool removeDealer(string did)
        {
            Dealer T = LoD.Find(temp => temp.getDID == did);
            if (LoD.Contains(T) && T.getLoV.Count == 0)
            {
                LoD.Remove(T);
                return true;
            }
            return false;
        }
        /*
        public bool removeDealer(string did)
        {
            for (i = 0; i < LoD.Count; i++)
                if (LoD[i].getDID.Equals(did))
                    if (LoD[i].getLoV.Count == 0)
                    {
                        LoD.RemoveAt(i);
                        return true;
                    }
            return false;
        }*/

        /// <summary>
        /// handles transfers from dealer to owner
        /// </summary>
        /// <param name="d">Dealer (From)</param>
        /// <param name="o">Owner (To)</param>
        /// <param name="V">Vehicle</param>
        public void D2O(Dealer d, Owner o, Vehicle V, string date, string price, string license)
        {
            if (d.RemoveVehicle(V))
                o.AddVehicle(V, date, price, license);
        }

        /// <summary>
        /// handles transfers from dealer to dealer
        /// </summary>
        /// <param name="d1">Dealer1 (From)</param>
        /// <param name="d2">Dealer2 (To)</param>
        /// <param name="V">Vehicle</param>
        public void D2D(Dealer d1, Dealer d2, Vehicle V, string date, string price)
        {
            if (d1.RemoveVehicle(V))
                d2.AddVehicle(V);
        }

        /// <summary>
        /// handles transfers from owner to owner
        /// </summary>
        /// <param name="o1">Owner1 (From)</param>
        /// <param name="o2">Owner2 (To)</param>
        /// <param name="V">Vehicle</param>
        public void O2O(Owner o1, Owner o2, Vehicle V, string date, string price, string license)
        {
            if (o1.RemoveVehicle(V))
                o2.AddVehicle(V, date, price, license);
        }

        /// <summary>
        /// handles transfers from owner to dealer
        /// </summary>
        /// <param name="o">Owner (From)</param>
        /// <param name="d">Dealer (To)</param>
        /// <param name="V">Vehicle</param>
        public void O2D(Owner o, Dealer d, Vehicle V, string date, string price)
        {
            if (o.RemoveVehicle(V))
                d.AddVehicle(V);
        }

        /// <summary>
        /// handles transfer from Maker to dealer ( used when adding a new vehicle)
        /// </summary>
        /// <param name="d">Dealer (To)</param>
        /// <param name="V">Vehicle</param>
        public void M2D(Dealer d, Vehicle V)
        {
            d.AddVehicle(V);
        }

    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace VehicleRegistrationCore
{
    [Serializable()] 
    public class Owner
    {
         
        string first, last, address, DoB, ssn;   //first/last refer to first and last names
        List<Vehicle> LoV = new List<Vehicle>(); //List of cars

        /// <summary>
        /// Owner Constructor
        /// </summary>
        /// <param name="s">SSN</param>
        /// <param name="f">First Name</param>
        /// <param name="l">Last NAme</param>
        /// <param name="a">Address</param>
        /// <param name="d">Date of Birth</param>
        public Owner(string s, string f, string l, string a, string d)
        {
            ssn = s;
            first = f;
            last = l;
            address = a;
            DoB = d;
        }

        /// <summary>
        /// Adds vehicles to owner list of vehicles
        /// </summary>
        /// <param name="V"></param>
        public void AddVehicle(Vehicle V, string date, string price, string license)
        {
            LoV.Add(V);
            V.newOwner(this, date, price, license);
        }

        /// <summary>
        /// Removes vehicle from owner list of vehicles
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

        //Get Properties
        public string getSSN
        {
            get { return ssn; }
            set { ssn = value; }
        }
        public string getFirstName
        {
            get { return first; }
            set { first = value; }
        }
        public string getLastName
        {
            get { return last; }
            set { last = value; }
        }
        public string getAddress
        {
            get { return address; }
            set { address = value; }
        }
        public string getDOB
        {
            get { return DoB; }
            set { DoB = value; }
        }
        public List<Vehicle> getLoV
        {
            get { return LoV; }
        }
        //End Get properties
        // display SSN, first name, last name, address and birth date
        /// <summary>
        /// Override ToString()
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            return ("SSN: "+ssn+", First Name: "+first+", Last Name: "+last+", Address: "+address+", Birth Date: "+DoB+".");
        }
    }

}

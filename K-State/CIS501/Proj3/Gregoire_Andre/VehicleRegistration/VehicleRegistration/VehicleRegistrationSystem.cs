using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using VehicleRegistrationCore;

namespace VehicleRegistration
{
    public partial class VehicleRegistrationSystem : Form
    {
        public MyConsole con = new MyConsole();
        public VehicleRegistrationSystem()
        {
            InitializeComponent();
        }

        private void bnDone_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void bnRegDealer_Click(object sender, EventArgs e)
        {
            DealerRegistrationDialogbox drd = new DealerRegistrationDialogbox();
            if (drd.ShowDialog() != DialogResult.OK) return;
            else
            {
                Dealer d = new Dealer(drd.DealerID, drd.DealerName, drd.DealerCity, drd.DealerState);
                con.addDealer(d);
            }
        }

        private void bnRegVehicle_Click(object sender, EventArgs e)
        {
            VehicleRegistrationDialogbox vrd = new VehicleRegistrationDialogbox();
            if (vrd.ShowDialog() != DialogResult.OK) return;
            else
            {
                Vehicle v = new Vehicle(vrd.VIN, vrd.Make, vrd.Model, vrd.Color, vrd.InitialDealerID, vrd.Year);
                con.AddVehicle(v, con.findDealer(v.getDID));
            }

        }

        private void bnRegOwner_Click(object sender, EventArgs e)
        {
            OwnerRegistrationDialogbox ord = new OwnerRegistrationDialogbox();
            if (ord.ShowDialog() != DialogResult.OK) return;
            else
            {
                Owner o = new Owner(ord.SSN, ord.FirstName, ord.LastName, ord.Address, ord.BirthDate);
                con.addOwner(o);
            }
           
        }

        private void bnDeleteDealer_Click(object sender, EventArgs e)
        {
            LocateDealerDialogbox ldd = new LocateDealerDialogbox();
            if (ldd.ShowDialog() != DialogResult.OK) return;
            else
            {
                if (con.removeDealer(ldd.DealerID)) return;
                MessageBox.Show("Dealer not found or Dealer still has vehicles");
            }
        }

        private void bnDeleteVehicle_Click(object sender, EventArgs e)
        {
            LocateVehicleDialogbox lvd = new LocateVehicleDialogbox();
            if (lvd.ShowDialog() != DialogResult.OK) return;
            else
            {
                con.removeVehicle(lvd.VIN);
            }
        }

        private void bnDeleteOwner_Click(object sender, EventArgs e)
        {
            LocateOwnerDialogbox lod = new LocateOwnerDialogbox();
            if (lod.ShowDialog() != DialogResult.OK) return;
            else
            {
                if (con.removeOwner(lod.SSN)) return;
                MessageBox.Show("Owner not found or Owner still has vehicles");
            }
        }

        private void bnListVehicles_Click(object sender, EventArgs e)
        {
            ListDialog ld = new ListDialog();
            //ld.AddDisplayItems(/* pass object[] */);
            object[] obj = con.getLoV.ToArray();
            ld.AddDisplayItems(obj);
            ld.ShowDialog();
        }

        private void bnListOwners_Click(object sender, EventArgs e)
        {
            ListDialog ld = new ListDialog();
            //ld.AddDisplayItems(/* pass object[] */);
            object[] obj = con.getLoO.ToArray();
            ld.AddDisplayItems(obj);
            ld.ShowDialog();
        }

        private void bnListDealers_Click(object sender, EventArgs e)
        {
            ListDialog ld = new ListDialog();
            //ld.AddDisplayItems(/* pass object[]*/);
            object[] obj = con.getLoD.ToArray();
            ld.AddDisplayItems(obj);
            ld.ShowDialog();
        }

        private void bnSave_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "VRS Files|*.vrs";
            saveFileDialog.AddExtension = true;
            saveFileDialog.InitialDirectory = Application.StartupPath;
            if (saveFileDialog.ShowDialog() == DialogResult.OK)
            {
                System.IO.FileStream f = new System.IO.FileStream(saveFileDialog.FileName,
                    System.IO.FileMode.Create);
                System.Runtime.Serialization.Formatters.Binary.BinaryFormatter fo = new
                    System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();               
            }
        }

        private void bnRestore_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "VRS Files|*.vrs";
            openFileDialog.InitialDirectory = Application.StartupPath;
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                System.IO.FileStream f = new System.IO.FileStream(openFileDialog.FileName,
                    System.IO.FileMode.OpenOrCreate, System.IO.FileAccess.Read);
                System.Runtime.Serialization.Formatters.Binary.BinaryFormatter fo = new
                 System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
                
  
            }
        }

        private void bnTransfer_Click(object sender, EventArgs e)
        {
            OwnershipTransferDialogbox otd = new OwnershipTransferDialogbox();
            if (otd.ShowDialog() != DialogResult.OK) return;
            else
            {
                if (otd.TransferFromDealer && otd.TransferToDealer)
                    TransferDealerToDealer(otd);
                else if (otd.TransferFromDealer && otd.TransferToPrivateOwner)
                    TransferDealerToOwner(otd);
                else if (otd.TransferFromPrivateOwner && otd.TransferToPrivateOwner)
                    TransferOwnerToOwner(otd);
                else if (otd.TransferFromPrivateOwner && otd.TransferToDealer)
                    TransferOwnerToDealer(otd);
            }
        }

        private void bnListOwnedVehicles_Click(object sender, EventArgs e)
        {
            ListDialog ld = new ListDialog();
            LocateOwnerDialogbox lod = new LocateOwnerDialogbox();
            if (lod.ShowDialog() != DialogResult.OK) return;
            ListOwnedVehicles(ld, lod);
            
           
        }

        private void ListOwnerHistory_Click(object sender, EventArgs e)
        {
            LocateVehicleDialogbox lvd = new LocateVehicleDialogbox();
            if (lvd.ShowDialog() != DialogResult.OK) return;
            ListOwnerHistory(lvd);
            
        }


        private void bnLoad_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "VRS Info Files|*.inf";
            openFileDialog.InitialDirectory = Application.StartupPath;
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {

                TextReader trs = new StreamReader(openFileDialog.FileName);
                string s;
                List<string> words;
                int stringIndex;
                while (((s = trs.ReadLine()) != null) && (s != ""))
                {
                    words = new List<string>();
                    while (true)
                    {
                        if ((stringIndex = s.IndexOf('"')) == -1) break;
                        s = s.Substring(stringIndex + 1);
                        
                        stringIndex = s.IndexOf('"');
                        words.Add(s.Substring(0, stringIndex));
                        s = s.Substring(stringIndex + 1);
                    }
                    if (words.Count == 0) continue;
                    else if (words[0].Equals("RegisterDealer")) LoadRegisterDealer(words);
                    else if (words[0].Equals("RegisterOwner")) LoadRegisterOwner(words);
                    else if (words[0].Equals("RegisterVehicle")) LoadRegisterVehicle(words);
                    else if (words[0].Equals("TransferD2O")) LoadTransferDealerToOwner(words);  
                    else if (words[0].Equals("TransferD2D")) LoadTransferDealerToDealer(words);
                    else if (words[0].Equals("TransferO2O")) LoadTransferOwnerToOwner(words);
                    else if (words[0].Equals("TransferO2D")) LoadTransferOwnerToDealer(words);
                    else if (words[0].Equals("ListOwnersOfVehicle")) LoadListOwnersOfVehicle(words);
                    else if (words[0].Equals("ListDealers")) bnListDealers.PerformClick();
                    else if (words[0].Equals("ListVehiclesOfOwner")) LoadListVehiclesOfOwner(words);
                    // Add your logic
                }

            }
        }//end Load Button

        // The rest are Refactoring Methods 
        private void LoadRegisterDealer(List<string> words)
        {
            con.addDealer(new Dealer(words[1], words[2], words[3], words[4]));
        }

        private void LoadRegisterOwner(List<string> words)
        {
            con.addOwner(new Owner(words[1], words[2], words[3], words[4], words[5]));
        }

        private void LoadRegisterVehicle(List<string> words)
        {
            con.AddVehicle(new Vehicle(words[1], words[2], words[3], words[5], words[6], words[4]), con.findDealer(words[6]));
        }

        private void LoadTransferDealerToOwner(List<string> words)
        {
            con.D2O(con.findDealer(words[1]), con.findOwner(words[2]), con.findVehicle(words[3]), words[4], words[5], words[6]);
        }

        private void LoadTransferDealerToDealer(List<string> words)
        {
            con.D2D(con.findDealer(words[1]), con.findDealer(words[2]), con.findVehicle(words[3]), words[4], words[5]);
        }

        private void LoadTransferOwnerToOwner(List<string> words)
        {
            con.O2O(con.findOwner(words[1]), con.findOwner(words[2]), con.findVehicle(words[3]), words[4], words[5], words[6]);
        }

        private void LoadTransferOwnerToDealer(List<string> words)
        {

            con.O2D(con.findOwner(words[1]), con.findDealer(words[2]), con.findVehicle(words[3]), words[4], words[5]);
        }
        private void TransferOwnerToDealer(OwnershipTransferDialogbox otd)
        {
            con.O2D(con.findOwner(otd.FromSSN), con.findDealer(otd.ToDealerID), con.findVehicle(otd.VIN), otd.Date, otd.Price);
        }

        private void TransferOwnerToOwner(OwnershipTransferDialogbox otd)
        {
            con.O2O(con.findOwner(otd.FromSSN), con.findOwner(otd.ToSSN), con.findVehicle(otd.VIN), otd.Date, otd.Price, otd.LicenceNumber);
        }

        private void TransferDealerToOwner(OwnershipTransferDialogbox otd)
        {
            con.D2O(con.findDealer(otd.FromDealerID), con.findOwner(otd.ToSSN), con.findVehicle(otd.VIN), otd.Date, otd.Price, otd.LicenceNumber);
        }

        private void TransferDealerToDealer(OwnershipTransferDialogbox otd)
        {
            con.D2D(con.findDealer(otd.FromDealerID), con.findDealer(otd.ToDealerID), con.findVehicle(otd.VIN), otd.Date, otd.Price);
        }
        private void ListOwnedVehicles(ListDialog ld, LocateOwnerDialogbox lod)
        {
            object[] obj;
            object[] obj2 = new object[1];
            foreach (Owner o in con.getLoO)
            {
                if (o.getSSN.Equals(lod.SSN))
                {
                    obj2[0] = o.ToString();
                    ld.AddDisplayItems(obj2);
                    obj = o.getLoV.ToArray();
                    ld.AddDisplayItems(obj);
                }
            }
            ld.ShowDialog();
        }
        private void ListOwnerHistory(LocateVehicleDialogbox lvd)
        {
            ListDialog ld = new ListDialog();
            object[] obj;
            object[] obj2 = new object[1];
            foreach (Vehicle v in con.getLoV)
            {
                if (v.getVIN.Equals(lvd.VIN))
                {
                    obj2[0] = v.ToString();
                    ld.AddDisplayItems(obj2);
                    obj = v.getHistory.ToArray();
                    ld.AddDisplayItems(obj);
                }
            }
            ld.ShowDialog();
        }
        private void LoadListVehiclesOfOwner(List<string> words)
        {
            ListDialog ld = new ListDialog();
            object[] obj;
            object[] obj2 = new object[1];
            foreach (Owner o in con.getLoO)
            {
                if (o.getSSN.Equals(words[1]))
                {
                    obj2[0] = o.ToString();
                    ld.AddDisplayItems(obj2);
                    obj = o.getLoV.ToArray();
                    ld.AddDisplayItems(obj);
                }
            }
            ld.ShowDialog();
        }
        private void LoadListOwnersOfVehicle(List<string> words)
        {
            ListDialog ld = new ListDialog();
            object[] obj;
            object[] obj2 = new object[1];
            foreach (Vehicle v in con.getLoV)
            {
                if (v.getVIN.Equals(words[1]))
                {
                    obj2[0] = v.ToString();
                    ld.AddDisplayItems(obj2);
                    obj = v.getHistory.ToArray();
                    ld.AddDisplayItems(obj);
                }
            }
            ld.ShowDialog();
        }
    }
}

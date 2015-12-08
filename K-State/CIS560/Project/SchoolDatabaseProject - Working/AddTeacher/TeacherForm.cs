using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace AddTeacher
{
    public partial class TeacherForm : Form
    {
        public TeacherForm()
        {
            InitializeComponent();
        }

        MySqlConnection myConnect;
        Dictionary<String, String> idVals;
        Dictionary<String, String> reverse = new Dictionary<String, String>();
        int tid;
        public TeacherForm(MySqlConnection connect, Dictionary<String, String> dict, int id, MySqlDataReader r) : this()
        {
            r.Close();
            myConnect = connect;
            idVals = dict;
            tid = id;
            schoolDropBox.Items.Add((object)"Select School");
            orgDropBox.Items.Add((object)"Select Organization");
            String[] degree = { "Select Degree", "N/A", "BS", "MS", "PHD" };
            degreeDropBox.Items.AddRange(degree.Cast<object>().ToArray());
            for (int i = 0; i < 999; i++)       //checks dictionary for schools (school ids start at 0-999)
            {
                if (idVals.ContainsKey(i.ToString()))
                {
                    String tmp; idVals.TryGetValue(i.ToString(), out tmp);
                    schoolDropBox.Items.Add((object)tmp);
                    reverse.Add(tmp, i.ToString());
                }
            }
            for (int i = 1000; i < 1999; i++)
            {
                if (idVals.ContainsKey(i.ToString()))
                {
                    String tmp; idVals.TryGetValue(i.ToString(), out tmp);
                    orgDropBox.Items.Add((object)tmp);
                    reverse.Add(tmp, i.ToString());
                }
            }
            schoolDropBox.SelectedIndex = 0;
            degreeDropBox.SelectedIndex = 0;
            orgDropBox.SelectedIndex = 0;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MySqlCommand add = new MySqlCommand("INSERT INTO Teacher (tid, name, degree, phone, office_hours, schoolid, oid) VALUES (@p1, @p2, @p3, @p4, @p5, @p6, @p7)", myConnect);

            //INSERT PARAMETERS
            add.Parameters.AddWithValue("@p1", tid+1);
            add.Parameters.AddWithValue("@p2", nameBox.Text);
            add.Parameters.AddWithValue("@p3", degreeDropBox.SelectedItem.ToString());
            add.Parameters.AddWithValue("@p4", phoneBox.Text);
            add.Parameters.AddWithValue("@p5", officeHoursBox.Text);
            String school; reverse.TryGetValue(schoolDropBox.SelectedItem.ToString(), out school);
            add.Parameters.AddWithValue("@p6", school);
            String oid; reverse.TryGetValue(orgDropBox.SelectedItem.ToString(), out oid);
            add.Parameters.AddWithValue("@p7", oid);

            try
            {
                add.ExecuteNonQuery();
                Application.ExitThread();
            }
            catch (MySqlException ex) { Console.Out.WriteLine(ex.ToString()); }
            
        }


    }
}

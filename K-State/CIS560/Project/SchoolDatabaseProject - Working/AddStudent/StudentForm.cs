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

namespace AddStudent
{
    public partial class StudentForm : Form
    {
        public StudentForm()
        {
            InitializeComponent();
        }

        MySqlConnection myConnect;
        Dictionary<String, String> idVals;
        Dictionary<String, String> schools = new Dictionary<string,string>();
        int sid;
        public StudentForm(MySqlConnection connect, Dictionary<String, String> dict, int id, MySqlDataReader r) : this()
        {
            r.Close();
            myConnect = connect;
            idVals = dict;
            sid = id;
            schoolDropBox.Items.Add((object)"Select School");
            schoolDropBox.SelectedIndex = 0;
            for (int i = 0; i < 999; i++)       //checks dictionary for schools (school ids start at 0-999)
            {
                if (idVals.ContainsKey(i.ToString()))
                {
                    String tmp; idVals.TryGetValue(i.ToString(), out tmp);
                    schoolDropBox.Items.Add((object)tmp);
                    schools.Add(tmp, i.ToString());
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {

            MySqlCommand add = new MySqlCommand("INSERT INTO Student (sid, name, phone, grade, schoolid, gpa) VALUES (@p1, @p2, @p3, @p4, @p5, @p6)", myConnect);
            add.Parameters.AddWithValue("@p1", sid + 1);
            add.Parameters.AddWithValue("@p2", nameBox.Text);
            add.Parameters.AddWithValue("p3", phoneBox.Text);
            add.Parameters.AddWithValue("@p4", Convert.ToInt32(gradeBox.Text));
            String school; schools.TryGetValue(schoolDropBox.SelectedItem.ToString(), out school);
            add.Parameters.AddWithValue("@p5", Convert.ToInt32(school));
            add.Parameters.AddWithValue("@p6", Convert.ToDouble(gpaBox.Text));
            try
            {
                add.ExecuteNonQuery();
            }
            catch (MySqlException ex) { Console.Out.WriteLine(ex.ToString()); }
            Application.ExitThread();
        }
    }
}

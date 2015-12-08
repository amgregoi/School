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

namespace StudentCard
{
    public partial class Student : Form
    {
        public Student()
        {
            InitializeComponent();
        }
        public Student(String name, String phone, String ID, String SchoolName, MySqlDataReader r):this()
        {
            nameLabel.Text = name;
            phoneLabel.Text = phone;
            label7.Text = SchoolName;
            idLabel.Text = ID;
            r.Close();
        }

        private void newStudent()
        {

        }
    }
}

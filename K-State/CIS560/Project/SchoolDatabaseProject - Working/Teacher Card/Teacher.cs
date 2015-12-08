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

namespace TeacherCard
{
    public partial class Teacher : Form
    {
        public Teacher()
        {
            InitializeComponent();
        }

        public Teacher(String name, String phone, String schoolid, String schoolName, String advisor, String officeH, String tid, MySqlDataReader r):this()
        {
            nameLabel.Text = name;
            phoneLabel.Text = phone;
            schoolIdLabel.Text = schoolid;
            schoolLabel.Text = schoolName;
            advisorLabel.Text = advisor;
            officeHoursLabel.Text = officeH;
            idLabel.Text = tid;
            r.Close();
        }
    }
}

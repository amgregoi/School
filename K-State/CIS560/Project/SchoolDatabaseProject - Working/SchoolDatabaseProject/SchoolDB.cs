using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.Runtime.InteropServices;
using StudentCard;
using TeacherCard;
using AddStudent;
using AddTeacher;

using MySql.Data.MySqlClient;

namespace SchoolDatabaseProject
{
    public partial class SchoolDB : Form
    {
        public SchoolDB()
        {
            InitializeComponent();
            init();
        }

        #region VARIABLES

            private MySqlConnection myConnection;
            private Dictionary<String, MySqlCommand> queryDict;
            private Dictionary<String, int> idValues;
            private Dictionary<String, String> reverseIdValues;
            private String dropDownParameter;
            private String dropDownParameter2;
            private String cardName;
            private String lastQuery;

        #endregion

        #region SETUP FUNCTIONS

            /// <summary>
            /// Initializse database connection and setups up GUI defaults/info
            /// </summary>
            private void init()
            {
                queryDict = new Dictionary<String, MySqlCommand>();
                idValues = new Dictionary<String, int>();
                reverseIdValues = new Dictionary<string, string>();
                listBox1.ContextMenuStrip = null;
                try
                {
                    myConnection = new MySqlConnection("user id=amgregoi;password=gregoire;server=mysql.cis.ksu.edu;database=amgregoi;connection timeout=10");
                    myConnection.Open();

                    loadQueries();
                    processQuery("getTeacherIds", null);
                    processQuery("getClubIds", null);
                    processQuery("getClassIds", null);
                    processQuery("getStudentIds", null);
                    processQuery("getSchoolIds", null);

                    /* setup drop boxes */
                    
                }
                catch (Exception e) {
                    Console.WriteLine(e.ToString());
                    MessageBox.Show("ERROR: connection to database");
                    Thread.CurrentThread.Abort();
                }
                resetQueryBoxes();
            }

            /// <summary>
            /// Loads queries into dicitonary (prepared statements)
            /// </summary>
            private void loadQueries()
            {
                /* Student Queries */
                String QS1 = "Class info";
                MySqlCommand Q1 = new MySqlCommand("SELECT * FROM Classes WHERE cid = @param1", myConnection);
                Q1.Prepare();
                queryDict.Add(QS1, Q1);

                String QS2 = "Student Schedule";
                MySqlCommand Q2 = new MySqlCommand("SELECT c.cname, c.cid FROM Classes c, Student s, Attend a WHERE s.sid = a.sid AND c.cid = a.cid AND s.sid = @param1", myConnection);
                Q2.Prepare();
                queryDict.Add(QS2, Q2);

                String QS3 = "Student info";
                MySqlCommand Q3 = new MySqlCommand("SELECT * FROM Student s WHERE s.sid = @param1", myConnection);
                Q3.Prepare();
                queryDict.Add(QS3, Q3);

                /* Teacher Queries */
                String QT1 = "List of classes";
                MySqlCommand Q4 = new MySqlCommand("SELECT t.name, c.cname, c.description, t.office_hours FROM Classes c, Teacher t, Teaches t1 WHERE c.cid = t1.cid AND t.tid = t1.tid AND t.tid = @param1", myConnection);
                Q4.Prepare();
                queryDict.Add(QT1, Q4);

                String QT2 = "Teacher information";
                MySqlCommand Q5 = new MySqlCommand("SELECT t.name, t.phone, t.schoolid, t.office_hours, t.tid, t.oid, t.degree FROM Teacher t WHERE t.tid = @param1", myConnection);
                Q5.Prepare();
                queryDict.Add(QT2, Q5);


                /* School Queries */
                String QSC1 = "List of students by school";
                MySqlCommand Q6 = new MySqlCommand("SELECT s.name, s.gpa, s.phone FROM Student s WHERE s.schoolid = @param1 ORDER BY s.grade DESC", myConnection);
                Q6.Prepare();
                queryDict.Add(QSC1, Q6);
	
                String QSC2 = "List of students in organization";
                MySqlCommand Q7 = new MySqlCommand("SELECT t.name, t.gpa FROM (SELECT s.name, s.gpa, p.oid FROM Student s, Participate p WHERE s.sid = p.sid)t WHERE t.oid = @param1 ORDER BY t.gpa ASC", myConnection);
                Q7.Prepare();
                queryDict.Add(QSC2, Q7);

                /* Misc Queries */

                String QM1 = "List Teachers";
                MySqlCommand Q8 = new MySqlCommand("SELECT t.name FROM Teacher t, School s WHERE t.schoolid = s.schoolid AND s.schoolid = @param1", myConnection);
                Q8.Prepare();
                queryDict.Add(QM1, Q8);

                String QM2 = "getClubIds";
                MySqlCommand Q9 = new MySqlCommand("SELECT c.name, c.oid FROM Organization c", myConnection);
                Q9.Prepare();
                queryDict.Add(QM2, Q9);

                String QM3 = "getTeacherIds";
                MySqlCommand Q10 = new MySqlCommand("SELECT t.name, t.tid FROM Teacher t", myConnection);
                Q10.Prepare();
                queryDict.Add(QM3, Q10); 
        
                String QM4 = "getClassIds";
                MySqlCommand Q11 = new MySqlCommand("SELECT c.cname, c.cid FROM Classes c", myConnection);
                Q11.Prepare();
                queryDict.Add(QM4, Q11);

                String QM5 = "getStudentIds";
                MySqlCommand Q12 = new MySqlCommand("SELECT s.name, s.sid FROM Student s", myConnection);
                Q12.Prepare();
                queryDict.Add(QM5, Q12);

                String QM6 = "getSchoolIds";
                MySqlCommand Q13 = new MySqlCommand("SELECT s.name, s.schoolid FROM School s", myConnection);
                Q13.Prepare();
                queryDict.Add(QM6, Q13);

                String QM7 = "getStudentsDropBox";
                MySqlCommand Q14 = new MySqlCommand("SELECT s.name FROM Student s WHERE s.schoolid = @param1", myConnection);
                Q14.Prepare();
                queryDict.Add(QM7, Q14);
            }

            /// <summary>
            /// returns ID value for string that is passed in
            /// </summary>
            private int getIdFromString(String str)
            {
                int ret = -1;
                try{            
                if (idValues.ContainsKey(str))
                    idValues.TryGetValue(str, out ret);
                }
                catch (ArgumentNullException e) { Console.Out.WriteLine(e.ToString()); };
                return ret;
            }

            /// <summary>
            /// returns String for the id value that is passed in
            /// </summary>
            private String getStringFromId(String id)
            {
                String ret = null;
                try
                {
                    if (reverseIdValues.ContainsKey(id))
                        reverseIdValues.TryGetValue(id, out ret);
                }
                catch (ArgumentNullException e) { Console.Out.WriteLine(e.ToString()); };
                return ret;
            }

            /// <summary>
            /// puts paramters into selected query, exectues the query, and places information into the gui
            /// </summary>
            private void processQuery(String queryName, String x)
        {
            MySqlCommand query = null;
            MySqlDataReader reader;
            List<String> tmp = new List<String>();

            switch (queryName)
            {
                case "Class info":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", getIdFromString(x));
                        reader = query.ExecuteReader(); 
                        while (reader.Read())
                            tmp.Add(reader["name"].ToString());
                        listBox2.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "Student Schedule":
                   #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        String tmp2 = studentDropBox.SelectedItem.ToString();
                        int id = Convert.ToInt32(getIdFromString(tmp2));
                        query.Parameters.AddWithValue("@param1", id);
                        reader = query.ExecuteReader();
                        tmp.Add(studentDropBox.SelectedItem.ToString()+"s School Schedule:");
                        while (reader.Read())
                        {
                            tmp.Add(("\tCID: " + reader["cid"].ToString()).PadRight(15) + "Class Name: " + reader["cname"].ToString());
                        }
                        listBox1.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "Student info":
                    #region

                    #endregion
                    break;
                case "List of classes":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", getIdFromString(x));
                        reader = query.ExecuteReader();
                        tmp.Add("Classes taught by "+dropDownParameter);
                        while (reader.Read())
                            tmp.Add("\t" + reader["cname"].ToString());
                        listBox2.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "Teacher information":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", getIdFromString(x));
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            tmp.Add("Name: " + reader["name"].ToString() + "\tDegree: " + reader["degree"].ToString() + " " + "\tPhone: " + reader["phone"].ToString());
                            tmp.Add("\tOffice Hours: " + reader["office_hours"].ToString());
                        }
                        reader.Close();
                        listBox2.Items.AddRange(tmp.Cast<object>().ToArray());
                    #endregion
                    break;
                case "List of students by school":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", x);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            //String test = "name: " + reader["name"].ToString();
                            tmp.Add(("Name: " + reader["name"].ToString()));//.PadRight(25)));
                        }
                        reader.Close();
                        listBox1.Items.AddRange(tmp.Cast<object>().ToArray());
                    #endregion
                    break;
                case "List of students in organization":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", getIdFromString(x));
                        reader = query.ExecuteReader();
                        while (reader.Read())
                            tmp.Add(("Name: " + reader["name"].ToString()));//.PadRight(25));
                        reader.Close();
                        listBox1.Items.AddRange(tmp.Cast<object>().ToArray());
                    #endregion
                    break;
                case "List Teachers":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", Convert.ToInt32(x));
                        reader = query.ExecuteReader();
                        while (reader.Read())
                            tmp.Add("Name: " + reader["name"].ToString());
                        listBox1.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "getClubIds":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            idValues.Add(reader["name"].ToString(), Convert.ToInt32(reader["oid"].ToString()));
                            reverseIdValues.Add(reader["oid"].ToString(), reader["name"].ToString());
                        }
                        reader.Close();
                    #endregion
                    break;
                case "getTeacherIds":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            idValues.Add(reader["name"].ToString(), Convert.ToInt32(reader["tid"].ToString()));
                            tmp.Add(reader["name"].ToString());
                        }
                        teacherDropBox.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "getClassIds":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            //idValues.Add(reader["cname"].ToString(), Convert.ToInt32(reader["cid"].ToString()));
                            tmp.Add(reader["cid"].ToString() + " : " + reader["cname"].ToString());
                        }
                        classDropBox.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;
                case "getStudentIds":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                            idValues.Add(reader["name"].ToString(), Convert.ToInt32(reader["sid"].ToString()));
                        reader.Close();
                    #endregion
                    break;
                case "getSchoolIds":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        reader = query.ExecuteReader();
                        while (reader.Read())
                        {
                            idValues.Add(reader["name"].ToString(), Convert.ToInt32(reader["schoolid"].ToString()));
                            reverseIdValues.Add(reader["schoolid"].ToString(), reader["name"].ToString());
                        }
                        reader.Close();
                    #endregion
                    break;
                case "getStudentsDropBox":
                    #region
                        queryDict.TryGetValue(queryName, out query);
                        query.Parameters.Clear();
                        query.Parameters.AddWithValue("@param1", Convert.ToInt32(x));
                        reader = query.ExecuteReader();
                        tmp.Add("Choose Student");
                        while (reader.Read())
                        {
                            tmp.Add(reader["name"].ToString());
                        }
                        studentDropBox.Items.AddRange(tmp.Cast<object>().ToArray());
                        reader.Close();
                    #endregion
                    break;                    
                default:
                    return;
            
            }
            try
            {
                query.Parameters.Remove(getIdFromString(x));
            }
            catch (Exception e) { Console.Out.WriteLine(e.ToString()); };
        }

        #endregion

        #region SCHOOL TAB FUNCTIONS

            /// <summary>
            /// Activates items on the gui depending on the selected item
            /// of the drop down box
            /// </summary>
            private void queryDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                if (queryDropBox.SelectedIndex != 0)
                {
                    listBox1.ContextMenuStrip = null;
                    lastQuery = queryDropBox.SelectedItem.ToString();
                    if (lastQuery.ToLower().Contains("school"))
                    {
                        schoolDropBox.Visible = true;
                        organizationDropBox.SelectedIndex = 0;
                        organizationDropBox.Visible = false;
                    }
                    else if (lastQuery.ToLower().Contains("organization"))
                    {
                        organizationDropBox.Visible = true;
                        schoolDropBox.SelectedIndex = 0;
                        schoolDropBox.Visible = false;
                    }
                    else if (lastQuery.ToLower().Contains("teacher"))
                    {
                        schoolDropBox.Visible = true;
                        organizationDropBox.SelectedIndex = 0;
                        organizationDropBox.Visible = false;
                    }
                    else if (lastQuery.ToLower().Contains("student"))
                    {
                        schoolDropBox.Visible = true;
                        organizationDropBox.SelectedIndex = 0;
                        organizationDropBox.Visible = false;
                    }
                }
                else
                {
                    schoolDropBox.Visible = false;
                    organizationDropBox.Visible = false;
                }
            }

            /// <summary>
            /// sets dropDownParameter to selected item of schoolDropBox
            /// </summary>
            private void schoolDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                dropDownParameter = schoolDropBox.SelectedItem.ToString();
                if (schoolDropBox.SelectedIndex != 0 && queryDropBox.SelectedIndex == 4)
                {
                    studentDropBox.Items.Clear();
                    studentDropBox.Visible = true;
                    processQuery("getStudentsDropBox", schoolDropBox.SelectedItem.ToString());
                    studentDropBox.SelectedIndex = 0;
                }
                else
                {
                    studentDropBox.Visible = false;
                }
            }

            /// <summary>
            /// sets dropDownParameter to selected item of orgainzationDropBox
            /// </summary>
            private void organizationDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                dropDownParameter = organizationDropBox.SelectedItem.ToString();
            }

            /// <summary>
            /// Calls processQuery to run a query based on the users input
            /// </summary>
            private void queryButton_Click(object sender, EventArgs e)
        {
            if (dropDownParameter != null)
            {
                
                try
                {
                    if (studentDropBox.Visible && studentDropBox.SelectedIndex == 0)
                        throw new Exception("Need to fill in student drop box");
                    listBox1.Items.Clear();
                    processQuery(queryDropBox.SelectedItem.ToString(), dropDownParameter);
                    resetQueryBoxes();
                    
                }
                catch (Exception ex) { Console.Out.WriteLine(ex.ToString()); }
            }
        }


            /// <summary>
            /// handles click events on listbox under school tab
            /// </summary>
            private void listBox1_MouseDoubleClick_2(object sender, MouseEventArgs e)
            {
                try
                {
                    String selected = listBox1.SelectedItem.ToString();
                    if (lastQuery.ToLower().Contains("student"))
                    {
                        //int x = selected.IndexOf('\t');
                        cardName = selected.Substring(6);

                        Thread thread = new Thread(new ThreadStart(this.StudentCard));
                        thread.Start();
                    }
                    else if (lastQuery.ToLower().Contains("teacher"))
                    {
                        // implement teacher card popup
                        //int x = selected.IndexOf('\t');
                        cardName = selected.Substring(6);
                        Thread thread = new Thread(new ThreadStart(this.TeacherCard));
                        thread.Start();

                    }

                }
                catch (Exception ex) { Console.Out.WriteLine(ex.ToString()); };
            }

        #endregion

        #region TEACHER TAB FUNCTIONS

            /// <summary>
            /// Activates items on the gui depending on the selected item
            /// of the drop down box
            /// </summary>
            private void queryDropBox2_SelectedIndexChanged(object sender, EventArgs e)
            {
                if (queryDropBox2.SelectedIndex != 0)
                {
                    lastQuery = queryDropBox2.SelectedItem.ToString();
                    if (lastQuery.ToLower().Contains("teach"))
                    {
                        teacherDropBox.Visible = true;
                        classDropBox.SelectedIndex = 0;
                        classDropBox.Visible = false;
                    }
                    else if (lastQuery.ToLower().Contains("class"))
                    {
                        //classDropBox.Visible = true;
                        teacherDropBox.SelectedIndex = 0;
                        teacherDropBox.Visible = true;
                    }
                }
                else
                {
                    classDropBox.Visible = false;
                    teacherDropBox.Visible = false;
                }
            }
            
            /// <summary>
            /// Calls processQuery to run a query based on the users input
            /// </summary>
            private void queryButton2_Click(object sender, EventArgs e)
            {
                try
                {
                    listBox2.Items.Clear();
                    processQuery(queryDropBox2.SelectedItem.ToString(), dropDownParameter);
                    if(teacherDropBox.Visible && teacherDropBox.SelectedIndex == 0)
                        throw new ArgumentNullException("Fill in teacher drop box");
                    resetQueryBoxes();
                }
                catch (ArgumentNullException ex) { Console.Out.WriteLine(ex.ToString()); }
            }

            /// <summary>
            /// sets dropDownParameter to selected item of schoolDropBox
            /// </summary>
            private void teacherDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                dropDownParameter = teacherDropBox.SelectedItem.ToString();
            }

            /// <summary>
            /// event handler for class drop box
            /// </summary>
            private void classDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                dropDownParameter = teacherDropBox.SelectedItem.ToString();
            }

            /// <summary>
            /// listBox2 double click event handler
            /// </summary>
            private void listBox2_MouseDoubleClick(object sender, MouseEventArgs e)
            {
                try
                {
                    String selected = listBox2.SelectedItem.ToString();
                    if (lastQuery.ToLower().Contains("student"))
                    {
                        int x = selected.IndexOf('\t');
                        cardName = selected.Substring(6, x - 6);

                        Thread thread = new Thread(new ThreadStart(this.StudentCard));
                        thread.Start();
                    }
                    else if (lastQuery.ToLower().Contains("teacher"))
                    {
                        // implement teacher card popup
                        int x = selected.IndexOf('\t');
                        cardName = selected.Substring(6, x - 6);
                        Thread thread = new Thread(new ThreadStart(this.TeacherCard));
                        thread.Start();
                    }

                }
                catch (Exception ex) { Console.Out.WriteLine(ex.ToString()); };
            }
        
        #endregion

        #region MISC FUNCTIONS

            /// <summary>
            /// resets GUI to default values
            /// </summary>
            private void resetQueryBoxes()
            {
                queryDropBox.SelectedIndex = 0;
                queryDropBox2.SelectedIndex = 0;
                organizationDropBox.SelectedIndex = 0;
                teacherDropBox.SelectedIndex = 0;
                schoolDropBox.SelectedIndex = 0;
                classDropBox.SelectedIndex = 0;
                schoolDropBox.Visible = false;
                organizationDropBox.Visible = false;
                teacherDropBox.Visible = false;
                studentDropBox.Visible = false;
                classDropBox.Visible = false;
                //dropDownParameter = null;
            }

            /// <summary>
            /// closes application
            /// </summary>
            private void exitToolStripMenuItem_Click(object sender, EventArgs e)
            {
                this.Close();
            }

            /// <summary>
            /// Opens up student card in new thread
            /// </summary>
            private void StudentCard()
            {
                MySqlCommand query = null;
                MySqlDataReader reader = null;
                try
                {
                    queryDict.TryGetValue("Student info", out query);
                    query.Parameters.Clear();
                    query.Parameters.AddWithValue("@param1", getIdFromString(cardName));
                    reader = query.ExecuteReader();
                    reader.Read();
                    Application.Run(new Student(cardName, reader["phone"].ToString(), reader["schoolid"].ToString(), 
                        getStringFromId(reader["schoolid"].ToString()), reader));
                }
                catch (MySqlException e) { reader.Close(); Console.Out.WriteLine(e.ToString()); };
            }

            /// <summary>
            /// Opens up student card in new thread
            /// </summary>
            private void TeacherCard()
            {
                MySqlCommand query = null;
                MySqlDataReader reader = null;
                try
                {
                    queryDict.TryGetValue("Teacher information", out query);
                    query.Parameters.Clear();
                    query.Parameters.AddWithValue("@param1", getIdFromString(cardName));
                    reader = query.ExecuteReader();
                    reader.Read();
                    Application.Run(new Teacher(cardName, reader["phone"].ToString(), reader["schoolid"].ToString(), getStringFromId(reader["schoolid"].ToString()),
                            getStringFromId(reader["oid"].ToString()), reader["office_hours"].ToString(), reader["tid"].ToString(), reader));
                }
                catch (Exception e) { reader.Close();  Console.Out.WriteLine(e.ToString()); };
            }

        #endregion

        #region MENU STRIPS

            // file menu strip
            private void studentToolStripMenuItem_Click(object sender, EventArgs e)
            {
                new Thread(new ThreadStart(this.newStudent)).Start();
            }

            private void newStudent()
            {
                try
                {
                    MySqlCommand studentID = new MySqlCommand("SELECT MAX(s.sid) as sid FROM Student s", myConnection);
                    MySqlDataReader reader = studentID.ExecuteReader();
                    if (reader.Read())
                    {
                        int largestStudentID = Convert.ToInt32(reader["sid"].ToString());
                        Application.Run(new StudentForm(myConnection, reverseIdValues, largestStudentID, reader));
                    }
                }
                catch (MySqlException ex) { Console.Out.WriteLine(ex.ToString()); }
            }

            private void teacherToolStripMenuItem_Click(object sender, EventArgs e)
            {
                new Thread(new ThreadStart(this.newTeacher)).Start();
            }

            private void newTeacher()
            {
                try
                {
                    MySqlCommand teacherID = new MySqlCommand("SELECT MAX(s.tid) as tid FROM Teacher s", myConnection);
                    MySqlDataReader reader = teacherID.ExecuteReader();
                    if (reader.Read())
                    {
                        int largestTeacherID = Convert.ToInt32(reader["tid"].ToString());
                        Application.Run(new TeacherForm(myConnection, reverseIdValues, largestTeacherID, reader));
                    }
                }
                catch (MySqlException ex) { Console.Out.WriteLine(ex.ToString()); }
            }

        
            // listbox menu strips
            private void listBox1_MouseDown(object sender, MouseEventArgs e)
            {
                int index = listBox1.IndexFromPoint(e.Location);
                if (e.Button == MouseButtons.Right && index > -1)
                    listBox1.SelectedIndex = index;
            }

            private void studentDropBox_SelectedIndexChanged(object sender, EventArgs e)
            {
                listBox1.ContextMenuStrip = contextMenuStrip1;
                dropDownParameter2 = studentDropBox.SelectedItem.ToString();
            }

            /* REMOVE STUDENT FROM CLASS */
            private void toolStripMenuItem2_Click(object sender, EventArgs e)
            {
                try
                {
                    if (lastQuery.Equals("Student Schedule"))
                    {
                        String value = listBox1.SelectedItem.ToString();
                        value = value.Substring(6, 4);
                        MySqlCommand remove = new MySqlCommand("DELETE FROM Attend WHERE sid = @param1 AND cid = @param2", myConnection);
                        remove.Parameters.AddWithValue("@param1", getIdFromString(dropDownParameter2));
                        remove.Parameters.AddWithValue("@param2", Convert.ToInt32(value));
                        remove.ExecuteNonQuery();
                        listBox1.Items.RemoveAt(listBox1.SelectedIndex);
                    }
                }
                catch (Exception ex) { Console.Out.WriteLine(ex.ToString()); }
            }

            /* ADD STUDENT FROM CLASS */
            private void toolStripMenuItem1_Click(object sender, EventArgs e)
            {

            }

        #endregion











    }
}

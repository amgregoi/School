namespace SchoolDatabaseProject
{
    partial class SchoolDB
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.studentClassAdd = new System.Windows.Forms.ToolStripMenuItem();
            this.studentClassRemove = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.addToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.studentToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.teacherToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.listBox2 = new System.Windows.Forms.ListBox();
            this.classDropBox = new System.Windows.Forms.ComboBox();
            this.queryButton2 = new System.Windows.Forms.Button();
            this.teacherDropBox = new System.Windows.Forms.ComboBox();
            this.queryDropBox2 = new System.Windows.Forms.ComboBox();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.studentDropBox = new System.Windows.Forms.ComboBox();
            this.listBox1 = new System.Windows.Forms.ListBox();
            this.queryButton = new System.Windows.Forms.Button();
            this.organizationDropBox = new System.Windows.Forms.ComboBox();
            this.schoolDropBox = new System.Windows.Forms.ComboBox();
            this.queryDropBox = new System.Windows.Forms.ComboBox();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.contextMenuStrip1.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.tabControl1.SuspendLayout();
            this.SuspendLayout();
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.studentClassAdd,
            this.studentClassRemove});
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(118, 48);
            // 
            // studentClassAdd
            // 
            this.studentClassAdd.Name = "studentClassAdd";
            this.studentClassAdd.Size = new System.Drawing.Size(117, 22);
            this.studentClassAdd.Text = "Add";
            this.studentClassAdd.Click += new System.EventHandler(this.toolStripMenuItem1_Click);
            // 
            // studentClassRemove
            // 
            this.studentClassRemove.Name = "studentClassRemove";
            this.studentClassRemove.Size = new System.Drawing.Size(117, 22);
            this.studentClassRemove.Text = "Remove";
            this.studentClassRemove.Click += new System.EventHandler(this.toolStripMenuItem2_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.BackColor = System.Drawing.Color.Transparent;
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(684, 24);
            this.menuStrip1.TabIndex = 3;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.addToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // addToolStripMenuItem
            // 
            this.addToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.studentToolStripMenuItem,
            this.teacherToolStripMenuItem});
            this.addToolStripMenuItem.Name = "addToolStripMenuItem";
            this.addToolStripMenuItem.Size = new System.Drawing.Size(96, 22);
            this.addToolStripMenuItem.Text = "Add";
            // 
            // studentToolStripMenuItem
            // 
            this.studentToolStripMenuItem.Name = "studentToolStripMenuItem";
            this.studentToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.studentToolStripMenuItem.Text = "Student";
            this.studentToolStripMenuItem.Click += new System.EventHandler(this.studentToolStripMenuItem_Click);
            // 
            // teacherToolStripMenuItem
            // 
            this.teacherToolStripMenuItem.Name = "teacherToolStripMenuItem";
            this.teacherToolStripMenuItem.Size = new System.Drawing.Size(116, 22);
            this.teacherToolStripMenuItem.Text = "Teacher";
            this.teacherToolStripMenuItem.Click += new System.EventHandler(this.teacherToolStripMenuItem_Click);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(96, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.listBox2);
            this.tabPage2.Controls.Add(this.classDropBox);
            this.tabPage2.Controls.Add(this.queryButton2);
            this.tabPage2.Controls.Add(this.teacherDropBox);
            this.tabPage2.Controls.Add(this.queryDropBox2);
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(687, 145);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "Teacher";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // listBox2
            // 
            this.listBox2.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBox2.FormattingEnabled = true;
            this.listBox2.Location = new System.Drawing.Point(228, -1);
            this.listBox2.Name = "listBox2";
            this.listBox2.Size = new System.Drawing.Size(459, 134);
            this.listBox2.TabIndex = 10;
            this.listBox2.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.listBox2_MouseDoubleClick);
            // 
            // classDropBox
            // 
            this.classDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.classDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.classDropBox.FormattingEnabled = true;
            this.classDropBox.Items.AddRange(new object[] {
            "Choose Class"});
            this.classDropBox.Location = new System.Drawing.Point(6, 45);
            this.classDropBox.Name = "classDropBox";
            this.classDropBox.Size = new System.Drawing.Size(145, 21);
            this.classDropBox.TabIndex = 9;
            this.classDropBox.Visible = false;
            // 
            // queryButton2
            // 
            this.queryButton2.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.queryButton2.Location = new System.Drawing.Point(43, 111);
            this.queryButton2.Name = "queryButton2";
            this.queryButton2.Size = new System.Drawing.Size(75, 23);
            this.queryButton2.TabIndex = 8;
            this.queryButton2.Text = "RunQuery";
            this.queryButton2.UseVisualStyleBackColor = true;
            this.queryButton2.Click += new System.EventHandler(this.queryButton2_Click);
            // 
            // teacherDropBox
            // 
            this.teacherDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.teacherDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.teacherDropBox.FormattingEnabled = true;
            this.teacherDropBox.Items.AddRange(new object[] {
            "Choose Teacher"});
            this.teacherDropBox.Location = new System.Drawing.Point(6, 45);
            this.teacherDropBox.Name = "teacherDropBox";
            this.teacherDropBox.Size = new System.Drawing.Size(145, 21);
            this.teacherDropBox.TabIndex = 7;
            this.teacherDropBox.Visible = false;
            this.teacherDropBox.SelectedIndexChanged += new System.EventHandler(this.teacherDropBox_SelectedIndexChanged);
            // 
            // queryDropBox2
            // 
            this.queryDropBox2.Cursor = System.Windows.Forms.Cursors.Default;
            this.queryDropBox2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.queryDropBox2.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.queryDropBox2.FormattingEnabled = true;
            this.queryDropBox2.Items.AddRange(new object[] {
            "Choose Query",
            "List of classes",
            "Teacher information"});
            this.queryDropBox2.Location = new System.Drawing.Point(6, 15);
            this.queryDropBox2.Name = "queryDropBox2";
            this.queryDropBox2.Size = new System.Drawing.Size(145, 21);
            this.queryDropBox2.TabIndex = 5;
            this.queryDropBox2.SelectedIndexChanged += new System.EventHandler(this.queryDropBox2_SelectedIndexChanged);
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.studentDropBox);
            this.tabPage1.Controls.Add(this.listBox1);
            this.tabPage1.Controls.Add(this.queryButton);
            this.tabPage1.Controls.Add(this.organizationDropBox);
            this.tabPage1.Controls.Add(this.schoolDropBox);
            this.tabPage1.Controls.Add(this.queryDropBox);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(687, 145);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "School";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // studentDropBox
            // 
            this.studentDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.studentDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.studentDropBox.FormattingEnabled = true;
            this.studentDropBox.Items.AddRange(new object[] {
            "Choose Student"});
            this.studentDropBox.Location = new System.Drawing.Point(6, 75);
            this.studentDropBox.Name = "studentDropBox";
            this.studentDropBox.Size = new System.Drawing.Size(145, 21);
            this.studentDropBox.TabIndex = 12;
            this.studentDropBox.Visible = false;
            this.studentDropBox.SelectedIndexChanged += new System.EventHandler(this.studentDropBox_SelectedIndexChanged);
            // 
            // listBox1
            // 
            this.listBox1.ContextMenuStrip = this.contextMenuStrip1;
            this.listBox1.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.listBox1.FormattingEnabled = true;
            this.listBox1.Location = new System.Drawing.Point(228, -1);
            this.listBox1.Name = "listBox1";
            this.listBox1.Size = new System.Drawing.Size(459, 134);
            this.listBox1.TabIndex = 5;
            this.listBox1.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.listBox1_MouseDoubleClick_2);
            this.listBox1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.listBox1_MouseDown);
            // 
            // queryButton
            // 
            this.queryButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.queryButton.Location = new System.Drawing.Point(43, 111);
            this.queryButton.Name = "queryButton";
            this.queryButton.Size = new System.Drawing.Size(75, 23);
            this.queryButton.TabIndex = 4;
            this.queryButton.Text = "RunQuery";
            this.queryButton.UseVisualStyleBackColor = true;
            this.queryButton.Click += new System.EventHandler(this.queryButton_Click);
            // 
            // organizationDropBox
            // 
            this.organizationDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.organizationDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.organizationDropBox.FormattingEnabled = true;
            this.organizationDropBox.Items.AddRange(new object[] {
            "Choose Organization",
            "FBLA",
            "FCA",
            "Spanish Club",
            "Student Council",
            "Football Team",
            "FFA"});
            this.organizationDropBox.Location = new System.Drawing.Point(6, 45);
            this.organizationDropBox.Name = "organizationDropBox";
            this.organizationDropBox.Size = new System.Drawing.Size(145, 21);
            this.organizationDropBox.TabIndex = 3;
            this.organizationDropBox.Visible = false;
            this.organizationDropBox.SelectedIndexChanged += new System.EventHandler(this.organizationDropBox_SelectedIndexChanged);
            // 
            // schoolDropBox
            // 
            this.schoolDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.schoolDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.schoolDropBox.FormattingEnabled = true;
            this.schoolDropBox.Items.AddRange(new object[] {
            "Choose School",
            "0001",
            "0002",
            "0003",
            "0004"});
            this.schoolDropBox.Location = new System.Drawing.Point(6, 45);
            this.schoolDropBox.Name = "schoolDropBox";
            this.schoolDropBox.Size = new System.Drawing.Size(145, 21);
            this.schoolDropBox.TabIndex = 2;
            this.schoolDropBox.Visible = false;
            this.schoolDropBox.SelectedIndexChanged += new System.EventHandler(this.schoolDropBox_SelectedIndexChanged);
            // 
            // queryDropBox
            // 
            this.queryDropBox.Cursor = System.Windows.Forms.Cursors.Default;
            this.queryDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.queryDropBox.FlatStyle = System.Windows.Forms.FlatStyle.Popup;
            this.queryDropBox.FormattingEnabled = true;
            this.queryDropBox.Items.AddRange(new object[] {
            "Choose Query",
            "List of students by school",
            "List of students in organization",
            "List Teachers",
            "Student Schedule"});
            this.queryDropBox.Location = new System.Drawing.Point(6, 15);
            this.queryDropBox.Name = "queryDropBox";
            this.queryDropBox.Size = new System.Drawing.Size(145, 21);
            this.queryDropBox.TabIndex = 0;
            this.queryDropBox.SelectedIndexChanged += new System.EventHandler(this.queryDropBox_SelectedIndexChanged);
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Location = new System.Drawing.Point(-6, 27);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.Padding = new System.Drawing.Point(8, 3);
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(695, 171);
            this.tabControl1.TabIndex = 4;
            // 
            // SchoolDB
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(684, 193);
            this.Controls.Add(this.tabControl1);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Name = "SchoolDB";
            this.Text = "School Database";
            this.contextMenuStrip1.ResumeLayout(false);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.tabPage2.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.tabControl1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.ComboBox classDropBox;
        private System.Windows.Forms.Button queryButton2;
        private System.Windows.Forms.ComboBox teacherDropBox;
        private System.Windows.Forms.ComboBox queryDropBox2;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.ListBox listBox1;
        private System.Windows.Forms.Button queryButton;
        private System.Windows.Forms.ComboBox organizationDropBox;
        private System.Windows.Forms.ComboBox schoolDropBox;
        internal System.Windows.Forms.ComboBox queryDropBox;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.ListBox listBox2;
        private System.Windows.Forms.ComboBox studentDropBox;
        private System.Windows.Forms.ToolStripMenuItem addToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem studentToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem teacherToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem studentClassAdd;
        private System.Windows.Forms.ToolStripMenuItem studentClassRemove;
    }
}


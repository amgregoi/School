namespace AddTeacher
{
    partial class TeacherForm
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
            this.button1 = new System.Windows.Forms.Button();
            this.officeHoursBox = new System.Windows.Forms.TextBox();
            this.phoneBox = new System.Windows.Forms.TextBox();
            this.nameBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.schoolDropBox = new System.Windows.Forms.ComboBox();
            this.orgDropBox = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.degreeDropBox = new System.Windows.Forms.ComboBox();
            this.label6 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Tahoma", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.button1.Location = new System.Drawing.Point(103, 261);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(96, 23);
            this.button1.TabIndex = 23;
            this.button1.Text = "Add Teacher";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // officeHoursBox
            // 
            this.officeHoursBox.Location = new System.Drawing.Point(140, 141);
            this.officeHoursBox.Name = "officeHoursBox";
            this.officeHoursBox.Size = new System.Drawing.Size(137, 20);
            this.officeHoursBox.TabIndex = 22;
            // 
            // phoneBox
            // 
            this.phoneBox.Location = new System.Drawing.Point(140, 101);
            this.phoneBox.Name = "phoneBox";
            this.phoneBox.Size = new System.Drawing.Size(137, 20);
            this.phoneBox.TabIndex = 20;
            // 
            // nameBox
            // 
            this.nameBox.Location = new System.Drawing.Point(140, 61);
            this.nameBox.Name = "nameBox";
            this.nameBox.Size = new System.Drawing.Size(137, 20);
            this.nameBox.TabIndex = 19;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.Location = new System.Drawing.Point(33, 141);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(97, 16);
            this.label5.TabIndex = 18;
            this.label5.Text = "Office Hours:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.Location = new System.Drawing.Point(33, 101);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(60, 16);
            this.label3.TabIndex = 16;
            this.label3.Text = "Phone: ";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(33, 61);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(57, 16);
            this.label2.TabIndex = 15;
            this.label2.Text = "Name: ";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(33, 26);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(64, 16);
            this.label1.TabIndex = 14;
            this.label1.Text = "School: ";
            // 
            // schoolDropBox
            // 
            this.schoolDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.schoolDropBox.FormattingEnabled = true;
            this.schoolDropBox.Location = new System.Drawing.Point(140, 21);
            this.schoolDropBox.Name = "schoolDropBox";
            this.schoolDropBox.Size = new System.Drawing.Size(137, 21);
            this.schoolDropBox.TabIndex = 13;
            // 
            // orgDropBox
            // 
            this.orgDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.orgDropBox.FormattingEnabled = true;
            this.orgDropBox.Location = new System.Drawing.Point(140, 181);
            this.orgDropBox.Name = "orgDropBox";
            this.orgDropBox.Size = new System.Drawing.Size(137, 21);
            this.orgDropBox.TabIndex = 26;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(33, 181);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(99, 16);
            this.label4.TabIndex = 25;
            this.label4.Text = "Organization:";
            // 
            // degreeDropBox
            // 
            this.degreeDropBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.degreeDropBox.FormattingEnabled = true;
            this.degreeDropBox.Location = new System.Drawing.Point(140, 221);
            this.degreeDropBox.Name = "degreeDropBox";
            this.degreeDropBox.Size = new System.Drawing.Size(137, 21);
            this.degreeDropBox.TabIndex = 29;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.Location = new System.Drawing.Point(33, 221);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(64, 16);
            this.label6.TabIndex = 28;
            this.label6.Text = "Degree:";
            // 
            // TeacherForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(322, 296);
            this.Controls.Add(this.degreeDropBox);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.orgDropBox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.officeHoursBox);
            this.Controls.Add(this.phoneBox);
            this.Controls.Add(this.nameBox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.schoolDropBox);
            this.Name = "TeacherForm";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.TextBox officeHoursBox;
        private System.Windows.Forms.TextBox phoneBox;
        private System.Windows.Forms.TextBox nameBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox schoolDropBox;
        private System.Windows.Forms.ComboBox orgDropBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox degreeDropBox;
        private System.Windows.Forms.Label label6;
    }
}


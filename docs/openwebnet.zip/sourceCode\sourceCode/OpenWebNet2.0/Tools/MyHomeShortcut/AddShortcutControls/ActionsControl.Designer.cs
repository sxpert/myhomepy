namespace MyHomeShortcut.AddShortcutControls
{
    partial class ActionsControl
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

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.commandTxt = new System.Windows.Forms.TextBox();
            this.label8 = new System.Windows.Forms.Label();
            this.removeActionBtn = new System.Windows.Forms.Button();
            this.addActionBtn = new System.Windows.Forms.Button();
            this.actionsListBox = new System.Windows.Forms.ListBox();
            this.label4 = new System.Windows.Forms.Label();
            this.whoComboBox = new System.Windows.Forms.ComboBox();
            this.label5 = new System.Windows.Forms.Label();
            this.toggleCheckBox = new System.Windows.Forms.CheckBox();
            this.whatComboBox = new System.Windows.Forms.ComboBox();
            this.whereLbl = new System.Windows.Forms.Label();
            this.whereTxt = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // commandTxt
            // 
            this.commandTxt.Location = new System.Drawing.Point(3, 59);
            this.commandTxt.Name = "commandTxt";
            this.commandTxt.Size = new System.Drawing.Size(124, 20);
            this.commandTxt.TabIndex = 32;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(3, 43);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(54, 13);
            this.label8.TabIndex = 31;
            this.label8.Text = "Command";
            // 
            // removeActionBtn
            // 
            this.removeActionBtn.Enabled = false;
            this.removeActionBtn.Location = new System.Drawing.Point(302, 114);
            this.removeActionBtn.Name = "removeActionBtn";
            this.removeActionBtn.Size = new System.Drawing.Size(75, 23);
            this.removeActionBtn.TabIndex = 30;
            this.removeActionBtn.Text = "Remove";
            this.removeActionBtn.UseVisualStyleBackColor = true;
            this.removeActionBtn.Click += new System.EventHandler(this.removeActionBtn_Click);
            // 
            // addActionBtn
            // 
            this.addActionBtn.Location = new System.Drawing.Point(302, 85);
            this.addActionBtn.Name = "addActionBtn";
            this.addActionBtn.Size = new System.Drawing.Size(75, 23);
            this.addActionBtn.TabIndex = 29;
            this.addActionBtn.Text = "Add";
            this.addActionBtn.UseVisualStyleBackColor = true;
            this.addActionBtn.Click += new System.EventHandler(this.addActionBtn_Click);
            // 
            // actionsListBox
            // 
            this.actionsListBox.FormattingEnabled = true;
            this.actionsListBox.Location = new System.Drawing.Point(3, 85);
            this.actionsListBox.Name = "actionsListBox";
            this.actionsListBox.Size = new System.Drawing.Size(293, 95);
            this.actionsListBox.TabIndex = 28;
            this.actionsListBox.SelectedIndexChanged += new System.EventHandler(this.actionsListBox_SelectedIndexChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.ForeColor = System.Drawing.Color.Red;
            this.label4.Location = new System.Drawing.Point(3, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(30, 13);
            this.label4.TabIndex = 21;
            this.label4.Text = "Who";
            // 
            // whoComboBox
            // 
            this.whoComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.whoComboBox.FormattingEnabled = true;
            this.whoComboBox.Location = new System.Drawing.Point(3, 16);
            this.whoComboBox.Name = "whoComboBox";
            this.whoComboBox.Size = new System.Drawing.Size(124, 21);
            this.whoComboBox.TabIndex = 22;
            this.whoComboBox.SelectedIndexChanged += new System.EventHandler(this.whoComboBox_SelectedIndexChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.ForeColor = System.Drawing.Color.Red;
            this.label5.Location = new System.Drawing.Point(130, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(33, 13);
            this.label5.TabIndex = 23;
            this.label5.Text = "What";
            // 
            // toggleCheckBox
            // 
            this.toggleCheckBox.AutoSize = true;
            this.toggleCheckBox.Location = new System.Drawing.Point(305, 61);
            this.toggleCheckBox.Name = "toggleCheckBox";
            this.toggleCheckBox.Size = new System.Drawing.Size(59, 17);
            this.toggleCheckBox.TabIndex = 27;
            this.toggleCheckBox.Text = "Toggle";
            this.toggleCheckBox.UseVisualStyleBackColor = true;
            // 
            // whatComboBox
            // 
            this.whatComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.whatComboBox.FormattingEnabled = true;
            this.whatComboBox.Location = new System.Drawing.Point(133, 16);
            this.whatComboBox.Name = "whatComboBox";
            this.whatComboBox.Size = new System.Drawing.Size(163, 21);
            this.whatComboBox.TabIndex = 24;
            // 
            // whereLbl
            // 
            this.whereLbl.AutoSize = true;
            this.whereLbl.ForeColor = System.Drawing.Color.Red;
            this.whereLbl.Location = new System.Drawing.Point(302, 1);
            this.whereLbl.Name = "whereLbl";
            this.whereLbl.Size = new System.Drawing.Size(39, 13);
            this.whereLbl.TabIndex = 25;
            this.whereLbl.Text = "Where";
            // 
            // whereTxt
            // 
            this.whereTxt.Location = new System.Drawing.Point(302, 16);
            this.whereTxt.Name = "whereTxt";
            this.whereTxt.Size = new System.Drawing.Size(75, 20);
            this.whereTxt.TabIndex = 26;
            // 
            // ActionsControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.commandTxt);
            this.Controls.Add(this.label8);
            this.Controls.Add(this.removeActionBtn);
            this.Controls.Add(this.addActionBtn);
            this.Controls.Add(this.actionsListBox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.whoComboBox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.toggleCheckBox);
            this.Controls.Add(this.whatComboBox);
            this.Controls.Add(this.whereLbl);
            this.Controls.Add(this.whereTxt);
            this.Name = "ActionsControl";
            this.Size = new System.Drawing.Size(384, 187);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox commandTxt;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.Button removeActionBtn;
        private System.Windows.Forms.Button addActionBtn;
        private System.Windows.Forms.ListBox actionsListBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox whoComboBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.CheckBox toggleCheckBox;
        private System.Windows.Forms.ComboBox whatComboBox;
        private System.Windows.Forms.Label whereLbl;
        private System.Windows.Forms.TextBox whereTxt;
    }
}

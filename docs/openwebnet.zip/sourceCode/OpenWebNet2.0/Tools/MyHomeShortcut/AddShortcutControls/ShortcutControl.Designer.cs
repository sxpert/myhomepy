namespace MyHomeShortcut.AddShortcutControls
{
    partial class ShortcutControl
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
            this.nameTxt = new System.Windows.Forms.TextBox();
            this.label7 = new System.Windows.Forms.Label();
            this.key1ComboBox = new System.Windows.Forms.ComboBox();
            this.key3ComboBox = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.key2ComboBox = new System.Windows.Forms.ComboBox();
            this.SuspendLayout();
            // 
            // nameTxt
            // 
            this.nameTxt.Location = new System.Drawing.Point(3, 16);
            this.nameTxt.Name = "nameTxt";
            this.nameTxt.Size = new System.Drawing.Size(372, 20);
            this.nameTxt.TabIndex = 25;
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.ForeColor = System.Drawing.Color.Red;
            this.label7.Location = new System.Drawing.Point(3, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(35, 13);
            this.label7.TabIndex = 24;
            this.label7.Text = "Name";
            // 
            // key1ComboBox
            // 
            this.key1ComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.key1ComboBox.FormattingEnabled = true;
            this.key1ComboBox.Location = new System.Drawing.Point(3, 57);
            this.key1ComboBox.Name = "key1ComboBox";
            this.key1ComboBox.Size = new System.Drawing.Size(124, 21);
            this.key1ComboBox.TabIndex = 18;
            // 
            // key3ComboBox
            // 
            this.key3ComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.key3ComboBox.FormattingEnabled = true;
            this.key3ComboBox.Location = new System.Drawing.Point(257, 57);
            this.key3ComboBox.Name = "key3ComboBox";
            this.key3ComboBox.Size = new System.Drawing.Size(118, 21);
            this.key3ComboBox.TabIndex = 22;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.ForeColor = System.Drawing.Color.Red;
            this.label1.Location = new System.Drawing.Point(3, 41);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(34, 13);
            this.label1.TabIndex = 17;
            this.label1.Text = "Key 1";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.ForeColor = System.Drawing.Color.Red;
            this.label3.Location = new System.Drawing.Point(254, 41);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(34, 13);
            this.label3.TabIndex = 21;
            this.label3.Text = "Key 3";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(130, 41);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(34, 13);
            this.label2.TabIndex = 19;
            this.label2.Text = "Key 2";
            // 
            // key2ComboBox
            // 
            this.key2ComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.key2ComboBox.FormattingEnabled = true;
            this.key2ComboBox.Location = new System.Drawing.Point(133, 57);
            this.key2ComboBox.Name = "key2ComboBox";
            this.key2ComboBox.Size = new System.Drawing.Size(118, 21);
            this.key2ComboBox.TabIndex = 20;
            // 
            // ShortcutControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.nameTxt);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.key1ComboBox);
            this.Controls.Add(this.key3ComboBox);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.key2ComboBox);
            this.Name = "ShortcutControl";
            this.Size = new System.Drawing.Size(379, 84);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox nameTxt;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.ComboBox key1ComboBox;
        private System.Windows.Forms.ComboBox key3ComboBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox key2ComboBox;
    }
}

namespace MyHomeShortcut.AddShortcutControls
{
    partial class MainShortcutControl
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
            this.nextBtn = new System.Windows.Forms.Button();
            this.backBtn = new System.Windows.Forms.Button();
            this.actionsControl = new MyHomeShortcut.AddShortcutControls.ActionsControl();
            this.shortcutControl = new MyHomeShortcut.AddShortcutControls.ShortcutControl();
            this.cancelBtn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // nextBtn
            // 
            this.nextBtn.Location = new System.Drawing.Point(307, 219);
            this.nextBtn.Name = "nextBtn";
            this.nextBtn.Size = new System.Drawing.Size(75, 23);
            this.nextBtn.TabIndex = 2;
            this.nextBtn.Text = "Next";
            this.nextBtn.UseVisualStyleBackColor = true;
            this.nextBtn.Click += new System.EventHandler(this.nextBtn_Click);
            // 
            // backBtn
            // 
            this.backBtn.Location = new System.Drawing.Point(145, 219);
            this.backBtn.Name = "backBtn";
            this.backBtn.Size = new System.Drawing.Size(75, 23);
            this.backBtn.TabIndex = 3;
            this.backBtn.Text = "Back";
            this.backBtn.UseVisualStyleBackColor = true;
            this.backBtn.Click += new System.EventHandler(this.backBtn_Click);
            // 
            // actionsControl
            // 
            this.actionsControl.Actions = null;
            this.actionsControl.Command = "";
            this.actionsControl.Location = new System.Drawing.Point(5, 3);
            this.actionsControl.Name = "actionsControl";
            this.actionsControl.Size = new System.Drawing.Size(384, 187);
            this.actionsControl.TabIndex = 1;
            this.actionsControl.What = OpenWebNet.WHAT.LightON;
            this.actionsControl.Where = "";
            this.actionsControl.Who = OpenWebNet.WHO.Lighting;
            // 
            // shortcutControl
            // 
            this.shortcutControl.KeyOne = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.None)));
            this.shortcutControl.KeyThree = System.Windows.Forms.Keys.D0;
            this.shortcutControl.KeyTwo = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.None)));
            this.shortcutControl.Location = new System.Drawing.Point(3, 3);
            this.shortcutControl.Name = "shortcutControl";
            this.shortcutControl.ShortcutName = "";
            this.shortcutControl.Size = new System.Drawing.Size(379, 84);
            this.shortcutControl.TabIndex = 0;
            // 
            // cancelBtn
            // 
            this.cancelBtn.Location = new System.Drawing.Point(226, 219);
            this.cancelBtn.Name = "cancelBtn";
            this.cancelBtn.Size = new System.Drawing.Size(75, 23);
            this.cancelBtn.TabIndex = 4;
            this.cancelBtn.Text = "Cancel";
            this.cancelBtn.UseVisualStyleBackColor = true;
            this.cancelBtn.Click += new System.EventHandler(this.cancelBtn_Click);
            // 
            // MainShortcutControl
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.cancelBtn);
            this.Controls.Add(this.backBtn);
            this.Controls.Add(this.nextBtn);
            this.Controls.Add(this.actionsControl);
            this.Controls.Add(this.shortcutControl);
            this.Name = "MainShortcutControl";
            this.Size = new System.Drawing.Size(392, 245);
            this.ResumeLayout(false);

        }

        #endregion

        private ShortcutControl shortcutControl;
        private ActionsControl actionsControl;
        private System.Windows.Forms.Button nextBtn;
        private System.Windows.Forms.Button backBtn;
        private System.Windows.Forms.Button cancelBtn;
    }
}

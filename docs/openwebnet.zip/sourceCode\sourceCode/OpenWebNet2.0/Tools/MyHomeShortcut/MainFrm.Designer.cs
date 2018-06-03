namespace MyHomeShortcut
{
    partial class MainFrm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainFrm));
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.optionsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.gatewayConfigurationToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.scenariosToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.addShortcutGroupBox = new System.Windows.Forms.GroupBox();
            this.mainShortcutControl1 = new MyHomeShortcut.AddShortcutControls.MainShortcutControl();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.modifyBtn = new System.Windows.Forms.Button();
            this.removeShortcutBtn = new System.Windows.Forms.Button();
            this.shortcutsListBox = new System.Windows.Forms.ListBox();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.notifyIcon = new System.Windows.Forms.NotifyIcon(this.components);
            this.connectToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripSeparator1 = new System.Windows.Forms.ToolStripSeparator();
            this.menuStrip1.SuspendLayout();
            this.addShortcutGroupBox.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.statusStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem,
            this.optionsToolStripMenuItem,
            this.toolStripMenuItem1});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(427, 24);
            this.menuStrip1.TabIndex = 2;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.connectToolStripMenuItem,
            this.toolStripSeparator1,
            this.exitToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // optionsToolStripMenuItem
            // 
            this.optionsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.gatewayConfigurationToolStripMenuItem,
            this.scenariosToolStripMenuItem});
            this.optionsToolStripMenuItem.Name = "optionsToolStripMenuItem";
            this.optionsToolStripMenuItem.Size = new System.Drawing.Size(61, 20);
            this.optionsToolStripMenuItem.Text = "Options";
            this.optionsToolStripMenuItem.Click += new System.EventHandler(this.optionsToolStripMenuItem_Click);
            // 
            // gatewayConfigurationToolStripMenuItem
            // 
            this.gatewayConfigurationToolStripMenuItem.Name = "gatewayConfigurationToolStripMenuItem";
            this.gatewayConfigurationToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.gatewayConfigurationToolStripMenuItem.Text = "Gateway";
            this.gatewayConfigurationToolStripMenuItem.Click += new System.EventHandler(this.gatewayConfigurationToolStripMenuItem_Click);
            // 
            // scenariosToolStripMenuItem
            // 
            this.scenariosToolStripMenuItem.Name = "scenariosToolStripMenuItem";
            this.scenariosToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.scenariosToolStripMenuItem.Text = "Scenarios";
            this.scenariosToolStripMenuItem.Click += new System.EventHandler(this.scenariosToolStripMenuItem_Click);
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.aboutToolStripMenuItem});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(24, 20);
            this.toolStripMenuItem1.Text = "?";
            // 
            // aboutToolStripMenuItem
            // 
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(107, 22);
            this.aboutToolStripMenuItem.Text = "About";
            this.aboutToolStripMenuItem.Click += new System.EventHandler(this.aboutToolStripMenuItem_Click);
            // 
            // addShortcutGroupBox
            // 
            this.addShortcutGroupBox.Controls.Add(this.mainShortcutControl1);
            this.addShortcutGroupBox.Location = new System.Drawing.Point(12, 27);
            this.addShortcutGroupBox.Name = "addShortcutGroupBox";
            this.addShortcutGroupBox.Size = new System.Drawing.Size(401, 272);
            this.addShortcutGroupBox.TabIndex = 7;
            this.addShortcutGroupBox.TabStop = false;
            this.addShortcutGroupBox.Text = "Add Shortcut";
            // 
            // mainShortcutControl1
            // 
            this.mainShortcutControl1.CurrentPage = MyHomeShortcut.AddShortcutControls.MainShortcutControl.ShortcutPage.FirstPage;
            this.mainShortcutControl1.Location = new System.Drawing.Point(6, 19);
            this.mainShortcutControl1.Name = "mainShortcutControl1";
            this.mainShortcutControl1.Shortcut = null;
            this.mainShortcutControl1.Size = new System.Drawing.Size(392, 245);
            this.mainShortcutControl1.TabIndex = 0;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.modifyBtn);
            this.groupBox1.Controls.Add(this.removeShortcutBtn);
            this.groupBox1.Controls.Add(this.shortcutsListBox);
            this.groupBox1.Location = new System.Drawing.Point(12, 305);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(401, 138);
            this.groupBox1.TabIndex = 8;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Shortcuts";
            // 
            // modifyBtn
            // 
            this.modifyBtn.Enabled = false;
            this.modifyBtn.Location = new System.Drawing.Point(315, 19);
            this.modifyBtn.Name = "modifyBtn";
            this.modifyBtn.Size = new System.Drawing.Size(75, 23);
            this.modifyBtn.TabIndex = 15;
            this.modifyBtn.Text = "Modify";
            this.modifyBtn.UseVisualStyleBackColor = true;
            this.modifyBtn.Click += new System.EventHandler(this.modifyBtn_Click);
            // 
            // removeShortcutBtn
            // 
            this.removeShortcutBtn.Enabled = false;
            this.removeShortcutBtn.Location = new System.Drawing.Point(315, 48);
            this.removeShortcutBtn.Name = "removeShortcutBtn";
            this.removeShortcutBtn.Size = new System.Drawing.Size(75, 23);
            this.removeShortcutBtn.TabIndex = 14;
            this.removeShortcutBtn.Text = "Remove";
            this.removeShortcutBtn.UseVisualStyleBackColor = true;
            this.removeShortcutBtn.Click += new System.EventHandler(this.removeShortcutBtn_Click);
            // 
            // shortcutsListBox
            // 
            this.shortcutsListBox.FormattingEnabled = true;
            this.shortcutsListBox.Location = new System.Drawing.Point(6, 19);
            this.shortcutsListBox.Name = "shortcutsListBox";
            this.shortcutsListBox.Size = new System.Drawing.Size(303, 108);
            this.shortcutsListBox.TabIndex = 0;
            this.shortcutsListBox.SelectedIndexChanged += new System.EventHandler(this.shortcutsListBox_SelectedIndexChanged);
            // 
            // statusStrip1
            // 
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1});
            this.statusStrip1.Location = new System.Drawing.Point(0, 456);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(427, 22);
            this.statusStrip1.TabIndex = 9;
            this.statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(0, 17);
            // 
            // notifyIcon
            // 
            this.notifyIcon.BalloonTipTitle = "MyHomeShortcut";
            this.notifyIcon.Icon = ((System.Drawing.Icon)(resources.GetObject("notifyIcon.Icon")));
            this.notifyIcon.Text = "MyHomeShortcut";
            this.notifyIcon.Visible = true;
            this.notifyIcon.Click += new System.EventHandler(this.notifyIcon_Click);
            // 
            // connectToolStripMenuItem
            // 
            this.connectToolStripMenuItem.Name = "connectToolStripMenuItem";
            this.connectToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.connectToolStripMenuItem.Text = "Connect";
            this.connectToolStripMenuItem.Click += new System.EventHandler(this.connectToolStripMenuItem_Click);
            // 
            // toolStripSeparator1
            // 
            this.toolStripSeparator1.Name = "toolStripSeparator1";
            this.toolStripSeparator1.Size = new System.Drawing.Size(149, 6);
            // 
            // MainFrm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(427, 478);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.addShortcutGroupBox);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.KeyPreview = true;
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(509, 546);
            this.Name = "MainFrm";
            this.Text = "MyHomeShortcut";
            this.Load += new System.EventHandler(this.MainFrm_Load);
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainFrm_FormClosing);
            this.Resize += new System.EventHandler(this.MainFrm_Resize);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.addShortcutGroupBox.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem optionsToolStripMenuItem;
        private System.Windows.Forms.GroupBox addShortcutGroupBox;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button removeShortcutBtn;
        private System.Windows.Forms.ListBox shortcutsListBox;
        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.NotifyIcon notifyIcon;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem aboutToolStripMenuItem;
        private System.Windows.Forms.Button modifyBtn;
        private System.Windows.Forms.ToolStripMenuItem gatewayConfigurationToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem scenariosToolStripMenuItem;
        private MyHomeShortcut.AddShortcutControls.MainShortcutControl mainShortcutControl1;
        private System.Windows.Forms.ToolStripMenuItem connectToolStripMenuItem;
        private System.Windows.Forms.ToolStripSeparator toolStripSeparator1;
    }
}


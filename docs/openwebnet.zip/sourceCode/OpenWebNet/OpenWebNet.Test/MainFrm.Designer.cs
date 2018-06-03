namespace OpenWebNet.Test
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
            this.label1 = new System.Windows.Forms.Label();
            this.gatewayComboBox = new System.Windows.Forms.ComboBox();
            this.connectBtn = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.ipTxt = new System.Windows.Forms.TextBox();
            this.portTxt = new System.Windows.Forms.TextBox();
            this.sendBtn = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.commandsListBox = new System.Windows.Forms.ComboBox();
            this.label5 = new System.Windows.Forms.Label();
            this.whereTxt = new System.Windows.Forms.TextBox();
            this.resultsTxt = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.disconnectBtn = new System.Windows.Forms.Button();
            this.label7 = new System.Windows.Forms.Label();
            this.parametersTxt = new System.Windows.Forms.TextBox();
            this.parametersLbl = new System.Windows.Forms.Label();
            this.testMessageBtn = new System.Windows.Forms.Button();
            this.superSocketBtn = new System.Windows.Forms.Button();
            this.monitorBtn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 14);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(52, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Gateway:";
            // 
            // gatewayComboBox
            // 
            this.gatewayComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.gatewayComboBox.FormattingEnabled = true;
            this.gatewayComboBox.Items.AddRange(new object[] {
            "USB",
            "WebServer"});
            this.gatewayComboBox.Location = new System.Drawing.Point(70, 12);
            this.gatewayComboBox.Name = "gatewayComboBox";
            this.gatewayComboBox.Size = new System.Drawing.Size(121, 21);
            this.gatewayComboBox.TabIndex = 1;
            this.gatewayComboBox.SelectedIndexChanged += new System.EventHandler(this.gatewayComboBox_SelectedIndexChanged);
            // 
            // connectBtn
            // 
            this.connectBtn.Location = new System.Drawing.Point(355, 10);
            this.connectBtn.Name = "connectBtn";
            this.connectBtn.Size = new System.Drawing.Size(90, 23);
            this.connectBtn.TabIndex = 2;
            this.connectBtn.Text = "Connetti";
            this.connectBtn.UseVisualStyleBackColor = true;
            this.connectBtn.Click += new System.EventHandler(this.connectBtn_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 81);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(19, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Ip:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 107);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(35, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "Porta:";
            // 
            // ipTxt
            // 
            this.ipTxt.Location = new System.Drawing.Point(70, 78);
            this.ipTxt.Name = "ipTxt";
            this.ipTxt.Size = new System.Drawing.Size(121, 20);
            this.ipTxt.TabIndex = 5;
            // 
            // portTxt
            // 
            this.portTxt.Location = new System.Drawing.Point(70, 104);
            this.portTxt.Name = "portTxt";
            this.portTxt.Size = new System.Drawing.Size(121, 20);
            this.portTxt.TabIndex = 6;
            // 
            // sendBtn
            // 
            this.sendBtn.Location = new System.Drawing.Point(451, 76);
            this.sendBtn.Name = "sendBtn";
            this.sendBtn.Size = new System.Drawing.Size(76, 23);
            this.sendBtn.TabIndex = 7;
            this.sendBtn.Text = "Invia";
            this.sendBtn.UseVisualStyleBackColor = true;
            this.sendBtn.Click += new System.EventHandler(this.sendBtn_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(213, 81);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(55, 13);
            this.label4.TabIndex = 8;
            this.label4.Text = "Comando:";
            // 
            // commandsListBox
            // 
            this.commandsListBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.commandsListBox.FormattingEnabled = true;
            this.commandsListBox.Location = new System.Drawing.Point(271, 78);
            this.commandsListBox.Name = "commandsListBox";
            this.commandsListBox.Size = new System.Drawing.Size(174, 21);
            this.commandsListBox.TabIndex = 9;
            this.commandsListBox.SelectedIndexChanged += new System.EventHandler(this.commandsListBox_SelectedIndexChanged);
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(213, 108);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(36, 13);
            this.label5.TabIndex = 10;
            this.label5.Text = "Dove:";
            // 
            // whereTxt
            // 
            this.whereTxt.Enabled = false;
            this.whereTxt.Location = new System.Drawing.Point(271, 105);
            this.whereTxt.Name = "whereTxt";
            this.whereTxt.Size = new System.Drawing.Size(174, 20);
            this.whereTxt.TabIndex = 11;
            // 
            // resultsTxt
            // 
            this.resultsTxt.Location = new System.Drawing.Point(12, 202);
            this.resultsTxt.Multiline = true;
            this.resultsTxt.Name = "resultsTxt";
            this.resultsTxt.ReadOnly = true;
            this.resultsTxt.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.resultsTxt.Size = new System.Drawing.Size(515, 145);
            this.resultsTxt.TabIndex = 12;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(9, 186);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(51, 13);
            this.label6.TabIndex = 13;
            this.label6.Text = "Risultato:";
            // 
            // disconnectBtn
            // 
            this.disconnectBtn.Location = new System.Drawing.Point(451, 9);
            this.disconnectBtn.Name = "disconnectBtn";
            this.disconnectBtn.Size = new System.Drawing.Size(76, 23);
            this.disconnectBtn.TabIndex = 14;
            this.disconnectBtn.Text = "Disconnetti";
            this.disconnectBtn.UseVisualStyleBackColor = true;
            this.disconnectBtn.Click += new System.EventHandler(this.disconnectBtn_Click);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(213, 134);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(54, 13);
            this.label7.TabIndex = 15;
            this.label7.Text = "Parametri:";
            // 
            // parametersTxt
            // 
            this.parametersTxt.Location = new System.Drawing.Point(271, 131);
            this.parametersTxt.Name = "parametersTxt";
            this.parametersTxt.Size = new System.Drawing.Size(174, 20);
            this.parametersTxt.TabIndex = 16;
            // 
            // parametersLbl
            // 
            this.parametersLbl.AutoSize = true;
            this.parametersLbl.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.parametersLbl.Location = new System.Drawing.Point(268, 154);
            this.parametersLbl.Name = "parametersLbl";
            this.parametersLbl.Size = new System.Drawing.Size(0, 16);
            this.parametersLbl.TabIndex = 18;
            // 
            // testMessageBtn
            // 
            this.testMessageBtn.Location = new System.Drawing.Point(451, 103);
            this.testMessageBtn.Name = "testMessageBtn";
            this.testMessageBtn.Size = new System.Drawing.Size(76, 23);
            this.testMessageBtn.TabIndex = 19;
            this.testMessageBtn.Text = "Message";
            this.testMessageBtn.UseVisualStyleBackColor = true;
            this.testMessageBtn.Click += new System.EventHandler(this.testMessageBtn_Click);
            // 
            // superSocketBtn
            // 
            this.superSocketBtn.Location = new System.Drawing.Point(355, 39);
            this.superSocketBtn.Name = "superSocketBtn";
            this.superSocketBtn.Size = new System.Drawing.Size(90, 23);
            this.superSocketBtn.TabIndex = 20;
            this.superSocketBtn.Text = "Super Socket";
            this.superSocketBtn.UseVisualStyleBackColor = true;
            this.superSocketBtn.Click += new System.EventHandler(this.superSocketBtn_Click);
            // 
            // monitorBtn
            // 
            this.monitorBtn.Location = new System.Drawing.Point(451, 38);
            this.monitorBtn.Name = "monitorBtn";
            this.monitorBtn.Size = new System.Drawing.Size(76, 23);
            this.monitorBtn.TabIndex = 21;
            this.monitorBtn.Text = "Monitor";
            this.monitorBtn.UseVisualStyleBackColor = true;
            this.monitorBtn.Click += new System.EventHandler(this.monitorBtn_Click);
            // 
            // MainFrm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(539, 359);
            this.Controls.Add(this.monitorBtn);
            this.Controls.Add(this.superSocketBtn);
            this.Controls.Add(this.testMessageBtn);
            this.Controls.Add(this.parametersLbl);
            this.Controls.Add(this.parametersTxt);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.disconnectBtn);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.resultsTxt);
            this.Controls.Add(this.whereTxt);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.commandsListBox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.sendBtn);
            this.Controls.Add(this.portTxt);
            this.Controls.Add(this.ipTxt);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.connectBtn);
            this.Controls.Add(this.gatewayComboBox);
            this.Controls.Add(this.label1);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(514, 395);
            this.Name = "MainFrm";
            this.Text = "MainFrm";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainFrm_FormClosing);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox gatewayComboBox;
        private System.Windows.Forms.Button connectBtn;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox ipTxt;
        private System.Windows.Forms.TextBox portTxt;
        private System.Windows.Forms.Button sendBtn;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.ComboBox commandsListBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox whereTxt;
        private System.Windows.Forms.TextBox resultsTxt;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Button disconnectBtn;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox parametersTxt;
        private System.Windows.Forms.Label parametersLbl;
        private System.Windows.Forms.Button testMessageBtn;
        private System.Windows.Forms.Button superSocketBtn;
        private System.Windows.Forms.Button monitorBtn;
    }
}
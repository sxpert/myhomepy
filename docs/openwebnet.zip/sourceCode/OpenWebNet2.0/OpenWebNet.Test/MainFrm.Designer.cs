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
            this.connectBtn = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.ipTxt = new System.Windows.Forms.TextBox();
            this.portTxt = new System.Windows.Forms.TextBox();
            this.sendBtn = new System.Windows.Forms.Button();
            this.commandResultsTxt = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.disconnectBtn = new System.Windows.Forms.Button();
            this.label7 = new System.Windows.Forms.Label();
            this.commandTxt = new System.Windows.Forms.TextBox();
            this.parametersLbl = new System.Windows.Forms.Label();
            this.monitorResultsTxt = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // connectBtn
            // 
            this.connectBtn.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.connectBtn.Location = new System.Drawing.Point(387, 13);
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
            this.label2.Location = new System.Drawing.Point(9, 84);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(19, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "Ip:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(9, 110);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(35, 13);
            this.label3.TabIndex = 4;
            this.label3.Text = "Porta:";
            // 
            // ipTxt
            // 
            this.ipTxt.Location = new System.Drawing.Point(67, 81);
            this.ipTxt.Name = "ipTxt";
            this.ipTxt.Size = new System.Drawing.Size(121, 20);
            this.ipTxt.TabIndex = 5;
            // 
            // portTxt
            // 
            this.portTxt.Location = new System.Drawing.Point(67, 107);
            this.portTxt.Name = "portTxt";
            this.portTxt.Size = new System.Drawing.Size(121, 20);
            this.portTxt.TabIndex = 6;
            // 
            // sendBtn
            // 
            this.sendBtn.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.sendBtn.Location = new System.Drawing.Point(483, 79);
            this.sendBtn.Name = "sendBtn";
            this.sendBtn.Size = new System.Drawing.Size(76, 23);
            this.sendBtn.TabIndex = 7;
            this.sendBtn.Text = "Invia";
            this.sendBtn.UseVisualStyleBackColor = true;
            this.sendBtn.Click += new System.EventHandler(this.sendBtn_Click);
            // 
            // commandResultsTxt
            // 
            this.commandResultsTxt.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.commandResultsTxt.Location = new System.Drawing.Point(12, 176);
            this.commandResultsTxt.Multiline = true;
            this.commandResultsTxt.Name = "commandResultsTxt";
            this.commandResultsTxt.ReadOnly = true;
            this.commandResultsTxt.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.commandResultsTxt.Size = new System.Drawing.Size(269, 270);
            this.commandResultsTxt.TabIndex = 12;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(9, 160);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(51, 13);
            this.label6.TabIndex = 13;
            this.label6.Text = "Comandi:";
            // 
            // disconnectBtn
            // 
            this.disconnectBtn.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.disconnectBtn.Location = new System.Drawing.Point(483, 12);
            this.disconnectBtn.Name = "disconnectBtn";
            this.disconnectBtn.Size = new System.Drawing.Size(76, 23);
            this.disconnectBtn.TabIndex = 14;
            this.disconnectBtn.Text = "Disconnetti";
            this.disconnectBtn.UseVisualStyleBackColor = true;
            this.disconnectBtn.Click += new System.EventHandler(this.disconnectBtn_Click);
            // 
            // label7
            // 
            this.label7.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(243, 84);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(55, 13);
            this.label7.TabIndex = 15;
            this.label7.Text = "Comando:";
            // 
            // commandTxt
            // 
            this.commandTxt.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.commandTxt.Location = new System.Drawing.Point(303, 81);
            this.commandTxt.Name = "commandTxt";
            this.commandTxt.Size = new System.Drawing.Size(174, 20);
            this.commandTxt.TabIndex = 16;
            // 
            // parametersLbl
            // 
            this.parametersLbl.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.parametersLbl.AutoSize = true;
            this.parametersLbl.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.parametersLbl.Location = new System.Drawing.Point(300, 157);
            this.parametersLbl.Name = "parametersLbl";
            this.parametersLbl.Size = new System.Drawing.Size(0, 16);
            this.parametersLbl.TabIndex = 18;
            // 
            // monitorResultsTxt
            // 
            this.monitorResultsTxt.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.monitorResultsTxt.Location = new System.Drawing.Point(290, 176);
            this.monitorResultsTxt.Multiline = true;
            this.monitorResultsTxt.Name = "monitorResultsTxt";
            this.monitorResultsTxt.ReadOnly = true;
            this.monitorResultsTxt.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.monitorResultsTxt.Size = new System.Drawing.Size(269, 270);
            this.monitorResultsTxt.TabIndex = 23;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(287, 160);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(45, 13);
            this.label1.TabIndex = 24;
            this.label1.Text = "Monitor:";
            // 
            // MainFrm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(571, 458);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.monitorResultsTxt);
            this.Controls.Add(this.parametersLbl);
            this.Controls.Add(this.commandTxt);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.disconnectBtn);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.commandResultsTxt);
            this.Controls.Add(this.sendBtn);
            this.Controls.Add(this.portTxt);
            this.Controls.Add(this.ipTxt);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.connectBtn);
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

        private System.Windows.Forms.Button connectBtn;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox ipTxt;
        private System.Windows.Forms.TextBox portTxt;
        private System.Windows.Forms.Button sendBtn;
        private System.Windows.Forms.TextBox commandResultsTxt;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Button disconnectBtn;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox commandTxt;
        private System.Windows.Forms.Label parametersLbl;
        private System.Windows.Forms.TextBox monitorResultsTxt;
        private System.Windows.Forms.Label label1;
    }
}
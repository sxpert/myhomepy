using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

using OpenWebNet;

namespace OpenWebNet.Test
{
    public partial class MessageFrm : Form
    {
        private string[] messages;

        public MessageFrm()
        {
            InitializeComponent();

            messages = new string[] 
            {
                "*1*0*11##",
                "*1*1*11##",
                "*1*50*11##", // dimmer 50%
                "*1*25*11##", // lampeggio

                "*2*0*11##",
                "*2*1*11##",
                "*2*2*11##",

                "*0*5*11##",
                "*0*5#0*11##",
                "*0*40#5*11##",
                "*0*41#5*11##",
                "*0*42*11##",
                "*0*42#5*11##",
                "*0*43*11##",
                "*0*44*11##",
                "*0*45*11##",
                "*0*46*11##"
            };
        }

        private void testBtn_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < messages.Length; i++)
            {
                resultsTxt.Text += messages[i] +  " ### " + MessageAnalyzer.GetMessage(messages[i]).ToString() + Environment.NewLine;
            }
        }
    }
}

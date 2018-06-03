using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using OpenWebNet;

namespace MyHomeShortcut
{
    public partial class OptionsFrm : Form
    {
        public OptionsFrm()
        {
            InitializeComponent();

            this.typeComboBox.DataSource = Enum.GetNames(typeof(GatewayType));
        }

        public string Ip
        {
            get
            {
                return ipTxt.Text;
            }

            set
            {
                ipTxt.Text = value;
            }
        }

        public string Port
        {
            get
            {
                return portTxt.Text;
            }

            set
            {
                portTxt.Text = value;
            }
        }

        public GatewayType Type
        {
            get
            {
                return (GatewayType)Enum.Parse(typeof(GatewayType), typeComboBox.SelectedItem.ToString());
            }

            set
            {
                typeComboBox.SelectedItem = value.ToString();
            }
        }

        private void okBtn_Click(object sender, EventArgs e)
        {
            int port;

            // controlli vari

            if (this.Type == GatewayType.Ethernet)
            {
                if (!int.TryParse(portTxt.Text, out port))
                {
                    MessageBox.Show("Field Gateway Port can contain only digit", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                if (string.IsNullOrEmpty(ipTxt.Text))
                {
                    MessageBox.Show("You have to specify the IP Address", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }
            }

            if (string.IsNullOrEmpty(portTxt.Text))
            {
                MessageBox.Show("You have to specify the port", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            this.Close();
        }

        private void cancelBtn_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace MyHomeShortcut
{
    public partial class ScenariosFrm : Form
    {
        public ScenariosFrm()
        {
            InitializeComponent();
        }

        public string ScenariosCentralUnitWhere
        {
            get
            {
                return centralUnitWhereTxt.Text;
            }

            set
            {
                centralUnitWhereTxt.Text = value;
            }
        }

        private void okBtn_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.OK;
            this.Close();
        }
    }
}

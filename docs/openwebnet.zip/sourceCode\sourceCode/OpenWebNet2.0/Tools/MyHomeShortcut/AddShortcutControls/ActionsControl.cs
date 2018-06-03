using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using OpenWebNet;
using MyHomeShortcut.Properties;

namespace MyHomeShortcut.AddShortcutControls
{
    public partial class ActionsControl : UserControl
    {
        private List<Action> actions;
        private string[] commands = new string[] { "LightON", "LightOFF", "AutomationUp", "AutomationDown", "AutomationStop", "DimmerUp", "DimmerDown",
            "ScenariosON", "ScenariosOFF" };

        public ActionsControl()
        {
            InitializeComponent();

            whoComboBox.DataSource = new string[] { "Lighting", "Automation", "Scenarios" };
        }

        #region Properties

        public WHO Who
        {
            get
            {
                if (whoComboBox.SelectedItem == null)
                    return WHO.None;

                return (WHO)Enum.Parse(typeof(WHO), whoComboBox.SelectedItem.ToString());
            }

            set
            {
                whoComboBox.SelectedItem = value.ToString();
            }
        }

        public WHAT What
        {
            get
            {
                if (whatComboBox.SelectedItem == null)
                    return WHAT.None;

                return (WHAT)Enum.Parse(typeof(WHAT), whatComboBox.SelectedItem.ToString());
            }

            set
            {
                whatComboBox.SelectedItem = value.ToString();
            }
        }

        public string Where
        {
            get
            {
                return whereTxt.Text;
            }

            set
            {
                whereTxt.Text = value;
            }
        }

        public string Command
        {
            get
            {
                return commandTxt.Text;
            }

            set
            {
                commandTxt.Text = value;
            }
        }

        public List<Action> Actions
        {
            get
            {
                return this.actions;
            }

            set
            {
                this.actions = value;

                actionsListBox.DataSource = null;
                actionsListBox.DataSource = this.actions;
            }
        }

        #endregion

        public void Clear()
        {
            whoComboBox.SelectedItem = WHO.None.ToString();
            whatComboBox.SelectedItem = WHAT.None.ToString();
            whereTxt.Text = string.Empty;
            commandTxt.Text = string.Empty;
            actionsListBox.DataSource = null;

            /*if (this.actions != null)
            {
                this.actions.Clear();
                actionsListBox.DataSource = this.actions;
            }*/
        }

        #region Event Handlers

        private void addActionBtn_Click(object sender, EventArgs e)
        {
            string where;
            WHAT what;
            WHO who;

            if ((Who == WHO.None || What == WHAT.None || string.IsNullOrEmpty(whereTxt.Text)) && string.IsNullOrEmpty(commandTxt.Text))
            {
                MessageBox.Show("All red field have to be specified", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            /*if (whoComboBox.SelectedItem == null || whatComboBox.SelectedItem == null || string.IsNullOrEmpty(whereTxt.Text) && string.IsNullOrEmpty(commandTxt.Text))
            {
                MessageBox.Show("All red field have to be specified", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }*/

            if (string.IsNullOrEmpty(commandTxt.Text))
            {
                what = What;
                who = Who;
                where = whereTxt.Text;
                /*what = (WHAT)Enum.Parse(typeof(WHAT), whatComboBox.SelectedItem.ToString());
                who = (WHO)Enum.Parse(typeof(WHO), whoComboBox.SelectedItem.ToString());
                where = whereTxt.Text;

                if (what == WHAT.None || who == WHO.None)
                {
                    MessageBox.Show("All red field have to be specified", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }*/
            }
            else
            {
                what = WHAT.None;
                who = WHO.None;
                where = string.Empty;
            }


            // controllare se gia' presente

            if (who == WHO.Scenarios && string.IsNullOrEmpty(Settings.Default.ScenariosCentralUnitWhere))
            {
                ScenariosFrm scenFrm;

                if (MessageBox.Show("You have to set the where's scenarios central unit in order to manage scenarios\n\r" +
                    "Do you want to set it now?", "MyHomeShortcut", MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.No)
                {
                    return;
                }

                scenFrm = new ScenariosFrm();

                if (scenFrm.ShowDialog() != DialogResult.OK)
                    return;

                Settings.Default.ScenariosCentralUnitWhere = scenFrm.ScenariosCentralUnitWhere;
                Settings.Default.Save();
            }

            this.actions.Add(new Action()
            {
                What = what,
                Who = who,
                Where = where,
                Toggle = toggleCheckBox.Checked,
                Command = (string.IsNullOrEmpty(commandTxt.Text) ? string.Empty : commandTxt.Text)
            });

            actionsListBox.DataSource = null;
            actionsListBox.DataSource = this.actions;

            What = WHAT.None;
            Who = WHO.None;
            Where = string.Empty;
            Command = string.Empty;
        }

        private void removeActionBtn_Click(object sender, EventArgs e)
        {
            Action action;

            if ((action = actionsListBox.SelectedItem as Action) == null)
                return;

            this.actions.Remove(action);

            actionsListBox.DataSource = null;
            actionsListBox.DataSource = this.actions;
        }

        private void actionsListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            Action action;

            if ((action = actionsListBox.SelectedItem as Action) == null)
            {
                removeActionBtn.Enabled = false;
                return;
            }

            removeActionBtn.Enabled = true;
        }

        private void whoComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            string[] what;
            WHO who;

            if (whoComboBox.SelectedItem == null)
                return;

            who = (WHO)Enum.Parse(typeof(WHO), whoComboBox.SelectedItem.ToString());
            whereLbl.Text = who == WHO.Scenarios ? "Scenario Number" : "Where";
            toggleCheckBox.Enabled = false;

            switch (who)
            {
                case WHO.Lighting:
                    what = (from w in commands
                            where w.Contains("Light") || w.Contains("Dimmer")
                            select w).ToArray();
                    toggleCheckBox.Enabled = true;
                    break;
                default:
                    what = (from w in commands
                            where w.Contains(who.ToString())
                            select w).ToArray();
                    break;
            }

            whatComboBox.DataSource = null;
            whatComboBox.DataSource = what;

        }

        #endregion
    }
}

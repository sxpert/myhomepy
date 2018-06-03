using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using MyHomeShortcut.Properties;
using System.IO;
using OpenWebNet;
using System.Runtime.InteropServices;
using System.Net.Sockets;
using OpenWebNet.Messages;

namespace MyHomeShortcut
{
    public partial class MainFrm : Form
    {
        private object toggleObject = new object();
        private readonly InterceptKeys.LowLevelKeyboardProc _proc;
        private IntPtr _hookID = IntPtr.Zero;

        private OpenWebNetGateway gateway;
        private List<Shortcut> shortcuts;
        private Dictionary<string, Action> toggleActions;

        private Lighting lighting;
        private Automation automation;
        private Scenarios scenarios;

        public MainFrm()
        {
            InitializeComponent();

            if (!File.Exists(Settings.Default.ShortcutsFilename))
                this.shortcuts = new List<Shortcut>();
            else
                this.shortcuts = Shortcut.Read(Settings.Default.ShortcutsFilename);

            this.shortcutsListBox.DataSource = null;
            this.shortcutsListBox.DataSource = this.shortcuts;
            this.shortcutsListBox.SelectedItem = null;

            toggleActions = new Dictionary<string, Action>();

            mainShortcutControl1.ShortcutEditingCompleted += new EventHandler<MyHomeShortcut.AddShortcutControls.ShortcutEventArgs>(mainShortcutControl1_ShortcutEditingCompleted);
        }

        public void ProcessShortcut(Keys key, bool ctrl, bool alt, bool shift)
        {
            bool hasKeyTwo = false;

            try
            {
                if (gateway == null)
                    return;

                if ((ctrl && alt) || (ctrl && shift) || (alt && shift))
                    hasKeyTwo = true;

                foreach (Shortcut s in this.shortcuts)
                {
                    if (s.KeyOne == Keys.Alt && alt || s.KeyOne == Keys.Control && ctrl || s.KeyOne == Keys.Shift && shift)
                    {
                        if (s.KeyTwo == Keys.None && hasKeyTwo || s.KeyTwo != Keys.None && !hasKeyTwo)
                        {
                            continue;
                        }
                        else if (s.KeyTwo == Keys.Alt && !alt || s.KeyTwo == Keys.Control && !ctrl || s.KeyTwo == Keys.Shift && !shift)
                        {
                            continue;
                        }

                        if (s.KeyThree == key)
                        {
                            ShowBallonTip(s.Name.ToString());

                            // execute action

                            foreach (Action a in s.Actions)
                            {
                                if (a.Toggle && a.Who == WHO.Lighting)
                                {
                                    lock (toggleActions)
                                    {
                                        if (!toggleActions.ContainsKey(a.Where))
                                        {
                                            toggleActions[a.Where] = a;

                                            if (lighting == null)
                                                lighting = new Lighting(gateway);
                                            
                                            lighting.GetLightStatus(a.Where);
                                        }
                                    }
                                }
                                else
                                {
                                    ExecuteAction(a);
                                }
                            }

                            break;
                        }
                    }
                }

            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #region Event Handlers

        #region Gateway Event Handlers

        private void gateway_ConnectionError(object sender, OpenWebNetErrorEventArgs e)
        {
            SocketException socketEx;

            if (e.Exception == null)
                return;

            socketEx = e.Exception as SocketException;

            if (socketEx == null)
            {
                MessageBox.Show("Error: " + e.Exception.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (socketEx.SocketErrorCode == SocketError.ConnectionRefused)
            {
                MessageBox.Show("The server has refused the connection...Check IP and Port", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void gateway_Connected(object sender, EventArgs e)
        {
            //connectToolStripMenuItem.Text = "Disconnect";

            toolStripStatusLabel1.Text = "Connected...";
            ShowBallonTip("Connected");
        }

        #endregion

        private void mainShortcutControl1_ShortcutEditingCompleted(object sender, MyHomeShortcut.AddShortcutControls.ShortcutEventArgs e)
        {
            if (this.shortcuts.Contains(e.Shortcut))
            {
                this.shortcuts.Remove(e.Shortcut);
            }

            this.shortcuts.Add(e.Shortcut);

            shortcutsListBox.DataSource = null;
            shortcutsListBox.DataSource = this.shortcuts;
        }

        private void removeShortcutBtn_Click(object sender, EventArgs e)
        {
            Shortcut shortcut;

            if ((shortcut = shortcutsListBox.SelectedItem as Shortcut) == null)
                return;

            this.shortcuts.Remove(shortcut);

            this.shortcutsListBox.DataSource = null;
            this.shortcutsListBox.DataSource = this.shortcuts;
            this.shortcutsListBox.SelectedItem = null;
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void MainFrm_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
                if (gateway != null)
                    gateway.Disconnect();

                Shortcut.Save(this.shortcuts, Settings.Default.ShortcutsFilename);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }

        private void MainFrm_Load(object sender, EventArgs e)
        {
            OptionsFrm options;

            try
            {
                if (Settings.Default.FirstTime)
                {
                    options = new OptionsFrm();

                    if (options.ShowDialog() != DialogResult.OK)
                    {
                        //connectToolStripMenuItem.Enabled = false;
                        return;
                    }

                    Settings.Default.IP = options.Ip;
                    Settings.Default.Port = options.Port;
                    Settings.Default.FirstTime = false;
                    Settings.Default.Save();
                }

                if (Settings.Default.GWType == GatewayType.Ethernet)
                {
                    gateway = new EthGateway(Settings.Default.IP, int.Parse(Settings.Default.Port), OpenSocketType.Command);
                }
                else
                {
                    gateway = new UsbGateway(Settings.Default.Port);
                }

                lighting = new Lighting(gateway);
                automation = new Automation(gateway);
                scenarios = new Scenarios(gateway);

                connectToolStripMenuItem.Enabled = false;

                gateway.ConnectionError += new EventHandler<OpenWebNetErrorEventArgs>(gateway_ConnectionError);
                gateway.Connected += new EventHandler(gateway_Connected);
                gateway.MessageReceived += new EventHandler<OpenWebNetMessageEventArgs>(gateway_MessageReceived);
                gateway.Connect();
            }
            catch (Exception ex)
            {
#if DEBUG
                throw ex;
#endif

                MessageBox.Show("Error: " + ex.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void gateway_MessageReceived(object sender, OpenWebNetMessageEventArgs e)
        {
            Action action;
            WHAT what;
            //OpenWebNet.Message msg;
            BaseMessage msg;

            try
            {
                // controllare se arriva un NACK durante la connessione...

                lock (toggleActions)
                {
                    msg = e.Message;

                    if (msg == null || msg.Who != WHO.Lighting)
                        return;

                    if (toggleActions.ContainsKey(msg.Where))
                    {
                        Action ac = toggleActions[msg.Where];

                        if (msg.What == WHAT.LightON || msg.What == WHAT.DimmerStrenght)
                        {
                            what = WHAT.LightOFF;
                        }
                        else if (msg.What == WHAT.LightOFF)
                        {
                            what = WHAT.LightON;
                        }
                        else
                        {
                            return;
                        }

                        action = new Action() { Who = ac.Who, What = what, Where = ac.Where };

                        toggleActions.Remove(msg.Where);
                        ExecuteAction(action);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void optionsToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void notifyIcon_Click(object sender, EventArgs e)
        {
            this.Show();
            this.Focus();
            this.Activate();
        }

        private void MainFrm_Resize(object sender, EventArgs e)
        {
            if (this.WindowState == FormWindowState.Minimized)
                this.Hide();
        }

        private void modifyBtn_Click(object sender, EventArgs e)
        {
            Shortcut shortcut;

            if ((shortcut = shortcutsListBox.SelectedItem as Shortcut) == null)
                return;

            mainShortcutControl1.Shortcut = shortcut;
        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AboutFrm aboutFrm = new AboutFrm();
            aboutFrm.ShowDialog();
        }

        private void gatewayConfigurationToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OptionsFrm options;

            options = new OptionsFrm();
            options.Ip = Settings.Default.IP;
            options.Port = Settings.Default.Port;
            options.Type = Settings.Default.GWType;

            if (options.ShowDialog() == DialogResult.OK)
            {
                Settings.Default.IP = options.Ip;
                Settings.Default.Port = options.Port;
                Settings.Default.GWType = options.Type;
                Settings.Default.FirstTime = false;
                Settings.Default.Save();

                MessageBox.Show("The application will be restarted", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);

                Application.Restart();
            }
        }

        private void scenariosToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ScenariosFrm scenariosFrm = new ScenariosFrm();
            scenariosFrm.ScenariosCentralUnitWhere = Settings.Default.ScenariosCentralUnitWhere;

            if (scenariosFrm.ShowDialog() == DialogResult.OK)
            {
                Settings.Default.ScenariosCentralUnitWhere = scenariosFrm.ScenariosCentralUnitWhere;
                Settings.Default.Save();
            }
        }

        private void shortcutsListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            Shortcut shortcut;

            if ((shortcut = shortcutsListBox.SelectedItem as Shortcut) == null)
            {
                modifyBtn.Enabled = false;
                removeShortcutBtn.Enabled = false;

                return;
            }

            modifyBtn.Enabled = true;
            removeShortcutBtn.Enabled = true;
        }

        #endregion

        #region Private Methods

        private void ShowBallonTip(string text)
        {
            notifyIcon.BalloonTipText = text;
            notifyIcon.BalloonTipTitle = "MyHomeShortcut";
            notifyIcon.ShowBalloonTip(1000);
        }

        private void ExecuteAction(Action action)
        {
            string where;

            try
            {
                if (!gateway.IsConnectedToGateway)
                {
                    MessageBox.Show("MyHomeShortcut isn't connected to the gateway...Check IP and Port", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                if (action == null)
                    return;

                if (action.What == WHAT.None || action.Who == WHO.None || string.IsNullOrEmpty(action.Where) && !string.IsNullOrEmpty(action.Command))
                {
                    gateway.SendData(action.Command);
                    return;
                }

                where = action.Where;

                switch (action.What)
                {
                    case WHAT.LightON:
                        lighting.LightON(where);
                        break;
                    case WHAT.LightOFF:
                        lighting.LightOFF(where);
                        break;
                    case WHAT.DimmerUp:
                        lighting.DimmerUp(where);
                        break;
                    case WHAT.DimmerDown:
                        lighting.DimmerDown(where);
                        break;
                    case WHAT.AutomationUp:
                        automation.Up(where);
                        break;
                    case WHAT.AutomationDown:
                        automation.Down(where);
                        break;
                    case WHAT.AutomationStop:
                        automation.Stop(where);
                        break;
                    case WHAT.ScenariosON:
                        scenarios.Activate(Settings.Default.ScenariosCentralUnitWhere, int.Parse(where));
                        break;
                    case WHAT.ScenariosOFF:
                        scenarios.Deactivate(Settings.Default.ScenariosCentralUnitWhere, int.Parse(where));
                        break;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #endregion

        private void connectToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {

                if (gateway == null)
                    return;

                if (gateway.IsConnected)
                {
                    gateway.Disconnect();
                    //connectToolStripMenuItem.Text = "Connect";
                }
                else
                    gateway.Connect();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}

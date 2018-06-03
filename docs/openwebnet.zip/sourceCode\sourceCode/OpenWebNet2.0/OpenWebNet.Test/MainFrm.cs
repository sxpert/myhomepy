using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Reflection;
using OpenWebNet;

namespace OpenWebNet.Test
{
    public partial class MainFrm : Form
    {
        private OpenWebNetGateway command, monitor;
        private delegate void UpdateResults(string data);

        private UpdateResults commandUpdateRes, monitorUpdateRes;
        private List<MethodInfo> commands;

        public MainFrm()
        {
            InitializeComponent();

            commandUpdateRes = new UpdateResults(this.UpdateCommandResults);
            monitorUpdateRes = new UpdateResults(this.UpdateMonitorResults);
            disconnectBtn.Enabled = false;

            ipTxt.Text = Properties.Settings.Default.Ip;
            portTxt.Text = Properties.Settings.Default.Port;
        }

        private void connectBtn_Click(object sender, EventArgs e)
        {
            command = new EthGateway(ipTxt.Text, int.Parse(portTxt.Text), OpenSocketType.Command);
            command.DataReceived += new EventHandler<OpenWebNetDataEventArgs>(command_DataReceived);
            command.ConnectionError += new EventHandler<OpenWebNetErrorEventArgs>(gateway_ConnectionError);

            monitor = new EthGateway(ipTxt.Text, int.Parse(portTxt.Text), OpenSocketType.Monitor);
            monitor.DataReceived += new EventHandler<OpenWebNetDataEventArgs>(monitor_DataReceived);
            monitor.ConnectionError += new EventHandler<OpenWebNetErrorEventArgs>(monitor_ConnectionError);

            monitor.Connect();
            command.Connect();



            disconnectBtn.Enabled = true;
            connectBtn.Enabled = false;
        }

        private void monitor_ConnectionError(object sender, OpenWebNetErrorEventArgs e)
        {
            this.Invoke(monitorUpdateRes, e.ErrorType.ToString());

            if (e.ErrorType == OpenWebNetErrorType.Exception)
                MessageBox.Show(e.Exception.ToString());
        }

        private void monitor_DataReceived(object sender, OpenWebNetDataEventArgs e)
        {
            this.Invoke(monitorUpdateRes, e.Data);
        }

        private void gateway_ConnectionError(object sender, OpenWebNetErrorEventArgs e)
        {
            this.Invoke(commandUpdateRes, e.ErrorType.ToString());

            if (e.ErrorType == OpenWebNetErrorType.Exception)
                MessageBox.Show(e.Exception.ToString());
        }

        private void command_DataReceived(object sender, OpenWebNetDataEventArgs e)
        {
            this.Invoke(commandUpdateRes, e.Data);
        }

        private void UpdateCommandResults(string data)
        {
            commandResultsTxt.Text += Environment.NewLine + data + Environment.NewLine;
        }

        private void UpdateMonitorResults(string data)
        {
            monitorResultsTxt.Text += Environment.NewLine + data + Environment.NewLine;
        }

        private void sendBtn_Click(object sender, EventArgs e)
        {
            try
            {
				command.SendCommand(commandTxt.Text);
                //command.SendData(commandTxt.Text);
            }
            catch (Exception ex)
            {
                commandResultsTxt.Text += Environment.NewLine + "### Error: " + ex.Message + Environment.NewLine;

                if (!command.IsConnected)
                {
                    commandResultsTxt.Text += Environment.NewLine + "Disconnesso" + Environment.NewLine;

                    disconnectBtn.Enabled = false;
                    connectBtn.Enabled = true;
                }
            }
        }

        private void disconnectBtn_Click(object sender, EventArgs e)
        {
            command.Disconnect();
            monitor.Disconnect();

            connectBtn.Enabled = true;
            disconnectBtn.Enabled = false;
        }

        private void MainFrm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Properties.Settings.Default.Ip = ipTxt.Text;
            Properties.Settings.Default.Port = portTxt.Text;

            Properties.Settings.Default.Save();
        }
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Reflection;
using OpenWebNet;
using log4net;

namespace OpenWebNet.Test
{
    public partial class MainFrm : Form
    {
        private ILog logger;

        private OpenWebNetGateway gateway;
        private delegate void UpdateResults(string data);

        private UpdateResults updateRes;
        private List<MethodInfo> commands;

        public MainFrm()
        {
            InitializeComponent();

            logger = LogManager.GetLogger(typeof(MainFrm));
            updateRes = new UpdateResults(this.UpdateResultsTxt);
            disconnectBtn.Enabled = false;
            
            commands = GetCommands();

            foreach (MethodInfo command in commands)
                commandsListBox.Items.Add(command.Name);

            ipTxt.Text = Properties.Settings.Default.Ip;
            portTxt.Text = Properties.Settings.Default.Port;

            logger.Debug("Logger caricato");
       }

        private void connectBtn_Click(object sender, EventArgs e)
        {
            if (gatewayComboBox.SelectedIndex == 0)
            {
                gateway = new UsbGateway(portTxt.Text);
                
                logger.Debug("Creato gateway USB");
            }
            else if (gatewayComboBox.SelectedIndex == 1)
            {
                gateway = new EthGateway(ipTxt.Text, int.Parse(portTxt.Text), OpenSocketType.Command);

                logger.Debug("Creato WebServer");
            }
            else
            {
                return;
            }

            
            gateway.MessageReceived += new EventHandler<OpenWebNetDataEventArgs>(gateway_MessageReceived);
            gateway.ConnectionError += new EventHandler<OpenWebNetErrorEventArgs>(gateway_ConnectionError);
            gateway.Connect();

            logger.Debug("Mi connetto");

            disconnectBtn.Enabled = true;
            connectBtn.Enabled = false;
            monitorBtn.Enabled = false;
        }

        private void gateway_ConnectionError(object sender, OpenWebNetErrorEventArgs e)
        {
            MessageBox.Show(e.Exception.ToString());
        }

        private void gateway_MessageReceived(object sender, OpenWebNetDataEventArgs e)
        {
            logger.Debug(string.Format("Message received: {0}", e.Data));

            this.Invoke(updateRes, e.Data);
        }

        private void gateway_DataReceived(object sender, OpenWebNetDataEventArgs e)
        {
            logger.Debug(string.Format("Data received: {0}", e.Data));

            this.Invoke(updateRes, e.Data);
        }

        private void UpdateResultsTxt(string data)
        {
            resultsTxt.Text += Environment.NewLine + data + Environment.NewLine;
        }

        private void sendBtn_Click(object sender, EventArgs e)
        {
            try
            {
                MethodInfo method;
                ParameterInfo[] parameters;
                string[] param;
                object[] invokeParameters = null;

                if (commandsListBox.SelectedIndex < 0)
                    return;

                method = commands[commandsListBox.SelectedIndex];
                parameters = method.GetParameters();
                invokeParameters = null;

                if (parameters.Length > 0)
                {
                    invokeParameters = new object[parameters.Length];
                    //invokeParameters = (object[])parametersTxt.Text.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
                    param = parametersTxt.Text.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
                    
                    //sistemare
                    if (param.Length != parameters.Length)
                    {
                        MessageBox.Show("Il numero di parametri non coincide");
                        return;
                    }

                    for (int i = 0; i < parameters.Length; i++)
                    {
                        if (parameters[i].ParameterType == typeof(int))
                        {
                            invokeParameters[i] = int.Parse(param[i]);
                        }
                        else if (parameters[i].ParameterType == typeof(uint))
                        {
                            invokeParameters[i] = uint.Parse(param[i]);
                        }
                        else if (parameters[i].ParameterType == typeof(double))
                        {
                            invokeParameters[i] = double.Parse(param[i]);
                        }
                        else
                        {
                            invokeParameters[i] = param[i];
                        }
                    }
                }

                logger.Debug(string.Format("Invoking {0}({1})", method.Name, parametersTxt.Text)); 

                method.Invoke(gateway, invokeParameters);
            }
            catch (Exception ex)
            {
                resultsTxt.Text += Environment.NewLine + "### Error: " + ex.Message + Environment.NewLine;


                logger.Error("Errore", ex);

                if (!gateway.IsConnected)
                {
                    resultsTxt.Text += Environment.NewLine + "Disconnesso" + Environment.NewLine;

                    disconnectBtn.Enabled = false;
                    connectBtn.Enabled = true;
                }
            }
        }

        private void disconnectBtn_Click(object sender, EventArgs e)
        {
            gateway.Disconnect();

            connectBtn.Enabled = true;
            disconnectBtn.Enabled = false;

            logger.Debug("Mi disconnetto");
        }

        private void gatewayComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (gatewayComboBox.SelectedIndex == 0)
            {
                portTxt.Text = "COM3";
                ipTxt.Text = "";
            }
            else
            {
                // port e ip
            }
        }

        private List<MethodInfo> GetCommands()
        {
            // un metodo 

            List<MethodInfo> methods = new List<MethodInfo>(typeof(OpenWebNetGateway).GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.DeclaredOnly));
            List<PropertyInfo> properties = new List<PropertyInfo>(typeof(OpenWebNetGateway).GetProperties());
            List<EventInfo> events = new List<EventInfo>(typeof(OpenWebNetGateway).GetEvents());

            MethodInfo m;

            for (int i = 0; i < methods.Count; i++)
            {
                foreach (EventInfo ev in events)
                {
                    m = ev.GetAddMethod();

                    if (m != null && methods[i].Name == m.Name)
                        methods.Remove(methods[i]);

                    m = ev.GetRemoveMethod();

                    if (m != null && methods[i].Name == m.Name)
                        methods.Remove(methods[i]);
                }

                foreach (PropertyInfo property in properties)
                {
                    m = property.GetGetMethod();

                    if (m != null && methods[i].Name == m.Name)
                        methods.Remove(methods[i]);

                    m = property.GetSetMethod();

                    if (m != null && methods[i].Name == m.Name)
                        methods.Remove(methods[i]);
                }

                if (methods[i].Name == "Connect")
                    methods.Remove(methods[i]);

                if (methods[i].Name == "Disconnect")
                    methods.Remove(methods[i]);
            }

            return methods;
        }

        private void commandsListBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            MethodInfo method;
            ParameterInfo[] parameters;

            if (commandsListBox.SelectedIndex < 0)
                return;

            method = commands[commandsListBox.SelectedIndex];
            parameters = method.GetParameters();
            parametersLbl.Text = "";

            if (parameters.Length > 0)
            {
                parametersTxt.Enabled = true;

                foreach (ParameterInfo param in parameters)
                {
                    parametersLbl.Text += param.Name + " , ";
                }
            }
        }

        private void MainFrm_FormClosing(object sender, FormClosingEventArgs e)
        {
            Properties.Settings.Default.Ip = ipTxt.Text;
            Properties.Settings.Default.Port = portTxt.Text;

            Properties.Settings.Default.Save();
        }

        private void testMessageBtn_Click(object sender, EventArgs e)
        {
            MessageFrm messFrm = new MessageFrm();

            messFrm.Show();
        }

        private void monitorBtn_Click(object sender, EventArgs e)
        {
            if (gatewayComboBox.SelectedIndex != 1)
                return;


            gateway = new EthGateway(ipTxt.Text, int.Parse(portTxt.Text), OpenSocketType.Monitor);

            logger.Debug("Creato WebServer");

            gateway.DataReceived += new EventHandler<OpenWebNetDataEventArgs>(gateway_DataReceived);
            gateway.MessageReceived += new EventHandler<OpenWebNetDataEventArgs>(gateway_MessageReceived);
            gateway.Connect();

            logger.Debug("Mi connetto");

            disconnectBtn.Enabled = true;
            connectBtn.Enabled = false;
            monitorBtn.Enabled = false;
        }

        private void superSocketBtn_Click(object sender, EventArgs e)
        {
            if (gatewayComboBox.SelectedIndex == 0)
            {
                gateway = new UsbGateway(portTxt.Text);

                logger.Debug("Creato gateway USB");
            }
            else if (gatewayComboBox.SelectedIndex == 1)
            {
                gateway = new EthGateway(ipTxt.Text, int.Parse(portTxt.Text), OpenSocketType.SuperCommand);

                logger.Debug("Creato WebServer");
            }
            else
            {
                return;
            }

            //gateway.DataReceived += new EventHandler<DataEventArgs>(gateway_DataReceived);
            gateway.MessageReceived += new EventHandler<OpenWebNetDataEventArgs>(gateway_MessageReceived);
            gateway.Connect();

            logger.Debug("Mi connetto");

            disconnectBtn.Enabled = true;
            connectBtn.Enabled = false;
            monitorBtn.Enabled = false;
        }
    }
}

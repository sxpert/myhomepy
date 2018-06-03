using System;
using System.Collections.Generic;
using System.Text;
using System.IO.Ports;
using OpenWebNet;

namespace OpenWebNet
{
    public class UsbGateway : OpenWebNetGateway
    {
        private SerialPort port;
        private string buffer;
        private bool connOK;

        public override event EventHandler<OpenWebNetDataEventArgs> DataReceived;
        public override event EventHandler<OpenWebNetDataEventArgs> MessageReceived;
        public override event EventHandler<OpenWebNetErrorEventArgs> ConnectionError;
        public override event EventHandler Connected;

        public UsbGateway(string portName)
            : base()
        {
            if (string.IsNullOrEmpty(portName))
                throw new ArgumentException("Specificare portName");

            port = new SerialPort(portName);

            port.DataBits = 8;
            port.BaudRate = 115200;
            port.StopBits = StopBits.One;
            port.Parity = Parity.None;
            port.Handshake = Handshake.None;
            port.ParityReplace = 63;
            port.ReceivedBytesThreshold = 1;
            port.ReadTimeout = -1;
            port.DataReceived += new SerialDataReceivedEventHandler(port_DataReceived);

            buffer = string.Empty;
        }

        public override bool IsConnected
        {
            get
            {
                return port.IsOpen;
            }
        }

        #region Static Methods

        public static string[] GetPorts()
        {
            return SerialPort.GetPortNames();
        }

        #endregion

        #region Public Methods

        public override void Connect()
        {
            if (!port.IsOpen)
                port.Open();

            if (!connOK)
            {
                connOK = true;

                if (Connected != null)
                    Connected(this, EventArgs.Empty);
            }
        }

        public override void Disconnect()
        {
            if (port.IsOpen)
                port.Close();

            connOK = false;
        }

        public override void SendCommand(WHO chi, string cosa, string dove)
        {
            if (dove == string.Empty)
                SendData(string.Format(CMD_BUS_NO_WHERE, chiValues[chi.ToString()], cosa));
            else
                SendData(string.Format(CMD_BUS, chiValues[chi.ToString()], cosa, dove));
        }

        public override void GetStateCommand(WHO chi, string dove)
        {
            if (string.IsNullOrEmpty(dove))
                SendData(string.Format(GET_STATE_NO_WHERE, chiValues[chi.ToString()]));
            else
                SendData(string.Format(GET_STATE, chiValues[chi.ToString()], dove));
        }

        public override void SendData(string data)
        {
            if (!port.IsOpen && !connOK)
                throw new InvalidOperationException("Non e' stata effettuata la connessione");

            if (!port.IsOpen && connOK)
                port.Open();

            port.DiscardOutBuffer();
            port.WriteLine(data);
        }

        #endregion

        #region Private Methods

        private void port_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            int index;
            string message, data;

            data = port.ReadExisting();

            if (DataReceived != null)
                DataReceived(this, new OpenWebNetDataEventArgs(data));

            // gestisco per l'evento CommandReceived

            // non controllo se e' un messaggio corretto...
            // creo solo il messaggio completo

            data = data.Trim();

            if ((index = data.IndexOf(MSG_END)) < 0)
            {
                // non ho un messaggio completo

                if (buffer == string.Empty)
                {
                    buffer = data;
                    return;

                }
                else
                {
                    buffer += data;
                }
            }
            else
            {
                while ((index = data.IndexOf(MSG_END)) >= 0)
                {
                    message = data.Substring(0, index + MSG_END.Length);
                    data = data.Remove(0, index + MSG_END.Length);

                    if (buffer == string.Empty)
                        buffer = message;
                    else
                        buffer += message;

                    if (MessageReceived != null)
                        MessageReceived(this, new OpenWebNetDataEventArgs(buffer));

                    buffer = string.Empty;
                }

                if (data != "")
                    buffer = data;
            }

            /*foreach (string d in datas)
            {
                if (data == PROT_NACK)
                {
                    // leggo per un NACK specifico e lancio un eccezione
                    throw new NACKException();
                }
            }*/
        }

        #endregion
    }
}


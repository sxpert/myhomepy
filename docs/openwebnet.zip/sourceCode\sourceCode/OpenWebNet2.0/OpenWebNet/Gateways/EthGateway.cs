using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Timers;
using OpenWebNet.Messages;
using System.Diagnostics;
using OpenWebNet.Common;

namespace OpenWebNet
{
    public class EthGateway : OpenWebNetGateway
    {
        private enum Status
        {
            Disconnected,     // TCP disconnected
            WaitConnection,   // waiting to complete connection
            WaitAck,          // waiting the first ACK response
            WaitAck2,         // waiting the second ACK response
            Handshaked,       // handshaking complete.
        }

        public override event EventHandler<OpenWebNetDataEventArgs> DataReceived;
        public override event EventHandler<OpenWebNetMessageEventArgs> MessageReceived;
        public override event EventHandler<OpenWebNetErrorEventArgs> ConnectionError;
        public override event EventHandler Connected;
        
        public event EventHandler Disconnected;

        private AsyncCallback onDataReady;
        private AsyncCallback onSendData;
        
        private Status status;
        private OpenSocketType socketType;
        private EndPoint endPoint;
        private Socket socket;
        private Timer ackTimer;
        
        private string host;
        private int port;
        private string bufferString;
        private string dataToSend;
        private byte[] buffer;
        private const int bufferSize = 10000;
        private bool openWebConnOk;

        internal const string PROT_CMD = "*99*0##";
        internal const string PROT_MON = "*99*1##";
        internal const string PROT_SCMD = "*99*9##"; 

        public EthGateway(string host, int port, OpenSocketType socketType)
        {
            if (string.IsNullOrEmpty(host))
                throw new ArgumentNullException("host");

            if (port < IPEndPoint.MinPort || port > IPEndPoint.MaxPort)
                throw new ArgumentOutOfRangeException("port");

            this.host = host;
            this.port = port;
            this.socketType = socketType;
            this.status = Status.Disconnected;
            this.buffer = new byte[bufferSize];
            this.bufferString = String.Empty;
            this.dataToSend = string.Empty;
            this.onDataReady = new AsyncCallback(OnDataReady);
            this.onSendData = new AsyncCallback(OnSendData);
            this.ackTimer = new Timer(15000);
            this.ackTimer.Elapsed += new ElapsedEventHandler(ackTimer_Elapsed);
        }

        #region Public Properties

        public string Host { get; internal set; }

        public int Port { get; internal set; }

        public override bool IsConnected
        {
            get
            {
                return (socket != null && socket.Connected);
            }
        }

        public override bool IsConnectedToGateway
        {
            get
            {
                return openWebConnOk;
            }
        }

        #endregion

        #region Public methods

        public override void Connect()
        {
            try
            {
                if (IsConnected)
                {
                    openWebConnOk = true;
                    return;
                }

                status = Status.WaitConnection;
                bufferString = string.Empty;

                if (endPoint == null)
                    endPoint = new IPEndPoint(IPAddress.Parse(host), port);

                if (socket == null)
                {
                    socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                    socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
                }

                socket.BeginConnect(endPoint, new AsyncCallback(OnConnect), null);
            }
            catch (Exception ex)
            {
                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.Exception, ex));

                status = Status.Disconnected;
                socket.Shutdown(SocketShutdown.Both);
            }
        }

        public override void Disconnect()
        {
            status = Status.Disconnected;

            if (socket != null)
            {
                if (IsConnected)
                {
                    ackTimer.Stop();
                    socket.Shutdown(SocketShutdown.Both);
                    socket.Close();
                    socket = null;

                    openWebConnOk = false;
                }

                if (Disconnected != null)
                    Disconnected(this, EventArgs.Empty);
            }
        }

        public override void SendCommand<T>(T message)
        {
            if (message == null)
            {
                throw new ArgumentNullException("message");
            }

            SendCommand(message.ToString());
        }

        public override void SendCommand(string data)
        {
            ASCIIEncoding enc;
            byte[] _buffer;

            //if (!openWebConnOk && !IsConnected)
            //    throw new InvalidOperationException("First you have to call Connect");

            if (!IsConnected)
                throw new InvalidOperationException("First you have to call Connect");

            try
            {
                if (openWebConnOk && !IsConnected)
                {
                    dataToSend = data;

                    if (socket == null)
                    {
                        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
                    }

                    socket.BeginConnect(endPoint, new AsyncCallback(OnConnect), null);

                    return;
                }

                enc = new ASCIIEncoding();
                _buffer = enc.GetBytes(data);

                socket.BeginSend(_buffer, 0, _buffer.Length, SocketFlags.None, onSendData, null);
            }
            catch (Exception ex)
            {
                // gestione exception

                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.Exception, ex));
            }
        }

        #endregion

        #region Private Methods

        private void ManageConnectionStatus(string message)
        {
            if ((status == Status.WaitAck || status == Status.WaitAck2 || status == Status.WaitConnection) && Utilities.CouldeBeAPasswordSequence(message))
            {
                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.PasswordNeeded, null));
            }

            // gestione dei NACK

            switch (status)
            {
                case Status.WaitAck:
                    if (message == ACK)
                    {
                        status = Status.WaitAck2;

                        if (socketType == OpenSocketType.Command)
                            SendCommand(PROT_CMD);
                        else if (socketType == OpenSocketType.Monitor)
                            SendCommand(PROT_MON);
                        else
                            SendCommand(PROT_SCMD);
                    }
                    else
                    {
                        Disconnect();
                    }
                    break;
                case Status.WaitAck2:
                    if (message == ACK)
                    {
                        status = Status.Handshaked;

                        if (!openWebConnOk)
                        {
                            if (Connected != null)
                                Connected(this, EventArgs.Empty);

                            openWebConnOk = true;
                            ackTimer.Start();
                        }

                        // invio i dati dopo aver eseguito la riconnessione

                        if (dataToSend != string.Empty)
                        {
                            SendCommand(dataToSend);
                            dataToSend = string.Empty;
                        }
                    }
                    else
                    {
                        Disconnect();
                    }
                    break;
            }
        }

        private void OnSendData(IAsyncResult res)
        {
            try
            {
                socket.EndSend(res);
            }
            catch (Exception ex)
            {
                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.Exception, ex));
            }
        }

        private void OnConnect(IAsyncResult result)
        {
            try
            {
                // sistemare

                if (!socket.Connected)
                    throw new SocketException((int)SocketError.ConnectionRefused);

                socket.EndConnect(result);
                status = Status.WaitAck;
                socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, onDataReady, null);
            }
            catch (Exception ex)
            {
                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.Exception, ex));
            }
        }    

        private void OnDataReady(IAsyncResult result)
        {
            int index;
            int numBytes;
            string data, message;
            ASCIIEncoding enc;
            BaseMessage msg;

            try
            {
                if (!IsConnected)
                    return;

                numBytes = socket.EndReceive(result);

                if (numBytes == 0)
                {
                    socket.Shutdown(SocketShutdown.Both);
                    socket.Close();
                    socket = null;

                    return;
                }

                enc = new ASCIIEncoding();
                data = enc.GetString(buffer, 0, numBytes);

                Debug.Write(string.Format("[{0}] {1}", socketType.ToString(), data));

                if (DataReceived != null)
                    DataReceived(this, new OpenWebNetDataEventArgs(data));

                // si occupa della gestione dei messaggi...

                data = data.Trim();

                if ((index = data.IndexOf(MSG_END)) < 0)
                {
                    // non ho un messaggio completo

                    if (bufferString == string.Empty)
                    {
                        bufferString = data;
                        return;

                    }
                    else
                    {
                        bufferString += data;
                    }
                }
                else
                {
                    while ((index = data.IndexOf(MSG_END)) >= 0)
                    {
                        message = data.Substring(0, index + MSG_END.Length);
                        data = data.Remove(0, index + MSG_END.Length);

                        if (bufferString == string.Empty)
                            bufferString = message;
                        else
                            bufferString += message;

                        /*if ((msg = MessageAnalyzer.GetMessage(bufferString)) != null)
                        {
                            if (MessageReceived != null)
                                MessageReceived(this, new OpenWebNetMessageEventArgs(msg));
                        }*/

                        ManageConnectionStatus(bufferString);

                        bufferString = string.Empty;
                    }

                    if (data != "")
                        bufferString = data;
                }

                if (IsConnected)
                    socket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, onDataReady, null);
            }
            catch (Exception ex)
            {
                if (ConnectionError != null)
                    ConnectionError(this, new OpenWebNetErrorEventArgs(OpenWebNetErrorType.Exception, ex));
            }
        }

        private void ackTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            if (!IsConnected)
                return;


            SendCommand(ACK);
            ackTimer.Start();
        }

        #endregion
    }
}

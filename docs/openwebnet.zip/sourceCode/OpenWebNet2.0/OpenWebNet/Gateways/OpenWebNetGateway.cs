using System;
using System.Collections.Generic;
using System.Text;
using System.IO.Ports;
using OpenWebNet.Messages;
using OpenWebNet.Common;

namespace OpenWebNet
{
    public enum WHO
    {
        [StringValue("0")] Scenarios,
        [StringValue("1")] Lighting,
        [StringValue("2")] Automation,
        [StringValue("3")] PowerManagement,
        [StringValue("4")] Heating,
        [StringValue("5")] Alarm,
        [StringValue("6")] RemoteControl, // c'e' su USB ma non TCP controllare
        [StringValue("7")] Multimedia,
        [StringValue("9")] Auxiliaries, // taken from Alarm doc
        [StringValue("13")] OutsideInterface,
        [StringValue("16")] SoundSystem,
        [StringValue("1001")] DiagnosticAutomation,
        [StringValue("1004")] DiagnosticHeating,
        [StringValue("1013")] DiagnosticDevice,
        [StringValue(null)] None
    }

    public enum OpenSocketType
    {
        Command, // Used to send commands
        SuperCommand, // Used to send scenar commands
        Monitor  // Used to monitor asynchronous events on the device
    }

    public abstract partial class OpenWebNetGateway
    {
        public abstract event EventHandler<OpenWebNetDataEventArgs> DataReceived;
        public abstract event EventHandler<OpenWebNetMessageEventArgs> MessageReceived;
        public abstract event EventHandler<OpenWebNetErrorEventArgs> ConnectionError;
        public abstract event EventHandler Connected;

        public const int MAX_LENGTH_OPEN = 1024;
        public const string MSG_START = "*";
        public const string MSG_END = "##";
        public const string ACK = "*#*1##";
        public const string NACK = "*#*0##";
        public const string NACK_NOP = "*#*2##";
        public const string NACK_RET = "*#*3##";
        public const string NACK_COLL = "*#*4##";
        public const string NACK_NOBUS = "*#*5##";
        public const string NACK_BUSY = "*#*6##";
        public const string NACK_PROC = "*#*7##";

        public abstract bool IsConnected { get; }

        public abstract bool IsConnectedToGateway { get; }

        #region Abstract Methods

        public abstract void Connect();

        public abstract void Disconnect();

        public abstract void SendCommand<T>(T message) where T : BaseMessage;

        public abstract void SendCommand(String command);

        #endregion

        #region Virtual Methods

        /*public virtual void SendDimensionCommand(WHO chi, string dove, string grandezza, params string[] valori)
        {
            StringBuilder sb = new StringBuilder();
            
            foreach (var item in valori)
            {
                sb.AppendFormat("{0}*", item);
            }
            
            sb.Remove(sb.Length - 1, 1);
            SendData(string.Format(CMD_SET_DIMENSION, chi, grandezza, sb.ToString()));
        }

        public virtual void GetStateCommand(WHO chi, string dove)
        {
            if (string.IsNullOrEmpty(dove))
                SendData(string.Format(GET_STATE_NO_WHERE, chiValues[chi.ToString()]));
            else
                SendData(string.Format(GET_STATE, chiValues[chi.ToString()], dove));
        }

        public virtual void GetDimensionCommand(WHO chi, string dove, string grandezza)
        {
            if (string.IsNullOrEmpty(dove))
                SendData(string.Format(GET_DIMENSION, chiValues[chi.ToString()], string.Empty, grandezza));
            else
                SendData(string.Format(GET_DIMENSION, chiValues[chi.ToString()], dove, grandezza));
        }

        public virtual void WriteDimension(WHO who, string where, string dimension, string parameter)
        {
            SendData(string.Format(CMD_SET_DIMENSION, chiValues[who.ToString()], where, dimension, parameter));
        }

        public virtual void SendExternalDeviceCommand(WHO who, string what)
        {
            SendData(string.Format(CMD_EXT_IFACE, chiValues[chiValues.ToString()], what)); 
        }*/

        public virtual void DiscoverDevices()
        {

        }

        #endregion

        //Check if Open message is well formed (taken from OpenClientSocket.cs)
        public static bool IsWellFormedMessage(string message)
        {
            if (message.Length > MAX_LENGTH_OPEN)
                return false;

            // check if it is too short to contain the message delimiters
            if (message.Length < MSG_START.Length + MSG_END.Length)
                return false;

            // check start and end delimiters
            if (
                message[0] != MSG_START[0]
                || message[message.Length - 2] != MSG_END[0]
                || message[message.Length - 1] != MSG_END[1]
                )
                return false;

            // check if it is ACK
            if (message == MSG_START + ACK + MSG_END)
                return true;

            // check if it is NACK
            if (message == MSG_START + NACK + MSG_END)
                return true;

            // valid characters are '0' to '9' and '*' and '#' 
            foreach (char c in message)
            {
                if (
                    (c < '0' || c > '9')
                    && !(c == '*' || c == '#')
                    )
                    return false;
            }
            return true;

        }
    }

    public enum OpenWebNetErrorType
    {
        Nack,
        Exception,
        PasswordNeeded
    }

    #region OpenWebNet EventArgs

    public class OpenWebNetMessageEventArgs : EventArgs
    {
        public OpenWebNetMessageEventArgs(BaseMessage message)
            : base()
        {
            if (message == null)
                throw new ArgumentNullException("message");

            this.Message = message;
        }

        public BaseMessage Message { get; internal set; }
    }

    public class OpenWebNetDataEventArgs : EventArgs
    {
        private string data;

        public OpenWebNetDataEventArgs(string data)
            : base()
        {
            if (string.IsNullOrEmpty(data))
                throw new ArgumentNullException("data");

            this.data = data;
        }

        public string Data
        {
            get
            {
                return data;
            }
        }
    }

    public class OpenWebNetErrorEventArgs : EventArgs
    {
        public OpenWebNetErrorType ErrorType { get; private set; }
        public Exception Exception { get; private set; }

        public OpenWebNetErrorEventArgs(OpenWebNetErrorType errorType, Exception ex) : base()
        {
            this.ErrorType = errorType;
            this.Exception = ex;
        }
    }

    #endregion
}

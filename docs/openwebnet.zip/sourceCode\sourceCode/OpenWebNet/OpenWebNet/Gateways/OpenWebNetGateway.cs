using System;
using System.Collections.Generic;
using System.Text;
using System.IO.Ports;

namespace OpenWebNet
{
    // scenario On
    // Connect sincrono

    public enum WHO
    {
        Scenarios = 0,
        Lighting = 1,
        Automation = 2,
        PowerManagement = 3,
        Heating = 4,
        Alarm = 5,
        RemoteControl = 6, // c'e' su USB ma non TCP controllare
        Multimedia = 7,
        OutsideInterface = 13,
        SoundSystem = 16,
        DiagnosticAutomation = 1001,
        DiagnosticHeating = 1004,
        DiagnosticDevice = 1013,
        None
    }

    public enum OpenSocketType
    {
        Command, // Used to send commands
        SuperCommand, // Used to send scenar commands
        Monitor  // Used to monitor asynchronous events on the device
    }

    public abstract partial class OpenWebNetGateway
    {
        protected Dictionary<string, int> chiValues;

        public abstract event EventHandler<OpenWebNetDataEventArgs> DataReceived;
        public abstract event EventHandler<OpenWebNetDataEventArgs> MessageReceived;
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

        internal const string CMD_BUS = "*{0}*{1}*{2}##"; // *CHI*COSA*DOVE##
        internal const string CMD_BUS_NO_WHERE = "*{0}*{1}##"; // *CHI*COSA##
        internal const string CMD_EXT_IFACE = "*#{0}**{1}##";
        internal const string CMD_SET_DIMENSION = "*#{0}*{1}*#{2}##"; // *#CHI*DOVE*#GRANDEZZA*VAL## 
        internal const string GET_STATE = "*#{0}*{1}##"; // *#CHI*DOVE##
        internal const string GET_STATE_NO_WHERE = "*#{0}##"; // *#CHI##
        internal const string GET_DIMENSION = "*#{0}*{1}*{2}##"; // *#CHI*DOVE*GRANDEZZA##
        internal const string SET_STATE = "*#{0}*{1}#{2}##"; // *#CHI*DOVE#LIV#INT##

        public OpenWebNetGateway()
        {
            int[] values;
            string[] names;

            chiValues = new Dictionary<string, int>();
            names = Enum.GetNames(typeof(WHO));
            values = (int[])Enum.GetValues(typeof(WHO));

            for (int i = 0; i < names.Length; i++)
                chiValues.Add(names[i], values[i]);
        }

        public abstract bool IsConnected { get; }

        public abstract void Connect();

        public abstract void Disconnect();

        public abstract void SendCommand(WHO chi, string cosa, string dove);

        public void SendDimensionCommand(WHO chi, string dove, string grandezza, params string[] valori)
        {
            StringBuilder sb = new StringBuilder();
            foreach (var item in valori)
            {
                sb.AppendFormat("{0}*", item);
            }
            sb.Remove(sb.Length - 1, 1);
            SendData(string.Format(CMD_SET_DIMENSION, chi, grandezza, sb.ToString()));
        }

        public abstract void GetStateCommand(WHO chi, string dove);

        public void GetDimensionCommand(WHO chi, string dove, string grandezza)
        {
            if (string.IsNullOrEmpty(dove))
                SendData(string.Format(GET_DIMENSION, chi, string.Empty, grandezza));
            else
                SendData(string.Format(GET_DIMENSION, chi, dove, grandezza));
        }

        public abstract void SendData(string data);

        //public abstract void GetStateCommand(WHO chi, string dove, string parametri);

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
        private Message message;

        public OpenWebNetMessageEventArgs(Message message) : base()
        {
            if (message == null)
                throw new ArgumentNullException("message");

            this.message = message;
        }

        public Message Message
        {
            get
            {
                return message;
            }
        }
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

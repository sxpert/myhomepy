using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenWebNet.Common;

namespace OpenWebNet.Messages
{
    public enum MessageType
    {
        /// <summary>
        /// Comando eseguito correttamente
        /// </summary>
        [StringValue(OpenWebNetGateway.ACK)] ACK,
        /// <summary>
        /// Comando non eseguito
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK)] NACK,
        /// <summary>
        /// Comando non riconosciuto
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_NOP)] NACK_NOP,
        /// <summary>
        /// Comando gestito ma il dispositivo non esiste
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_RET)] NACK_RET,
        /// <summary>
        /// Comando non eseguito per collisione sul bus
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_COLL)] NACK_COLL,
        /// <summary>
        /// Comando non eseguito per impossibilita' ad accedere al bus
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_NOBUS)] NACK_NOBUS,
        /// <summary>
        /// Comando non eseguito in quanto l'interfaccia e' gia' impegnata in trasmissione
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_BUSY)] NACK_BUSY,
        /// <summary>
        /// Procedura multiframe non eseguita completemante
        /// </summary>
        [StringValue(OpenWebNetGateway.NACK_PROC)] NACK_PROC,
        /// <summary>
        /// Comando
        /// </summary>
        [StringValue(null)] Command,
        /// <summary>
        /// A password sequence
        /// </summary>
        [StringValue(null)] PasswordSequence,
        /// <summary>
        /// Stringa non riconosciuta
        /// </summary>
        [StringValue(null)] None
    }

    public class BaseMessage
    {
        protected const string CMD_BUS = "*{0}*{1}*{2}##"; // *WHO*WHAT*WHERE##
        protected const string CMD_BUS_NO_WHERE = "*{0}*{1}##"; // *WHO*WHAT##
        protected const string CMD_EXT_IFACE = "*#{0}**{1}##";
        protected const string CMD_SET_DIMENSION = "*#{0}*{1}*#{2}*{3}##"; // *#WHO*WHERE*#DIMENSION*VAL## 
        protected const string GET_STATE = "*#{0}*{1}##"; // *#WHO*WHERE##
        protected const string GET_STATE_NO_WHERE = "*#{0}##"; // *#WHO##
        protected const string GET_DIMENSION = "*#{0}*{1}*{2}##"; // *#WHO*WHERE*DIMENSION##
        protected const string SET_STATE = "*#{0}*{1}#{2}##"; // *#WHO*WHERE#LIV#INT##

        public WHO Who { get; set; }
        public MessageType MessageType { get; set; }
        public Where Where { get; set; }
        public String Message { get; set; }

        public BaseMessage()
        {
            Who = WHO.None;
            MessageType = MessageType.None;
            Where = null;
            Message = null;
        }
    }
}

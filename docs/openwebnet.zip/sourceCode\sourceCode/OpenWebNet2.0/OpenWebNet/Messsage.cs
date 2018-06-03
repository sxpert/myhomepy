using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public enum MessageType
    {
        /// <summary>
        /// Comando eseguito correttamente
        /// </summary>
        ACK,
        /// <summary>
        /// Comando non eseguito
        /// </summary>
        NACK,
        /// <summary>
        /// Comando non riconosciuto
        /// </summary>
        NACK_NOP,
        /// <summary>
        /// Comando gestito ma il dispositivo non esiste
        /// </summary>
        NACK_RET,
        /// <summary>
        /// Comando non eseguito per collisione sul bus
        /// </summary>
        NACK_COLL,
        /// <summary>
        /// Comando non eseguito per impossibilita' ad accedere al bus
        /// </summary>
        NACK_NOBUS,
        /// <summary>
        /// Comando non eseguito in quanto l'interfaccia e' gia' impegnata in trasmissione
        /// </summary>
        NACK_BUSY,
        /// <summary>
        /// Procedura multiframe non eseguita completemante
        /// </summary>
        NACK_PROC,
        /// <summary>
        /// Comando
        /// </summary>
        Command,
        /// <summary>
        /// Stringa non riconosciuta
        /// </summary>
        None
    }

    public class Message
    {
        public WHO Who { get; set; }
        public WHAT What { get; set; }
        public MessageType MessageType { get; set; }
        public string Where { get; set; }
        public string[] Parameters { get; set; }

        public Message()
        {
            Who = WHO.None;
            What = WHAT.None;
            MessageType = MessageType.None;
            Where = string.Empty;
            Parameters = null;
        }

        public override string ToString()
        {
            return string.Format("{0} - {1} - {2} - {3}", MessageType, Who.ToString(), What.ToString(), where);
        }
    }
}

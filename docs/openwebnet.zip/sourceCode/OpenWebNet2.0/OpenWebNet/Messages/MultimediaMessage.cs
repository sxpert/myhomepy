using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
    public class MultimediaMessage : BaseMessage
    {
        public MultimediaMessage() : base()
        {
            Who = WHO.RemoteControl;
            MessageType = MessageType.Command;
        }

        public int DisplayDialX { get; set; }
        public int DisplayDialY { get; set; }
    }
}

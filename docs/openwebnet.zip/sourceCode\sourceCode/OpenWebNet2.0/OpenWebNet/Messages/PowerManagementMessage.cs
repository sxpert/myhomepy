using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
    public class PowerManagementMessage : BaseMessage
    {
        public PowerManagementMessage() : base()
        {
            this.MessageType = MessageType.Command;
            this.Who = WHO.PowerManagement;
        }

        public int Voltage { get; set; }
        public int Current { get; set; }
        public int Power { get; set; }
        public int Energy { get; set; }
    }
}

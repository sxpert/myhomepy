using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
    public enum AutomationWhat
    {
        [StringValue(null)] None,
        [StringValue("1")] AutomationUp,
        [StringValue("2")] AutomationDown,
        [StringValue("0")] AutomationStop,
		[StringValue(null)] GetStatus
    }

    public class AutomationMessage : BaseMessage
    {
        public AutomationMessage() : base()
        {
            this.MessageType = MessageType.Command;
            this.Who = WHO.Automation;
            this.What = AutomationWhat.None;
        }

        public AutomationWhat What { get; set; }

        public override String ToString()
        {
			String value = null;

			switch (What)
			{
				case AutomationWhat.AutomationUp:
				case AutomationWhat.AutomationDown:
				case AutomationWhat.AutomationStop:
					value = String.Format(CMD_BUS, Who.GetStringValue(), What.GetStringValue(), Where);
					break;
				case AutomationWhat.GetStatus:
					value = String.Format(GET_STATE, Who.GetStringValue(), Where);
					break;
			}

			return value;
        }
    }
}

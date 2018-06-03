using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;

namespace OpenWebNet.Messages
{
    public class DeviceMessage : BaseMessage
    {
        public DeviceMessage() : base()
        {
            this.MessageType = MessageType.Command;
            this.Who = WHO.OutsideInterface;
        }

        public TimeSpan Time { get; set; }
        public DateTime Date { get; set; }
        public IPAddress IP { get; set; }
        public IPAddress Netmask { get; set; }
        public string MACAddress { get; set; }
        public GatewayModel Model { get; set; }
        public ProductVersion Firmware { get; set; }
        public TimeSpan Uptime { get; set; }
        public DateTime DateTime { get; set; }
        public ProductVersion Kernel { get; set; }
        public ProductVersion Distribution { get; set; }
    }
}

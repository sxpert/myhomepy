using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.NetworkInformation;
using OpenWebNet.Messages;
using System.Net.Sockets;

namespace OpenWebNet
{
    [Obsolete]
    public enum GatewayType
    {
        Ethernet,
        Usb
    }

    public class Gateway
    {
        public string Ip { get; set; }
        public string Port { get; set; }

        public GatewayModel Model { get; set; }

        [Obsolete]
        public GatewayType Type { get; set; }
    }
}


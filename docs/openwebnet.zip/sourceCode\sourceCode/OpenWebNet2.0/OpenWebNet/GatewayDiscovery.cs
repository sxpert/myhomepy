using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Net.NetworkInformation;

namespace OpenWebNet
{
    public class GatewayDiscovery
    {
        public Gateway Discovery()
        {
            IPInterfaceProperties ifaceProp;
            List<string> addresses;

            if (!NetworkInterface.GetIsNetworkAvailable())
                return null;

            NetworkInterface[] interfaces = NetworkInterface.GetAllNetworkInterfaces();
            NetworkInterface iface = null;

            for (int i = 0; i < interfaces.Length; i++)
            {
                if (interfaces[i].OperationalStatus == OperationalStatus.Up)
                {
                    iface = interfaces[i];
                    break;
                }
            }

            if (iface == null)
                return null;

            ifaceProp = iface.GetIPProperties();
            addresses = GetIPAddresses(ifaceProp.UnicastAddresses[0].Address.ToString());

            foreach (string ip in addresses)
            {
                try
                {
                    TestConnectivity(ip);
                }
                catch (Exception ex)
                {
                    continue;
                }
            }

            return null;
        }

        private List<string> GetIPAddresses(string ip)
        {
            // 35,1,254,2,253,3,252
            string addr;
            List<string> addrs = new List<string>(253);
            int lastDot = ip.LastIndexOf('.');
            string formatIp = ip.Substring(0, lastDot) + "{0}";

            addrs.Add(string.Format(formatIp, "1"));
            addrs.Add(string.Format(formatIp, "2"));
            addrs.Add(string.Format(formatIp, "3"));
            addrs.Add(string.Format(formatIp, "35"));
            addrs.Add(string.Format(formatIp, "252"));
            addrs.Add(string.Format(formatIp, "253"));
            addrs.Add(string.Format(formatIp, "254"));

            for (int i = 0; i < 254; i++)
            {
                addr = string.Format(formatIp, i);

                if (addrs.Contains(addr))
                    continue;

                addrs.Add(addr);
            }

            return addrs;
        }

        private void TestConnectivity(string ip)
        {
            EthGateway gw = new EthGateway(ip, 20000, OpenSocketType.Command);
            gw.Connected += new EventHandler(gw_Connected);
            //gw.MessageReceived += new EventHandler<OpenWebNetDataEventArgs>(gw_MessageReceived);
            gw.MessageReceived += new EventHandler<OpenWebNetMessageEventArgs>(gw_MessageReceived);
        }

        private void gw_MessageReceived(object sender, OpenWebNetMessageEventArgs e)
        {
            throw new NotImplementedException();
        }

        private void gw_Connected(object sender, EventArgs e)
        {
            //EthGateway e = sender as EthGateway;
            //e.SendData("*#13**15##");
        }
    }

    public enum GatewayType
    {
        Ethernet,
        Usb
    }

    public class Gateway
    {
        public string Ip { get; set; }
        public string Port { get; set; }
        public GatewayType Type { get; set; }
    }
}


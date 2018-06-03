using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Timers;

namespace OpenWebNet
{
    public enum CheckGatewayConnectionResult
    {
        Successful,
        Failed
    }

    public class CheckGatewayConnection
    {
        public event EventHandler<CheckGatewayConnectionEventArgs> CheckGatewayConnectionCompleted;

        private Gateway gw;
        private OpenWebNetGateway openGW;
        private Timer timer;

        public CheckGatewayConnection(Gateway gw)
            : this(gw, 2000)
        {
        }

        public CheckGatewayConnection(Gateway gw, double interval)
        {
            if (gw == null)
                throw new ArgumentNullException("gw");

            if (interval < 0)
                throw new ArgumentOutOfRangeException("interval");

            this.gw = gw;
            this.timer = new Timer(interval);
            this.timer.Elapsed += new ElapsedEventHandler(timer_Elapsed);
        }

        public void Check()
        {
            try
            {
                if (openGW == null)
                {
                    if (gw.Type == GatewayType.Ethernet)
                    {
                        openGW = new EthGateway(gw.Ip, int.Parse(gw.Port), OpenSocketType.Command);
                    }
                    else if (gw.Type == GatewayType.Usb)
                    {
                        openGW = new UsbGateway(gw.Port);
                    }

                    openGW.Connected += new EventHandler(openGW_Connected);
                    openGW.DataReceived += new EventHandler<OpenWebNetDataEventArgs>(openGW_DataReceived);
                }
                else
                {
                    if (openGW.IsConnected)
                        openGW.Disconnect();
                }

                openGW.Connect();
            }
            catch (Exception ex)
            {
                if (CheckGatewayConnectionCompleted != null)
                    CheckGatewayConnectionCompleted(this, new CheckGatewayConnectionEventArgs() { Gateway = gw, Result = CheckGatewayConnectionResult.Failed });
            }
        }

        private void openGW_DataReceived(object sender, OpenWebNetDataEventArgs e)
        {
            try
            {
                if (e.Data == null || !e.Data.Contains("*#13**15*"))
                    return;

                if (CheckGatewayConnectionCompleted != null)
                    CheckGatewayConnectionCompleted(this, new CheckGatewayConnectionEventArgs() { Gateway = gw, Result = CheckGatewayConnectionResult.Successful });
            }
            catch (Exception)
            {
                if (CheckGatewayConnectionCompleted != null)
                    CheckGatewayConnectionCompleted(this, new CheckGatewayConnectionEventArgs() { Gateway = gw, Result = CheckGatewayConnectionResult.Failed });
            }
        }

        private void openGW_Connected(object sender, EventArgs e)
        {
            try
            {
                openGW.SendData("*#13**15##");
            }
            catch (Exception)
            {
                if (CheckGatewayConnectionCompleted != null)
                    CheckGatewayConnectionCompleted(this, new CheckGatewayConnectionEventArgs() { Gateway = gw, Result = CheckGatewayConnectionResult.Failed });
            }
        }

        private void timer_Elapsed(object sender, ElapsedEventArgs e)
        {
            //DisposeUsbGateway();
            //DisposeEthGateway();

            if (CheckGatewayConnectionCompleted != null)
                CheckGatewayConnectionCompleted(this, new CheckGatewayConnectionEventArgs() { Gateway = gw, Result = CheckGatewayConnectionResult.Failed });
        }

        /*private void DisposeEthGateway()
        {
            if (ethGW == null)
                return;

            if (ethGW.IsConnected)
                ethGW.Disconnect();

            ethGW.Connected -= ethGW_Connected;
            ethGW.MessageReceived -= ethGW_MessageReceived;
            ethGW = null;
        }

        private void DisposeUsbGateway()
        {
            if (usbGW == null)
                return;

            usbGW.DataReceived -= usbGW_DataReceived;
            usbGW = null;
        }*/
    }

    public class CheckGatewayConnectionEventArgs : EventArgs
    {
        public Gateway Gateway { get; set; }
        public CheckGatewayConnectionResult Result { get; set; }

        public CheckGatewayConnectionEventArgs() : base() { }

        public CheckGatewayConnectionEventArgs(Gateway gw, CheckGatewayConnectionResult result)
            : this()
        {
            this.Gateway = gw;
            this.Result = result;
        }
    }
}

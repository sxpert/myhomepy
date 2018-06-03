namespace OpenWebNet
{
    #region Using

    using System;
    using OpenWebNet.Messages;

    #endregion

    /*
     * Il virtual configurator per fare lo scanning invia:
     * 1)	*#1001*00*1## in maniera tale da ottenere le risposte di tutte le periferiche presenti nell’ambiente 0 (da controllare) (*1*0*12##, *1*0*13##)
     * 2)	*#1001*1*1## richiede i modelli dei device nell’ambiente 0 e continua cosi fino al 9
     * 3)	*#1001*11*0## per ogni periferica trovata viene fatta questa richiesta
     */

    public class DeviceDiscovery : IDisposable
    {
        private const string SCAN_DEVICES = "*#1001*{0}*1##";

        public event EventHandler<DeviceFoundEventArgs> DeviceFound;

        private OpenWebNetGateway gw;

        public DeviceDiscovery(OpenWebNetGateway gw)
        {
            if (gw == null)
                throw new ArgumentNullException("gw");

            this.gw = gw;
            this.gw.MessageReceived += new EventHandler<OpenWebNetMessageEventArgs>(gw_MessageReceived);
        }

        public void Scan()
        {
            for (int i = 0; i < 9; i++)
            {
                gw.SendData(string.Format(SCAN_DEVICES, i));
            }
        }

        public void Dispose()
        {
            gw.MessageReceived -= gw_MessageReceived;
            gw = null;
        }

        protected virtual void OnDeviceFound(Device device)
        {
            EventHandler<DeviceFoundEventArgs> handler = DeviceFound;

            if (handler != null)
                handler(this, new DeviceFoundEventArgs(device));
        }

        private void gw_MessageReceived(object sender, OpenWebNetMessageEventArgs e)
        {
            if (e.Message.MessageType != MessageType.Command)
                return;

            OnDeviceFound(new Device() { Where = e.Message.Where });
        }
    }

    public class DeviceFoundEventArgs : EventArgs
    {
        public Device Device { get; internal set; }

        public DeviceFoundEventArgs(Device device)
        {
            if (device == null)
                throw new ArgumentNullException("device");

            this.Device = device;
        }
    }
}

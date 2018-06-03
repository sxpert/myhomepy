namespace OpenWebNet
{
    #region Using

    using System;
    using OpenSource.UPnP;

    #endregion

    /// <summary>
    /// Used to discover gateways (TS, F453AV, MH200, ...) that support UPnP protocol
    /// </summary>
    public class UPnPGatewayDiscovery : IDisposable
    {
        public event EventHandler<GatewayFoundEventArgs> DeviceFound;

        private UPnPSmartControlPoint upnp;

        public UPnPGatewayDiscovery()
        {
            upnp = new UPnPSmartControlPoint();
            upnp.OnAddedDevice += new UPnPSmartControlPoint.DeviceHandler(upnp_OnAddedDevice);
        }

        public void StartDiscovery()
        {
            upnp.Rescan();
        }

        private void upnp_OnAddedDevice(UPnPSmartControlPoint sender, UPnPDevice device)
        {
            // create Gateway from UPnPDevice
        }

        protected virtual void OnGatewayFound(GatewayFoundEventArgs e)
        {
            EventHandler<GatewayFoundEventArgs> handler = DeviceFound;

            if (handler != null)
                handler(this, e);
        }

        #region IDisposable Members

        public void Dispose()
        {
            upnp.OnAddedDevice -= new UPnPSmartControlPoint.DeviceHandler(upnp_OnAddedDevice);
            upnp = null;
        }

        #endregion
    }

    public class GatewayFoundEventArgs : EventArgs
    {
        public GatewayFoundEventArgs(Gateway gateway)
            : base()
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.Gateway = gateway;
        }

        public Gateway Gateway { get; internal set; }
    }
}

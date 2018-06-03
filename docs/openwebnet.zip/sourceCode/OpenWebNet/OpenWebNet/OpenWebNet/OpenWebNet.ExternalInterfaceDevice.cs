using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
	{
        public void GetTime()
        {
            SendCommand(WHO.OutsideInterface, "0", string.Empty);
        }

        public void GetDate()
        {
            SendCommand(WHO.OutsideInterface, "1", string.Empty);
        }

        public void GetIp()
        {
            SendCommand(WHO.OutsideInterface, "10", string.Empty);
        }

        public void GetNetmask()
        {
            SendCommand(WHO.OutsideInterface, "11", string.Empty);
        }

        public void GetMacAddress()
        {
            SendCommand(WHO.OutsideInterface, "12", string.Empty);
        }

        public void GetModelType()
        {
            SendCommand(WHO.OutsideInterface, "15", string.Empty);
        }

        public void GetFirmwareVersion()
        {
            SendCommand(WHO.OutsideInterface, "16", string.Empty);
        }

        public void GetUptime()
        {
            SendCommand(WHO.OutsideInterface, "19", string.Empty);
        }

        public void GetDateAndTime()
        {
            SendCommand(WHO.OutsideInterface, "22", string.Empty);
        }

        public void GetKernelVersion()
        {
            SendCommand(WHO.OutsideInterface, "23", string.Empty);
        }

        public void GetDistributionVersion()
        {
            SendCommand(WHO.OutsideInterface, "24", string.Empty);
        }
	}
}

using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;
using System.Net;

namespace OpenWebNet
{
    public class ExternalInterfaceDevice
    {
        private OpenWebNetGateway gw;

        public ExternalInterfaceDevice(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        public void GetTime()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "0");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "0");
        }

        public void GetDate()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "1");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "1");
        }

        public void GetIp()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "10");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "10");
        }

        public void GetNetmask()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "11");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "11");
        }

        public void GetMacAddress()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "12");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "12");
        }

        public void GetGatewayModel()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "15");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "15");
        }

        public void GetFirmwareVersion()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "16");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "16");
        }

        public void GetUptime()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "19");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "19");
        }

        public void GetDateAndTime()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "27");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "27");
        }

        public void GetKernelVersion()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "23");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "23");
        }

        public void GetDistributionVersion()
        {
            gw.SendExternalDeviceCommand(WHO.OutsideInterface, "24");
            //gw.GetDimensionCommand(WHO.OutsideInterface, string.Empty, "24");
            //gw.SendCommand(WHO.OutsideInterface, "24", string.Empty);
        }

        public static WHAT GetWhat(string what)
        {
            int value;
            WHAT retWhat = WHAT.None;

            if (int.TryParse(what, out value))
            {
                switch (value)
                {
                    case 0:
                        retWhat = WHAT.TimeRequest;
                        break;
                    case 1:
                        retWhat = WHAT.DateRequest;
                        break;
                    case 10:
                        retWhat = WHAT.IpRequest;
                        break;
                    case 11:
                        retWhat = WHAT.NetmaskRequest;
                        break;
                    case 12:
                        retWhat = WHAT.MacAddressRequest;
                        break;
                    case 15:
                        retWhat = WHAT.ModelTypeRequest;
                        break;
                    case 16:
                        retWhat = WHAT.FirmwareVersionRequest;
                        break;
                    case 19:
                        retWhat = WHAT.UptimeRequest;
                        break;
                    case 22:
                        retWhat = WHAT.DateAndTimeRequest;
                        break;
                    case 23:
                        retWhat = WHAT.KernelVersionRequest;
                        break;
                    case 24:
                        retWhat = WHAT.DistributionVersionRequest;
                        break;
                }
            }

            return retWhat;
        }

        public static DeviceMessage GetMessage(string data)
        {
            // A kind of device command *#13**0*H*M*S*T##

            DeviceMessage message = null;
            string[] content;

            if (string.IsNullOrEmpty(data))
                return null;

            try
            {

                data = data.Remove(0, 2);
                content = data.Remove(data.Length - 2, 2).Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                message = new DeviceMessage();
                message.What = GetWhat(content[1]);

                switch (message.What)
                {
                    case WHAT.TimeRequest:
                        message.Time = new TimeSpan(int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]));
                        break;
                    case WHAT.DateRequest:
                        message.Date = new DateTime(int.Parse(content[5]), int.Parse(content[4]), int.Parse(content[3]));
                        break;
                    case WHAT.IpRequest:
                        message.IP = IPAddress.Parse(string.Format("{0}.{1}.{2}.{3}", content[2], content[3],
                            content[4], content[5]));
                        break;
                    case WHAT.NetmaskRequest:
                        message.Netmask = IPAddress.Parse(string.Format("{0}.{1}.{2}.{3}", content[2], content[3],
                            content[4], content[5]));
                        break;
                    case WHAT.MacAddressRequest:
                        message.MACAddress = string.Format("{0}:{1}:{2}:{3}:{4}:{5}", content[2], content[3], content[4],
                            content[5], content[6], content[7]);
                        break;
                    case WHAT.ModelTypeRequest:
                        message.Model = Utilities.GetGatewayModel(content[2]);
                        break;
                    case WHAT.FirmwareVersionRequest:
                        message.Firmware = new ProductVersion(int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]));
                        break;
                    case WHAT.UptimeRequest:
                        message.Uptime = new TimeSpan(int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]),
                            int.Parse(content[5]));
                        break;
                    case WHAT.DateAndTimeRequest:
                        message.DateTime = new DateTime(int.Parse(content[9]), int.Parse(content[8]), int.Parse(content[7]),
                            int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]));
                        break;
                    case WHAT.KernelVersionRequest:
                        message.Kernel = new ProductVersion(int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]));
                        break;
                    case WHAT.DistributionVersionRequest:
                        message.Distribution = new ProductVersion(int.Parse(content[2]), int.Parse(content[3]), int.Parse(content[4]));
                        break;
                }
            }
            catch (Exception ex)
            {
                return null;
            }

            return message;
        }
    }
}

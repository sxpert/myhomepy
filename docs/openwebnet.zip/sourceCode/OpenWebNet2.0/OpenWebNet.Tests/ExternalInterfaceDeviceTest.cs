using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;
using System.Net;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class ExternalInterfaceDeviceTest
    {
        [TestMethod]
        public void GetMessageTimeRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**0*1*2*3*4##");
            Assert.AreEqual<int>(message.Time.Hours, 1);
            Assert.AreEqual<int>(message.Time.Minutes, 2);
            Assert.AreEqual<int>(message.Time.Seconds, 3);
            Assert.AreEqual<WHAT>(message.What, WHAT.TimeRequest);
        }

        [TestMethod]
        public void GetMessageDateRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**1*1*2*3*2001##");
            Assert.AreEqual<int>(message.Date.Day, 2);
            Assert.AreEqual<int>(message.Date.Month, 3);
            Assert.AreEqual<int>(message.Date.Year, 2001);
            Assert.AreEqual<WHAT>(message.What, WHAT.DateRequest);
        }

        [TestMethod]
        public void GetMessageIPRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**10*192*168*1*254##");
            Assert.AreEqual<WHAT>(message.What, WHAT.IpRequest);
            Assert.AreEqual<IPAddress>(message.IP, IPAddress.Parse("192.168.1.254"));
        }

        [TestMethod]
        public void GetMessageNetmaskRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**11*255*255*255*0##");
            Assert.AreEqual<WHAT>(message.What, WHAT.NetmaskRequest);
            Assert.AreEqual<IPAddress>(message.Netmask, IPAddress.Parse("255.255.255.0"));
        }

        [TestMethod]
        public void GetMessageMACAddressRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**12*01*02*03*04*05*06##");
            Assert.AreEqual<WHAT>(message.What, WHAT.MacAddressRequest);
            Assert.AreEqual<string>(message.MACAddress, "01:02:03:04:05:06");
        }

        [TestMethod]
        public void GetMessageGatewayModelRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**15*2##");
            Assert.AreEqual<WHAT>(message.What, WHAT.ModelTypeRequest);
            Assert.AreEqual<GatewayModel>(message.Model, GatewayModel.MHServer);
        }

        [TestMethod]
        public void GetMessageFirmwareRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**16*1*2*3##");
            Assert.AreEqual<WHAT>(message.What, WHAT.FirmwareVersionRequest);
            Assert.AreEqual<int>(message.Firmware.Version, 1);
            Assert.AreEqual<int>(message.Firmware.Release, 2);
            Assert.AreEqual<int>(message.Firmware.Build, 3);
        }

        [TestMethod]
        public void GetMessageUptimeRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**19*1*2*3*4##");
            Assert.AreEqual<WHAT>(message.What, WHAT.UptimeRequest);
            Assert.AreEqual<int>(message.Uptime.Days, 1);
            Assert.AreEqual<int>(message.Uptime.Hours, 2);
            Assert.AreEqual<int>(message.Uptime.Minutes, 3);
            Assert.AreEqual<int>(message.Uptime.Seconds, 4);
        }

        [TestMethod]
        public void GetMessageDateAndTimeRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**22*1*2*3*15*16*4*5*6##");
            Assert.AreEqual<WHAT>(message.What, WHAT.DateAndTimeRequest);
            Assert.AreEqual<int>(message.DateTime.Hour, 1);
            Assert.AreEqual<int>(message.DateTime.Minute, 2);
            Assert.AreEqual<int>(message.DateTime.Second, 3);
            Assert.AreEqual<int>(message.DateTime.Day, 4);
            Assert.AreEqual<int>(message.DateTime.Month, 5);
            Assert.AreEqual<int>(message.DateTime.Year, 6);
        }

        [TestMethod]
        public void GetMessageKernelRequestTestShouldPass()
        {
            DeviceMessage message = ExternalInterfaceDevice.GetMessage("*#13**23*1*2*3##");
            Assert.AreEqual<WHAT>(message.What, WHAT.KernelVersionRequest);
            Assert.AreEqual<int>(message.Kernel.Version, 1);
            Assert.AreEqual<int>(message.Kernel.Release, 2);
            Assert.AreEqual<int>(message.Kernel.Build, 3);
        }
    }
}

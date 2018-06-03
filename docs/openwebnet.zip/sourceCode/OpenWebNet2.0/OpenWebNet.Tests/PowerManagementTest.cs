using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class PowerManagementTest
    {
        [TestMethod]
        public void GetMessageLoadForcedTest()
        {
            PowerManagementMessage message = PowerManagement.GetMessage("*3*2*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.PowerManagementLoadForced);
        }

        [TestMethod]
        public void GetMessageAllDimensionsTest()
        {
            PowerManagementMessage message = PowerManagement.GetMessage("*#3*10*0*1*2*3*4##");
            Assert.AreEqual<WHAT>(message.What, WHAT.PowerManagementAllDimensionsRequest);
            Assert.AreEqual<int>(message.Voltage, 1);
            Assert.AreEqual<int>(message.Current, 2);
            Assert.AreEqual<int>(message.Power, 3);
            Assert.AreEqual<int>(message.Energy, 4);
        }

        [TestMethod]
        public void GetMessageVoltageRequestTest()
        {
            PowerManagementMessage message = PowerManagement.GetMessage("*#3*10*1*1##");
            Assert.AreEqual<WHAT>(message.What, WHAT.PowerManagementVoltageRequest);
            Assert.AreEqual<int>(message.Voltage, 1);
        }
    }
}

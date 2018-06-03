using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class AlarmTest
    {
        [TestMethod]
        public void GetMessageZoneEngagedShouldPass()
        {
            AlarmMessage message = Alarm.GetMessage("*5*11*#10##");
            Assert.AreEqual<WHAT>(WHAT.AlarmActiveZone, message.What);
            Assert.AreEqual<int>(message.Zone, 10);
        }

        [TestMethod]
        public void GetMessageBatteryKOShouldPass()
        {
            AlarmMessage message = Alarm.GetMessage("*5*10**##");
            Assert.AreEqual<WHAT>(WHAT.AlarmBatteryUnloads, message.What);
        }
    }
}

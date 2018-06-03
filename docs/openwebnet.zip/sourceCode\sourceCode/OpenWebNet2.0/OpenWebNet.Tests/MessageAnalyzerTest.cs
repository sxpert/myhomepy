using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class MessageAnalyzerTest
    {
        [TestMethod]
        public void GetMessageLightONShouldPass()
        {
            BaseMessage message = MessageAnalyzer.GetMessage("*1*1*11##");
            Assert.AreEqual<WHAT>(WHAT.LightON, message.What);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
            Assert.AreEqual<WHO>(message.Who, WHO.Lighting);
        }

        [TestMethod]
        public void GetMessageDateAndTimeRequestTestShouldPass()
        {
            DeviceMessage message = MessageAnalyzer.GetMessage("*#13**22*1*2*3*15*16*4*5*6##") as DeviceMessage;
            Assert.AreEqual<WHAT>(message.What, WHAT.DateAndTimeRequest);
            Assert.AreEqual<WHO>(message.Who, WHO.OutsideInterface);
            Assert.AreEqual<int>(message.DateTime.Hour, 1);
            Assert.AreEqual<int>(message.DateTime.Minute, 2);
            Assert.AreEqual<int>(message.DateTime.Second, 3);
            Assert.AreEqual<int>(message.DateTime.Day, 4);
            Assert.AreEqual<int>(message.DateTime.Month, 5);
            Assert.AreEqual<int>(message.DateTime.Year, 6);
        }
    }
}

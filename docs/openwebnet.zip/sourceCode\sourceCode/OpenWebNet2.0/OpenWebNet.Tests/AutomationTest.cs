using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class AutomationTest
    {
        [TestMethod]
        public void GetMessageUpTestShouldPass()
        {
            AutomationMessage message = Automation.GetMessage("*2*1*31##");
            Assert.AreEqual<WHAT>(message.What, WHAT.AutomationUp);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageDownTestShouldPass()
        {
            AutomationMessage message = Automation.GetMessage("*2*2*31##");
            Assert.AreEqual<WHAT>(message.What, WHAT.AutomationDown);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageStopTestShouldPass()
        {
            AutomationMessage message = Automation.GetMessage("*2*0*31##");
            Assert.AreEqual<WHAT>(message.What, WHAT.AutomationStop);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }
    }
}

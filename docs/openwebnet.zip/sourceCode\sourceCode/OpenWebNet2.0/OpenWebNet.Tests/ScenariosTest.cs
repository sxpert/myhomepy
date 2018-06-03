using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class ScenariosTest
    {
        [TestMethod]
        public void GetMessageEndProgrammingTestShouldPass()
        {
            ScenarioMessage message = Scenarios.GetMessage("*0*41#11*31##");

            Assert.AreEqual<int>(message.ScenarioNumber, 11);
            Assert.AreEqual<WHAT>(message.What, WHAT.ScenariosEndProgramming);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageActivateTestShouldPass()
        {
            ScenarioMessage message = Scenarios.GetMessage("*0*11*31##");

            Assert.AreEqual<int>(message.ScenarioNumber, 11);
            Assert.AreEqual<WHAT>(message.What, WHAT.ScenariosON);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageDeactivateTestShouldPass()
        {
            ScenarioMessage message = Scenarios.GetMessage("*0*11#0*31##");

            Assert.AreEqual<int>(message.ScenarioNumber, 11);
            Assert.AreEqual<WHAT>(message.What, WHAT.ScenariosOFF);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageEraseAllTestShouldPass()
        {
            ScenarioMessage message = Scenarios.GetMessage("*0*42*31##");

            Assert.AreEqual<WHAT>(message.What, WHAT.ScenariosEraseAll);
            Assert.AreEqual<int>(message.Where.A, 3);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }
    }
}

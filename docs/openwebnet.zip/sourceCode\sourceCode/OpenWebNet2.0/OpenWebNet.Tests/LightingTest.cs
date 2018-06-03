using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class LightingTest
    {
        [TestMethod]
        public void GetMessageLightOFFTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*0*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightOFF);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageLightOFFAtSpeedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*0#100*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightOffAtSpeed);
            Assert.AreEqual<int>(message.Speed, 100);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageLightONAtSpeedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*1#100*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightOnAtSpeed);
            Assert.AreEqual<int>(message.Speed, 100);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageDimmerStrenghtTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*3*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.DimmerStrenght);
            Assert.AreEqual<int>(message.DimmerStrenght, 30);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageDimmerUpOfYAtXSpeedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*30#100#200*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.DimmerUpAtSpeed);
            Assert.AreEqual<int>(message.Level, 100);
            Assert.AreEqual<int>(message.Speed, 200);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageDimmerDownOfYAtXSpeedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*31#100#200*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.DimmerDownAtSpeed);
            Assert.AreEqual<int>(message.Level, 100);
            Assert.AreEqual<int>(message.Speed, 200);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageTemporizationTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*#1*11*1*1*2*3##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightTemporization);
            Assert.AreEqual<int>(message.Temporization.Hours, 1);
            Assert.AreEqual<int>(message.Temporization.Minutes, 2);
            Assert.AreEqual<int>(message.Temporization.Seconds, 3);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageLuminousIntensityChangeTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*#1*11*2*200*100##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightLuminousIntensityChange);
            Assert.AreEqual<int>(message.Level, 200);
            Assert.AreEqual<int>(message.Speed, 100);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }
    }
}

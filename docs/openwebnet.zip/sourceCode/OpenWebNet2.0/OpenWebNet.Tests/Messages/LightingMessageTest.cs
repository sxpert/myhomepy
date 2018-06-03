using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;
using OpenWebNet.Common;

namespace OpenWebNet.Tests.Messages
{
    [TestClass]
    public class LightingMessageTest
    {
        private const String LIGHT_11_OFF = "*1*0*11##";
        private const String LIGHT_11_OFF_AT_SPEED_100 = "*1*0#100*11##";
        private const String LIGHT_11_ON_AT_SPEED_100 = "*1*1#100*11##";
		private const String LIGHT_11_GETSTATUS = "*#1*11##";
		private const String LIGHT_11_DIMMER_STRENGHT = "*1*3*11##";

        [TestMethod]
        public void Set_LightingMessage_Properties()
        {
            var message = new LightingMessage();
            message.Message = LIGHT_11_OFF;
            message.What = LightingWhat.LightOFF;
            message.Where = Where.GetWhere("11");

            Assert.AreEqual(message.MessageType, MessageType.Command);
            Assert.AreEqual(message.Who, WHO.Lighting);
            Assert.AreEqual(message.What, LightingWhat.LightOFF);
            Assert.AreEqual(message.Message,  LIGHT_11_OFF);
            Assert.AreEqual(message.Where.A, 1);
            Assert.AreEqual(message.Where.PL, 1);
        }

        [TestMethod]
        public void Invoke_LightingMessage_ToString_With_Light_11_OFF()
        {
            var message = new LightingMessage();
            message.Message = LIGHT_11_OFF;
            message.What = LightingWhat.LightOFF;
            message.Where = Where.GetWhere("11");

            Assert.AreEqual(message.ToString(), LIGHT_11_OFF);
        }

        [TestMethod]
        public void Invoke_LightingMessage_ToString_With_Light_11_OFF_At_Speed_100()
        {
            var message = new LightingMessage();
            message.Message = LIGHT_11_OFF_AT_SPEED_100;
            message.What = LightingWhat.LightOffAtSpeed;
			message.Speed = 100;
            message.Where = Where.GetWhere("11");

            Assert.AreEqual(message.ToString(), LIGHT_11_OFF_AT_SPEED_100);
        }

        [TestMethod]
        public void Invoke_LightingMessage_ToString_With_Light_11_ON_At_Speed_100()
        {
            var message = new LightingMessage();
            message.Message = LIGHT_11_ON_AT_SPEED_100;
            message.What = LightingWhat.LightOnAtSpeed;
			message.Speed = 100;
            message.Where = Where.GetWhere("11");

            Assert.AreEqual(message.ToString(), LIGHT_11_ON_AT_SPEED_100);
        }

		[TestMethod]
		public void Invoke_LightingMessage_ToString_With_GetStatus_11()
		{
			var message = new LightingMessage();
			message.Message = LIGHT_11_GETSTATUS;
			message.What = LightingWhat.GetStatus;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.ToString(), LIGHT_11_GETSTATUS);
		}

        [TestMethod]
        public void Invoke_LightMessage_ToString_With_Dimmer_Strenght_30()
        {
			var message = new LightingMessage();
			message.What = LightingWhat.DimmerStrenght;
			message.DimmerStrenght = 30;
			message.Where = Where.GetWhere("11");
			message.Message = LIGHT_11_DIMMER_STRENGHT;

			Assert.AreEqual(message.ToString(), LIGHT_11_DIMMER_STRENGHT);
        }

        /*[TestMethod]
        public void GetMessageLuminousIntensityChangeTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*#1*11*2*200*100##");
            Assert.AreEqual<WHAT>(message.What, WHAT.LightLuminousIntensityChange);
            Assert.AreEqual<int>(message.Level, 200);
            Assert.AreEqual<int>(message.Speed, 100);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
        }

        [TestMethod]
        public void GetMessageBrightnessChangedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*#1*11*6*1234##");
            Assert.AreEqual<WHAT>(message.What, WHAT.BrightnessChanged);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Where.PL, 1);
            Assert.AreEqual<int>(message.Brightness, 1234);
        }

        [TestMethod]
        public void GetMessageBrightnessChangedWithA1TestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*#1*1*6*1234##");
            Assert.AreEqual<WHAT>(message.What, WHAT.BrightnessChanged);
            Assert.AreEqual<int>(message.Where.A, 1);
            Assert.AreEqual<int>(message.Brightness, 1234);
        }

        [TestMethod]
        public void GetMessageMotionPresenceDetectedTestShouldPass()
        {
            LightingMessage message = Lighting.GetMessage("*1*34*11##");
            Assert.AreEqual<WHAT>(message.What, WHAT.MotionPresenceDetected);
            Assert.AreEqual<int>(message.Where.PL, 1);
            Assert.AreEqual<int>(message.Where.A, 1);
        }*/
    }
}

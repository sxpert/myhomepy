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
    public class AutomationMessageTest
    {

		private const String AUTOMATION_11_UP = "*2*1*11##";
		private const String AUTOMATION_11_DOWN = "*2*2*11##";
		private const String AUTOMATION_11_STOP = "*2*0*11##";
		private const String AUTOMATION_11_GET_STATUS = "*#2*11##";

		[TestMethod]
		public void Set_AutomatioMessage_Properties()
		{
			var message = new AutomationMessage();
			message.Message = AUTOMATION_11_UP;
			message.What = AutomationWhat.AutomationUp;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.MessageType, MessageType.Command);
			Assert.AreEqual(message.Who, WHO.Automation);
			Assert.AreEqual(message.What, AutomationWhat.AutomationUp);
			Assert.AreEqual(message.Message, AUTOMATION_11_UP);
			Assert.AreEqual(message.Where.A, 1);
			Assert.AreEqual(message.Where.PL, 1);
		}

		[TestMethod]
		public void Invoke_AutomationMessage_ToString_With_Automation_11_Up()
		{
			var message = new AutomationMessage();
			message.Message = AUTOMATION_11_UP;
			message.What = AutomationWhat.AutomationUp;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.ToString(), AUTOMATION_11_UP);
		}

		[TestMethod]
		public void Invoke_AutomationMessage_ToString_With_Automation_11_Down()
		{
			var message = new AutomationMessage();
			message.Message = AUTOMATION_11_DOWN;
			message.What = AutomationWhat.AutomationDown;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.ToString(), AUTOMATION_11_DOWN);
		}

		[TestMethod]
		public void Invoke_AutomationMessage_ToString_With_Automation_11_Stop()
		{
			var message = new AutomationMessage();
			message.Message = AUTOMATION_11_STOP;
			message.What = AutomationWhat.AutomationStop;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.ToString(), AUTOMATION_11_STOP);
		}

		[TestMethod]
		public void Invoke_AutomationMessage_ToString_With_Get_Status_11()
		{
			var message = new AutomationMessage();
			message.Message = AUTOMATION_11_GET_STATUS;
			message.What = AutomationWhat.GetStatus;
			message.Where = Where.GetWhere("11");

			Assert.AreEqual(message.ToString(), AUTOMATION_11_GET_STATUS);
		}
    }
}

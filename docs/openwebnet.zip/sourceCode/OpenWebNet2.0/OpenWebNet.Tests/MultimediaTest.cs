using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Messages;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class MultimediaTest
    {
        [TestMethod]
        public void GetMessageReceivedVideoShouldPass()
        {
            MultimediaMessage message = Multimedia.GetMessage("*7*0*4001*##");
            Assert.AreEqual<WHAT>(WHAT.MultimediaCameraON, message.What);
            Assert.AreEqual<int>(4001, message.Where.PL);
        }

        [TestMethod]
        public void GetMessageVideoOFFShouldPass()
        {
            MultimediaMessage message = Multimedia.GetMessage("*7*8**##");
            Assert.AreEqual<WHAT>(WHAT.MultimediaCameraOFF, message.What);
        }

        [TestMethod]
        public void GetMessageFreeAudioAndVideoResourceShouldPass()
        {
            MultimediaMessage message = Multimedia.GetMessage("*7*9**##");
            Assert.AreEqual<WHAT>(WHAT.MultimediaAudioVideoOFF, message.What);
        }

        [TestMethod]
        public void GetMessageIncreaseXShouldPass()
        {
            MultimediaMessage message = Multimedia.GetMessage("*7*130##");
            Assert.AreEqual<WHAT>(WHAT.MultimediaIncreaseX, message.What);
        }

        [TestMethod]
        public void GetMessageDisplayDialXYShouldPass()
        {
            MultimediaMessage message = Multimedia.GetMessage("*7*311##");
            Assert.AreEqual<WHAT>(WHAT.MultimediaDisplayDialXY, message.What);
            Assert.AreEqual<int>(message.DisplayDialX, 1);
            Assert.AreEqual<int>(message.DisplayDialY, 1);
        }
    }
}

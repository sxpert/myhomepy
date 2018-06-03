using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace OpenWebNet.Tests
{
    /// <summary>
    /// Summary description for UnitTest1
    /// </summary>
    [TestClass]
    public class UtilitiesTest
    {
        public UtilitiesTest()
        {
            //
            // TODO: Add constructor logic here
            //
        }

        #region Additional test attributes
        //
        // You can use the following additional attributes as you write your tests:
        //
        // Use ClassInitialize to run code before running the first test in the class
        // [ClassInitialize()]
        // public static void MyClassInitialize(TestContext testContext) { }
        //
        // Use ClassCleanup to run code after all tests in a class have run
        // [ClassCleanup()]
        // public static void MyClassCleanup() { }
        //
        // Use TestInitialize to run code before running each test 
        // [TestInitialize()]
        // public void MyTestInitialize() { }
        //
        // Use TestCleanup to run code after each test has run
        // [TestCleanup()]
        // public void MyTestCleanup() { }
        //
        #endregion

        [TestMethod]
        public void CouldBeAPasswordSequenceTestShouldPass()
        {
            Assert.IsTrue(Utilities.CouldeBeAPasswordSequence("*#408377968##"));
        }

        [TestMethod]
        public void CouldBeAPasswordSequenceTestShoulFail()
        {
            Assert.IsFalse(Utilities.CouldeBeAPasswordSequence("*408377968##"));
        }

        [TestMethod]
        public void GetGatewayModelTestShouldPass()
        {
            Assert.AreEqual<GatewayModel>(GatewayModel.L4686SDK, Utilities.GetGatewayModel("27"));
        }

        [TestMethod]
        public void GetGatewayModelTestShouldFail()
        {
            Assert.AreNotEqual<GatewayModel>(GatewayModel.L4686SDK, Utilities.GetGatewayModel("28"));
        }
    }
}

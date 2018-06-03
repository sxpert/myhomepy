using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using OpenWebNet.Common;

namespace OpenWebNet.Tests
{
    [TestClass]
    public class WhereTest
    {
        [TestMethod]
        public void GetWhereTestWithoutInterfaceShouldPass()
        {
            Where where = Where.GetWhere("12");
            Assert.AreEqual<int>(where.A, 1);
            Assert.AreEqual<int>(where.PL, 2);
        }

        [TestMethod]
        public void GetWhereTestWithInterfaceShouldPass()
        {
            Where where = Where.GetWhere("12#4#11");
            Assert.AreEqual<int>(where.A, 1);
            Assert.AreEqual<int>(where.PL, 2);
            Assert.AreEqual<Bus>(where.Liv, Bus.LocalBus);
            Assert.AreEqual<int>(where.I, 11);
        }

        [TestMethod]
        public void GetWhereTestWithInterfaceAndGroupShouldPass()
        {
            Where where = Where.GetWhere("#1#4#11");
            Assert.AreEqual<int>(where.G, 1);
            Assert.AreEqual<Bus>(where.Liv, Bus.LocalBus);
            Assert.AreEqual<int>(where.I, 11);
        }

        [TestMethod]
        public void GetWhereTestWithGroupShouldPass()
        {
            Where where = Where.GetWhere("#2");
            Assert.AreEqual<int>(where.G, 2);
        }

        [TestMethod]
        public void GetWhereTestWithGeneralWhereShouldPass()
        {
            Where where = Where.GetWhere("0");
            Assert.IsTrue(where.IsGeneral);
        }
    }
}

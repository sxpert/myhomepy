using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenWebNet;

namespace MyHomeShortcut
{
    public class MessageCreator
    {
        private OpenWebNetGateway gateway;

        public MessageCreator(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gateway = gateway;
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenWebNet;
using System.Xml.Linq;

namespace MyHomeShortcut
{
    public class Action
    {
        public WHO Who { get; set; }
        public string Where { get; set; }
        public WHAT What { get; set; }
        public string Command { get; set; }
        public bool Toggle { get; set; }

        public Action()
        {
            this.Who = WHO.None;
            this.What = WHAT.None;
            this.Where = string.Empty;
            this.Command = string.Empty;
        }

        public override string ToString()
        {
            if (string.IsNullOrEmpty(Command))
            {
                return string.Format("{0} - {1} - {2}", Who, What, Where);
            }
            else
            {
                return Command;
            }
        }
    }
}

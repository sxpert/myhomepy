using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
    public class ScenarioMessage : BaseMessage
    {
        public ScenarioMessage()
            : base()
        {
            this.Who = WHO.Scenarios;
            this.MessageType = MessageType.Command;
        }

        public ScenarioMessage(int scenario) : this()
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario must be between 1 and 32");

            this.ScenarioNumber = scenario;
        }

        public int ScenarioNumber { get; set; }
    }
}

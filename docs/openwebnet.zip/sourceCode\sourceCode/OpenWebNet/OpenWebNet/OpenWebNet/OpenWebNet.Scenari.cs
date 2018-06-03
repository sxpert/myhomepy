using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNet
    {
        public void ScenarioON(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenari, scenario.ToString(), dove);
        }

        public void ScenarioOFF(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenari, string.Format("{0}#0", scenario), dove);
        }

        public void CancellaScenari(string dove)
        {
            SendCommand(WHO.Scenari, "42", dove);
        }

        public void CancellaScenario(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenari, string.Format("42#{0}", scenario), dove);
        }

        public void BloccaCentralinaScenari(string dove)
        {
            SendCommand(WHO.Scenari, "43", dove);
        }

        public void SbloccaCentralinaScenari(string dove)
        {
            SendCommand(WHO.Scenari, "44", dove);
        }
    }
}

using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        /// <summary>
        /// Alza il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da alzare</param>
        public void AutomationUp(string dove)
        {
            SendCommand(WHO.Automation, "1", dove);
        }

        /// <summary>
        /// Abbassa il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da abbassare</param>
        public void AutomationDown(string dove)
        {
            SendCommand(WHO.Automation, "2", dove);
        }

        /// <summary>
        /// Ferma il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da fermare</param>
        public void AutomationStop(string dove)
        {
            SendCommand(WHO.Automation, "0", dove);
        }

        /// <summary>
        /// Richiede lo stato del punto automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione</param>
        public void AutomationGetStatus(string dove)
        {
            GetStateCommand(WHO.Automation, dove);
        }
    }
}

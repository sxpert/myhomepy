using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        /// <summary>
        /// Attiva lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da attivare</param>
        public void ScenariosActivate(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenarios, scenario.ToString(), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Disattiva lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da disattivare</param>
        public void ScenariosDeactivate(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenarios, string.Format("0#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Attiva la programmazione dello scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da creare</param>
        public void ScenariosStartProgramming(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenarios, string.Format("40#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Termina la programmazione dello scenario
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario di cui terminare la creazione</param>
        public void ScenariosEndProgramming(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenarios, string.Format("41#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Cancella tutti gli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void ScenariosEraseAll(string dove)
        {
            SendCommand(WHO.Scenarios, "42", Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Cancella lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da cancellare</param>
        public void ScenariosErase(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            SendCommand(WHO.Scenarios, string.Format("42#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Blocca la centralina degli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void ScenariosLockCentralUnit(string dove)
        {
            SendCommand(WHO.Scenarios, "43", Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Sblocca la centralina degli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void ScenariosUnlockCentralUnit(string dove)
        {
            SendCommand(WHO.Scenarios, "44", Utilities.PadWhere(dove));
        }
    }
}

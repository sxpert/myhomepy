using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class Scenarios
    {
        private OpenWebNetGateway gw;

        public Scenarios(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        /// <summary>
        /// Attiva lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da attivare</param>
        public void Activate(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            gw.SendCommand(WHO.Scenarios, scenario.ToString(), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Disattiva lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da disattivare</param>
        public void Deactivate(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            gw.SendCommand(WHO.Scenarios, string.Format("0#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Attiva la programmazione dello scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da creare</param>
        public void StartProgramming(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            gw.SendCommand(WHO.Scenarios, string.Format("40#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Termina la programmazione dello scenario
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario di cui terminare la creazione</param>
        public void EndProgramming(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            gw.SendCommand(WHO.Scenarios, string.Format("41#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Cancella tutti gli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void EraseAll(string dove)
        {
            gw.SendCommand(WHO.Scenarios, "42", Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Cancella lo scenario specificato
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        /// <param name="scenario">Scenario da cancellare</param>
        public void Erase(string dove, int scenario)
        {
            if (scenario < 1 || scenario > 32)
                throw new ArgumentOutOfRangeException("Scenario deve essere compreso tra 1 e 32");

            gw.SendCommand(WHO.Scenarios, string.Format("42#{0}", scenario), Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Blocca la centralina degli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void LockCentralUnit(string dove)
        {
            gw.SendCommand(WHO.Scenarios, "43", Utilities.PadWhere(dove));
        }

        /// <summary>
        /// Sblocca la centralina degli scenari
        /// </summary>
        /// <param name="dove">Centralina degli scenari</param>
        public void ScenariosUnlockCentralUnit(string dove)
        {
            gw.SendCommand(WHO.Scenarios, "44", Utilities.PadWhere(dove));
        }

        public static WHAT GetWhat(string what)
        {
            WHAT retWhat;
            int value;

            retWhat = WHAT.None;

            if (int.TryParse(what, out value))
            {
                switch (value)
                {
                    case 40:
                        retWhat = WHAT.ScenariosStartProgramming;
                        break;
                    case 41:
                        retWhat = WHAT.ScenariosEndProgramming;
                        break;
                    case 42:
                        retWhat = WHAT.ScenariosEraseAll; // WHAT.ScenariosErase;
                        break;
                    case 43:
                        retWhat = WHAT.ScenariosLockCentralUnit;
                        break;
                    case 44:
                        retWhat = WHAT.ScenariosUnlockCentralUnit;
                        break;
                    case 45:
                        retWhat = WHAT.ScenariosCentralUnitUnavailable;
                        break;
                    case 46:
                        retWhat = WHAT.ScenariosCentralUnitMemoryFull;
                        break;
                }
            }

            return retWhat;
        }

        public static ScenarioMessage GetMessage(string data)
        {
            ScenarioMessage message = null;
            string[] content, parts;
            int value;

            if (string.IsNullOrEmpty(data))
                return null;

            try
            {
                content = data.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                if (int.TryParse(content[1], out value))
                {
                    if (value >= 1 && value <= 32)
                    {
                        // *0*scenario*where##

                        message = new ScenarioMessage(value);
                        message.What = WHAT.ScenariosON;
                    }
                    else
                    {
                        // *0*what*where##

                        message = new ScenarioMessage();
                        message.What = GetWhat(value.ToString());
                    }

                    message.Where = Where.GetWhere(content[2]);
                }
                else
                {
                    parts = content[1].Split(new char[] { '#' }, StringSplitOptions.RemoveEmptyEntries);

                    if (int.TryParse(parts[0], out value) && value >= 1 && value <= 32)
                    {
                        // *0*sceanario#0*where##
                        
                        message = new ScenarioMessage(value);
                        message.What = WHAT.ScenariosOFF;
                        message.Where = Where.GetWhere(content[2]);
                    }
                    else if (int.TryParse(parts[1], out value) && value >= 1 && value <= 32)
                    {
                        // *0*41#scenario*where##

                        message = new ScenarioMessage(value);
                        message.What = GetWhat(parts[0]);
                        message.Where = Where.GetWhere(content[2]);
                    }
                }
            }
            catch (Exception ex)
            {
                return null;
            }

            return message;
        }
    }
}

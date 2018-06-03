using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class Automation
    {
        private OpenWebNetGateway gw;

        public Automation(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        /// <summary>
        /// Alza il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da alzare</param>
        public void Up(string dove)
        {
            gw.SendCommand(WHO.Automation, "1", dove);
        }

        /// <summary>
        /// Abbassa il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da abbassare</param>
        public void Down(string dove)
        {
            gw.SendCommand(WHO.Automation, "2", dove);
        }

        /// <summary>
        /// Ferma il punto di Automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione da fermare</param>
        public void Stop(string dove)
        {
            gw.SendCommand(WHO.Automation, "0", dove);
        }

        /// <summary>
        /// Richiede lo stato del punto automazione
        /// </summary>
        /// <param name="dove">Specifica il punto automazione</param>
        public void GetStatus(string dove)
        {
            gw.GetStateCommand(WHO.Automation, dove);
        }

        public static WHAT GetWhat(string what)
        {
            WHAT retWhat;
            int value;

            retWhat = WHAT.None;

            if (int.TryParse(what, out value))
            {
                if (value == 0)
                {
                    retWhat = WHAT.AutomationStop;
                }
                else if (value == 1)
                {
                    retWhat = WHAT.AutomationUp;
                }
                else if (value == 2)
                {
                    retWhat = WHAT.AutomationDown;
                }
            }

            return retWhat;
        }

        public static AutomationMessage GetMessage(string data)
        {
            AutomationMessage message = null;
            string[] content;

            try
            {
                content = data.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);
                message = new AutomationMessage();
                message.What = GetWhat(content[1]);
                message.Where = Where.GetWhere(content[2]);
            }
            catch (Exception ex)
            {
                return null;
            }

            return message;
        }
    }
}

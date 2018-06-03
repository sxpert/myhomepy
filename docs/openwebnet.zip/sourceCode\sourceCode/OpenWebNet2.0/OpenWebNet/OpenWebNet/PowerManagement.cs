using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class PowerManagement
    {
        private OpenWebNetGateway gw;

        public PowerManagement(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="dove"></param>
        public void LoadForced(string dove)
        {
            gw.SendCommand(WHO.PowerManagement, "2", dove);
        }

        /// <summary>
        /// Richiede lo stato di ogni singola priorita'
        /// </summary>
        public void GetGeneralStatus()
        {
            gw.GetStateCommand(WHO.PowerManagement, "");
        }

        /// <summary>
        /// Richiede lo stato di una singola priorita'
        /// </summary>
        /// <param name="dove">Priorita'</param>
        public void GetPriorityStatus(string dove)
        {
            gw.GetStateCommand(WHO.PowerManagement, dove);
        }

        /// <summary>
        /// Richiede tutte le grandezze (Tensione, Corrente, Potenza, EneServeria)
        /// </summary>
        public void GetAllDimensions()
        {
            // *#3*10*0##

            gw.GetStateCommand(WHO.PowerManagement, "10*0");
        }

        /// <summary>
        /// Richiede la tensione
        /// </summary>
        public void GetVoltageStatus()
        {
            // *#3*10*1##

            gw.GetStateCommand(WHO.PowerManagement, "10*1");
        }

        /// <summary>
        /// Richiede la corrente
        /// </summary>
        public void GetCurrentStatus()
        {
            // *#3*10*2##

            gw.GetStateCommand(WHO.PowerManagement, "10*2");
        }

        /// <summary>
        /// Richiede la potenza
        /// </summary>
        public void GetPowerStatus()
        {
            // *#3*10*3##

            gw.GetStateCommand(WHO.PowerManagement, "10*3");
        }

        /// <summary>
        /// Richiede l'energia
        /// </summary>
        public void GetEnergyStatus()
        {
            // *#3*10*4##

            gw.GetStateCommand(WHO.PowerManagement, "10*4");
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
                    retWhat = WHAT.PowerManagementLoadDisabled;
                }
                else if (value == 1)
                {
                    retWhat = WHAT.PowerManagementLoadEnabled;
                }
                else if (value == 2)
                {
                    retWhat = WHAT.PowerManagementLoadForced;
                }
                else if (value == 3)
                {
                    retWhat = WHAT.PowerManagementLoadEndForced;
                }
                else if (value == 10)
                {
                    retWhat = WHAT.PowerManagementAllDimensionsRequest;
                }
            }

            return retWhat;
        }

        public static PowerManagementMessage GetMessage(string data)
        {
            PowerManagementMessage message = null;
            string[] content;

            if (string.IsNullOrEmpty(data))
                return null;

            try
            {
                message = new PowerManagementMessage();
                content = data.Remove(data.Length - 2, 2).Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                if (data.StartsWith("*#"))
                {
                    if (content[1] == "10")
                    {
                        switch (content[2])
                        {
                            case "0":
                                message.What = WHAT.PowerManagementAllDimensionsRequest;
                                message.Voltage = int.Parse(content[3]);
                                message.Current = int.Parse(content[4]);
                                message.Power = int.Parse(content[5]);
                                message.Energy = int.Parse(content[6]);
                                break;
                            case "1":
                                message.What = WHAT.PowerManagementVoltageRequest;
                                message.Voltage = int.Parse(content[3]);
                                break;
                            case "2":
                                message.What = WHAT.PowerManagementCurrentRequest;
                                message.Current = int.Parse(content[3]);
                                break;
                            case "3":
                                message.What = WHAT.PowerManagementPowerRequest;
                                message.Power = int.Parse(content[3]);
                                break;
                            case "4":
                                message.What = WHAT.PowerManagementEnergyRequest;
                                message.Energy = int.Parse(content[3]);
                                break;
                        }
                    }
                }
                else
                {
                    message.What = GetWhat(content[1]);
                    message.Where = Where.GetWhere(content[2]);
                }

            }
            catch (Exception)
            {
                return null;
            }

            return message;
        }
    }
}

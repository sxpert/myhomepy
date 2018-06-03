using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="dove"></param>
        public void PowerManagementLoadForced(string dove)
        {
            SendCommand(WHO.PowerManagement, "2", dove);
        }

        /// <summary>
        /// Richiede lo stato di ogni singola priorita'
        /// </summary>
        public void PowerManagementGetGeneralStatus()
        {
            GetStateCommand(WHO.PowerManagement, "");
        }

        /// <summary>
        /// Richiede lo stato di una singola priorita'
        /// </summary>
        /// <param name="dove">Priorita'</param>
        public void PowerManagementGetPriorityStatus(string dove)
        {
            GetStateCommand(WHO.PowerManagement, dove);
        }

        /// <summary>
        /// Richiede tutte le grandezze (Tensione, Corrente, Potenza, EneServeria)
        /// </summary>
        public void PowerManagementGetAllDimensions()
        {
            // *#3*10*0##

            GetStateCommand(WHO.PowerManagement, "10*0");
        }

        /// <summary>
        /// Richiede la tensione
        /// </summary>
        public void PowerManagementGetVoltageStatus()
        {
            // *#3*10*1##

            GetStateCommand(WHO.PowerManagement, "10*1");
        }

        /// <summary>
        /// Richiede la corrente
        /// </summary>
        public void PowerManagementGetCurrentStatus()
        {
            // *#3*10*2##

            GetStateCommand(WHO.PowerManagement, "10*2");
        }

        /// <summary>
        /// Richiede la potenza
        /// </summary>
        public void PowerManagementGetPowerStatus()
        {
            // *#3*10*3##

            GetStateCommand(WHO.PowerManagement, "10*3");
        }

        /// <summary>
        /// Richiede l'energia
        /// </summary>
        public void PowerManagementGetEnergyStatus()
        {
            // *#3*10*4##

            GetStateCommand(WHO.PowerManagement, "10*4");
        }
    }
}

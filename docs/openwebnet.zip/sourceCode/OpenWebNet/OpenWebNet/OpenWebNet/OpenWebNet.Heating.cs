using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{

    public enum TermoMode
    {
        Heating = 1,
        Cooling = 2,
        Generic = 3
    }

    public partial class OpenWebNetGateway
    {
        public void HeatingSettaZonaAutomatico(string dove)
        {
            SendCommand(WHO.Heating, "311", string.Format("#{0}", dove)); 
        }

        public void HeatingSetZonaOFF(string dove)
        {
            SendCommand(WHO.Heating, "303", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneAntigelo(string dove)
        {
            SendCommand(WHO.Heating, "102", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneTermica(string dove)
        {
            SendCommand(WHO.Heating, "202", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneGenerica(string dove)
        {
            SendCommand(WHO.Heating, "302", string.Format("#{0}", dove));
        }

        public void HeatingImpostaSetpoint(string dove, Single newSetpoint, TermoMode mode)
        {
            string sp = string.Format("{0:0000}", newSetpoint * 10);
            if (newSetpoint <= 5)
            { sp = "0050"; }
            else if (newSetpoint >= 40)
            { sp = "0400"; }
            string modo = ((int)mode).ToString();
            SendDimensionCommand(WHO.Heating, dove, "14", sp, modo);
        }

        public void HeatingSbloccaSonda(string dove)
        {
            SendCommand(WHO.Heating, "40", dove);
        }

        public void HeatingGetTemperaturaZona(string dove)
        {
            GetDimensionCommand(WHO.Heating, dove, "0");
        }

        public void HeatingGetSetpoint(string dove)
        {
            GetDimensionCommand(WHO.Heating, dove, "14");
        }

        public void HeatingGetImpostazioneZona(string dove)
        {
            GetDimensionCommand(WHO.Heating, dove, "13");
        }

        public void HeatingGetStatoZona(string dove)
        {
            GetStateCommand(WHO.Heating, dove);
        }

        public void HeatingGetStatoValvole(string dove)
        {
            GetDimensionCommand(WHO.Heating, dove, "19");
        }

        public void HeatingCentraleOFF()
        {
            SendCommand(WHO.Heating, "303", "#0");
        }

        public void HeatingSettaCentraleProtezioneTermica()
        {
            SendCommand(WHO.Heating, "202", "#0");
        }

        public void HeatingSettaCentraleProtezioneAntigelo()
        {
            SendCommand(WHO.Heating, "102", "#0");
        }

        public void HeatingProgrammaSettimanaleCondizionamentoON(int cosa)
        {
            if (cosa < 2101 || cosa > 2103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingProgrammaSettimanaleRiscaldamentoON(int cosa)
        {
            if (cosa < 1101 || cosa > 1103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingProgrammaSettimanaleON(int cosa)
        {
            if (cosa < 3101 || cosa > 3103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingUltimoProgrammaSettimanaleImpostatoON()
        {
            SendCommand(WHO.Heating, "3100", "#0");
        }

        public void HeatingScenarioCondizionamentoON(int cosa)
        {
            if (cosa < 2201 || cosa > 2216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingScenarioRiscaldamentoON(int cosa)
        {
            if (cosa < 1201 || cosa > 1216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingScenarioON(int cosa)
        {
            if (cosa < 3201 || cosa > 3216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingUltimoScenarioON()
        {
            SendCommand(WHO.Heating, "3200", "#0");
        }
    }
}

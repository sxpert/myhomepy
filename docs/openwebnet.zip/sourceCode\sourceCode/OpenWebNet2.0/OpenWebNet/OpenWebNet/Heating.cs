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

    public class Heating
    {
        private OpenWebNetGateway gw;

        public Heating(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        public void HeatingSettaZonaAutomatico(string dove)
        {
            gw.SendCommand(WHO.Heating, "311", string.Format("#{0}", dove));
        }

        public void HeatingSetZonaOFF(string dove)
        {
            gw.SendCommand(WHO.Heating, "303", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneAntigelo(string dove)
        {
            gw.SendCommand(WHO.Heating, "102", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneTermica(string dove)
        {
            gw.SendCommand(WHO.Heating, "202", string.Format("#{0}", dove));
        }

        public void HeatingSettaZonaProtezioneGenerica(string dove)
        {
            gw.SendCommand(WHO.Heating, "302", string.Format("#{0}", dove));
        }

        public void HeatingImpostaSetpoint(string dove, Single newSetpoint, TermoMode mode)
        {
            string sp = string.Format("{0:0000}", newSetpoint * 10);
            
            if (newSetpoint <= 5)
            {
                sp = "0050";
            }
            else if (newSetpoint >= 40)
            {
                sp = "0400";
            }
            
            string modo = ((int)mode).ToString();
            
            gw.SendDimensionCommand(WHO.Heating, dove, "14", sp, modo);
        }

        public void HeatingSbloccaSonda(string dove)
        {
            gw.SendCommand(WHO.Heating, "40", dove);
        }

        public void HeatingGetTemperaturaZona(string dove)
        {
            gw.GetDimensionCommand(WHO.Heating, dove, "0");
        }

        public void HeatingGetSetpoint(string dove)
        {
            gw.GetDimensionCommand(WHO.Heating, dove, "14");
        }

        public void HeatingGetImpostazioneZona(string dove)
        {
            gw.GetDimensionCommand(WHO.Heating, dove, "13");
        }

        public void HeatingGetStatoZona(string dove)
        {
            gw.GetStateCommand(WHO.Heating, dove);
        }

        public void HeatingGetStatoValvole(string dove)
        {
            gw.GetDimensionCommand(WHO.Heating, dove, "19");
        }

        public void HeatingCentraleOFF()
        {
            gw.SendCommand(WHO.Heating, "303", "#0");
        }

        public void HeatingSettaCentraleProtezioneTermica()
        {
            gw.SendCommand(WHO.Heating, "202", "#0");
        }

        public void HeatingSettaCentraleProtezioneAntigelo()
        {
            gw.SendCommand(WHO.Heating, "102", "#0");
        }

        public void HeatingProgrammaSettimanaleCondizionamentoON(int cosa)
        {
            if (cosa < 2101 || cosa > 2103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingProgrammaSettimanaleRiscaldamentoON(int cosa)
        {
            if (cosa < 1101 || cosa > 1103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingProgrammaSettimanaleON(int cosa)
        {
            if (cosa < 3101 || cosa > 3103)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingUltimoProgrammaSettimanaleImpostatoON()
        {
            gw.SendCommand(WHO.Heating, "3100", "#0");
        }

        public void HeatingScenarioCondizionamentoON(int cosa)
        {
            if (cosa < 2201 || cosa > 2216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingScenarioRiscaldamentoON(int cosa)
        {
            if (cosa < 1201 || cosa > 1216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingScenarioON(int cosa)
        {
            if (cosa < 3201 || cosa > 3216)
                throw new ArgumentOutOfRangeException("Cosa value wrong");

            gw.SendCommand(WHO.Heating, cosa.ToString(), "#0");
        }

        public void HeatingUltimoScenarioON()
        {
            gw.SendCommand(WHO.Heating, "3200", "#0");
        }

        public static WHAT GetWhat(string what, out string[] parameters)
        {
            WHAT retWhat = WHAT.None;
            int value;

            parameters = null;
            if (int.TryParse(what, out value))
            {

                switch (value)
                {
                    case 0:
                        retWhat = WHAT.TermoCoolingMode;
                        break;
                    case 1:
                        retWhat = WHAT.TermoHeatingMode;
                        break;
                    case 102:
                        retWhat = WHAT.TermoAntiFreezeProtection;
                        break;
                    case 202:
                        retWhat = WHAT.TermoCoolingProtection;
                        break;
                    case 302:
                        retWhat = WHAT.TermoProtection;
                        break;
                    case 103:
                        retWhat = WHAT.TermoHeatingOff;
                        break;
                    case 203:
                        retWhat = WHAT.TermoCoolingOff;
                        break;
                    case 303:
                        retWhat = WHAT.TermoOff;
                        break;
                    case 110:
                        retWhat = WHAT.TermoHeatingManual;
                        break;
                    case 210:
                        retWhat = WHAT.TermoCoolingManual;
                        break;
                    case 310:
                        retWhat = WHAT.TermoManual;
                        break;
                    case 111:
                        retWhat = WHAT.TermoProgrammingHeating;
                        break;
                    case 211:
                        retWhat = WHAT.TermoProgrammingCooling;
                        break;
                    case 311:
                        retWhat = WHAT.TermoProgramming;
                        break;
                }
            }
            return retWhat;
        }
    }
}

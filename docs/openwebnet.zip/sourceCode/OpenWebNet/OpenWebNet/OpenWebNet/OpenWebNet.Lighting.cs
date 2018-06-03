using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        /// <summary>
        /// Turn ON the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn ON</param>
        public void LightingLightON(string where)
        {
            SendCommand(WHO.Lighting, "1", where);
        }

        /// <summary>
        /// Turn OFF the light point specified
        /// </summary>
        /// <param name="where">Specify the light point to turn ON</param>
        public void LightingLightOFF(string where)
        {
            SendCommand(WHO.Lighting, "0", where);
        }

        /// <summary>
        /// Turn ON the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn ON</param>
        /// <param name="speed">Speed(0 (immediate) - 255 (maximum delay)</param>
        public void LightingLightON(string where, uint speed)
        {
            if (speed < 0 || speed > 255)
                throw new ArgumentOutOfRangeException("Speed value has to be between 0 and 255");

            SendCommand(WHO.Lighting, string.Format("1#{0}", speed), where);
        }

        /// <summary>
        /// Turn OFF the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn OFF</param>
        /// <param name="speed">Speed(0 (immediate) - 255 (maximum delay)</param>
        public void LightingLightOFF(string where, uint speed)
        {
            if (speed < 0 || speed > 255)
                throw new ArgumentException("Speed value has to be between 0 and 255");

            SendCommand(WHO.Lighting, string.Format("0#{0}", speed), where);
        }

        /// <summary>
        /// Change the strenght of the specified dimmer
        /// </summary>
        /// <param name="where">Specify the dimmer</param>
        /// <param name="percentuale">Strenght value (Values: 20, 30, 40, 50, 60, 70, 80, 90, 100)</param>
        public void LightingDimmerStrenght(string where, uint strenght)
        {
            if (strenght < 20 || strenght > 100 || strenght % 10 != 0)
                throw new ArgumentException("Strenght value wrong");

            SendCommand(WHO.Lighting, string.Format("{0}", strenght / 10), where);
        }

        /// <summary>
        /// Fa lampeggiare il punto luce specificato per un certo numero di secondi
        /// </summary>
        /// <param name="where">Specify the light point</param>
        /// <param name="seconds">Seconds (Valori: 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)</param>
        public void LightingLightBlinking(string where, double seconds)
        {
            string what;

            if (seconds == 0.5)
                what = "20";
            else if (seconds == 1)
                what = "21";
            else if (seconds == 1.5)
                what = "22";
            else if (seconds == 2)
                what = "23";
            else if (seconds == 2.5)
                what = "24";
            else if (seconds == 3)
                what = "25";
            else if (seconds == 3.5)
                what = "26";
            else if (seconds == 4)
                what = "27";
            else if (seconds == 4.5)
                what = "28";
            else if (seconds == 5)
                what = "29";
            else
                throw new ArgumentException("Seconds value wrong");

            SendCommand(WHO.Lighting, what, where);
        }

        /// <summary>
        /// Aumenta l'intensità del punto luce di un livello
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void LightingDimmerUp(string dove)
        {
            SendCommand(WHO.Lighting, "30", dove);
        }

        /// <summary>
        /// Diminuisce l'intensità del punto luce di un livello
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void LightingDimmerDown(string dove)
        {
            SendCommand(WHO.Lighting, "31", dove);
        }

        /// <summary>
        /// Aumenta l'intensita' del punto luce di n livelli ad una certa velocita'
        /// </summary>
        /// <param name="dove">Speicifica il punto luce</param>
        /// <param name="livelli">Specifica il numero di livelli (da 1 = Accensione a 100 = Spegnimento)</param>
        /// <param name="velocita">Specifica la velocita' (da 0 = immediato a 255 = ritardo massimo)</param>
        public void LightingDimmerUp(string dove, int livelli, int velocita)
        {
            string cosa = "30#{0}#{1}";

            if (livelli < 1 || livelli > 100)
                throw new ArgumentOutOfRangeException("Valore di livelli errato");

            if (velocita < 0 || velocita > 255)
                throw new ArgumentOutOfRangeException("Valore di velocita' errato");

            SendCommand(WHO.Lighting, string.Format(cosa, livelli, velocita), dove);
        }

        /// <summary>
        /// Diminuisce l'intensita' del punto luce di n livelli ad una certa velocita'
        /// </summary>
        /// <param name="dove">Speicifica il punto luce</param>
        /// <param name="livelli">Specifica il numero di livelli (da 1 = Accensione a 100 = Spegnimento)</param>
        /// <param name="velocita">Specifica la velocita' (da 0 = immediato a 255 = ritardo massimo)</param>
        public void LightingDimmerDown(string dove, int livelli, int velocita)
        {
            string cosa = "31#{0}#{1}";

            if (livelli < 1 || livelli > 100)
                throw new ArgumentOutOfRangeException("Valore di livelli errato");

            if (velocita < 0 || velocita > 255)
                throw new ArgumentOutOfRangeException("Valore di velocita' errato");

            SendCommand(WHO.Lighting, string.Format(cosa, livelli, velocita), dove);
        }

        public void LightingLightONTemporization(string dove, int min)
        {
            string cosa = string.Empty;

            if (min == 1)
                cosa = "11";
            else if (min == 2)
                cosa = "12";
            else if (min == 3)
                cosa = "13";
            else if (min == 4)
                cosa = "14";
            else if (min == 5)
                cosa = "15";
            else if (min == 15)
                cosa = "16";
            else
                throw new ArgumentOutOfRangeException("Min value wrong");

            SendCommand(WHO.Lighting, cosa, dove);
        }

        /// <summary>
        /// Richiede lo stato di un punto luce
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void LightingGetLightStatus(string dove)
        {
            GetStateCommand(WHO.Lighting, dove);
        }
    }
}

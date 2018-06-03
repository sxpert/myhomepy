using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class Lighting
    {
        private OpenWebNetGateway gw;

        public Lighting(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        /// <summary>
        /// Turn ON the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn ON</param>
        public void LightON(string where)
        {
            gw.SendCommand(WHO.Lighting, "1", where);
        }

        /// <summary>
        /// Turn OFF the light point specified
        /// </summary>
        /// <param name="where">Specify the light point to turn OFF</param>
        public void LightOFF(string where)
        {
            gw.SendCommand(WHO.Lighting, "0", where);
        }

        /// <summary>
        /// Turn ON the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn ON</param>
        /// <param name="speed">Speed(0 (immediate) - 255 (maximum delay)</param>
        public void LightON(string where, uint speed)
        {
            if (speed < 0 || speed > 255)
                throw new ArgumentOutOfRangeException("Speed value has to be between 0 and 255");

            gw.SendCommand(WHO.Lighting, string.Format("1#{0}", speed), where);
        }

        /// <summary>
        /// Turn OFF the specified light point
        /// </summary>
        /// <param name="where">Specify the light point to turn OFF</param>
        /// <param name="speed">Speed(0 (immediate) - 255 (maximum delay)</param>
        public void LightOFF(string where, uint speed)
        {
            if (speed < 0 || speed > 255)
                throw new ArgumentException("Speed value has to be between 0 and 255");

            gw.SendCommand(WHO.Lighting, string.Format("0#{0}", speed), where);
        }

        /// <summary>
        /// Change the strenght of the specified dimmer
        /// </summary>
        /// <param name="where">Specify the dimmer</param>
        /// <param name="percentuale">Strenght value (Values: 20, 30, 40, 50, 60, 70, 80, 90, 100)</param>
        public void DimmerStrenght(string where, uint strenght)
        {
            if (strenght < 20 || strenght > 100 || strenght % 10 != 0)
                throw new ArgumentException("Strenght value wrong");

            gw.SendCommand(WHO.Lighting, string.Format("{0}", strenght / 10), where);
        }

        /// <summary>
        /// Fa lampeggiare il punto luce specificato per un certo numero di secondi
        /// </summary>
        /// <param name="where">Specify the light point</param>
        /// <param name="seconds">Seconds (Valori: 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)</param>
        public void LightBlinking(string where, double seconds)
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

            gw.SendCommand(WHO.Lighting, what, where);
        }

        /// <summary>
        /// Aumenta l'intensità del punto luce di un livello
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void DimmerUp(string dove)
        {
            gw.SendCommand(WHO.Lighting, "30", dove);
        }

        /// <summary>
        /// Diminuisce l'intensità del punto luce di un livello
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void DimmerDown(string dove)
        {
            gw.SendCommand(WHO.Lighting, "31", dove);
        }

        /// <summary>
        /// Aumenta l'intensita' del punto luce di n livelli ad una certa velocita'
        /// </summary>
        /// <param name="dove">Speicifica il punto luce</param>
        /// <param name="livelli">Specifica il numero di livelli (da 1 = Accensione a 100 = Spegnimento)</param>
        /// <param name="velocita">Specifica la velocita' (da 0 = immediato a 255 = ritardo massimo)</param>
        public void DimmerUp(string dove, int livelli, int velocita)
        {
            string cosa = "30#{0}#{1}";

            if (livelli < 1 || livelli > 100)
                throw new ArgumentOutOfRangeException("Valore di livelli errato");

            if (velocita < 0 || velocita > 255)
                throw new ArgumentOutOfRangeException("Valore di velocita' errato");

            gw.SendCommand(WHO.Lighting, string.Format(cosa, livelli, velocita), dove);
        }

        /// <summary>
        /// Diminuisce l'intensita' del punto luce di n livelli ad una certa velocita'
        /// </summary>
        /// <param name="dove">Speicifica il punto luce</param>
        /// <param name="livelli">Specifica il numero di livelli (da 1 = Accensione a 100 = Spegnimento)</param>
        /// <param name="velocita">Specifica la velocita' (da 0 = immediato a 255 = ritardo massimo)</param>
        public void DimmerDown(string dove, int livelli, int velocita)
        {
            string cosa = "31#{0}#{1}";

            if (livelli < 1 || livelli > 100)
                throw new ArgumentOutOfRangeException("Valore di livelli errato");

            if (velocita < 0 || velocita > 255)
                throw new ArgumentOutOfRangeException("Valore di velocita' errato");

            gw.SendCommand(WHO.Lighting, string.Format(cosa, livelli, velocita), dove);
        }

        public void LightONTemporization(string dove, int min)
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

            gw.SendCommand(WHO.Lighting, cosa, dove);
        }

        /// <summary>
        /// Richiede lo stato di un punto luce
        /// </summary>
        /// <param name="dove">Specifica il punto luce</param>
        public void GetLightStatus(string dove)
        {
            gw.GetStateCommand(WHO.Lighting, dove);
        }

        public static WHAT GetWhat(string what)
        {
            int value;
            WHAT retWhat;

            retWhat = WHAT.None;

            if (int.TryParse(what, out value))
            {
                if (value == 1)
                {
                    retWhat = WHAT.LightON;
                }
                else if (value == 0)
                {
                    retWhat = WHAT.LightOFF;
                }
                else if (value >= 2 && value <= 10)
                {
                    retWhat = WHAT.DimmerStrenght;
                }
                else if (value >= 20 && value <= 29)
                {
                    retWhat = WHAT.LightBlinking;
                }
                else if (value == 30)
                {
                    retWhat = WHAT.DimmerUp;
                }
                else if (value == 31)
                {
                    retWhat = WHAT.DimmerDown;
                }
                else if (value == 19)
                {
                    retWhat = WHAT.DimmerNoLoad;
                }
            }

            return retWhat;
        }

        // parte di temporizzazione da controllare & blinking

        public static LightingMessage GetMessage(string data)
        {
            LightingMessage message = null;
            string[] content, parts;

            if (string.IsNullOrEmpty(data))
                return null;

            try
            {
                message = new LightingMessage();
                content = data.Remove(data.Length - 2, 2).Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                if (content[0].Contains("#"))
                {
                    // Could be a Temporization or a Luminous Intensity Changed command

                    if (content[2] == "1")
                    {
                        message.What = WHAT.LightTemporization;
                        message.Temporization = new TimeSpan(int.Parse(content[3]), int.Parse(content[4]), int.Parse(content[5]));
                    }
                    else if (content[2] == "2")
                    {
                        message.What = WHAT.LightLuminousIntensityChange;
                        message.Level = int.Parse(content[3]);
                        message.Speed = int.Parse(content[4]);
                    }

                    message.Where = Where.GetWhere(content[1]);
                }
                else
                {
                    parts = content[1].Split(new char[] { '#' }, StringSplitOptions.RemoveEmptyEntries);

                    if (parts.Length == 3)
                    {
                        // Could be a "y levels at x speed" command

                        switch (GetWhat(parts[0]))
                        {
                            case WHAT.DimmerUp:
                                message.What = WHAT.DimmerUpAtSpeed;
                                break;
                            case WHAT.DimmerDown:
                                message.What = WHAT.DimmerDownAtSpeed;
                                break;
                        }

                        message.Level = int.Parse(parts[1]);
                        message.Speed = int.Parse(parts[2]);

                    }
                    else if (parts.Length == 2)
                    {
                        // Could be a "at speed" command
                        switch (GetWhat(parts[0]))
                        {
                            case WHAT.LightON:
                                message.What = WHAT.LightOnAtSpeed;
                                break;
                            case WHAT.LightOFF:
                                message.What = WHAT.LightOffAtSpeed;
                                break;
                        }

                        message.Speed = int.Parse(parts[1]);
                    }
                    else
                    {
                        message.What = GetWhat(parts[0]);

                        if (message.What == WHAT.DimmerStrenght)
                        {
                            message.DimmerStrenght = int.Parse(parts[0]) * 10;
                        }
                    }

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

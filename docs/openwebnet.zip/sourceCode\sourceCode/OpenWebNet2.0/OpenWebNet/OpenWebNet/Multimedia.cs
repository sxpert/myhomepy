using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class Multimedia
    {
        private OpenWebNetGateway gw;

        public Multimedia(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        public void CameraON(string dove)
        {
            gw.SendCommand(WHO.RemoteControl, "0", dove + "*");
        }

        public void CameraOFF()
        {
            gw.SendCommand(WHO.RemoteControl, "8", "*");
        }

        public void FreeAudioAndVideoResources()
        {
            gw.SendCommand(WHO.RemoteControl, "9", "*");
        }

        public void ZoomIn()
        {
            gw.SendCommand(WHO.RemoteControl, "120", "");
        }

        public void ZoomOut()
        {
            gw.SendCommand(WHO.RemoteControl, "121", "");
        }

        public void IncreasesX()
        {
            gw.SendCommand(WHO.RemoteControl, "130", "");
        }

        public void DecreasesX()
        {
            gw.SendCommand(WHO.RemoteControl, "131", "");
        }

        public void IncreasesY()
        {
            gw.SendCommand(WHO.RemoteControl, "140", "");
        }

        public void DecreasesY()
        {
            gw.SendCommand(WHO.RemoteControl, "141", "");
        }

        public void IncreasesLuminosity()
        {
            gw.SendCommand(WHO.RemoteControl, "150", "");
        }

        public void DecreasesLuminosity()
        {
            gw.SendCommand(WHO.RemoteControl, "151", "");
        }

        public void IncreasesContrast()
        {
            gw.SendCommand(WHO.RemoteControl, "160", "");
        }

        public void DecreasesContrast()
        {
            gw.SendCommand(WHO.RemoteControl, "161", "");
        }

        public void IncreasesColour()
        {
            gw.SendCommand(WHO.RemoteControl, "170", "");
        }

        public void DecreasesColour()
        {
            gw.SendCommand(WHO.RemoteControl, "171", "");
        }

        public void IncreasesQuality()
        {
            gw.SendCommand(WHO.RemoteControl, "180", "");
        }

        public void DecreasesQuality()
        {
            gw.SendCommand(WHO.RemoteControl, "181", "");
        }

        public void DisplayDialXY(int x, int y)
        {
            if (x < 1 || x > 4)
                throw new ArgumentOutOfRangeException("X must be between 1 and 4");

            if (y < 1 || y > 4)
                throw new ArgumentOutOfRangeException("Y must be between 1 and 4");

            gw.SendCommand(WHO.RemoteControl, string.Format("3{0}{1}", x, y), "");
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
                    case 0:
                        retWhat = WHAT.MultimediaCameraON;
                        break;
                    case 8:
                        retWhat = WHAT.MultimediaCameraOFF;
                        break;
                    case 9:
                        retWhat = WHAT.MultimediaAudioVideoOFF;
                        break;
                    case 120:
                        retWhat = WHAT.MultimediaZoomIn;
                        break;
                    case 121:
                        retWhat = WHAT.MultimediaZoomOut;
                        break;
                    case 130:
                        retWhat = WHAT.MultimediaIncreaseX;
                        break;
                    case 131:
                        retWhat = WHAT.MultimediaDecreaseX;
                        break;
                    case 140:
                        retWhat = WHAT.MultimediaIncreaseY;
                        break;
                    case 141:
                        retWhat = WHAT.MultimediaDecreaseY;
                        break;
                    case 150:
                        retWhat = WHAT.MultimediaIncreaseLuminosity;
                        break;
                    case 151:
                        retWhat = WHAT.MultimediaDecreaseLuminosity;
                        break;
                    case 160:
                        retWhat = WHAT.MultimediaIncreaseContrast;
                        break;
                    case 161:
                        retWhat = WHAT.MultimediaDecreaseContrast;
                        break;
                    case 170:
                        retWhat = WHAT.MultimediaIncreaseColor;
                        break;
                    case 171:
                        retWhat = WHAT.MultimediaDecreaseColor;
                        break;
                    case 180:
                        retWhat = WHAT.MultimediaIncreaseQuality;
                        break;
                    case 181:
                        retWhat = WHAT.MultimediaDecreaseQuality;
                        break;
                }
            }

            return retWhat;
        }

        public static MultimediaMessage GetMessage(string data)
        {
            if (string.IsNullOrEmpty(data))
                return null;

            string[] content;
            MultimediaMessage message = null;

            try
            {
                content = data.Remove(data.Length - 2, 2).Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                message = new MultimediaMessage();
                message.What = GetWhat(content[1]);

                if (content.Length == 3)
                    message.Where = Where.GetWhere(content[2]);

                if (content[1].StartsWith("3"))
                {
                    // It's a Display Dial X-Y message
                    message.DisplayDialX = int.Parse(content[1][1].ToString());
                    message.DisplayDialY = int.Parse(content[1][2].ToString());
                    message.What = WHAT.MultimediaDisplayDialXY;
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

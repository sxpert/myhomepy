using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        // Non funziona nulla con WHO.Multimedia (7)...devo usare ControlloRemoto
        // I comandi sono diversi dallo standard

        public void MultimediaCameraON(string dove)
        {
            // controllare motivo

            SendCommand(WHO.RemoteControl, "0", dove + "*");
        }

        public void MultimediaCameraOFF()
        {
            // sistemare
            // 8 ---> video
            // 9 ---> audio/video
            SendCommand(WHO.RemoteControl, "9**", "");
        }

        public void MultimediaZoomIn()
        {
            SendCommand(WHO.RemoteControl, "120", "");
        }

        public void MultimediaZoomOut()
        {
            SendCommand(WHO.RemoteControl, "121", "");
        }

        public void MultimediaIncreasesX()
        {
            SendCommand(WHO.RemoteControl, "130", "");
        }

        public void MultimediaDecreasesX()
        {
            SendCommand(WHO.RemoteControl, "131", "");
        }

        public void MultimediaIncreasesY()
        {
            SendCommand(WHO.RemoteControl, "140", "");
        }

        public void MultimediaDecreasesY()
        {
            SendCommand(WHO.RemoteControl, "141", "");
        }

        public void MultimediaIncreasesLuminosity()
        {
            SendCommand(WHO.RemoteControl, "150", "");
        }

        public void MultimediaDecreasesLuminosity()
        {
            SendCommand(WHO.RemoteControl, "151", "");
        }

        public void MultimediaIncreasesContrast()
        {
            SendCommand(WHO.RemoteControl, "160", "");
        }

        public void MultimediaDecreasesContrast()
        {
            SendCommand(WHO.RemoteControl, "161", "");
        }

        public void MultimediaIncreasesColour()
        {
            SendCommand(WHO.RemoteControl, "170", "");
        }

        public void MultimediaDecreasesColour()
        {
            SendCommand(WHO.RemoteControl, "171", "");
        }

        public void MultimediaIncreasesQuality()
        {
            SendCommand(WHO.RemoteControl, "180", "");
        }

        public void MultimediaDecreasesQuality()
        {
            SendCommand(WHO.RemoteControl, "181", "");
        }

        public void MultimediaDisplayDialXY(int x, int y)
        {
            if (x < 1 || x > 4)
                throw new ArgumentOutOfRangeException("X deve essere compreso tra 1 e 4");

            if (y < 1 || y > 4)
                throw new ArgumentOutOfRangeException("Y deve essere compreso tra 1 e 4");

            SendCommand(WHO.RemoteControl, string.Format("3{0}{1}", x, y), "");
        }
    }
}

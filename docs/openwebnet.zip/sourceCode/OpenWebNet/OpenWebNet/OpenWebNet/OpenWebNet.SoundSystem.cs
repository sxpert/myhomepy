using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public partial class OpenWebNetGateway
    {
        public void SoundSystemAmplifiersON(int what, string where)
        {
            if (what != 0 && what != 3)
                throw new ArgumentOutOfRangeException("What value has to be either 0 or 3");

            SendCommand(WHO.SoundSystem, what.ToString(), where);
        }

        public void SoundSystemAmplifiersOFF(int what, string where)
        {
            if (what != 10 && what != 13)
                throw new ArgumentOutOfRangeException("What value has to be either 10 or 13");

            SendCommand(WHO.SoundSystem, what.ToString(), where);
        }

        public void SoundSystemCycleSources(int room)
        {
        }

        public void SoundSystemSleepON(int cosa, string dove)
        {
            if (cosa != 30 && cosa != 33)
                throw new ArgumentOutOfRangeException("Cosa puo' essere 30 o 33");

            SendCommand(WHO.SoundSystem, cosa.ToString(), dove);
        }

        public void SoundSystemSleepOFF(string dove)
        {
            SendCommand(WHO.SoundSystem, "40", dove);
        }

        public void SoundSystemFollowMe(int room)
        {
            if (room < 1 || room > 9)
                throw new ArgumentOutOfRangeException("Room value wrong");

            SendCommand(WHO.SoundSystem, "53", string.Format("1{0}0", room));
        }

        public void SoundSystemStartSendingRDS(string where)
        {
            SendCommand(WHO.SoundSystem, "101", where);
        }

        public void SoundSystemStopSendingRDS(string where)
        {
            SendCommand(WHO.SoundSystem, "102", where);
        }

        public void SoundSystemVolumeUP(int volume, string where)
        {
            if (volume < 1 || volume > 15)
                throw new ArgumentOutOfRangeException("Volume value must be beetwen 1 and 15");

            SendCommand(WHO.SoundSystem, string.Format("100{0}", volume), where);
        }

        public void SoundSystemVolumeDOWN(int volume, string where)
        {
            if (volume < 1 || volume > 15)
                throw new ArgumentOutOfRangeException("Volume value must be beetwen 1 and 15");

            SendCommand(WHO.SoundSystem, string.Format("110{0}", volume), where);
        }
    }
}

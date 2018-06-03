using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public class SoundSystem
    {
        private OpenWebNetGateway gw;

        public SoundSystem(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        public void AmplifiersONStereoChannel(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "3", where);
        }

        public void AmplifiersONBaseband(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "0", where);
        }

        public void AmplifiersOFFStereoChannel(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "13", where);
        }

        public void AmplifiersOFFBaseband(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "10", where);
        }

        // SourcesON - SourcesOFF

        public void CycleSourcesBaseband(int room)
        {
            gw.SendCommand(WHO.SoundSystem, "23", string.Format("1{0}0", room));
        }

        public void CycleSourceStereoChannel(int room)
        {
            gw.SendCommand(WHO.SoundSystem, "20", string.Format("1{0}0", room));
        }

        public void SleepONBaseband(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "30", where);
        }

        public void SleepONStereoChannel(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "33", where);
        }

        public void SleepOFF(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "40", where);
        }

        public void FollowMe(int room)
        {
            gw.SendCommand(WHO.SoundSystem, "53", string.Format("1{0}0", room));
        }

        public void StartSendingRDS(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "101", where);
        }

        public void StopSendingRDS(string where)
        {
            gw.SendCommand(WHO.SoundSystem, "102", where);
        }

        public void VolumeUp(int volume, string where)
        {
            string what;

            if (volume < 1 || volume > 15)
                throw new ArgumentOutOfRangeException("Volume value must be beetwen 1 and 15");

            if (volume < 10)
                what = string.Format("100{0}", volume);
            else
                what = string.Format("10{0}", volume);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void VolumeDown(int volume, string where)
        {
            string what;

            if (volume < 1 || volume > 15)
                throw new ArgumentOutOfRangeException("Volume value must be beetwen 1 and 15");

            if (volume < 10)
                what = string.Format("100{0}", volume);
            else
                what = string.Format("10{0}", volume);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void FrequencyUp(int frequency, string where)
        {
            string what;

            if (frequency < 1 || frequency > 15)
                throw new ArgumentOutOfRangeException("Frequency value must be beetwen 1 and 15");

            if (frequency < 10)
                what = string.Format("500{0}", frequency);
            else
                what = string.Format("50{0}", frequency);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void FrequencyDown(int frequency, string where)
        {
            string what;

            if (frequency < 1 || frequency > 15)
                throw new ArgumentOutOfRangeException("Frequency value must be beetwen 1 and 15");

            if (frequency < 10)
                what = string.Format("510{0}", frequency);
            else
                what = string.Format("51{0}", frequency);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void NextStation(int station, string where)
        {
            string what;

            if (station < 1 || station > 15)
                throw new ArgumentOutOfRangeException("Station value must be beetwen 1 and 15");

            if (station < 10)
                what = string.Format("600{0}", station);
            else
                what = string.Format("60{0}", station);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void PreviousStation(int station, string where)
        {
            string what;

            if (station < 1 || station > 15)
                throw new ArgumentOutOfRangeException("Station value must be beetwen 1 and 15");

            if (station < 10)
                what = string.Format("610{0}", station);
            else
                what = string.Format("61{0}", station);

            gw.SendCommand(WHO.SoundSystem, what, where);
        }

        public void GetSoundSystemMatrix()
        {
            gw.GetDimensionCommand(WHO.SoundSystem, "1000", "11");
        }

        public void GetVolume(string where)
        {
            gw.GetDimensionCommand(WHO.SoundSystem, where, "1");
        }

        public void GetStatus(string where)
        {
            gw.GetDimensionCommand(WHO.SoundSystem, where, "5");
        }

        public void GetFrequency(string where)
        {
            gw.GetDimensionCommand(WHO.SoundSystem, where, "6");
        }

        public void GetStation(string where)
        {
            gw.GetDimensionCommand(WHO.SoundSystem, where, "7");
        }

        public void GetRDS(string where)
        {
            gw.GetDimensionCommand(WHO.SoundSystem, where, "8");
        }

        public void WriteVolume(int volume, string where)
        {
            if (volume < 0 || volume > 31)
                throw new ArgumentOutOfRangeException("Volume value must be beetwen 1 and 31");

            gw.WriteDimension(WHO.SoundSystem, where, "1", volume.ToString());
        }

        public void WriteFrequency(int frequency, string where)
        {
            // sistemare

            gw.WriteDimension(WHO.SoundSystem, where, "6", string.Format("0*{0}", frequency));
        }

        public void WriteRadioStation(int station, string where)
        {
            gw.WriteDimension(WHO.SoundSystem, where, "7", station.ToString());
        }

        public static WHAT GetWhat(string what, out string[] parameters)
        {
            WHAT retWhat;
            int value;

            retWhat = WHAT.None;
            parameters = null;

            if (int.TryParse(what, out value))
            {
                if (value >= 1001 && value <= 1015)
                {
                    retWhat = WHAT.SoundSystemVolumeUp;
                }
                else if (value >= 1101 && value <= 1115)
                {
                    retWhat = WHAT.SoundSystemVolumeDown;
                }
            }

            return retWhat;
        }
    }
}

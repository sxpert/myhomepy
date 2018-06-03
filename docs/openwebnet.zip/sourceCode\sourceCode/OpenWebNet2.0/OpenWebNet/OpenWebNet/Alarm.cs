using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public class Alarm
    {
        private OpenWebNetGateway gw;

        public Alarm(OpenWebNetGateway gateway)
        {
            if (gateway == null)
                throw new ArgumentNullException("gateway");

            this.gw = gateway;
        }

        public void GetZoneStatus(int n)
        {
            if (n < 1 || n > 8)
                throw new ArgumentOutOfRangeException("N value wrong");

            gw.GetStateCommand(WHO.Alarm, string.Format("#{0}", n.ToString()));
        }

        public void GetCentralUnitStatusFromWebServer()
        {
            gw.GetStateCommand(WHO.Alarm, string.Empty);
        }

        public void GetCentralUnitStatusFromCentralUnit()
        {
            gw.GetStateCommand(WHO.Alarm, "1");
        }

        public void GetAuxiliaresStatusFromWebServer()
        {
            gw.GetStateCommand(WHO.Auxiliaries, string.Empty);
        }

        public static WHAT GetWhat(string what)
        {
            int value;
            WHAT retWhat = WHAT.None;

            if (int.TryParse(what, out value))
            {
                if (value == 0)
                    retWhat = WHAT.AlarmMaintenance;
                else if (value == 1)
                    retWhat = WHAT.AlarmActivation;
                else if (value == 2)
                    retWhat = WHAT.AlarmDisactivation;
                else if (value == 3)
                    retWhat = WHAT.AlarmDelayEnd;
                else if (value == 4)
                    retWhat = WHAT.AlarmBatteryFault;
                else if (value == 5)
                    retWhat = WHAT.AlarmBatteryOK;
                else if (value == 6)
                    retWhat = WHAT.AlarmNetworkFault;
                else if (value == 7)
                    retWhat = WHAT.AlarmNetworkOK;
                else if (value == 8)
                    retWhat = WHAT.AlarmEngage;
                else if (value == 9)
                    retWhat = WHAT.AlarmDisengage;
                else if (value == 10)
                    retWhat = WHAT.AlarmBatteryUnloads;
                else if (value == 11)
                    retWhat = WHAT.AlarmActiveZone;
                else if (value == 12)
                    retWhat = WHAT.AlarmTechnicalAlarm;
                else if (value == 13)
                    retWhat = WHAT.AlarmResetTechnicalAlarm;
                else if (value == 14)
                    retWhat = WHAT.AlarmNoReception;
                else if (value == 15)
                    retWhat = WHAT.AlarmIntrusion;
                else if (value == 16)
                    retWhat = WHAT.AlarmTampering;
                else if (value == 17)
                    retWhat = WHAT.AlarmAntipanic;
                else if (value == 18)
                    retWhat = WHAT.AlarmNonActiveZone;
                else if (value == 26)
                    retWhat = WHAT.AlarmStartProgramming;
                else if (value == 27)
                    retWhat = WHAT.AlarmStopProgramming;
                else if (value == 31)
                    retWhat = WHAT.AlarmSilentAlarm;
            }
            return retWhat;
        }

        public static AlarmMessage GetMessage(string data)
        {
            AlarmMessage message = null;
            string[] content;

            try
            {
                content = data.Remove(data.Length - 2).Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

                if (content[0] == "5")
                {
                    // content[0] == 5 ==> Alarm
                    // content[0] == 9 ==> Auxiliaries

                    message = new AlarmMessage();
                    message.What = GetWhat(content[1]);

                    if (content.Length == 3)
                    {
                        switch (message.What)
                        {
                            case WHAT.AlarmSilentAlarm:
                            case WHAT.AlarmResetTechnicalAlarm:
                                message.Aux = int.Parse(content[2].Substring(1));
                                break;
                            case WHAT.AlarmNoReception:
                                message.Device = int.Parse(content[2].Substring(1));
                                break;
                            default:
                                message.Zone = int.Parse(content[2].Substring(1));
                                break;
                        }

                        //message.Where = Where.GetWhere(content[2].Substring(1));
                    }
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

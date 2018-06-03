using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
	public enum AlarmWhat
	{
		None,
		AlarmMaintenance,
		AlarmActivation,
		AlarmDisactivation,
		AlarmDelayEnd,
		AlarmBatteryFault,
		AlarmBatteryOK,
		AlarmNetworkFault,
		AlarmNetworkOK,
		AlarmEngage,
		AlarmDisengage,
		AlarmBatteryUnloads,
		AlarmActiveZone,
		AlarmTechnicalAlarm,
		AlarmResetTechnicalAlarm,
		AlarmNoReception,
		AlarmIntrusion,
		AlarmTampering,
		AlarmAntipanic,
		AlarmNonActiveZone,
		AlarmStartProgramming,
		AlarmStopProgramming,
		AlarmSilentAlarm,

		[StringValue("#{0}")] GetZoneStatus,
		[StringValue(null)] GetCentralUnitStatusFromWebServer,
		[StringValue("0")] GetCentralUnitStatusFromCentralUnit,
		[StringValue(null)] GetAuxiliaresStatusFromWebServer
	}

    public class AlarmMessage : BaseMessage
    {
        public AlarmMessage() : base()
        {
            MessageType = MessageType.Command;
            Who = WHO.Alarm;
            What = AlarmWhat.None;
        }

        public AlarmWhat What { get; private set; }

        public int Zone { get; set; }
        public int Aux { get; set; }
        public int Device { get; set; }

		public override string ToString()
		{
			String value = null;

			switch (What)
			{
				case AlarmWhat.GetZoneStatus:
					value = String.Format(GET_STATE, Who.GetStringValue(), String.Format(What.GetStringValue(), Zone));
					break;
				case AlarmWhat.GetCentralUnitStatusFromWebServer:
					value = String.Format(GET_STATE_NO_WHERE, Who.GetStringValue());
					break;
				case AlarmWhat.GetCentralUnitStatusFromCentralUnit:
					value = String.Format(GET_STATE, Who.GetStringValue(), What.GetStringValue());
					break;
				case AlarmWhat.GetAuxiliaresStatusFromWebServer:
					value = String.Format(GET_STATE_NO_WHERE, WHO.Auxiliaries.GetStringValue());
					break;
			}

			return value;
		}
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet.Messages
{
    public enum LightingWhat
    {
        [StringValue(null)] None,

        [StringValue("1")] LightON,
        [StringValue("0")] LightOFF,
        [StringValue("1#{0}")] LightOnAtSpeed,
        [StringValue("0#{0}")] LightOffAtSpeed,
        
        [StringValue(null)] LightLuminousIntensityChange,
        [StringValue(null)] MotionPresenceDetected,
        [StringValue(null)] BrightnessChanged,
        
        [StringValue("30")] DimmerUp,
        [StringValue("31")] DimmerDown,
        [StringValue(null)] DimmerStrenght,
        [StringValue(null)] DimmerNoLoad,

		[StringValue(null)] GetStatus
    }

    public class LightingMessage : BaseMessage
    {
        public LightingMessage() : base()
        {
            this.MessageType = MessageType.Command;
            this.Who = WHO.Lighting;
            this.What = LightingWhat.None;
        }

        public LightingWhat What { get; set; }

        public int Speed { get; set; }
        public int DimmerStrenght { get; set; }
        public int Brightness { get; set; }

        public override String ToString()
        {
            String value = null;

            switch (What)
            {
                case LightingWhat.DimmerDown:
                case LightingWhat.DimmerUp:
                case LightingWhat.LightOFF:
                case LightingWhat.LightON:
                    value = String.Format(CMD_BUS, Who.GetStringValue(), What.GetStringValue(), Where);
                    break;
                case LightingWhat.DimmerStrenght:
                    value = String.Format(CMD_BUS, Who.GetStringValue(), DimmerStrenght / 10, Where);
                    break;
                case LightingWhat.LightOnAtSpeed:
                case LightingWhat.LightOffAtSpeed:
                    value = String.Format(CMD_BUS, Who.GetStringValue(), String.Format(What.GetStringValue(), Speed), Where);
                    break;
				case LightingWhat.GetStatus:
					value = String.Format(GET_STATE, Who.GetStringValue(), Where);
					break;
            }

            return value;
        }
    }
}

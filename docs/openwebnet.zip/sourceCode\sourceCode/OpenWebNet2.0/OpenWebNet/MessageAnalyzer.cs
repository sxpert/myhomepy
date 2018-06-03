using System;
using System.Collections.Generic;
using System.Text;
using OpenWebNet.Messages;

namespace OpenWebNet
{
    public enum WHAT
    {
        None,

        LightON,
        LightOFF,
        LightOnAtSpeed,
        LightOffAtSpeed,
        LightBlinking,
        LightTemporization,
        LightLuminousIntensityChange,

        DimmerUp,
        DimmerDown,
        DimmerStrenght,
        DimmerNoLoad,
        DimmerUpAtSpeed,
        DimmerDownAtSpeed,

        AutomationUp,
        AutomationDown,
        AutomationStop,

        SoundSystemVolumeUp,
        SoundSystemVolumeDown,

        ScenariosON,
        ScenariosOFF,
        ScenariosStartProgramming,
        ScenariosEndProgramming,
        ScenariosEraseAll,
        ScenariosErase,
        ScenariosLockCentralUnit,
        ScenariosUnlockCentralUnit,
        ScenariosCentralUnitUnavailable,
        ScenariosCentralUnitMemoryFull,

        PowerManagementLoadForced,
        PowerManagementLoadEnabled,
        PowerManagementLoadDisabled,
        PowerManagementLoadEndForced,
        PowerManagementAllDimensionsRequest,
        PowerManagementVoltageRequest,
        PowerManagementCurrentRequest,
        PowerManagementPowerRequest,
        PowerManagementEnergyRequest,


        TermoCoolingMode,
        TermoHeatingMode,
        TermoCoolingProtection,
        TermoAntiFreezeProtection,
        TermoProtection,
        TermoHeatingOff,
        TermoCoolingOff,
        TermoOff,
        TermoHeatingManual,
        TermoCoolingManual,
        TermoManual,
        TermoProgrammingHeating,
        TermoProgrammingCooling,
        TermoProgramming,
        TermoHolidaysHeating,
        TermoHolidaysCooling,
        TermoHolidays,
        TermoDimensions,

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

        MultimediaCameraON,
        MultimediaCameraOFF,
        MultimediaAudioVideoOFF,
        MultimediaZoomIn,
        MultimediaZoomOut,
        MultimediaIncreaseLuminosity,
        MultimediaDecreaseLuminosity,
        MultimediaIncreaseContrast,
        MultimediaDecreaseContrast,
        MultimediaIncreaseColor,
        MultimediaDecreaseColor,
        MultimediaIncreaseQuality,
        MultimediaDecreaseQuality,
        MultimediaDisplayDialXY,
        MultimediaIncreaseX,
        MultimediaDecreaseX,
        MultimediaIncreaseY,
        MultimediaDecreaseY,

        TimeRequest,
        DateRequest,
        IpRequest,
        NetmaskRequest,
        MacAddressRequest,
        ModelTypeRequest,
        FirmwareVersionRequest,
        UptimeRequest,
        DateAndTimeRequest,
        KernelVersionRequest,
        DistributionVersionRequest,

        GatewayModel
    }

    public class MessageAnalyzer
    {
        public static BaseMessage GetMessage(string data)
        {
            BaseMessage message;
            string[] parts;
            string content;

            if (string.IsNullOrEmpty(data) || !data.EndsWith("##"))
                return null;

            try
            {
                message = new BaseMessage();

                if (data == OpenWebNetGateway.ACK)
                {
                    message.MessageType = MessageType.ACK;
                }
                else if (data == OpenWebNetGateway.NACK)
                {
                    message.MessageType = MessageType.NACK;
                }
                else if (data == OpenWebNetGateway.NACK_BUSY)
                {
                    message.MessageType = MessageType.NACK_BUSY;
                }
                else if (data == OpenWebNetGateway.NACK_COLL)
                {
                    message.MessageType = MessageType.NACK_COLL;
                }
                else if (data == OpenWebNetGateway.NACK_NOBUS)
                {
                    message.MessageType = MessageType.NACK_NOBUS;
                }
                else if (data == OpenWebNetGateway.NACK_NOP)
                {
                    message.MessageType = MessageType.NACK_NOP;
                }
                else if (data == OpenWebNetGateway.NACK_PROC)
                {
                    message.MessageType = MessageType.NACK_PROC;
                }
                else if (data == OpenWebNetGateway.NACK_RET)
                {
                    message.MessageType = MessageType.NACK_RET;
                }
                else if (data.StartsWith("*#"))
                {
                    // remove *# and ##
                    content = data.Substring(2, data.Length - 4);
                    parts = content.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);
                    message = GetMessageFromWHO((WHO)Enum.Parse(typeof(WHO), parts[0]), data);
                }
                else if (data.StartsWith("*"))
                {
                    // remove *# and ##
                    content = data.Substring(1, data.Length - 3);
                    parts = content.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);
                    message = GetMessageFromWHO((WHO)Enum.Parse(typeof(WHO), parts[0]), data);
                }
                else
                    message = null;

                return message;
            }
            catch (Exception ex)
            {
#if DEBUG
                throw ex;
#endif
                return null;
            }
        }

        private static BaseMessage GetMessageFromWHO(WHO who, string data)
        {
            BaseMessage message = null;

            switch (who)
            {
                case WHO.Alarm:
                    message = Alarm.GetMessage(data);
                    break;
                case WHO.Automation:
                    message = Automation.GetMessage(data);
                    break;
                case WHO.Lighting:
                    message = Lighting.GetMessage(data);
                    break;
                case WHO.Multimedia:
                    message = Multimedia.GetMessage(data);
                    break;
                case WHO.OutsideInterface:
                    message = ExternalInterfaceDevice.GetMessage(data);
                    break;
                case WHO.PowerManagement:
                    message = PowerManagement.GetMessage(data);
                    break;
                case WHO.Scenarios:
                    message = Scenarios.GetMessage(data);
                    break;
            }

            return message;
        }
    }
}

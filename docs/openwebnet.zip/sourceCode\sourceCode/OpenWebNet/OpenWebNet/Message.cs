using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
  public enum MessageType
  {
    /// <summary>
    /// Comando eseguito correttamente
    /// </summary>
    ACK,
    /// <summary>
    /// Comando non eseguito
    /// </summary>
    NACK,
    /// <summary>
    /// Comando non riconosciuto
    /// </summary>
    NACK_NOP,
    /// <summary>
    /// Comando gestito ma il dispositivo non esiste
    /// </summary>
    NACK_RET,
    /// <summary>
    /// Comando non eseguito per collisione sul bus
    /// </summary>
    NACK_COLL,
    /// <summary>
    /// Comando non eseguito per impossibilita' ad accedere al bus
    /// </summary>
    NACK_NOBUS,
    /// <summary>
    /// Comando non eseguito in quanto l'interfaccia e' gia' impegnata in trasmissione
    /// </summary>
    NACK_BUSY,
    /// <summary>
    /// Procedura multiframe non eseguita completemante
    /// </summary>
    NACK_PROC,
    /// <summary>
    /// Comando
    /// </summary>
    Command,
    /// <summary>
    /// Stringa non riconosciuta
    /// </summary>
    None
  }

  public enum WHAT
  {
    None,

    LightON,
    LightOFF,
    LightOnAtSpeed,
    LightOffAtSpeed,
    LightBlinking,
    DimmerUp,
    DimmerDown,
    DimmerStrenght,
    DimmerNoLoad,
    DimmertAtSpeed,

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
    AlarmBatteryOk,
    AlarmNetworkFault,
    AlarmNetworkOk,
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
    DistributionVersionRequest
  }

  public class Message
  {
    private WHO who;
    private WHAT what;
    private MessageType type;
    private string where;
    private string[] parameters;

    public Message()
    {
      who = WHO.None;
      what = WHAT.None;
      type = MessageType.None;
      where = string.Empty;
      parameters = null;
    }

    public WHO Who
    {
      get
      {
        return who;
      }

      set
      {
        who = value;
      }
    }

    public WHAT What
    {
      get
      {
        return what;
      }

      set
      {
        what = value;
      }
    }

    public string Where
    {
      get
      {
        return where;
      }

      set
      {
        where = value;
      }
    }

    public MessageType MessageType
    {
      get
      {
        return type;
      }

      set
      {
        type = value;
      }
    }

    public string[] Parameters
    {
      get
      {
        return parameters;
      }

      set
      {
        parameters = value;
      }
    }

    public override string ToString()
    {
      return string.Format("{0} - {1} - {2} - {3}", MessageType, Who.ToString(), What.ToString(), where);
    }
  }

  public class MessageAnalyzer
  {
    public static Message GetMessage(string data)
    {
      Message message;
      string[] parts;
      string[] parameters;

      if (string.IsNullOrEmpty(data) || !data.EndsWith("##"))
        return null;

      try
      {
        message = new Message();

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
        else if (data.StartsWith("*#")) //indica un frame "Grandezze"
        {
          message.MessageType = MessageType.Command;

          string content = data.Substring(2, data.Length - 2);
          content = content.Remove(content.Length - 2);

          parts = content.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

          message.Who = (WHO)Enum.Parse(typeof(WHO), parts[0]);
          if (message.Who == WHO.Heating)
          {
            message.What = WHAT.TermoDimensions;
            message.Where = parts[1];
            message.Parameters = new string[parts.Length - 2];
            Array.ConstrainedCopy(parts, 2, message.Parameters, 0, parts.Length - 2);
          }
          else
          {
            message = null;
          }
        }
        else if (data.StartsWith("*"))
        {
          message.MessageType = MessageType.Command;

          parts = data.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

          if (parts.Length == 3)
          {
            message.Who = (WHO)Enum.Parse(typeof(WHO), parts[0]);
            message.What = GetWhat(parts[1], message.Who, out parameters);
            message.Where = parts[2].Substring(0, parts[2].Length - 2);
            message.Parameters = parameters;
          }
          else if (parts.Length == 2)
          {
            message.Who = (WHO)Enum.Parse(typeof(WHO), parts[0]);
            message.What = GetWhat(parts[1], message.Who, out parameters);
            message.Where = string.Empty;
            message.Parameters = parameters;
          }
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
    #region GetWhat

    private static WHAT GetWhat(string what, WHO who, out string[] parameters)
    {
      WHAT retWhat;

      retWhat = WHAT.None;
      parameters = null;

      switch (who)
      {
        case WHO.Lighting:
          retWhat = GetLightingWhat(what, out parameters);
          break;
        case WHO.Automation:
          retWhat = GetAutomationWhat(what, out parameters);
          break;
        case WHO.Scenarios:
          retWhat = GetScenariosWhat(what, out parameters);
          break;
        case WHO.PowerManagement:
          retWhat = GetPowerManagementWhat(what, out parameters);
          break;
        case WHO.Heating:
          retWhat = GetHeatingWhat(what, out parameters);
          break;
        case WHO.Alarm:
          retWhat = GetAlarmWhat(what, out parameters);
          break;
        case WHO.SoundSystem:
          retWhat = GetSoundSystemWhat(what, out parameters);
          break;
        case WHO.OutsideInterface:
          retWhat = GetOutsideInterfaceWhat(what, out parameters);
          break;
      }

      return retWhat;
    }


    private static WHAT GetLightingWhat(string what, out string[] parameters)
    {
      int value;
      string[] parts;
      WHAT retWhat;

      retWhat = WHAT.None;
      parameters = null;

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
          parameters = new string[] { value.ToString() };
        }
        else if (value >= 20 && value <= 29)
        {
          retWhat = WHAT.LightBlinking;
          parameters = new string[] { value.ToString() };
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
      else
      {
        // x#level#speed or x#speed

        parts = what.Split(new char[] { '#' }, StringSplitOptions.RemoveEmptyEntries);

        if (parts.Length == 3)
        {
          retWhat = WHAT.DimmertAtSpeed;
          parameters = new string[] { parts[0], parts[1] };
        }
        else if (parts.Length == 2)
        {
          if (int.TryParse(parts[0], out value))
          {
            retWhat = value == 0 ? WHAT.LightOffAtSpeed : WHAT.LightOnAtSpeed;
            parameters = new string[] { parts[1] };
          }
        }
      }

      return retWhat;
    }

    private static WHAT GetAutomationWhat(string what, out string[] parameters)
    {
      WHAT retWhat;
      int value;

      retWhat = WHAT.None;
      parameters = null;

      if (int.TryParse(what, out value))
      {
        if (value == 0)
        {
          retWhat = WHAT.AutomationStop;
        }
        else if (value == 1)
        {
          retWhat = WHAT.AutomationUp;
        }
        else if (value == 2)
        {
          retWhat = WHAT.AutomationDown;
        }
      }

      return retWhat;
    }

    private static WHAT GetScenariosWhat(string what, out string[] parameters)
    {
      WHAT retWhat;
      int value;
      string[] parts;

      retWhat = WHAT.None;
      parameters = null;

      if (int.TryParse(what, out value))
      {
        if (value >= 1 && value <= 32)
        {
          retWhat = WHAT.ScenariosON;
          parameters = new string[] { value.ToString() };
        }
        else if (value == 42)
        {
          retWhat = WHAT.ScenariosEraseAll;
        }
        else if (value == 43)
        {
          retWhat = WHAT.ScenariosLockCentralUnit;
        }
        else if (value == 44)
        {
          retWhat = WHAT.ScenariosUnlockCentralUnit;
        }
        else if (value == 45)
        {
          retWhat = WHAT.ScenariosCentralUnitUnavailable;
        }
        else if (value == 46)
        {
          retWhat = WHAT.ScenariosCentralUnitMemoryFull;
        }
      }
      else
      {
        // scenario#0 or x#scenario

        parts = what.Split(new char[] { '#' }, StringSplitOptions.RemoveEmptyEntries);

        if (parts.Length == 2)
        {
          if (int.TryParse(parts[0], out value))
          {
            if (value >= 1 && value <= 32)
            {
              // scenario#0

              retWhat = WHAT.ScenariosOFF;
              parameters = new string[] { value.ToString() };
            }
            else if (value == 40)
            {
              retWhat = WHAT.ScenariosStartProgramming;
              parameters = new string[] { parts[1] };
            }
            else if (value == 41)
            {
              retWhat = WHAT.ScenariosEndProgramming;
              parameters = new string[] { parts[1] };
            }
            else if (value == 42)
            {
              retWhat = WHAT.ScenariosErase;
              parameters = new string[] { parts[1] };
            }
          }
        }
      }

      return retWhat;
    }

    private static WHAT GetSoundSystemWhat(string what, out string[] parameters)
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

    private static WHAT GetHeatingWhat(string what, out string[] parameters)
    {
      WHAT retWhat = WHAT.None;
      int value;

      parameters = null;
      if (int.TryParse(what, out value))
      {

        switch (value)
        {
          case 0:
            retWhat = WHAT.TermoCoolingMode;
            break;
          case 1:
            retWhat = WHAT.TermoHeatingMode;
            break;
          case 102:
            retWhat = WHAT.TermoAntiFreezeProtection;
            break;
          case 202:
            retWhat = WHAT.TermoCoolingProtection;
            break;
          case 302:
            retWhat = WHAT.TermoProtection;
            break;
          case 103:
            retWhat = WHAT.TermoHeatingOff;
            break;
          case 203:
            retWhat = WHAT.TermoCoolingOff;
            break;
          case 303:
            retWhat = WHAT.TermoOff;
            break;
          case 110:
            retWhat = WHAT.TermoHeatingManual;
            break;
          case 210:
            retWhat = WHAT.TermoCoolingManual;
            break;
          case 310:
            retWhat = WHAT.TermoManual;
            break;
          case 111:
            retWhat = WHAT.TermoProgrammingHeating;
            break;
          case 211:
            retWhat = WHAT.TermoProgrammingCooling;
            break;
          case 311:
            retWhat = WHAT.TermoProgramming;
            break;
        }
      }
      return retWhat;
    }

    private static WHAT GetAlarmWhat(string what, out string[] parameters)
    {
      int value;
      WHAT retWhat = WHAT.None;
      parameters = null;

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
          retWhat = WHAT.AlarmBatteryOk;
        else if (value == 6)
          retWhat = WHAT.AlarmNetworkFault;
        else if (value == 7)
          retWhat = WHAT.AlarmNetworkOk;
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

    private static WHAT GetPowerManagementWhat(string what, out string[] parameters)
    {
      WHAT retWhat;
      int value;

      retWhat = WHAT.None;
      parameters = null;

      if (int.TryParse(what, out value))
      {
        if (value == 0)
        {
          retWhat = WHAT.PowerManagementLoadDisabled;
        }
        else if (value == 1)
        {
          retWhat = WHAT.PowerManagementLoadEnabled;
        }
        else if (value == 2)
        {
          retWhat = WHAT.PowerManagementLoadForced;
        }
        else if (value == 3)
        {
          retWhat = WHAT.PowerManagementLoadEndForced;
        }
      }

      return retWhat;
    }

    private static WHAT GetMultimediaWhat(string what, out string[] parameters)
    {
      WHAT retWhat;
      int value;

      retWhat = WHAT.None;
      parameters = null;

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

    private static WHAT GetOutsideInterfaceWhat(string what, out string[] parameters)
    {
      WHAT retWhat;
      int value;

      retWhat = WHAT.None;
      parameters = null;

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

    #endregion
  }

  /*public class ComposeMessage
  {
      public EventHandler<OpenWebNetDataEventArgs> MessageComposed;

      private string bufferString;

      public ComposeMessage()
      {
          bufferString = string.Empty;
      }

      public void AddData(string data)
      {
          int index;
          string message;

          data = data.Trim();

          if ((index = data.IndexOf(OpenWebNet.MSG_END)) < 0)
          {
              // non ho un messaggio completo

              if (bufferString == string.Empty)
              {
                  bufferString = data;
                  return;

              }
              else
              {
                  bufferString += data;
              }
          }
          else
          {
              while ((index = data.IndexOf(OpenWebNet.MSG_END)) >= 0)
              {
                  message = data.Substring(0, index + OpenWebNet.MSG_END.Length);
                  data = data.Remove(0, index + OpenWebNet.MSG_END.Length);

                  if (bufferString == string.Empty)
                      bufferString = message;
                  else
                      bufferString += message;

                  if (MessageComposed != null)
                      MessageComposed(this, new OpenWebNetDataEventArgs(bufferString));

                  bufferString = string.Empty;
              }

              if (data != "")
                  bufferString = data;
          }
      }
  }*/
}


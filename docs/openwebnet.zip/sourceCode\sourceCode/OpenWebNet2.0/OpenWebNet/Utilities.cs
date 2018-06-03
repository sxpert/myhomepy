namespace OpenWebNet
{
    #region Using

    using System;
    using System.Collections.Generic;
    using System.Xml.Linq;
    using System.Reflection;

    #endregion

    public enum GatewayModel
    {
        MHServer = 2,
        MH200 = 4,
        F452 = 6,
        F452AV = 7,
        MHServer2 = 11,
        F453AV = 12,
        HL4684 = 13,
        L4686SDK = 27,
        BMNE500 = 35,
        Unknown
    }

    public static class Utilities
    {
        private static Dictionary<Enum, StringValueAttribute> _values;

        static Utilities()
        {
            _values = new Dictionary<Enum, StringValueAttribute>();
        }

        #region Extension Methods

        public static String GetStringValue(this Enum value)
        {
            String output = null;
            Type type = value.GetType();

            //Check first in our cached results...

            if (_values.ContainsKey(value))
            {
                output = _values[value].Value;
            }
            else
            {
                //Look for our 'StringValueAttribute' 
                //in the field's custom attributes

                FieldInfo fi = type.GetField(value.ToString());
                StringValueAttribute[] attrs = fi.GetCustomAttributes(typeof(StringValueAttribute), false) as StringValueAttribute[];
                
                if (attrs.Length > 0)
                {
                    _values.Add(value, attrs[0]);
                    output = attrs[0].Value;
                }
            }

            return output;
        }


        public static void IsBetween(this int value, int v1, int v2)
        {
            IsBetween(value, v1, v2, string.Format("Value must be between {0} and {1}", v1, v2));
        }

        public static void IsBetween(this int value, int v1, int v2, string errorMessage)
        {
            if (value < v1 || value > v2)
                throw new ArgumentOutOfRangeException(errorMessage);
        }

        #endregion

        #region Public Methods

        #region PowerManagement Methods

        /// <summary>
        /// Estrae le varie grandezze ritornate dal metodo GestioneEnergiaStatoGrandezze secondo quest'ordine: T, C, P, E
        /// </summary>
        /// <param name="data">Comando ritornato da GestioneEnergiaStatoGrandezze</param>
        /// <returns>Array con i valori estratti</returns>
        public static string[] GetPowerManagementValues(string data)
        {
            // *#3*10*0*T*C*P*E##

            string[] values;

            if (string.IsNullOrEmpty(data) || !data.StartsWith("*#3*10*0*"))
                return null;

            values = data.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

            if (values.Length < 7)
                return null;

            return new string[] { values[3], values[4], values[5], values[6].Substring(0, values[6].Length - 2) };
        }

        /// <summary>
        /// Estrae la tensione ritornata dal metodo GestioneEnergiaStatoTensione
        /// </summary>
        /// <param name="data">Comando ritornato da GestioneEnergiaStatoTensione</param>
        /// <returns>Valore della tensione</returns>
        public static string GetTension(string data)
        {
            if (string.IsNullOrEmpty(data) || !data.StartsWith("*#3*10*1*"))
                return null;

            return GetPowerManagementValue(data);
        }

        /// <summary>
        /// Estrae la corrente ritornata dal metodo GestioneEnergiaStatoCorrente
        /// </summary>
        /// <param name="data">Comando ritornato da GestioneEnergiaStatoCorrente</param>
        /// <returns>Valore della corrente</returns>
        public static string GetCurrent(string data)
        {
            if (string.IsNullOrEmpty(data) || !data.StartsWith("*#3*10*2*"))
                return null;

            return GetPowerManagementValue(data);
        }

        /// <summary>
        /// Estrae la potenza ritornata dal metodo GestioneEnergiaStatoPotenza
        /// </summary>
        /// <param name="data">Comando ritornato da GestioneEnergiaStatoPotenza</param>
        /// <returns>Valore della potenza</returns>
        public static string GetPower(string data)
        {
            if (string.IsNullOrEmpty(data) || !data.StartsWith("*#3*10*3*"))
                return null;

            return GetPowerManagementValue(data);
        }

        /// <summary>
        /// Estrae l'energia ritornata dal metodo GestioneEnergiaStatoEnergia
        /// </summary>
        /// <param name="data">Comando ritornato da GestioneEnergiaStatoEnergia</param>
        /// <returns>Valore dell'energia</returns>
        public static string GetEnergy(string data)
        {
            if (string.IsNullOrEmpty(data) || !data.StartsWith("*#3*10*4*"))
                return null;

            return GetPowerManagementValue(data);
        }

        #endregion

        #region Temperature Method

        public static double GetTemperature(string data)
        {
            double temp = 0;

            //*#4*dove*0*T##
            // c1c2c3c4 0000 0500 (50 gradi)
            // c1 = 0 temp > 0
            // c2c3 temperature
            // c4 decimale

            if (data.Length < 4)
                return double.NaN;

            temp = double.Parse(data.Substring(1, 2));

            if (data[0] != '0')
                temp = -temp;

            temp += double.Parse("0." + data[3].ToString());

            return temp;
        }

        #endregion

        public static bool IsNACK(string msg)
        {
            if (string.IsNullOrEmpty(msg))
                return false;

            return (msg == OpenWebNetGateway.NACK || msg == OpenWebNetGateway.NACK_BUSY ||
                msg == OpenWebNetGateway.NACK_COLL || msg == OpenWebNetGateway.NACK_NOBUS ||
                msg == OpenWebNetGateway.NACK_NOP || msg == OpenWebNetGateway.NACK_PROC ||
                msg == OpenWebNetGateway.NACK_RET);
        }

        public static bool CouldeBeAPasswordSequence(string sequence)
        {
            if (string.IsNullOrEmpty(sequence))
                return false;

            if (sequence.IndexOf("*#") == -1 || sequence.IndexOf(OpenWebNetGateway.MSG_END) == -1)
                return false;

            // This's a password sequence *#408377968##

            foreach (char c in sequence.Substring(2, sequence.Length - 4))
            {
                if (!char.IsDigit(c))
                    return false;
            }

            return true;
        }

        /// <summary>
        /// Try to get the Gateway's mode
        /// You could use it after a RequestGatewayModel call
        /// </summary>
        /// <param name="num">The N parameter of this message: *#13**15*N## </param>
        /// <returns>The gateway's model</returns>
        public static GatewayModel GetGatewayModel(string num)
        {
            return (GatewayModel)Enum.Parse(typeof(GatewayModel), num);
        }

        public static void DiscoverDevices()
        {
            // *#1001*WHERE*1##
            // *#1001*WHERE*7##
        }

        public static void IdentifyDeviceFromCode(string code)
        {
            // *#1001*11*1*129*5*0*0##
        }

        #endregion

        #region Internal Methods

        internal static string PadWhere(string dove)
        {
            return (dove.Length == 1 ? "0" + dove : dove);
        }

        #endregion

        #region Private Methods

        private static string GetPowerManagementValue(string data)
        {
            string[] values;

            values = data.Split(new char[] { '*' }, StringSplitOptions.RemoveEmptyEntries);

            if (values.Length < 4)
                return null;

            return values[3].Substring(0, values[3].Length - 2);
        }

        #endregion
    }

    //public static class Int32EnsureExtension
    //{
    //    public static Ensure<Int32> IsBetween(this Ensure<Int32> validator, int v1, int v2)
    //    {
    //        validator.ThrowIfTrue(v => v < v1 || v > v2);

    //        return validator;
    //    }
    //}
}

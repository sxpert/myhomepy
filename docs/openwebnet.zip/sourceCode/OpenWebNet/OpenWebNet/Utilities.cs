using System;
using System.Collections.Generic;
using System.Text;

namespace OpenWebNet
{
    public static class Utilities
    {
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

        public static bool IsPasswordSequence(string sequence)
        {
            if (string.IsNullOrEmpty(sequence))
                return false;

            // sistemare
            return false;
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
}

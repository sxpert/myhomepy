using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace MyHomeShortcut
{
    public class Utilities
    {
        public static string NumberToString(Keys num)
        {
            string keythree;

            switch (num)
            {
                case (Keys.D0):
                    keythree = "0";
                    break;
                case (Keys.D1):
                    keythree = "1";
                    break;
                case (Keys.D2):
                    keythree = "2";
                    break;
                case (Keys.D3):
                    keythree = "3";
                    break;
                case (Keys.D4):
                    keythree = "4";
                    break;
                case (Keys.D5):
                    keythree = "5";
                    break;
                case (Keys.D6):
                    keythree = "6";
                    break;
                case (Keys.D7):
                    keythree = "7";
                    break;
                case (Keys.D8):
                    keythree = "8";
                    break;
                case (Keys.D9):
                    keythree = "9";
                    break;
                default:
                    keythree = "";
                    break;
            }

            return keythree;
        }

        public static Keys NumberToKey(string num)
        {
            Keys keythree;

            switch (num)
            {
                case "0":
                    keythree = Keys.D0;
                    break;
                case "1":
                    keythree = Keys.D1;
                    break;
                case "2":
                    keythree = Keys.D2;
                    break;
                case "3":
                    keythree = Keys.D3;
                    break;
                case "4":
                    keythree = Keys.D4;
                    break;
                case "5":
                    keythree = Keys.D5;
                    break;
                case "6":
                    keythree = Keys.D6;
                    break;
                case "7":
                    keythree = Keys.D7;
                    break;
                case "8":
                    keythree = Keys.D8;
                    break;
                case "9":
                    keythree = Keys.D9;
                    break;
                default:
                    keythree = Keys.None;
                    break;
            }

            return keythree;
        }
    }
}

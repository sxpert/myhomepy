using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenWebNet
{
    // We've to manage the Alarm and Sound System where
    // A kind of Sound System where is: #6 (Room 6 Amplifier) or 101 (Source 1)

    public enum Bus
    {
        PrivateRiserBus = 3,
        LocalBus = 4
    }

    public class Where
    {
        public Where(int group)
            : this(0, 0, 0, Bus.LocalBus, group)
        {
        }

        public Where(int a, int pl)
            : this(a, pl, 0, Bus.LocalBus, 0)
        {
        }

        public Where(int a, int pl, int i, Bus liv, int g)
        {
            if (a == 0)
                this.IsGeneral = true;

            this.A = a;
            this.PL = pl;
            this.I = i;
            this.Liv = liv;
            this.G = g;
        }

        public int A { get; internal set; }
        public int PL { get; internal set; }
        public int I { get; internal set; }
        public Bus Liv { get; internal set; }
        public int G { get; internal set; }
        public bool IsGeneral { get; internal set; }

        public override string ToString()
        {
            return string.Format("{0}{1} - {2}", A, PL, I);
        }

        private void CheckIntervalValue(int value, string message)
        {
            if (value < 0 || value > 9)
                throw new ArgumentOutOfRangeException(message);
        }

        public static Where GetWhere(string data)
        {
            Where where = null;
            string[] content;
            int value;

            if (string.IsNullOrEmpty(data))
                return null;

            try
            {
                if (int.TryParse(data, out value) && (value >= 4000 && value <= 4003) || value == 5000)
                {
                    // Multimedia where
                    where = new Where(0, value);
                }
                else
                {
                    content = data.Split(new char[] { '#' }, StringSplitOptions.RemoveEmptyEntries);

                    if (content.Length == 3)
                    {
                        // APL#LIV#INT or #G#LIV#INT

                        if (data.StartsWith("#"))
                        {
                            // It's a group command
                            where = new Where(0, 0, int.Parse(content[2]), (Bus)Enum.Parse(typeof(Bus), content[1]),
                                int.Parse(content[0]));

                        }
                        else
                        {
                            if (content[0].Length == 1)
                            {
                                // only A
                                where = new Where(int.Parse(content[0][0].ToString()), 0, int.Parse(content[2]),
                                    (Bus)Enum.Parse(typeof(Bus), content[1]), 0);
                            }
                            else
                            {
                                // A and PL

                                where = new Where(int.Parse(content[0][0].ToString()), int.Parse(content[0][1].ToString()),
                                    int.Parse(content[2]), (Bus)Enum.Parse(typeof(Bus), content[1]), 0);
                            }
                        }
                    }
                    else
                    {
                        if (data.StartsWith("#"))
                        {
                            // It's a group command
                            where = new Where(int.Parse(data.Substring(1)));
                        }
                        else
                        {
                            if (data.Length == 1)
                            {
                                // only A
                                where = new Where(int.Parse(data), 0);
                            }
                            else
                            {
                                // A and PL
                                where = new Where(int.Parse(data[0].ToString()), int.Parse(data[1].ToString()));
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                return null;
            }

            return where;
        }
    }
}

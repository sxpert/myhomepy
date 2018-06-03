using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Xml.Linq;
using OpenWebNet;

namespace MyHomeShortcut
{
    public class Shortcut
    {
        /* <MyHomeShortcuts>
         *  <Shortcut name="" keyone="" keytwo="" keythree="">
         *      <Actions>
         *          <Action who="" where="" what="" command="" />
         *      </Actions>
         *  </Shortcut>
         * </MyHomeShortcuts>
         */

        public string Name { get; set; }
        public Keys KeyOne { get; set; }
        public Keys KeyTwo { get; set; }
        public Keys KeyThree { get; set; }

        public List<Action> Actions { get; set; }

        public Shortcut()
        {
            this.KeyOne = Keys.None;
            this.KeyTwo = Keys.None;
            this.KeyThree = Keys.None;
            this.Actions = null;
        }

        public override string ToString()
        {
            /*string keythree;

            switch (KeyThree)
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
            }*/

            return string.Format("{0} -> {1} + {2} + {3}", Name, KeyOne, KeyTwo, Utilities.NumberToString(KeyThree));
        }

        public static List<Shortcut> Read(string filename)
        {
            if (string.IsNullOrEmpty(filename))
                throw new ArgumentNullException("filename");

            if (!File.Exists(filename))
                throw new FileNotFoundException(filename);

            XDocument doc = XDocument.Load(filename);

            return (from s in doc.Root.Elements("Shortcut")
                    select new Shortcut()
                    {
                        Name = s.Attribute("name").Value,
                        KeyOne = (Keys)Enum.Parse(typeof(Keys), s.Attribute("keyone").Value),
                        KeyTwo = (Keys)Enum.Parse(typeof(Keys), s.Attribute("keytwo").Value),
                        KeyThree = (Keys)Enum.Parse(typeof(Keys), s.Attribute("keythree").Value),
                        Actions = (from a in s.Element("Actions").Elements()
                                  select new Action()
                                  {
                                      Who = (WHO)Enum.Parse(typeof(WHO), a.Attribute("who").Value),
                                      What = (WHAT)Enum.Parse(typeof(WHAT), a.Attribute("what").Value),
                                      Where = a.Attribute("where").Value,
                                      Command = a.Attribute("command").Value,
                                      Toggle = bool.Parse(a.Attribute("toggle").Value)
                                  }).ToList<Action>()
                    }).ToList<Shortcut>();
        }

        public static void Save(List<Shortcut> shortcuts, string filename)
        {
            XElement doc;

            doc = new XElement("Shortcuts",from s in shortcuts
                                select new XElement("Shortcut",
                                    new XAttribute("name", s.Name),
                                    new XAttribute("keyone", s.KeyOne),
                                    new XAttribute("keytwo", s.KeyTwo),
                                    new XAttribute("keythree", s.KeyThree),

                                    new XElement("Actions",
                                        from a in s.Actions
                                        select new XElement("Action",
                                            new XAttribute("who", a.Who),
                                            new XAttribute("what", a.What),
                                            new XAttribute("where", a.Where),
                                            new XAttribute("toggle", a.Toggle),
                                            new XAttribute("command", a.Command)))));

            doc.Save(filename);
        }
    }
}

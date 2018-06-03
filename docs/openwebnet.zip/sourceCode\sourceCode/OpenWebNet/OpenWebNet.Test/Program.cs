using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Text;
using OpenWebNet;

namespace OpenWebNet.Test
{
    class Program
    {
        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainFrm());

            /*string[] ports = UsbGateway.GetPorts();

            Console.WriteLine("Porte disponibili...");

            foreach (string port in ports)
                Console.WriteLine(port);

            if (ports.Length == 0)
                return;

            Console.WriteLine();
            Console.WriteLine("Uso COM3...");

            UsbGateway gateway = new UsbGateway("COM3");
            gateway.Connect();

            Console.WriteLine("Accendo luce PL = 1...");
            gateway.LuceON("11");

            Console.ReadLine();

            Console.WriteLine("Spengo luce PL = 1...");
            gateway.LuceOFF("11");

            Console.ReadLine();

            Console.WriteLine("Ripengo luce PL = 1...");
            gateway.LuceOFF("11");

            Console.ReadLine();

            Console.WriteLine("Accendo luce A = 1...");
            gateway.LuceON("1");

            Console.ReadLine();

            Console.WriteLine("Spengo luce A = 1...");
            gateway.LuceOFF("1");

            Console.ReadLine();

            Console.WriteLine("Automatismo su PL = 22...");
            gateway.PuntoAutomazioneSU("2");

            Console.ReadLine();

            Console.WriteLine("Automatismo giu PL = 22...");
            gateway.PuntoAutomazioneGIU("22");

            Console.ReadLine();

            Console.WriteLine("Automatismo stop PL = 22...");
            gateway.PuntoAutomazioneSU("22");

            Console.ReadLine();

            Console.WriteLine("Automatismo su PL = 22...");
            gateway.PuntoAutomazioneSU("2");

            Console.ReadLine();

            Console.WriteLine("Livello su PL = 11");
            gateway.LuceON("11");

            gateway.LuceLivelloSU("11");
            gateway.LuceLivelloSU("11");
            gateway.LuceLivelloSU("11");
            gateway.LuceLivelloSU("11");

            Console.ReadLine();*/
        }
    }
}

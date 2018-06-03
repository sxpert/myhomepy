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
        }
    }
}

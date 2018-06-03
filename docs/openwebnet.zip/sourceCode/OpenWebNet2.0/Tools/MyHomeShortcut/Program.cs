using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using System.Threading;
using System.Net.Sockets;
using System.Runtime.InteropServices;

namespace MyHomeShortcut
{
    static class Program
    {
        private static MainFrm mainFrm;
        private static readonly InterceptKeys.LowLevelKeyboardProc _proc = HookCallback;
        private static IntPtr _hookID = IntPtr.Zero;

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            try
            {
                _hookID = InterceptKeys.SetHook(_proc);
            }
            catch
            {
                if (_hookID != IntPtr.Zero)
                    InterceptKeys.UnhookWindowsHookEx(_hookID);
            }


            AppDomain.CurrentDomain.UnhandledException += new UnhandledExceptionEventHandler(CurrentDomain_UnhandledException);
            Application.SetUnhandledExceptionMode(UnhandledExceptionMode.CatchException);
            Application.ThreadException += new ThreadExceptionEventHandler(Application_ThreadException);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            mainFrm = new MainFrm();
            
            Application.Run(mainFrm);

            InterceptKeys.UnhookWindowsHookEx(_hookID);
        }

        public static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam)
        {
            if (nCode >= 0)
            {
                bool alt = (Control.ModifierKeys & Keys.Alt) != 0;
                bool ctrl = (Control.ModifierKeys & Keys.Control) != 0;
                bool shift = (Control.ModifierKeys & Keys.Shift) != 0;

                int vkCode = Marshal.ReadInt32(lParam);
                Keys key = (Keys)vkCode;

                mainFrm.ProcessShortcut(key, ctrl, alt, shift);
            }

            return InterceptKeys.CallNextHookEx(_hookID, nCode, wParam, lParam);
        }

        private static void CurrentDomain_UnhandledException(object sender, UnhandledExceptionEventArgs e)
        {
            SocketException socketEx;

            socketEx = e.ExceptionObject as SocketException;

            if (socketEx == null)
            {
                MessageBox.Show("Error: " + e.ExceptionObject, "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            if (socketEx.SocketErrorCode == SocketError.ConnectionRefused)
            {
                MessageBox.Show("The server has refused the connection...Check either IP/Port or the range", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private static void Application_ThreadException(object sender, ThreadExceptionEventArgs e)
        {
            MessageBox.Show("Error: " + e.Exception.ToString(), "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}

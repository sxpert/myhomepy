using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using OpenWebNet;
using log4net;

namespace MyEnergy
{
    public partial class MainWindow : Window
    {
        private delegate void UpdateUIDelegate(string[] values);

        private WindowState windowState;
        private DispatcherTimer timer;
        private EthGateway server;
        private UpdateUIDelegate updateUI;

        public MainWindow()
        {
            InitializeComponent();

            timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromSeconds(3);
            timer.Tick += new EventHandler(timer_Tick);

            updateUI = new UpdateUIDelegate(UpdateUI);

            App.logger = LogManager.GetLogger(typeof(MainWindow));
        }

        private void notifyIcon_Click(object sender, EventArgs e)
        {
            Show();

            WindowState = windowState;
        }

        private void timer_Tick(object sender, EventArgs e)
        {
            // send command to retrieve data
            server.PowerManagementGetAllDimensions();

            App.logger.Debug("Call PowerManagementGetAllDimensions");
        }

        private void server_MessageReceived(object sender, OpenWebNetDataEventArgs e)
        {
            string[] values;

            if (string.IsNullOrEmpty(e.Data))
                return;

            App.logger.Debug(string.Format("Received: {0}", e.Data)); 

            values = Utilities.GetPowerManagementValues(e.Data);

            if (values == null || values.Length < 4)
            {
                App.logger.Debug("Parsing...no values");
                return;
            }

            this.Dispatcher.Invoke(updateUI, DispatcherPriority.Normal, (object)values);
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
        }

        /*private void Window_StateChanged(object sender, EventArgs e)
        {
            if (WindowState == WindowState.Minimized)
            {
                Hide();

                if (notifyIcon != null)
                    notifyIcon.ShowBalloonTip(2000);
            }
            else
                windowState = WindowState;
        }

        private void Window_IsVisibleChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            if (notifyIcon != null)
                notifyIcon.Visible = !IsVisible;
        }*/

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            LoadConfig(false);
        }

        private void start_MouseDown(object sender, MouseButtonEventArgs e)
        {
            server.Connect();

            App.logger.Debug(string.Format("Connecting...{0}:{1}", server.Host, server.Port));
        }

        private void settings_MouseDown(object sender, MouseButtonEventArgs e)
        {
            LoadConfig(true);
        }

        private void LoadConfig(bool load)
        {
            OptionsWindow optWin;

            if (Properties.Settings.Default.IsFirstTime || load)
            {
                optWin = new OptionsWindow();

                optWin.IP = Properties.Settings.Default.Ip;
                optWin.Port = Properties.Settings.Default.Port;

                if (!(bool)optWin.ShowDialog())
                    return;

                Properties.Settings.Default.Ip = optWin.IP;
                Properties.Settings.Default.Port = optWin.Port;

                Properties.Settings.Default.IsFirstTime = false;
                Properties.Settings.Default.Save();
            }

            if (server != null)
            {
                server.MessageReceived -= new EventHandler<OpenWebNetDataEventArgs>(server_MessageReceived);
                server = null;
            }

            server = new EthGateway(Properties.Settings.Default.Ip, Properties.Settings.Default.Port, OpenSocketType.Command);
            server.MessageReceived += new EventHandler<OpenWebNetDataEventArgs>(server_MessageReceived);
            server.Connected += new EventHandler(server_Connected);
        }

        private void UpdateUI(string[] values)
        {
            tensionLbl.Content = values[0];
            currentLbl.Content = values[1];
            powerLbl.Content = values[2];
            energyLbl.Content = values[3];
        }

        private void server_Connected(object sender, EventArgs e)
        {
            timer.Start();
            App.logger.Debug("Connected...");
        }
    }
}

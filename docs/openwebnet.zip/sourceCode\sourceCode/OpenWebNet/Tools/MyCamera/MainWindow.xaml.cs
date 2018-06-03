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
using System.IO;
using System.Net;
using OpenWebNet;

namespace MyCamera
{
    public partial class MainWindow : Window
    {
        private WebServer server;
        private DispatcherTimer timer;
        private DispatcherTimer setCameraTimer;
        private string whereCamera;

        public MainWindow()
        {
            InitializeComponent();

            timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromSeconds(0.5);
            timer.Tick += new EventHandler(timer_Tick);

            setCameraTimer = new DispatcherTimer();
            setCameraTimer.Interval = TimeSpan.FromSeconds(40);
            setCameraTimer.Tick += new EventHandler(setCameraTimer_Tick);
        }

        private void setCameraTimer_Tick(object sender, EventArgs e)
        {
            //try
            //{
                server.MultimediaCameraON(whereCamera);
            /*}
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);

                throw ex;
            }*/
        }

        private void timer_Tick(object sender, EventArgs e)
        {
            cameraImage.Source = GetImage();
        }

        private void brightnessPlusBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaIncreasesLuminosity();
        }

        private void brightnessMinBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaDecreasesLuminosity();
        }

        private void qualityPlusBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaIncreasesQuality();
        }

        private void qualityMinBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaDecreasesQuality();
        }

        private void colorPlusBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaIncreasesColour();
        }

        private void colorMinBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaDecreasesColour();
        }

        private void contrastMinBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaDecreasesContrast();
        }

        private void contrastPlusBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaIncreasesContrast();
        }

        private void zoomMinBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaZoomOut();
        }

        private void zoomPlusBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
                return;

            server.MultimediaZoomIn();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            if (!Properties.Settings.Default.IsFirstTime)
                return;

            ShowOptions();
        }

        private ImageSource GetImage()
        {
            try
            {
                JpegBitmapDecoder decoder;
                Stream stream;
                WebResponse resp;
                HttpWebRequest req;

                req = (HttpWebRequest)WebRequest.Create(string.Format("http://{0}/telecamera.php", server.Host));
                req.Timeout = 10000;

                // get response

                resp = req.GetResponse();
                stream = resp.GetResponseStream();

                decoder = new JpegBitmapDecoder(stream, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.Default);

                return decoder.Frames[0];
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);

                throw ex;
            }

            return null;
        }

        private void changeBtn_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                whereCamera = whereCameraTxt.Text;

                server.MultimediaCameraON(whereCamera);

                setCameraTimer.Start();
                timer.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);

                throw ex;
            }
        }

        private void optionsBtn_Click(object sender, RoutedEventArgs e)
        {
            ShowOptions();
        }

        private void connectBtn_Click(object sender, RoutedEventArgs e)
        {
            if (server == null)
            {
                server = new WebServer(Properties.Settings.Default.IP, Properties.Settings.Default.Port, OpenSocketType.Command);
                server.Connected += new EventHandler(server_Connected);
                server.Connect();
            }
        }

        private void server_Connected(object sender, EventArgs e)
        {
            Dispatcher.Invoke(new Action<bool>(UpdateChangeBtn), true);
        }
        
        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (server == null)
                return;

            server.Disconnect();
            server = null;
        }

        private void UpdateChangeBtn(bool value)
        {
            changeBtn.IsEnabled = value;
        }

        private void ShowOptions()
        {
            OptionsWindow optWnd;

            optWnd = new OptionsWindow();
            optWnd.IP = Properties.Settings.Default.IP;
            optWnd.Port = Properties.Settings.Default.Port;

            if (!(bool)optWnd.ShowDialog())
                return;

            Properties.Settings.Default.IsFirstTime = false;
            Properties.Settings.Default.IP = optWnd.IP;
            Properties.Settings.Default.Port = optWnd.Port;

            Properties.Settings.Default.Save();
        }
    }
}

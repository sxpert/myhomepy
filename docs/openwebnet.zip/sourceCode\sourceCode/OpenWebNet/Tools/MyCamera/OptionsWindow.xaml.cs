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
using System.Windows.Shapes;

namespace MyCamera
{
    /// <summary>
    /// Interaction logic for OptionsWindow.xaml
    /// </summary>
    public partial class OptionsWindow : Window
    {
        public OptionsWindow()
        {
            InitializeComponent();
        }

        public string IP
        {
            get
            {
                return ipTxt.Text;
            }

            set
            {
                ipTxt.Text = value;
            }
        }

        public int Port
        {
            get
            {
                return int.Parse(portTxt.Text);
            }

            set
            {
                portTxt.Text = value.ToString();
            }
        }

        private void okBtn_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = true;
            Close();
        }   
    }
}

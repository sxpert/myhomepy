using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;

namespace MyEnergy
{
    public partial class Resources : ResourceDictionary
    {
        private void closeBtn_Click(object sender, RoutedEventArgs e)
        {
            ((Window)((FrameworkElement)sender).TemplatedParent).Close();
        }

        private void WindowTitleBorder_MouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            ((Window)((FrameworkElement)sender).TemplatedParent).DragMove();
        }
    }
}

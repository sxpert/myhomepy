using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace MyHomeShortcut.AddShortcutControls
{
    public partial class ShortcutControl : UserControl
    {
        public ShortcutControl()
        {
            InitializeComponent();

            this.key1ComboBox.DataSource = new string[] { Keys.Shift.ToString(), Keys.Control.ToString(), Keys.Alt.ToString() };
            this.key2ComboBox.DataSource = new string[] { Keys.Shift.ToString(), Keys.Control.ToString(), Keys.Alt.ToString(), Keys.None.ToString() };
            this.key3ComboBox.DataSource = new string[] { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" };
        }

        public string ShortcutName
        {
            get
            {
                return nameTxt.Text;
            }

            set
            {
                nameTxt.Text = value;
            }
        }

        public Keys KeyOne
        {
            get
            {
                if (key1ComboBox.SelectedItem == null)
                    return Keys.None;

                return (Keys)Enum.Parse(typeof(Keys), key1ComboBox.SelectedItem.ToString());
            }

            set
            {
                key1ComboBox.SelectedItem = value.ToString();
            }
        }

        public Keys KeyTwo
        {
            get
            {
                if (key2ComboBox.SelectedItem == null)
                    return Keys.None;

                return (Keys)Enum.Parse(typeof(Keys), key2ComboBox.SelectedItem.ToString());
            }

            set
            {
                key2ComboBox.SelectedItem = value.ToString();
            }
        }

        public Keys KeyThree
        {
            get
            {
                if (key3ComboBox.SelectedItem == null)
                    return Keys.None;

                return Utilities.NumberToKey(key3ComboBox.SelectedItem.ToString());
            }

            set
            {
                key3ComboBox.SelectedItem = Utilities.NumberToString(value);
            }
        }

        public void Clear()
        {
            nameTxt.Text = string.Empty;
            key1ComboBox.SelectedItem = Keys.Shift.ToString();
            key2ComboBox.SelectedItem = Keys.None.ToString();
            key3ComboBox.SelectedItem = "0";
        }
    }
}

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
    public partial class MainShortcutControl : UserControl
    {
        // controlli cambiamento pagina
        // settare shortcut a null
        // pulire schermata principale

        public enum ShortcutPage
        {
            FirstPage,
            SecondPage,
            Finished,
            Cancel
        }

        public event EventHandler<ShortcutEventArgs> ShortcutEditingCompleted;

        private ShortcutPage shortcutPage;
        private Shortcut shortcut;

        public MainShortcutControl()
        {
            InitializeComponent();

            this.CurrentPage = ShortcutPage.FirstPage;
        }

        public Shortcut Shortcut
        {
            get
            {
                return this.shortcut;
            }

            set
            {
                this.shortcut = value;

                if (this.shortcut != null)
                {
                    actionsControl.Actions = this.shortcut.Actions;
                    this.CurrentPage = ShortcutPage.FirstPage;
                }
                else
                {
                    // pulisco
                    shortcutControl.Clear();
                    actionsControl.Clear();
                }
            }
        }

        public ShortcutPage CurrentPage
        {
            get
            {
                return this.shortcutPage;
            }

            set
            {
                this.shortcutPage = value;

                if (this.shortcut == null)
                {
                    this.shortcut = new Shortcut();
                    this.shortcut.Actions = new List<Action>();
                }

                switch (value)
                {
                    case ShortcutPage.FirstPage:
                        {
                            backBtn.Visible = false;
                            actionsControl.Visible = false;
                            shortcutControl.Visible = true;
                            nextBtn.Text = "Next";

                            shortcutControl.ShortcutName = this.shortcut.Name;
                            shortcutControl.KeyOne = this.shortcut.KeyOne;
                            shortcutControl.KeyTwo = this.shortcut.KeyTwo;
                            shortcutControl.KeyThree = this.shortcut.KeyThree;

                            break;
                        }
                    case ShortcutPage.SecondPage:
                        {
                            backBtn.Visible = true;
                            nextBtn.Text = "Save";
                            actionsControl.Visible = true;
                            shortcutControl.Visible = false;

                            this.shortcut.Name = shortcutControl.ShortcutName;
                            this.shortcut.KeyOne = shortcutControl.KeyOne;
                            this.shortcut.KeyTwo = shortcutControl.KeyTwo;
                            this.shortcut.KeyThree = shortcutControl.KeyThree;

                            actionsControl.Actions = this.shortcut.Actions;

                            break;
                        }
                    case ShortcutPage.Finished:
                        {
                            if (ShortcutEditingCompleted != null)
                                ShortcutEditingCompleted(this, new ShortcutEventArgs(this.shortcut));

                            // torno all'inizio
                            this.CurrentPage = ShortcutPage.FirstPage;
                            this.Shortcut = null;

                            break;
                        }
                    case ShortcutPage.Cancel:
                        {
                            // torno all'inizio
                            this.CurrentPage = ShortcutPage.FirstPage;
                            this.Shortcut = null;

                            break;
                        }
                }
            }
        }

        private bool ValidateFirstPage()
        {
            if (string.IsNullOrEmpty(shortcutControl.ShortcutName) || shortcutControl.KeyOne == Keys.None || shortcutControl.KeyThree == Keys.None)
            {
                MessageBox.Show("All red field have to be specified", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }

            return true;
        }

        private bool ValidateSecondPage()
        {
            if (actionsControl.Actions == null || actionsControl.Actions.Count == 0)
            {
                MessageBox.Show("A shortcut must have at least an action", "MyHomeShortcut", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return false;
            }

            return true;
        }

        private void backBtn_Click(object sender, EventArgs e)
        {
            this.CurrentPage = ShortcutPage.FirstPage;
        }

        private void nextBtn_Click(object sender, EventArgs e)
        {
            if (this.CurrentPage == ShortcutPage.FirstPage)
            {
                if (ValidateFirstPage())
                    this.CurrentPage = ShortcutPage.SecondPage;
            }
            else
            {
                if (ValidateSecondPage())
                    this.CurrentPage = ShortcutPage.Finished;
            }
        }

        private void cancelBtn_Click(object sender, EventArgs e)
        {
            this.CurrentPage = ShortcutPage.Cancel;
        }
    }

    public class ShortcutEventArgs : EventArgs
    {
        public Shortcut Shortcut { get; set; }

        public ShortcutEventArgs(Shortcut shortcut)
            : base()
        {
            this.Shortcut = shortcut;
        }
    }
}

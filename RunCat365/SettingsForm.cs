// Copyright 2025 Takuto Nakamura
//
//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
//
//        http://www.apache.org/licenses/LICENSE-2.0
//
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.

using RunCat365.Properties;
using System.IO;
using System.Windows.Forms;

namespace RunCat365
{
    internal partial class SettingsForm : Form
    {
        private readonly Func<Theme> getSystemTheme;
        private readonly Func<Theme> getManualTheme;
        private readonly Action<Theme> setManualTheme;

        public SettingsForm(Func<Theme> getSystemTheme, Func<Theme> getManualTheme, Action<Theme> setManualTheme)
        {
            this.getSystemTheme = getSystemTheme;
            this.getManualTheme = getManualTheme;
            this.setManualTheme = setManualTheme;

            InitializeComponent();
            LoadCustomRunners();
        }

        private void LoadCustomRunners()
        {
            var customRunners = CustomRunnerExtension.GetCustomRunners();
            listViewCustomRunners.Items.Clear();
            foreach (var runner in customRunners)
            {
                var listViewItem = new ListViewItem(runner.Name);
                listViewItem.SubItems.Add(runner.FrameCount.ToString());
                listViewCustomRunners.Items.Add(listViewItem);
            }
        }

        private void buttonImportGif_Click(object sender, EventArgs e)
        {
            using var openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "GIF files (*.gif)|*.gif";
            openFileDialog.Title = "Import Custom Runner";

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                var runnerName = Path.GetFileNameWithoutExtension(openFileDialog.FileName);
                if (CustomRunnerExtension.ImportGif(openFileDialog.FileName, runnerName))
                {
                    LoadCustomRunners();
                    MessageBox.Show($"Successfully imported runner: {runnerName}");
                }
                else
                {
                    MessageBox.Show("Failed to import runner. Please check the GIF file.");
                }
            }
        }

        private void buttonRemoveRunner_Click(object sender, EventArgs e)
        {
            if (listViewCustomRunners.SelectedItems.Count > 0)
            {
                var runnerName = listViewCustomRunners.SelectedItems[0].Text;
                var runnersFolder = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "resources", "custom_runners");
                var runnerFolder = Path.Combine(runnersFolder, runnerName);

                if (Directory.Exists(runnerFolder))
                {
                    Directory.Delete(runnerFolder, true);
                    LoadCustomRunners();
                    MessageBox.Show($"Successfully removed runner: {runnerName}");
                }
            }
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}

namespace RunCat365
{
    partial class SettingsForm
    {
        private System.ComponentModel.IContainer components = null;
        private ListView listViewCustomRunners;
        private Button buttonImportGif;
        private Button buttonRemoveRunner;
        private Button buttonClose;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.listViewCustomRunners = new System.Windows.Forms.ListView();
            this.columnHeaderName = new System.Windows.Forms.ColumnHeader();
            this.columnHeaderFrames = new System.Windows.Forms.ColumnHeader();
            this.buttonImportGif = new System.Windows.Forms.Button();
            this.buttonRemoveRunner = new System.Windows.Forms.Button();
            this.buttonClose = new System.Windows.Forms.Button();
            this.SuspendLayout();

            this.listViewCustomRunners.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeaderName,
            this.columnHeaderFrames});
            this.listViewCustomRunners.FullRowSelect = true;
            this.listViewCustomRunners.GridLines = true;
            this.listViewCustomRunners.Location = new System.Drawing.Point(12, 12);
            this.listViewCustomRunners.Name = "listViewCustomRunners";
            this.listViewCustomRunners.Size = new System.Drawing.Size(300, 200);
            this.listViewCustomRunners.TabIndex = 0;
            this.listViewCustomRunners.UseCompatibleStateImageBehavior = false;
            this.listViewCustomRunners.View = System.Windows.Forms.View.Details;

            this.columnHeaderName.Text = "Name";
            this.columnHeaderName.Width = 150;
            this.columnHeaderFrames.Text = "Frames";
            this.columnHeaderFrames.Width = 50;

            this.buttonImportGif.Location = new System.Drawing.Point(12, 218);
            this.buttonImportGif.Name = "buttonImportGif";
            this.buttonImportGif.Size = new System.Drawing.Size(90, 25);
            this.buttonImportGif.TabIndex = 1;
            this.buttonImportGif.Text = "Import GIF";
            this.buttonImportGif.UseVisualStyleBackColor = true;
            this.buttonImportGif.Click += new System.EventHandler(this.buttonImportGif_Click);

            this.buttonRemoveRunner.Location = new System.Drawing.Point(118, 218);
            this.buttonRemoveRunner.Name = "buttonRemoveRunner";
            this.buttonRemoveRunner.Size = new System.Drawing.Size(90, 25);
            this.buttonRemoveRunner.TabIndex = 2;
            this.buttonRemoveRunner.Text = "Remove";
            this.buttonRemoveRunner.UseVisualStyleBackColor = true;
            this.buttonRemoveRunner.Click += new System.EventHandler(this.buttonRemoveRunner_Click);

            this.buttonClose.Location = new System.Drawing.Point(224, 218);
            this.buttonClose.Name = "buttonClose";
            this.buttonClose.Size = new System.Drawing.Size(90, 25);
            this.buttonClose.TabIndex = 3;
            this.buttonClose.Text = "Close";
            this.buttonClose.UseVisualStyleBackColor = true;
            this.buttonClose.Click += new System.EventHandler(this.buttonClose_Click);

            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(324, 250);
            this.Controls.Add(this.listViewCustomRunners);
            this.Controls.Add(this.buttonImportGif);
            this.Controls.Add(this.buttonRemoveRunner);
            this.Controls.Add(this.buttonClose);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "SettingsForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Settings";
            this.ResumeLayout(false);
        }

        private ColumnHeader columnHeaderName;
        private ColumnHeader columnHeaderFrames;
    }
}

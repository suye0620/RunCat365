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
using System.Drawing;

namespace RunCat365
{
    internal class CustomToolStripMenuItem : ToolStripMenuItem
    {
        private static readonly Font MenuFont = new(
            SupportedLanguageExtension.GetCurrentLanguage().GetFontName(),
            9F,
            FontStyle.Regular
        );

        internal CustomToolStripMenuItem() : base()
        {
            Font = MenuFont;
        }

        internal CustomToolStripMenuItem(string? text) : base(text)
        {
            Font = MenuFont;
        }

        private CustomToolStripMenuItem(string? text, Image? image, object? tag, bool isChecked, EventHandler? onClick) : base(text, image, onClick)
        {
            Tag = tag;
            Checked = isChecked;
            Font = MenuFont;
        }

        private readonly TextFormatFlags multiLineTextFlags =
            TextFormatFlags.LeftAndRightPadding |
            TextFormatFlags.VerticalCenter |
            TextFormatFlags.WordBreak |
            TextFormatFlags.TextBoxControl;

        private readonly TextFormatFlags singleLineTextFlags =
            TextFormatFlags.LeftAndRightPadding |
            TextFormatFlags.VerticalCenter |
            TextFormatFlags.EndEllipsis;

        public override Size GetPreferredSize(Size constrainingSize)
        {
            Size baseSize = base.GetPreferredSize(constrainingSize);
            if (string.IsNullOrEmpty(Text))
            {
                return new Size(baseSize.Width, 22);
            }
            var textRenderWidth = Math.Max(constrainingSize.Width - 20, 1);

            SizeF measuredSize = TextRenderer.MeasureText(
                Text,
                Font,
                new Size(textRenderWidth, int.MaxValue),
                Flags()
            );
            var calculatedHeight = (int)Math.Ceiling(measuredSize.Height) + 4;
            var height = IsSingleLine() ? calculatedHeight : Math.Max(baseSize.Height, calculatedHeight);
            return new Size(baseSize.Width, height);
        }

        internal bool IsSingleLine()
        {
            return string.IsNullOrEmpty(Text) || !Text.Contains('\n');
        }

        internal TextFormatFlags Flags()
        {
            return IsSingleLine() ? singleLineTextFlags : multiLineTextFlags;
        }

        internal void SetupSubMenusFromEnum<T>(
            Func<T, string> getTitle,
            Action<CustomToolStripMenuItem, object?, EventArgs> onClick,
            Func<T, bool> isChecked,
            Func<Runner, Bitmap?> getRunnerThumbnailBitmap,
            Func<T, bool>? isVisible = null
        ) where T : Enum
        {
            isVisible ??= _ => true;
            var items = new List<CustomToolStripMenuItem>();
            foreach (T value in Enum.GetValues(typeof(T)))
            {
                if (!isVisible(value)) continue;
                var entityName = getTitle(value);
                var iconImage = value is Runner runner ? getRunnerThumbnailBitmap(runner) : null;
                var item = new CustomToolStripMenuItem(
                    entityName,
                    iconImage,
                    value,
                    isChecked(value),
                    (sender, e) => onClick(this, sender, e)
                );
                items.Add(item);
            }
            DropDownItems.AddRange([.. items]);
        }

        internal void SetupRunnerMenu(
            Func<Runner> getRunner,
            Action<Runner> setRunner,
            Func<Theme> getSystemTheme,
            Func<Theme> getManualTheme
        )
        {
            var items = new List<CustomToolStripMenuItem>();

            foreach (var runner in RunnerExtension.GetAllRunners())
            {
                var entityName = runner.GetLocalizedString();
                var iconImage = GetRunnerThumbnailBitmap(getSystemTheme(), getManualTheme(), runner);
                var item = new CustomToolStripMenuItem(
                    entityName,
                    iconImage,
                    runner,
                    getRunner() == runner,
                    (sender, e) => HandleRunnerSelection(sender, setRunner)
                );
                items.Add(item);
            }

            var customRunners = CustomRunnerExtension.GetCustomRunners();
            if (customRunners.Count > 0)
            {
                items.Add(new CustomToolStripMenuItem("-"));
                foreach (var runner in customRunners)
                {
                    var entityName = runner.GetLocalizedString();
                    var iconImage = runner.GetRunnerThumbnailBitmap(getManualTheme() == Theme.System ? getSystemTheme() : getManualTheme());
                    var item = new CustomToolStripMenuItem(
                        entityName,
                        iconImage,
                        runner,
                        IsCustomRunnerSelected(runner, getRunner),
                        (sender, e) => HandleCustomRunnerSelection(sender, setRunner)
                    );
                    items.Add(item);
                }
            }

            DropDownItems.AddRange([.. items]);
        }

        private static Bitmap? GetRunnerThumbnailBitmap(Theme systemTheme, Theme manualTheme, Runner runner)
        {
            var theme = manualTheme == Theme.System ? systemTheme : manualTheme;
            var color = theme.GetContrastColor();
            var iconName = $"{runner.GetString()}_0".ToLower();
            var obj = Resources.ResourceManager.GetObject(iconName);
            if (obj is not Bitmap bitmap) return null;
            return theme == Theme.Light ? bitmap : bitmap.Recolor(color);
        }

        private static void HandleRunnerSelection(object? sender, Action<Runner> setRunner)
        {
            if (sender is null) return;
            var item = (ToolStripMenuItem)sender;
            if (item.Tag is Runner runner)
            {
                setRunner(runner);
            }
        }

        private static void HandleCustomRunnerSelection(object? sender, Action<Runner> setRunner)
        {
            if (sender is null) return;
            var item = (ToolStripMenuItem)sender;
            if (item.Tag is CustomRunner customRunner)
            {
                if (Enum.TryParse(customRunner.Name, out Runner parsedRunner))
                {
                    setRunner(parsedRunner);
                }
            }
        }

        private static bool IsCustomRunnerSelected(CustomRunner runner, Func<Runner> getRunner)
        {
            return getRunner().ToString().Equals(runner.Name, StringComparison.OrdinalIgnoreCase);
        }
    }
}

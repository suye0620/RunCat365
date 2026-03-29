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
using System.Drawing.Imaging;
using System.IO;

namespace RunCat365
{
    internal class CustomRunner
    {
        internal string Name { get; }
        internal string FolderPath { get; }
        internal int FrameCount { get; }

        internal CustomRunner(string name, string folderPath, int frameCount)
        {
            Name = name;
            FolderPath = folderPath;
            FrameCount = frameCount;
        }

        internal Bitmap? GetFrame(int index)
        {
            var imagePath = Path.Combine(FolderPath, $"{Name}_{index}.png");
            if (File.Exists(imagePath))
            {
                return new Bitmap(imagePath);
            }
            return null;
        }
    }

    internal static class CustomRunnerExtension
    {
        private const string CustomRunnersFolder = "custom_runners";

        internal static List<CustomRunner> GetCustomRunners()
        {
            var customRunners = new List<CustomRunner>();
            var runnersFolder = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "resources", CustomRunnersFolder);

            if (!Directory.Exists(runnersFolder))
            {
                return customRunners;
            }

            foreach (var folder in Directory.GetDirectories(runnersFolder))
            {
                var name = Path.GetFileName(folder);
                if (string.IsNullOrEmpty(name)) continue;

                var frameCount = CountFrames(folder, name);
                if (frameCount > 0)
                {
                    customRunners.Add(new CustomRunner(name, folder, frameCount));
                }
            }

            return customRunners;
        }

        private static int CountFrames(string folderPath, string runnerName)
        {
            int count = 0;
            while (File.Exists(Path.Combine(folderPath, $"{runnerName}_{count}.png")))
            {
                count++;
            }
            return count;
        }

        internal static string GetLocalizedString(this CustomRunner runner)
        {
            return runner.Name;
        }

        internal static Bitmap? GetRunnerThumbnailBitmap(this CustomRunner runner, Theme theme)
        {
            var color = theme.GetContrastColor();
            var frame = runner.GetFrame(0);
            if (frame is null) return null;

            return theme == Theme.Light ? frame : frame.Recolor(color);
        }

        internal static bool ImportGif(string gifPath, string runnerName)
        {
            try
            {
                var runnersFolder = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "resources", CustomRunnersFolder);
                var runnerFolder = Path.Combine(runnersFolder, runnerName);

                Directory.CreateDirectory(runnerFolder);

                using var gif = Image.FromFile(gifPath);
                var frameCount = gif.GetFrameCount(FrameDimension.Time);

                for (int i = 0; i < frameCount; i++)
                {
                    gif.SelectActiveFrame(FrameDimension.Time, i);
                    using var frame = gif.Clone() as Bitmap;
                    if (frame != null)
                    {
                        // Resize to 32x32 if necessary
                        using var resizedFrame = new Bitmap(32, 32);
                        using var graphics = Graphics.FromImage(resizedFrame);
                        graphics.DrawImage(frame, 0, 0, 32, 32);
                        
                        var framePath = Path.Combine(runnerFolder, $"{runnerName}_{i}.png");
                        resizedFrame.Save(framePath, ImageFormat.Png);
                    }
                }

                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
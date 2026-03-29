# RunCat365 PyQt Implementation

A cross-platform implementation of RunCat365 using PyQt5.

## Features

- System tray icon with animation
- System performance monitoring (CPU, Memory, Network)
- Animation speed adjusts based on system load
- Custom runner support (import GIF files)
- Theme support (System, Light, Dark)
- Endless game mode
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install dependencies

```bash
# Using pip
pip install -r requirements.txt

# Using uv (recommended)
uv install
```

## Usage

### Run the application

```bash
python app/main.py
```

### Custom Runners

1. Right-click on the system tray icon
2. Select "Manage Runners"
3. Click "Import GIF" to import a custom runner
4. The GIF will be automatically processed and added to the runner list

### Settings

- **Runner**: Select from built-in or custom runners
- **Theme**: Choose between System, Light, or Dark theme
- **Speed based on**: Select which system metric to use for animation speed
- **FPS Max Limit**: Set maximum animation speed
- **Launch at startup**: Enable/disable automatic startup

## Project Structure

```
runcat-pyqt/
├── app/                  # Main application code
│   ├── monitor/          # System performance monitoring
│   ├── animation/        # Animation system
│   ├── game/             # Endless game mode
│   ├── settings/         # Settings management
│   └── utils/            # Utility functions
├── resources/            # Resource files
│   ├── runners/          # Built-in runners
│   ├── custom_runners/   # Custom runners
│   └── game/             # Game resources
├── translations/         # Translation files
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## Supported Platforms

- Windows
- macOS
- Linux

## License

Apache License 2.0

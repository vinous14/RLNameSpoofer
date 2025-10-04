# vinxzn's Name Spoofer

A powerful and user-friendly application for spoofing names in Rocket League with a sleek navy blue interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **🎮 Rocket League Name Spoofing** - Change your display name in Rocket League
- **🔄 Real-time Proxy Control** - Start/stop proxy with a single click
- **🚀 Auto-attach to Rocket League** - Automatically detect and attach to the game
- **⚡ Boot at Startup** - Option to start with Windows
- **🎨 Modern UI** - Clean navy blue interface with gold accents
- **📝 Persistent Settings** - Remembers your preferences between sessions
- **🛡️ Safe & Secure** - Local proxy operation, no external servers

## 🖥️ Interface

- **Header**: Prominent logo and title display
- **Input Field**: Enter your desired display name
- **Control Button**: Activate/Deactivate the proxy
- **Options**: Auto-attach and startup toggles
- **Status Indicator**: Real-time proxy status
- **Watermark**: "Made by vinxzn" signature

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **Dependencies**: Listed in `requirements.txt`

## 🚀 Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```

## 📦 Dependencies

The application requires the following packages:

- **customtkinter** - Modern GUI framework
- **Pillow** - Image processing for logo display
- **mitmproxy** - HTTP proxy functionality
- **olefile** - Additional image format support

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Operation
1. **Launch** the application
2. **Enter** your desired name in the input field
3. **Click "ACTIVATE"** to start the proxy
4. **Launch Rocket League** and enjoy your new display name
5. **Click "DEACTIVATE"** when finished

### Auto-attach Feature
- Enable **"Auto-attach to Rocket League"** to automatically detect the game
- The spoofer will monitor for Rocket League and attach when detected

### Startup Option
- Enable **"Boot at startup"** to launch the spoofer with Windows
- Adds the application to Windows startup registry

## ⚙️ Configuration

The application stores settings in `config.json`:
- Last used spoof name
- Auto-scan preferences
- Proxy configuration

## 🔧 Technical Details

### Proxy Operation
- **Protocol**: HTTP/HTTPS interception
- **Method**: mitmproxy-based traffic modification
- **Scope**: Local system proxy settings
- **Port**: Configurable (default varies)

### System Integration
- **Registry**: Windows startup management
- **Proxy**: System-wide proxy configuration
- **Logging**: Comprehensive activity logging

## 🛠️ File Structure

```
vinxzn spoofer/
├── main.py              # Application entry point
├── gui.py               # User interface
├── config.py            # Configuration management
├── mitmproxy_addon.py   # Proxy functionality
├── utils.py             # Utility functions
├── logger_setup.py      # Logging configuration
├── requirements.txt     # Python dependencies
├── icon.png.ico         # Application icon
└── README.md           # This file
```

## 🎨 Customization

### Colors
- **Primary**: `#01024D` (Navy Blue)
- **Accent**: `#BD9F4C` (Gold) - Title bar
- **Text**: `#FFFFFF` (White)
- **Active Status**: `#00FF00` (Green)

### Interface
- Monochromatic navy design
- Gold title bar (Windows 10/11)
- Modern CustomTkinter components
- Responsive layout

## ⚠️ Important Notes

### Legal Disclaimer
- This tool is for **educational purposes** only
- Use responsibly and in accordance with game terms of service
- The author is not responsible for any consequences of misuse

### Security
- All operations are performed locally
- No data is sent to external servers
- Proxy settings are temporary and reversible

### Compatibility
- **Windows Only** - Uses Windows-specific APIs
- **Rocket League** - Designed specifically for this game
- **Modern Systems** - Optimized for Windows 10/11

## 🐛 Troubleshooting

### Common Issues

**"Port in use" error**:
- Another proxy application is running
- Close other proxy software and retry

**"Could not set system proxy"**:
- Run as administrator if needed
- Check Windows proxy settings

**Icon not loading**:
- Ensure `icon.png.ico` is in the application folder
- Falls back to emoji if icon missing

### Logs
Check the application logs for detailed error information and debugging.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**vinxzn**
- Created with ❤️ for the Rocket League community
- Professional tools with attention to detail

## 🌟 Acknowledgments

- CustomTkinter for the modern GUI framework
- mitmproxy team for the proxy functionality
- Rocket League community for inspiration

---

**Made by vinxzn :)** 
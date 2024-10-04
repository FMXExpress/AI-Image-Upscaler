# AI Image Upscaler
 AI Image Upscaler desktop GUI using FireMonkey for Python.


This project is a cross-platform GUI application built with [DelphiFMX for Python](https://github.com/Embarcadero/DelphiFMX4Python), providing an interface for AI-based image upscaling. The app leverages the [Replicate API](https://replicate.com/) to upscale images by adding detail and enhancing image quality. The app supports real-time status updates, running the upscaling in the background without freezing the UI.

## Features

- **Cross-Platform GUI**: Built using DelphiFMX for Python, the app runs on Windows, macOS, and Linux.
- **AI-Powered Image Upscaling**: Uses the [philz1337x/clarity-upscaler](https://replicate.com/philz1337x/clarity-upscaler) model from Replicate to enhance image details.
- **Asynchronous Processing**: The app handles image processing in the background, ensuring the UI remains responsive.
- **Status Updates**: Displays real-time progress of the upscaling process.
- **Image Display**: Shows both the original and upscaled images within the app.

## Requirements

- Python 3.8 or higher
- DelphiFMX for Python
- Replicate API key
- [Replicate Python package](https://pypi.org/project/replicate/)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/image-upscaler-fmx.git
   cd image-upscaler-fmx
   ```

2. Install the required Python packages:
   ```bash
   pip install replicate delphifmx
   ```

3. Set your Replicate API key:
   - Sign up at [Replicate](https://replicate.com/) and get your API key.
   - Set the API key as an environment variable:
     ```bash
     export REPLICATE_API_TOKEN="your_replicate_api_key"
     ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open the app and click **Select** to choose an image from your file system.
2. The app will display the original image on the left side.
3. Once an image is selected, it will be processed using the Replicate API. The status bar at the bottom will show real-time updates.
4. After the upscaling is completed, the upscaled image will appear on the right side of the screen.

## Code Overview

### Imports

```python
import os
import replicate
import urllib.request
import hashlib
from delphifmx import *
import threading  # To handle background process without blocking the app
```

- **os**: Used for environment variables.
- **replicate**: Connects to the [Replicate API](https://replicate.com/) for AI-based image upscaling.
- **urllib.request**: Downloads the upscaled image.
- **hashlib**: Ensures unique filenames for downloaded images.
- **delphifmx**: Provides cross-platform GUI components via [DelphiFMX for Python](https://github.com/Embarcadero/DelphiFMX4Python).
- **threading**: Runs the upscaling process in the background without locking the UI.

### Core Components

- **Form Layout**: The main window contains components for image upload, original image display, upscaled image display, and a status bar.
- **Asynchronous Processing**: Upscaling runs in the background using the `Replicate API`, and the app updates the UI in real-time.
- **Timer**: Periodically checks the status of the upscaling process and updates the status bar accordingly.

### Example API Call

The app uses the Replicate model for upscaling:

```python
model = replicate.models.get("philz1337x/clarity-upscaler")
version = model.versions.get("dfad41707589d68ecdccd1dfa600d55a208f9310748e44bfe35b4a6291453d5e")
self.prediction = replicate.predictions.create(
    version=version,
    input={"image": open(file_path, "rb")}
)
```

## Contributing

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/new-feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DelphiFMX for Python](https://github.com/Embarcadero/DelphiFMX4Python)
- [Replicate API](https://replicate.com/)
- [philz1337x/clarity-upscaler](https://replicate.com/philz1337x/clarity-upscaler)

```

This README provides an overview of the project, including instructions for installation, usage, and contributing, along with links to the necessary resources.
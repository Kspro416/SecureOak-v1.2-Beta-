# SecureOak (v1.2 beta)

## Introduction

This is an upgraded version (v1.2) of the basicSecureOak System application (v1.1). The current version introduces a fully functional GUI-based secure login system using PySide6 with integrated encryption and user authentication stored in an encrypted JSON file.

## Table of Contents


- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Features

- Clean and modern GUI using **PySide6**
- Encrypted user data stored in a file
- Login verification against securely stored credentials
- Real-time validation with error and success messages
- Improved security over the previous version (1.1)

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` is not present, install manually:

```bash
pip install PySide6 cryptography
```

3. Ensure you have the encrypted user data file (`imp_1`) in the same directory.

## Usage

To run the application:

```bash
python "1.2 Pass.py"
```

Upon launch:
- Enter the username and password.
- On success, you will receive a "Login successful!" message.
- Invalid credentials or missing inputs will trigger appropriate alerts.

## Configuration

It will be Configured On 26th May exactly at 12:00 ISO
Configurations wil be announced On the Mentioned Date Above.

This file is encrypted using the `cryptography.fernet` module.

## Dependencies

- `PySide6` — for GUI components
- `cryptography` — for encryption and decryption
- `json`, `os`, `tempfile`, `sys` — standard libraries

## Security

- Credentials are securely stored and only temporarily written to disk for validation.
- The use of `Fernet` encryption ensures that user data cannot be accessed without the key.

## Troubleshooting

- **"Invalid credentials" error**: Double-check your username and password.
- **Application crashes or no GUI appears**: Ensure PySide6 is installed and compatible with your Python version.
- **"Error opening file"**: Make sure the `imp_1` file is present and correctly formatted/encrypted.

## Contributors

- [Kspro416](#https://github.com/Kspro416), [Vedustorm](#https://github.com/VeduStorm)

## License

This Project Is Not Licensed As It Cannot Be Used On Production Purpose

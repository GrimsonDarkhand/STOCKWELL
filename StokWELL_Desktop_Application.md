# StokWELL Desktop Application

A modern desktop application for managing stokvels (rotating savings groups) built with Python and PyQt5.

## Features

- **User Management**: Secure user registration and authentication with password hashing
- **Stokvel Creation**: Create and manage multiple stokvels
- **Contribution Tracking**: Make contributions and track transaction history
- **Dashboard**: View personal balance, recent transactions, and stokvel memberships
- **Modern UI**: Clean, intuitive graphical user interface
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Dual Interface**: Both GUI and command-line interfaces available

## Installation

### Prerequisites
- Python 3.6 or later
- pip (Python package installer)

### Quick Install
1. Download or clone the StokWELL application
2. Navigate to the StokWELL directory
3. Run the installation script:
   ```bash
   ./install.sh
   ```

### Manual Install
1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Make scripts executable:
   ```bash
   chmod +x stokwell.py stokwell_cli.py
   ```

## Usage

### GUI Version (Recommended)
```bash
python3 stokwell.py
```

### Command-Line Version
```bash
python3 stokwell.py --cli
```

### Running Tests
```bash
python3 test_stokwell.py
```

## Application Workflow

1. **Registration/Login**: Create a new account or login with existing credentials
2. **Dashboard**: View your account balance, recent transactions, and stokvels
3. **Create Stokvel**: Start a new stokvel group
4. **Contribute**: Make financial contributions to your stokvels
5. **Track Progress**: Monitor your financial activities and stokvel growth

## Project Structure

```
StokWELL/
├── stokwell.py              # Main application launcher
├── stokwell_cli.py          # Command-line interface
├── controller.py            # GUI application controller
├── data_manager.py          # Data persistence layer
├── user_manager.py          # User management logic
├── stokvel_manager.py       # Stokvel management logic
├── utils.py                 # Utility functions
├── ui/                      # User interface components
│   ├── login_window.py      # Login/registration window
│   ├── dashboard_window.py  # Main dashboard
│   ├── create_stokvel_dialog.py  # Stokvel creation dialog
│   └── contribute_dialog.py # Contribution dialog
├── stokvel_data.json        # Data storage file
├── test_stokwell.py         # Test suite
├── requirements.txt         # Python dependencies
├── install.sh              # Installation script
└── README.md               # This file
```

## Data Storage

StokWELL uses JSON file storage for simplicity and portability. All data is stored in `stokvel_data.json` with the following structure:

- **Users**: Account information, balances, transaction history
- **Stokvels**: Member lists, contributions, balances, creation dates

## Security Features

- Password hashing using SHA-256
- Input validation for all user inputs
- Safe data handling and error management

## Development

### Running Tests
The application includes a comprehensive test suite covering all major functionality:

```bash
python3 test_stokwell.py
```

### Architecture
StokWELL follows the Model-View-Controller (MVC) pattern:
- **Model**: Data management and business logic
- **View**: PyQt5-based user interface
- **Controller**: Application coordination and event handling

## Future Enhancements

- Database migration (SQLite/PostgreSQL)
- Multi-user network support
- Advanced reporting and analytics
- Mobile application companion
- Automated payout scheduling
- Integration with banking APIs

## Troubleshooting

### GUI Issues
If the GUI version fails to start:
1. Ensure PyQt5 is properly installed
2. Try the CLI version: `python3 stokwell.py --cli`
3. Check for display/X11 issues on Linux systems

### Permission Issues
If you encounter permission errors:
```bash
chmod +x stokwell.py stokwell_cli.py install.sh
```

### Dependencies
If installation fails, try updating pip:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## License

This project is developed for educational and demonstration purposes.

## Support

For issues or questions, please refer to the test suite and documentation within the code files.


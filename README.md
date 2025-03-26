# 🚀Python Script Obfuscation with PyArmor🚀

## Description
This guide provides steps to obfuscate a Python script using PyArmor and package it into an executable with PyInstaller.

## 📥Requirements
- Python 3.x
- `pyarmor==7.6.0`
- `pyinstaller`

## 📥Installation
```bash
pip install pyarmor==7.6.0
pip install pyinstaller

```
## Obfuscation Process
Obfuscate the script using PyArmor:
```bash
pyarmor obfuscate socket_client.py
```
Package the obfuscated script into an executable:
```bash
pyinstaller --onefile --noconsole dist/socket_client.py

```

## 📜License
This will display correctly on GitHub and maintain readability. Let me know if you need further refinements! 🚀

## 👨‍💻 Author

Damrith Som ✨  
Happy Coding! 🚀



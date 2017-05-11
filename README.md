# KnightSpider-MainFrame

Python version >= 3

### Required packages
* https://pypi.python.org/pypi/tinyik/1.2.0
* https://pypi.python.org/pypi/pyax12
* https://pypi.python.org/pypi/numpy (Must be 1.12 or higher, 
    version in default repository is too low, jessie-backports has a updated version)


## Configuring the Raspberry Pi

Choose the device and baudrate    
Device should probably be serial0, baudrate can be 57600 or 1000000

### Configure the boot settings
Edit `/boot/config.txt` and add the following lines at the end:    
```
enable_uart=1    
init_uart_clock=16000000
```

Edit `/boot/cmdline.txt` and remove all references to your device    
This is most likely something like `console=serial0,115000`

### Configuring the serial baudrate
Run `sudo stty -F /dev/serial0 1000000` (Or any other baudrate)
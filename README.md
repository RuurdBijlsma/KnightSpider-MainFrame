# KnightSpider-MainFrame
[![f](https://github.com/ruurdbijlsma/KnightSpider-MainFrame/blob/master/.gh/spider.gif?raw=true)](https://www.youtube.com/embed/-7goAt89zZw?start=125&end=138&autoplay=1)

Python version >= 3

### Required packages
* https://pypi.python.org/pypi/numpy (Must be 1.12 or higher, 
    version in default repository is too low, jessie-backports has an updated version)


## Configuring the Raspberry Pi

Choose the device and baudrate    
Device should probably be serial0, baudrate can be 57600 or 1000000

### Configure the boot settings
Edit `/boot/config.txt` and add the following lines at the end:    
```
enable_uart=1    
init_uart_clock=16000000
core_freq=250
dtoverlay=pi3-miniuart-bt
```

Edit `/boot/cmdline.txt` and remove all references to your device    
This is most likely something like `console=serial0,115000`

### Configuring the serial baudrate
Run `sudo stty -F /dev/serial0 1000000` (Or any other baudrate)

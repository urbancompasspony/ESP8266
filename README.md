# Driver

sudo apt install esptool

or

sudo pacman -S esptool

# ESP8266

HOW TO TURN ON:

= 3v or 3.3v on 2 pins VCC and CH_PD (aliases: EN, Enable, CHIP_EN or CH_D)

= Ground to 2 pins GRD and PIN 16 (aliases: GPIO 15, MTDO, SS, PWM, TX0, D15, SPI CS, UART0 RTS or I2S0 BLK)

# Dica de Ouro

Se alternar entre deauther e micropython, limpe os 4mb de ROM:

sudo esptool --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect -fm dio 0x000000  blank_1MB.bin

sudo esptool --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect -fm dio 0x100000  blank_1MB.bin

sudo esptool --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect -fm dio 0x200000  blank_1MB.bin

sudo esptool --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect -fm dio 0x300000  blank_1MB.bin

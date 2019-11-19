
Adafruit 128x64 1.3" OLED bonnet driver for pwnagotchi 1.3.0

Make sure the pwnagotchi is connected to the internet
Run install.sh as root(first run of pip3 can take awhile)

Add bonnet as the display type in config.yml:

ui:
  display:
    type: 'bonnet'
    color: 'black'

It is probably best to turn off auto-update in config.yml:

main:
  plugins:
    auto-update:
      enabled: false

Reboot add the display should be working:)

Key bindings:
 5 - Sleep or wake up screen
 6 - Short press AUTO, long press(3s) shutdown
 L - Turn off Screen Saver
 R - Trun On Screen Saver
 U - Flip screen up
 D - Flip screen down





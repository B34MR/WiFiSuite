import os
#Theme v1.05052017
App = ' WiFiSuite '
Version = ' v 1.05282017'
Author = 'Nick Sanzotta/@Beamr'

# Colors
class colors:
   white = "\033[1;37m"
   normal = "\033[0;00m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"
   lightblue = "\033[0;34m"
# Symbols
def blue(symbol):
  blue_symbol = ' [' + colors.blue + symbol + colors.normal + '] ' + colors.normal
  return str(blue_symbol)
def lblue(symbol):
  lblue_symbol = ' [' + colors.lightblue + symbol + colors.normal + '] ' + colors.normal
  return str(lblue_symbol)
def green(symbol):
  green_symbol = ' [' + colors.green + symbol + colors.normal + '] ' + colors.normal
  return str(green_symbol)
def red(symbol):
  red_symbol = ' [' + colors.red + symbol + colors.normal + '] ' + colors.normal
  return str(red_symbol)
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
# Banner
def banner():
  banner = colors.blue + '\n' + App + Version \
  + colors.normal + '\n Description: Enterprise WPA Wireless Tool suite.' + '\n'\
  + colors.normal + ' Created by: ' + Author + '\n'\
  + colors.normal + ' ' + '*' * 79 +'\n' + colors.normal
  print(banner)

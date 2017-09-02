import os
#Theme v1.05052017
App = ' WiFiSuite '
Version = ' v 1.09042017'
Author = 'Nick Sanzotta/@Beamr'

# Colors
class colors:
   normal = "\033[0;00m"
   # Bold Colors
   white = "\033[1;37m"
   red = "\033[1;31m"
   blue = "\033[1;34m"
   green = "\033[1;32m"
   # Regular Colors
   lightgreen="\033[0;32m" 
   ligtblue = "\033[0;34m"
   lightred="\033[0;31m"
   lightyellow="\033[0;33m"

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
def white(symbol):
  white_symbol = ' [' + colors.white + symbol + colors.normal + '] ' + colors.normal
  return str(white_symbol)
def normal(symbol):
  normal_symbol = ' [' + colors.normal + symbol + colors.normal + '] ' + colors.normal
  return str(normal_symbol)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
# Banner
def banner():
  banner = colors.blue + '\n' + App + Version \
  + colors.normal + '\n Description: Enterprise WPA Wireless Tool suite.' + '\n'\
  + colors.normal + ' Created by: ' + Author + '\n'\
  + colors.normal + ' ' + '*' * 79 +'\n' + colors.normal
  print(banner)

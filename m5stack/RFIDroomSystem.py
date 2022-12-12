from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit
import _thread

####################
# variables
####################
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xe1e1e1)

screens = []
current_screen = 0

# セマフォを作成し、競合状態を回避
lock_obj = _thread.allocate_lock()
lockIdle = _thread.allocate_lock()


####################
# screen settings
####################

########## screen0 ##########
screen0_TitleText = M5Label('RFID', x=20, y=20, color=0x00ff00, font=FONT_MONT_30, parent=None)
screen0_isCardNearText = M5Label('card near', x=20, y=70, color=0x00ff00, font=FONT_MONT_14, parent=None)
screen0_isCardNear = M5Label('', x=120, y=70, color=0x00ffff, font=FONT_MONT_14, parent=None)
screen0_cardUidText = M5Label('card uid', x=20, y=110, color=0x00ff00, font=FONT_MONT_14, parent=None)
screen0_isCardNearLine = M5Line(x1=20, y1=96, x2=250, y2=96, color=0x00ff00, width=1, parent=None)
screen0_cardUid = M5Label('', x=120, y=113, color=0x00ffff, font=FONT_MONT_14, parent=None)
screen0_line0 = M5Line(x1=100, y1=65, x2=100, y2=130, color=0x00ff00, width=1, parent=None)
screen0_addrText = M5Label('addr', x=20, y=150, color=0x00ff00, font=FONT_MONT_14, parent=None)
screen0_addr = M5Label('', x=120, y=150, color=0x00ffff, font=FONT_MONT_14, parent=None)
screen0_line1 = M5Line(x1=100, y1=65, x2=100, y2=170, color=0x00ff00, width=1, parent=None)
screen0_line2 = M5Line(x1=20, y1=138, x2=250, y2=138, color=0x00ff00, width=1, parent=None)
screen0_message = M5Label('', x=20, y=190, color=0xffff00, font=FONT_MONT_14, parent=None)

# save screen with all current content
screen0 = screen.get_act_screen()
screens.append(screen0)

########## screen1 ##########
screen1 = screen.get_new_screen()
screen.load_screen(screen1)

screen1_TitleText = M5Label('RFID', x=20, y=20, color=0x00ff00, font=FONT_MONT_30, parent=None)

# save screen with all current content
screens.append(screen1)

########## screenX ##########
screenX = screen.get_new_screen()
screen.load_screen(screenX)

# save screen with all current content
screens.append(screenX)


########## screen functions ##########
def goPrevScreen():
  global current_screen, screens
  lock_obj.acquire()
  print('goPrevScreen called')
  current_screen-=1  
  if current_screen < 0 :
    current_screen=0
  else:
    screen.load_screen(screens[current_screen])
  lock_obj.release()

def goNextScreen():
  global current_screen, screens
  lock_obj.acquire()
  print('goNextScreen called')
  current_screen+=1
  if current_screen > len(screens)-1 :
    current_screen=len(screens)-1
  else:
    screen.load_screen(screens[current_screen])
  lock_obj.release()

def goScreen(n):
  global current_screen, screens
  lock_obj.acquire()
  print('getScreen called with number:' + str(n))
  current_screen = n
  if current_screen > len(screens)-1 :
    pass
  else:
    screen.load_screen(screens[current_screen])
  lock_obj.release()


####################
# setup
####################
screen.load_screen(screens[0])
rfid_0 = unit.get(unit.RFID, unit.PORTA)


####################
# loop
####################
while True:
  screen0_isCardNear.set_text(str(rfid_0.isCardOn()))
  if rfid_0.isCardOn():
    screen0_cardUid.set_text(str(rfid_0.readUid()))
    screen0_addr.set_text(str(rfid_0.readBlockStr(1)))
    screen0_message.set_text('Hello M5 !!!')
    speaker.playTone(440, 1)
    goScreen(1)

  elif not (rfid_0.isCardOn()):
    screen0_cardUid.set_text('')
    screen0_addr.set_text('')
    screen0_message.set_text('')
  wait(0.5)
  wait_ms(2)

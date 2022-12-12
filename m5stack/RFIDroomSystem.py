from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit
import _thread

####################
# variables
####################
DEBUG = True

screen = M5Screen()
screen.clean_screen()

screens = []
current_screen = 0

rfid_0 = unit.get(unit.RFID, unit.PORTA)

# セマフォを作成し、競合状態を回避
lock_obj = _thread.allocate_lock()
lockIdle = _thread.allocate_lock()


####################
# screen settings
####################
_screen0 = screen.get_act_screen()
HOME_SCREEN = 0
TAG_ADD_SCREEN = 1
TAG_REMOVE_SCREEN = 2
ENTER_ROOM_SCREEN = 3
LEAVE_ROOM_SCREEN = 4
DEBUG_SCREEN = 5

########## screen functions ##########
def goPrevScreen():
  global current_screen, screens
  lock_obj.acquire()
  print('goPrevScreen called')
  current_screen-=1  
  if current_screen < 0 :
    current_screen=0
  else:
    screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goNextScreen():
  global current_screen, screens
  lock_obj.acquire()
  print('goNextScreen called')
  current_screen+=1
  if current_screen > len(screens)-1 :
    current_screen=len(screens)-1
  else:
    screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goHomeScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = HOME_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goTagAddScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = TAG_ADD_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goTagRemoveScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = TAG_REMOVE_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goEnterRoomScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = ENTER_ROOM_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goLeaveRoomScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = LEAVE_ROOM_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

def goDebugScreen():
  global current_screen, screens
  lock_obj.acquire()
  current_screen = DEBUG_SCREEN
  screen.load_screen(screens[current_screen].get_screen())
  lock_obj.release()

########## DebugScreen ##########
class DebugScreen:

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)
    
    self.TitleText = M5Label('debug screen', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)
    self.isCardNearText = M5Label('card near', x=20, y=70, color=0x000000, font=FONT_MONT_14, parent=None)
    self.isCardNear = M5Label('', x=120, y=70, color=0x000000, font=FONT_MONT_14, parent=None)
    self.cardUidText = M5Label('card uid', x=20, y=110, color=0x000000, font=FONT_MONT_14, parent=None)
    self.isCardNearLine = M5Line(x1=20, y1=96, x2=250, y2=96, color=0x000000, width=1, parent=None)
    self.cardUid = M5Label('', x=120, y=113, color=0x000000, font=FONT_MONT_14, parent=None)
    self.line0 = M5Line(x1=100, y1=65, x2=100, y2=130, color=0x000000, width=1, parent=None)
    self.addrText = M5Label('addr', x=20, y=150, color=0x000000, font=FONT_MONT_14, parent=None)
    self.addr = M5Label('', x=120, y=150, color=0x000000, font=FONT_MONT_14, parent=None)
    self.line1 = M5Line(x1=100, y1=65, x2=100, y2=170, color=0x000000, width=1, parent=None)
    self.line2 = M5Line(x1=20, y1=138, x2=250, y2=138, color=0x000000, width=1, parent=None)
    self.message = M5Label('', x=20, y=190, color=0x000000, font=FONT_MONT_14, parent=None)


    # save screen with all current content
    self.screen = local_screen
  
  def get_screen(self):
    return self.screen

  def loop(self):
    self.isCardNear.set_text(str(rfid_0.isCardOn()))
    if rfid_0.isCardOn():
      self.cardUid.set_text(str(rfid_0.readUid()))
      self.addr.set_text(str(rfid_0.readBlockStr(1)))
      self.message.set_text('Hello M5 !!!')
      speaker.playTone(440, 1)

    elif not (rfid_0.isCardOn()):
      self.cardUid.set_text('')
      self.addr.set_text('')
      self.message.set_text('')
    wait(0.5)
    wait_ms(2)


########## HomeScreen ##########
class HomeScreen:
  def enter_pressed(self):
    _thread.start_new_thread(goEnterRoomScreen, ())

  def leave_pressed(self):
    _thread.start_new_thread(goLeaveRoomScreen, ())
    
  def add_pressed(self):
    _thread.start_new_thread(goTagAddScreen, ())
    
  def remove_pressed(self):
    _thread.start_new_thread(goTagRemoveScreen, ())

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('HOME', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    self.enter_btn = M5Btn(text='Enter', x=20, y=70, w=130, h=80, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_30, parent=None)
    self.leave_btn = M5Btn(text='Leave', x=170, y=70, w=130, h=80, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_30, parent=None)
    self.add_btn = M5Btn(text='add', x=70, y=170, w=80, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.remove_btn = M5Btn(text='remove', x=170, y=170, w=80, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)

    self.enter_btn.pressed(self.enter_pressed)
    self.leave_btn.pressed(self.leave_pressed)
    self.add_btn.pressed(self.add_pressed)
    self.remove_btn.pressed(self.remove_pressed)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def loop(self):
    pass

########## TagAddScreen ##########
class TagAddScreen:

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Tag Add', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen
    
  def loop(self):
    pass

########## TagRemoveScreen ##########
class TagRemoveScreen:

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Tag Remove', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def loop(self):
    pass

########## EnterRoomScreen ##########
class EnterRoomScreen:

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Enter Room', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def loop(self):
    pass

########## LeaveRoomScreen ##########
class LeaveRoomScreen:

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Leave Room', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def loop(self):
    pass


####################
# setup
####################
screens.append(HomeScreen())
screens.append(TagAddScreen())
screens.append(TagRemoveScreen())
screens.append(EnterRoomScreen())
screens.append(LeaveRoomScreen())
screens.append(DebugScreen())

if DEBUG:
  current_screen = DEBUG_SCREEN
else:
  current_screen = HOME_SCREEN
screen.load_screen(screens[current_screen].get_screen())
screen.set_screen_bg_color(0xe1e1e1)


####################
# event
####################
def buttonA_wasPressed():
  _thread.start_new_thread(goPrevScreen, ())
  pass
if DEBUG:
  btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  _thread.start_new_thread(goNextScreen, ())
  pass
if DEBUG:
  btnC.wasPressed(buttonB_wasPressed)

####################
# loop
####################
while True:
  screens[current_screen].loop()

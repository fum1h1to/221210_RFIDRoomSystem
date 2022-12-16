from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit
import _thread
import wifiCfg
import urequests
import ujson

####################
# variables
####################
DEBUG = True
SCREEN_WIDTH = 320
SERVER_IP = '192.168.68.104'
SERVER_PORT = 5000

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
    self.add_btn = M5Btn(text='add', x=20, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.remove_btn = M5Btn(text='remove', x=170, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)

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
  isScanning = True
  detectTagId = ''

  def add_btn_pressed(self):
    self.cancel_btn.set_hidden(True)
    self.add_btn.set_hidden(True)
    self._set_centerText_and_centering("adding tag....")

    try:
      data = {
        "tagid": self.detectTagId
      }

      header = {
        'Content-Type' : 'application/json'
      }

      req = urequests.post(url= 'http://' + SERVER_IP + '/api/addTag', data = ujson.dumps(data).encode("utf-8"), headers=header)
      if (req.status_code) == 200:
        res_json = req.json()
        print(res_json)
        if res_json['status'] == '0':
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

        elif res_json['status'] == '1':
          self._set_centerText_and_centering("success!!")
          self.ok_btn.set_hidden(False)
        
        elif res_json['status'] == '2':
          self._set_centerText_and_centering("already exists")
          self.ok_btn.set_hidden(False)
        
        else:
          self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)

      else:
        self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)
  
    except:
      self._set_centerText_and_centering("failed")
      self.ok_btn.set_hidden(False)

    finally:
      req.close()

  def cancel_btn_pressed(self):
    self.cancel_btn.set_hidden(True)
    self.add_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()

  def ok_btn_pressed(self):
    self.ok_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()
  
  def changeDetectMode(self):
    self.isScanning = True
    self.detectTagId = ''

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Tag Add', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    self.centerText = M5Label('Please hold up your tag.', x=51, y=111, color=0x000, font=FONT_MONT_18, parent=None)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

    self.cancel_btn = M5Btn(text='cancel', x=20, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.cancel_btn.set_hidden(True)
    self.cancel_btn.pressed(self.cancel_btn_pressed)
    self.add_btn = M5Btn(text='add', x=170, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.add_btn.set_hidden(True)
    self.add_btn.pressed(self.add_btn_pressed)

    self.ok_btn = M5Btn(text='OK', x=95, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.ok_btn.set_hidden(True)
    self.ok_btn.pressed(self.ok_btn_pressed)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def _set_centerText_and_centering(self, str):
    self.centerText.set_text(str)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

  def loop(self):
    if rfid_0.isCardOn() and self.isScanning:
      self._set_centerText_and_centering("scanning....")
      self.detectTagId = str(rfid_0.readUid())
    else:
      pass
  
    if len(self.detectTagId) != 0 and self.isScanning:
      self._set_centerText_and_centering(self.detectTagId + " detedted")
      self.cancel_btn.set_hidden(False)
      self.add_btn.set_hidden(False)
      self.isScanning = False

########## TagRemoveScreen ##########
class TagRemoveScreen:

  isScanning = True
  detectTagId = ''

  def remove_btn_pressed(self):
    self.cancel_btn.set_hidden(True)
    self.remove_btn.set_hidden(True)
    self._set_centerText_and_centering("removing tag....")

    try:
      data = {
        "tagid": self.detectTagId
      }

      header = {
        'Content-Type' : 'application/json'
      }

      req = urequests.post(url= 'http://' + SERVER_IP + '/api/removeTag', data = ujson.dumps(data).encode("utf-8"), headers=header)
      if (req.status_code) == 200:
        res_json = req.json()
        print(res_json)
        if res_json['status'] == '0':
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

        elif res_json['status'] == '1':
          self._set_centerText_and_centering("success!!")
          self.ok_btn.set_hidden(False)
        
        elif res_json['status'] == '2':
          self._set_centerText_and_centering("does not exist")
          self.ok_btn.set_hidden(False)
        
        else:
          self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)

      else:
        self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)
      
    except:
      self._set_centerText_and_centering("failed")
      self.ok_btn.set_hidden(False)
    
    finally:
      req.close()

  def cancel_btn_pressed(self):
    self.cancel_btn.set_hidden(True)
    self.remove_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()

  def ok_btn_pressed(self):
    self.ok_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()
  
  def changeDetectMode(self):
    self.isScanning = True
    self.detectTagId = ''

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Tag Remove', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    self.centerText = M5Label('Please hold up your tag.', x=51, y=111, color=0x000, font=FONT_MONT_18, parent=None)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

    self.cancel_btn = M5Btn(text='cancel', x=20, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.cancel_btn.set_hidden(True)
    self.cancel_btn.pressed(self.cancel_btn_pressed)
    self.remove_btn = M5Btn(text='remove', x=170, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.remove_btn.set_hidden(True)
    self.remove_btn.pressed(self.remove_btn_pressed)

    self.ok_btn = M5Btn(text='OK', x=95, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.ok_btn.set_hidden(True)
    self.ok_btn.pressed(self.ok_btn_pressed)

    # save screen with all current content
    self.screen = local_screen

  def get_screen(self):
    return self.screen

  def _set_centerText_and_centering(self, str):
    self.centerText.set_text(str)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

  def loop(self):
    if rfid_0.isCardOn() and self.isScanning:
      self._set_centerText_and_centering("scanning....")
      self.detectTagId = str(rfid_0.readUid())
    else:
      pass
  
    if len(self.detectTagId) != 0 and self.isScanning:
      self._set_centerText_and_centering(self.detectTagId + " detedted")
      self.cancel_btn.set_hidden(False)
      self.remove_btn.set_hidden(False)
      self.isScanning = False

########## EnterRoomScreen ##########
class EnterRoomScreen:
  isScanning = True
  detectTagId = ''

  def ok_btn_pressed(self):
    self.ok_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()

  def _enter_room(self, tagid):
    self._set_centerText_and_centering("entering room....")

    try:
      data = {
        "tagid": tagid
      }

      header = {
        'Content-Type' : 'application/json'
      }

      req = urequests.post(url= 'http://' + SERVER_IP + '/api/enter', data = ujson.dumps(data).encode("utf-8"), headers=header)
      if (req.status_code) == 200:
        res_json = req.json()
        print(res_json)
        if res_json['status'] == '0':
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

        elif res_json['status'] == '1':
          self._set_centerText_and_centering("success!!")
          self.ok_btn.set_hidden(False)
        
        elif res_json['status'] == '2':
          self._set_centerText_and_centering("not exists")
          self.ok_btn.set_hidden(False)
        
        else:
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

      else:
        self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)

    except:
      self._set_centerText_and_centering("failed")
      self.ok_btn.set_hidden(False)

    finally:
      req.close()
  
  def changeDetectMode(self):
    self.isScanning = True
    self.detectTagId = ''

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Enter Room', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    self.centerText = M5Label('Please hold up your tag.', x=51, y=111, color=0x000, font=FONT_MONT_18, parent=None)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

    self.ok_btn = M5Btn(text='OK', x=95, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.ok_btn.set_hidden(True)
    self.ok_btn.pressed(self.ok_btn_pressed)

    # save screen with all current content
    self.screen = local_screen

  def _set_centerText_and_centering(self, str):
    self.centerText.set_text(str)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

  def get_screen(self):
    return self.screen

  def loop(self):
    if rfid_0.isCardOn() and self.isScanning:
      self._set_centerText_and_centering("scanning....")
      self.detectTagId = str(rfid_0.readUid())
    else:
      pass
  
    if len(self.detectTagId) != 0 and self.isScanning:
      self._set_centerText_and_centering(self.detectTagId + " detedted")
      self.isScanning = False
      self._enter_room(self.detectTagId)

########## LeaveRoomScreen ##########
class LeaveRoomScreen:
  isScanning = True
  detectTagId = ''

  def ok_btn_pressed(self):
    self.ok_btn.set_hidden(True)
    self._set_centerText_and_centering("Please hold up your tag.")
    self.changeDetectMode()

  def _leave_room(self, tagid):
    self._set_centerText_and_centering("leaving room....")

    try:
      data = {
        "tagid": tagid
      }

      header = {
        'Content-Type' : 'application/json'
      }

      req = urequests.post(url= 'http://' + SERVER_IP + '/api/leave', data = ujson.dumps(data).encode("utf-8"), headers=header)
      if (req.status_code) == 200:
        res_json = req.json()
        print(res_json)
        if res_json['status'] == '0':
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

        elif res_json['status'] == '1':
          self._set_centerText_and_centering("success!!")
          self.ok_btn.set_hidden(False)
        
        elif res_json['status'] == '2':
          self._set_centerText_and_centering("not exists")
          self.ok_btn.set_hidden(False)
        
        else:
          self._set_centerText_and_centering("failed")
          self.ok_btn.set_hidden(False)

      else:
        self._set_centerText_and_centering("failed")
        self.ok_btn.set_hidden(False)

    except:
      self._set_centerText_and_centering("failed")
      self.ok_btn.set_hidden(False)

    finally:
      req.close()
  
  def changeDetectMode(self):
    self.isScanning = True
    self.detectTagId = ''

  def __init__(self):
    local_screen = screen.get_new_screen()
    screen.load_screen(local_screen)

    self.TitleText = M5Label('Leave Room', x=20, y=20, color=0x000000, font=FONT_MONT_30, parent=None)

    self.centerText = M5Label('Please hold up your tag.', x=51, y=111, color=0x000, font=FONT_MONT_18, parent=None)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

    self.ok_btn = M5Btn(text='OK', x=95, y=170, w=130, h=40, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_18, parent=None)
    self.ok_btn.set_hidden(True)
    self.ok_btn.pressed(self.ok_btn_pressed)

    # save screen with all current content
    self.screen = local_screen

  def _set_centerText_and_centering(self, str):
    self.centerText.set_text(str)
    self.centerText.set_pos(int((SCREEN_WIDTH / 2) - (self.centerText.get_width() / 2)) ,111)

  def get_screen(self):
    return self.screen

  def loop(self):
    if rfid_0.isCardOn() and self.isScanning:
      self._set_centerText_and_centering("scanning....")
      self.detectTagId = str(rfid_0.readUid())
    else:
      pass
  
    if len(self.detectTagId) != 0 and self.isScanning:
      self._set_centerText_and_centering(self.detectTagId + " detedted")
      self.isScanning = False
      self._leave_room(self.detectTagId)


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
  current_screen = HOME_SCREEN
else:
  current_screen = HOME_SCREEN
screen.load_screen(screens[current_screen].get_screen())
screen.set_screen_bg_color(0xe1e1e1)

# wifiCfg.doConnect('ssid', 'password')
# if not (wifiCfg.wlan_sta.isconnected()):
#   print("try reconnect")
#   wifiCfg.reconnect()
# print("get ifconfig")
print(wifiCfg.wlan_sta.ifconfig())
wait(5)

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
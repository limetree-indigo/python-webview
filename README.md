## PYTHON WEBVIEW

### python 3.9

### pip install pywebview
### pip install cefpython3
### pip install kivy
### pip install pyside6
### pip install schedule
### pip install playsound==1.2.2  -> 현재 1.3.0 최신버전이지만 한번씩 장치를 찾을 수없다는 오류가 발생하여 아래 버전을 사용
### pip install pyinstaller
### pip install pygame -> 소리를 설정하기 위해서 사용, mp3, wav 모두 가능 백그라운드에서 동작

#### pyinstaller 사용시 해당 데이터를 포함하려면
#### ` pyinstaller -w --add-data "notification.wav;." --add-data "order_wait.png;." --add-data "order_alert.png;." --add-data "hands_logo.ico;." -n HandsPos -i=hands_logo.ico  pos.hands.alert.app.v3.py`
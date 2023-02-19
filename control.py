import serial
import pyautogui

ser = serial.Serial("COM4",921600)
win_size = pyautogui.size()
val = None
while True:
	if ser.in_waiting:
		val = ser.read()
	else:
		val = None

	if val is not None:
		val = chr(int.from_bytes(val, 'big'))
		print(val)
		if val == 'u':
			pyautogui.press("up")
		elif val == 'r':
			pyautogui.press("right")
		elif val == 'd':
			pyautogui.press("down")
		elif val == 'l':
			pyautogui.press("left")
		elif val == 'a':
			pyautogui.press("a")

ser.close()
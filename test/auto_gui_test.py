import unittest
import pyautogui

class autoGuiTest(unittest.TestCase):
    def test_move(self):
        '''
        Test movement of cursor
        '''
        pyautogui.moveTo(90, 150, duration=0.5)

    def test_right_click(self):
        '''
        Test right click of cursor
        '''
        pyautogui.moveTo(90, 150, duration=0.5)
        pyautogui.rightClick(90, 150)

    def test_left_click(self):
        '''
        Test left click of cursor
        '''
        pyautogui.moveTo(90, 150, duration=0.5)
        pyautogui.click(90, 150)

    def test_left_double_click(self):
        '''
        Test double left click of cursor
        '''
        pyautogui.moveTo(90, 150, duration=0.5)
        pyautogui.doubleClick(90, 150)
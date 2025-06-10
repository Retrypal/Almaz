import tkinter
import pyautogui as p
from pynput import mouse
import win32gui
import win32api
import threading
import keyboard as k
import time
from os import path
from win32api import GetSystemMetrics
x1,y1,x2,y2=None,None,None,None
color=win32api.RGB(255,0,0)
window_enable=True
start_enable=True
start=True
try:
    filer=path.dirname(__file__)
except:
    pass
class main_window:
    def __init__(self):

        self.window=tkinter.Tk()
        self.window.geometry('320x220')
        self.window.resizable(False, False)
        self.status=tkinter.Label(self.window,text='Статус')
        self.status.place(x=0,y=0,width=320,height=40)
        self.cycle=tkinter.Entry(self.window,justify='right')
        self.cycle.place(x=0,y=40,width=200,height=40)
        try:
            with open (filer+'/setting.txt','r') as f:
                t=f.readlines()
        except:
            with open ('setting.txt','r') as f:
                t=f.readlines()
        self.cycle.insert(0,t[0])
        self.cycle_status=tkinter.Label(self.window,text='сек текущее время\nобновления')
        self.cycle_status.place(x=200,y=40,width=120,height=40)
        self.pos1=tkinter.Button(self.window,text='первая позиция',command=self.button1)
        self.pos1.place(x=0,y=80,width=160,height=60)
        self.pos2=tkinter.Button(self.window,text='вторая позиция',command=self.button2)
        self.pos2.place(x=160,y=80,width=160,height=60)
        self.start_stop=tkinter.Button(self.window,text='Начать',command=self.starter)
        self.start_stop.place(x=0,y=140,width=320,height=80)
        self.start_stoplabel=tkinter.Label(self.window,text='off')
        self.window.mainloop()
    def button1(self):
        global x1,y1,old
        self.status.config(text='выберите 1 позицию')
        self.window.update()
        with mouse.Listener(on_click=self.is_clicked) as listener:
            listener.join()
        self.window.update()
        self.status.config(text='Позиция 1 выбрана')
        x1,y1=p.position()
        print(x1,y1)
        if x2 and y2:
            old=p.screenshot(region=(x1+3,y1+3,x2-x1-3,y2-y1-3))
            proc=threading.Thread(target=self.draw)
            proc.start()
            
    def draw(self):
        global window_enable
        if window_enable:
            window_enable=False
            deltax=x2-x1
            deltay=y2-y1
            print(deltax)
            dc = win32gui.GetDC(0)
            while True:
                for xxx in range(deltax):
                    try:
                        win32gui.SetPixel(dc,x1+xxx,y1,color)
                        win32gui.SetPixel(dc,x1+xxx,y1+deltay,color)
                    except:pass
                for yyy in range(deltay):
                    try:
                        win32gui.SetPixel(dc,x1+deltax,y1+yyy,color)
                        win32gui.SetPixel(dc,x1,y1+yyy,color)
                    except:pass
                p.sleep(1)
    def button2(self):
        global x2,y2,old
        self.status.config(text='выберите 2 позицию')
        self.window.update()
        with mouse.Listener(on_click=self.is_clicked) as listener:
            listener.join()
        self.window.update()
        self.status.config(text='Позиция 2 выбрана')
        x2,y2=p.position()
        if x1 and y1:
            proc=threading.Thread(target=self.draw)
            proc.start()
            old=p.screenshot(region=(x1,y1,x2-x1,y2-y1))
    def is_clicked(self,x,y,button,pressed):
            if pressed:
                return False
    def starter(self):
        global old,start_enable,start
        
        if self.start_stoplabel.cget('text')=='on':
            self.start_stoplabel.config(text='off')
        
        else:
            self.start_stoplabel.config(text='on')
        if start_enable:
            start_enable=False           
            proc1=threading.Thread(target=self.potok_okna)
            proc1.start()
    def potok_okna(self):
        global x,old
        x=1
        timer=time.time()
        while (time.time()-timer)<3:
            pass
        while True:
                self.window.update()
                while self.start_stoplabel.cget('text')=='on':
                    self.window.update()
                    while x and self.start_stoplabel.cget('text')=='on':
                        self.window.update()
                        k.press('4')
                        p.sleep(1)
                        self.window.update()
                        k.press('4')
                        p.sleep(0.5)
                        self.window.update()
                        k.press('3')
                        p.sleep(1)
                        self.window.update()
                        k.press('2')
                        p.sleep(1)
                        self.window.update()
                        k.press('2')
                        p.sleep(float(self.cycle.get()))
                        self.window.update()
                        screenshot = p.screenshot(region=(x1+3,y1+3,x2-x1-3,y2-y1-3))
                        count=0
                        for i in range(5):
                            try:
                                file=p.locateOnScreen(old,confidence=0.95)
                                count+=1
                                print('Голда не изменилась')
                                break
                            except:
                                print('определило изменение')
                                pass
                        print('Новый цикл')
                        screenshot.save("processed_screenshot.png")
                        old=screenshot
                        if count==0 or (count==1 and ((time.time()-timer)>45)):
                            k.press('1')
                            p.sleep(1)
                            k.press('1')   
                            p.sleep(12) 
                            x=0
                            timer=time.time()
                        
                        
                    self.window.update()
                    x=1
if __name__=="__main__":
    app=main_window()
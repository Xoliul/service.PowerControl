import time, threading, os, sys, time
sys.path.append('/storage/.kodi/addons/virtual.rpi-tools/lib')

import xbmc, xbmcaddon, xbmcgui
import RPi.GPIO as GPIO


def shutdownCallback(p_pin):
    print("shutdown signal detected!")
    xbmcgui.Dialog().notification(__addonname__, "Shutting Down!", xbmcgui.NOTIFICATION_INFO, 2000)
    time.sleep(0.5)
    xbmc.executebuiltin("ShutDown")



if __name__ == '__main__':

    m_shuttingdown = False


    __addon__ = xbmcaddon.Addon()
    __addonname__ = __addon__.getAddonInfo('name')

    m_alivePin = int(__addon__.getSetting("alivepin"))
    m_shutdownPin = int(__addon__.getSetting("shutdownpin"))
    m_shutdowncallback = False
    m_lastvalue = GPIO.HIGH


    GPIO.setmode(GPIO.BCM)

    GPIO.setup(m_alivePin, GPIO.OUT)
    GPIO.setup(m_shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(m_alivePin, GPIO.LOW)
    try:
        GPIO.add_event_detect(m_shutdownPin,
                              GPIO.FALLING,
                              callback=shutdownCallback,
                              bouncetime=250)
        m_shutdowncallback = True
    except:
        xbmc.log("Powerman Service: failed to add callback fro shutdown, reverting to looping")
    xbmc.log("Powerman Service started and initialised")

    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if not m_shutdowncallback:
            v = GPIO.input(m_shutdownPin)
            if m_lastvalue == GPIO.HIGH and v == GPIO.LOW:
                if not m_shuttingdown:
                    m_shuttingdown = True
                    print("shutdown signal detected!")
                    xbmcgui.Dialog().notification(__addonname__, "Shutting Down!", xbmcgui.NOTIFICATION_INFO, 2000)
                    time.sleep(0.5)
                    os.system("shutdown now")
            m_lastvalue = v
        if monitor.waitForAbort(0.5):
            # Abort was requested while waiting. We should exit
            xbmc.log("Powerman Service: Loop stopped")
            GPIO.output(m_alivePin, GPIO.HIGH)
            GPIO.cleanup()
            break



        
# Add common but missing functions to time module (from redefined/recreated Micropython module)
import asyncio
import pygame
import os
import sys

sys.path.append("lib")

import time
import utime

time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

async def main():
	import gc
	gc.enable()
	import thumby
	import sys
	import ujson
	sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
	from classLib import TextForScroller
	from funcLib import await thingAquired, await battleStartAnimation, buttonInput, showOptions
	#import micropython
	
	async def openScreen():
	    gc.collect()
	    #micropython.mem_info()
	    thumby.display.setFPS(40)
	    f = open('/Games/Tiny_Monster_Trainer/Curtain/Other.ujson')
	    images = ujson.load(f)
	    myScroller = TextForScroller("Welcome! Press A/B to Start!")
	    
	    while(1):
	        whatDo = 0
	        thumby.display.fill(0)
	        thumby.display.blit(bytearray(images["introTail"]), 0, 0, 25, 30, 0, 0, 0)
	        thumby.display.blit(bytearray(images["introHead"]), 47, 0, 25, 30, 0, 1, 0)
	        await thingAquired("Tiny", "Monster", "Trainer!", "", 0, 1, 1)
	        thumby.display.drawLine(0, 28, 72, 28, 1)
	        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
	        await thumby.display.update()
	        whatDo = buttonInput(whatDo)
	        if whatDo >= 30:
	            await battleStartAnimation(0)
	            f.close()
	            try:
	                p = open("/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson", "r")
	                p.close()
	                p = open("/Games/Tiny_Monster_Trainer/Curtain/here_be_monsters.ujson", "r")
	                p.close()
	                break
	            except OSError:
	                gc.collect()
	                import createPlayer
	                del sys.modules["createPlayer"]
	                break 
	
	 
	async def optionScreen():
	    thumby.display.fill(0)
	    curSelect = 0
	    tempSelect = curSelect
	    cancelCheck = 0
	    optionList = ["Wilderness"]
	    while cancelCheck != 1:
	        if curSelect == 28 or curSelect == 29:
	            curSelect = tempSelect
	        tempSelect = curSelect
	        curSelect = showOptions(optionList, curSelect, "Choose Mode")
	        if curSelect == 31:
	            curSelect = tempSelect
	            if optionList[curSelect] == optionList[0]:
	                await thingAquired( "vvvvvvvvvvvvv", "The", "Wilderness!", "^^^^^^^^^^^^^", 0, 0, 0)
	                gc.collect()
	                #micropython.mem_info()
	                import wilderness
	        if curSelect == 30:
	            cancelCheck = 1
	            thumby.display.fill(0)
	        await thumby.display.update()
	
	
	while(1):
	    await openScreen()
	    #micropython.mem_info()
	    #print("in While")
	    await optionScreen()

asyncio.run(main())
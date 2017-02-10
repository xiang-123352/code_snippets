;
; AutoHotkey Version: 1.x
; Language:       English
; Platform:       Win9x/NT/2k/7
; Author:         Ikem Krueger <ikem.krueger@gmail.com>
;
; Script Function:
;	Keynav Mod for Windows
;
#SingleInstance force

#IfWinExist,_keynav
; Cursor zoom
c::
	CoordMode, Mouse, Screen
	MouseGetPos, posX, posY
	scWidth = 100
	scHeight = 100
	posX -= scWidth/2
	posY -= scHeight/2
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return

; Move the region left
Left::
	posX -= %scWidth%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Move the region down
Down::
	posY += %scHeight%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Move the region top
Up::
	posY -= %scHeight%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Move the region right
Right::
	posX += %scWidth%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return

; Select the left half of the region
+Left::
	scWidth /= 2
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the bottom half of the region
+Down::
	scHeight /= 2
	posY += %scHeight%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the top half of the region
+Up::
	scHeight /= 2
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the right half of the region
+Right::
	scWidth /= 2
	posX += %scWidth%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return

; Select the left half of the region
^Left::
	scWidth /= 2
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the bottom half of the region
^Down::
	scHeight /= 2
	posY += %scHeight%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the top half of the region
^Up::
	scHeight /= 2
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return
; Select the right half of the region
^Right::
	scWidth /= 2
	posX += %scWidth%
        Draw( _keynav, posX, posY, scWidth, scHeight ) 
	Return

; Move the mouse and left-click
Enter::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Left
	Gui,destroy
	Return
; Move the mouse and double-left-click
+Enter::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Left,,,2
	Gui,destroy
	Return
; Move the mouse and right-click
AppsKey::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Right
	Gui,destroy
	Return

; Move the mouse and left-click
1::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Left
	Gui,destroy
	Return
; Move the mouse and double-left-click
+1::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Left,,,2
	Gui,destroy
	Return
; Move the mouse and middle-click
2::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Middle
	Gui,destroy
	Return
; Move the mouse and right-click
3::
        Warp( posX, posY, scWidth, scHeight )
	MouseClick,Right
	Gui,destroy
	Return

; Cancel the move
Esc::
	Gui,destroy
	return
#IfWinExist

; Window zoom
F4::
^!Space::

#IfWinExist,_keynav
Gui, destroy
#IfWinExist

; Get active window position and size
WinGetActiveStats, scTitle, scWidth, scHeight, posX, posY

; TODO: Make that Window version specific:
; Compensate Windows 10 drop shadows
scWidth -= 14
scHeight -= 7
posX += 7

Gui +AlwaysOnTop -Caption +ToolWindow
Gui, Color, EEEEEE, _keynav
Gui, Show, NoActivate, _keynav
WinSet, Transparent, 0, _keynav
WinSet, ExStyle, ^0x20, _keynav
WinSet, TransColor, EEEEEE, _keynav
Draw( _keynav, posX, posY, scWidth, scHeight ) 
Return

GuiClose:
ExitApp

Draw( _keynav, posX, posY, scWidth, scHeight ) 
{
    CoordMode, Mouse, Screen
    WinMove, _keynav, , %posX%, %posY%, %scWidth%, %scHeight%
    CrossHair( scWidth, scHeight )
}

Warp( posX, posY, scWidth, scHeight )
{
    CoordMode, Mouse, Screen
    toX := posX + scWidth/2
    toY := posY + scHeight/2
    MouseMove, toX, toY, 0
}

CrossHair( scWidth, scHeight )
{
    Gui, Add, Text, % "x0 y" . scHeight/2 . " w" . scWidth . " h1 0x10 +BackgroundTrans"
    Gui, Add, Text, % "x" . scWidth/2 . " y0 w1 h" . scHeight . " 0x11 +BackgroundTrans"

    Gui, Add, Text, % "x0 y0 w" . scWidth .  " h1 0x10 +BackgroundTrans"
    Gui, Add, Text, % "x0 y0 w1 h" . scHeight . " 0x11 +BackgroundTrans"

    Gui, Add, Text, % "x0 y" . scHeight-1 . " w" . scWidth . " h1 0x10 +BackgroundTrans"
    Gui, Add, Text, % "x" . scWidth-1 . " y0 w1 h" . scHeight . " 0x11 +BackgroundTrans"
}


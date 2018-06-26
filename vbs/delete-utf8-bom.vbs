Option Explicit

Const UTF8_BOM = "ï»¿"

Const ForReading = 1
Const ForWriting = 2

Dim fso
Set fso = WScript.CreateObject("Scripting.FileSystemObject")

Dim f
f = WScript.Arguments.Item(0)

Dim t
t = fso.OpenTextFile(f, ForReading).ReadAll

If Left(t, 3) = UTF8_BOM Then
  fso.OpenTextFile(f, ForWriting).Write (Mid(t, 4))
  MsgBox "BOM gelöscht!"
Else
  MsgBox "UTF-8-BOM nicht vorhanden!"
End If
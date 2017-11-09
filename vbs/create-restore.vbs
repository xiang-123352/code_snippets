'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
'Script to create a System Restore point in Windows 7 | Vista | XP
'May 10 2008 - Revised on Jan 10, 2009
'© 2008 Ramesh Srinivasan. http://www.winhelponline.com
'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
If GetOS = "Windows XP" Then
	CreateSRP
End If

If GetOS = "Windows Vista" Or GetOS = "Windows 7" Then
	If WScript.Arguments.length =0 Then
  		Set objShell = CreateObject("Shell.Application")
		objShell.ShellExecute "wscript.exe", """" & _
  		  WScript.ScriptFullName & """" & " uac","", "runas", 1
	Else
  		CreateSRP
  	End If
End If

Sub CreateSRP
	Set SRP = getobject("winmgmts:\\.\root\default:Systemrestore")
	sDesc = "Daily Restore Point"
' sDesc = InputBox ("Enter a description.", "System Restore script : winhelponline.com","Manual Restore Point")
	If Trim(sDesc) <> "" Then
		sOut = SRP.createrestorepoint (sDesc, 0, 100)
		If sOut <> 0 Then
	 		WScript.echo "Error " & sOut & _
	 		  ": Unable to create Restore Point."
		End If
	End If
End Sub

Function GetOS    
    Set objWMI = GetObject("winmgmts:{impersonationLevel=impersonate}!\\" & _
    	".\root\cimv2")
    Set colOS = objWMI.ExecQuery("Select * from Win32_OperatingSystem")
    For Each objOS in colOS
        If instr(objOS.Caption, "Windows 7") Then
        	GetOS = "Windows 7"    
        ElseIf instr(objOS.Caption, "Vista") Then
        	GetOS = "Windows Vista"
        elseIf instr(objOS.Caption, "Windows XP") Then
      		GetOS = "Windows XP"
        End If
	Next
End Function
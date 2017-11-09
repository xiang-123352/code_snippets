netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
devcon disable =Net USB\*
devcon enable =Net USB\*

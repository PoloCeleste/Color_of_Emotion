- 추가 설치

```bash
pip install -U "Twisted[tls,http2]"
```

```md
<!-- ssl 인증서 -->

https://app.zerossl.com/dashboard

<!-- 무료 도메인 -->

https://xn--220b31d95hq8o.xn--3e0b707e/
```

```bash
# zerossl에서 받은 인증서 하나로 합치기
cat certificate.crt ca_bundle.crt > cert.pem

# ssl 적용해서 daphne 서버 실행
daphne -e ssl:443:privateKey=private.key:certKey=cert.pem emotion_server.asgi:application
```

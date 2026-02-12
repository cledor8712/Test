# gapcli

암호화폐 갭투자 아이디어를 빠르게 검증하기 위한 터미널 도구입니다.

## 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 사용

```bash
gap config init
gap once
gap watch --count 5 --interval 0.5
```

현재는 `MockExchange` 기반으로 동작하며, 실제 거래소 API 커넥터는 다음 단계에서 추가하면 됩니다.

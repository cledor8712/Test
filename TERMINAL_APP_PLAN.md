# 암호화폐 갭투자 터미널 앱 전환안

## 목표
모바일 앱 대신 터미널(CLI) 기반으로 **실시간 가격 차이(스프레드) 탐지 + 알림 + (선택)주문 실행**이 가능한 도구를 제공한다.

## MVP 범위
1. 거래소 2곳(예: 업비트, 바이낸스) 시세 수집
2. 순스프레드 계산
3. 조건 충족 시 터미널 알림(및 선택적 텔레그램 알림)
4. 페이퍼 트레이딩(실주문 없이 시뮬레이션)

## 추천 CLI UX
- `gap scan` : 실시간 스캔 시작
- `gap once` : 1회 계산 후 결과 출력
- `gap watch --pair BTC/USDT --min-net 0.8` : 특정 조건 모니터링
- `gap paper --strategy basic` : 페이퍼 트레이딩 실행
- `gap config init` : 설정 파일 생성

## 기술 스택(빠른 구현 기준)
- Python 3.11+
- Typer (CLI 프레임워크)
- httpx / websockets (거래소 통신)
- rich (테이블/컬러 출력)
- pydantic-settings (.env + 설정 관리)

## 계산 핵심
순스프레드 예시:

`net_spread = (sell_price - buy_price) / buy_price - fee_buy - fee_sell - slippage - transfer_cost`

실제 알림 조건에는 아래를 함께 반영한다.
- 호가 잔량(체결 가능 수량)
- 최소 거래대금
- 거래소별 입출금 상태

## 디렉터리 구조 제안
```text
src/
  cli.py
  config.py
  exchanges/
    base.py
    upbit.py
    binance.py
  engine/
    spread.py
    risk.py
  notifier/
    stdout.py
    telegram.py
  paper/
    simulator.py
```

## 개발 순서(1주 압축)
- Day 1: CLI 뼈대 + 설정 로딩
- Day 2: 거래소 커넥터 2개 + 공통 심볼 매핑
- Day 3: 순스프레드 계산 + rich 대시보드 출력
- Day 4: watch 모드 + 알림
- Day 5: 페이퍼 트레이딩 + 로그 저장
- Day 6~7: 예외처리/레이트리밋/문서화

## 보안/리스크 최소 기준
- API 키는 환경변수로만 주입하고 파일 평문 저장 금지
- 기본 모드는 읽기 전용(알림/시뮬레이션)
- 자동주문 기능은 별도 플래그로 명시적 활성화
- 일일 손실 한도, 최대 동시 포지션 수 제한

## 다음 단계
원하면 바로 아래 산출물을 이어서 제공 가능:
1. 실행 가능한 `Typer` 기반 CLI 초기 코드
2. 샘플 `.env.example` / `config.yaml`
3. `gap once` + `gap watch` 구현

# Deepening

의존성을 고려해 shallow module cluster를 안전하게 deepening하는 방법이다. [SKILL.md](SKILL.md)의 어휘인 **module**, **interface**, **seam**, **adapter**를 전제로 한다.

## Dependency category

deepening 후보를 평가할 때는 의존성을 분류한다. category는 깊어진 module을 seam 너머에서 어떻게 테스트할지 결정한다.

### 1. In-process

순수 계산, in-memory 상태, I/O 없음. 항상 deepening할 수 있다. module들을 병합하고 새 interface를 통해 직접 테스트한다. adapter는 필요 없다.

### 2. Local-substitutable

로컬 테스트 대역이 있는 의존성(Postgres용 PGLite, in-memory filesystem). 대역이 있다면 deepening할 수 있다. 깊어진 module은 test suite 안에서 실행되는 대역으로 테스트한다. seam은 internal이며, module의 external interface에는 port를 두지 않는다.

### 3. Remote but owned (Ports & Adapters)

네트워크 너머의 직접 소유한 서비스(microservice, internal API). seam에 **port**(interface)를 정의한다. deep module이 logic을 소유하고, transport는 **adapter**로 주입된다. 테스트는 in-memory adapter를 사용한다. production은 HTTP/gRPC/queue adapter를 사용한다.

추천 문장 형태: *"seam에 port를 정의하고 production용 HTTP adapter와 테스트용 in-memory adapter를 구현해, 네트워크를 넘어 배포되더라도 logic이 하나의 deep module 안에 놓이게 한다."*

### 4. True external (Mock)

직접 제어하지 않는 third-party service(Stripe, Twilio 등). 깊어진 module은 외부 의존성을 주입된 port로 받고, 테스트는 mock adapter를 제공한다.

## Seam discipline

- **Adapter 하나는 가설적 seam이다. Adapter 둘은 실제 seam이다.** 최소 두 adapter(보통 production + test)가 정당화되지 않는다면 port를 도입하지 않는다. adapter가 하나뿐인 seam은 단순한 간접화일 뿐이다.
- **Internal seam vs external seam.** deep module은 interface에 놓인 external seam뿐 아니라 internal seam도 가질 수 있다. internal seam은 implementation에 private하고 자체 테스트에서 사용된다. 테스트가 사용한다는 이유만으로 internal seam을 interface로 노출하지 않는다.

## 테스트 전략: layer를 쌓지 말고 교체한다

- deepened module의 interface에 대한 테스트가 생기면 shallow module에 대한 기존 unit test는 낭비가 된다. 삭제한다.
- deepened module의 interface에 새 테스트를 작성한다. **interface가 테스트 표면이다**.
- 테스트는 내부 상태가 아니라 interface를 통해 관찰 가능한 결과를 검증한다.
- 테스트는 내부 refactor 이후에도 살아남아야 한다. 테스트는 implementation이 아니라 behaviour를 설명한다. implementation이 바뀔 때 테스트도 바뀌어야 한다면 interface를 넘어 테스트하고 있는 것이다.

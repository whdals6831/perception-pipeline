---
name: codebase-design
description: 깊은 module을 설계하기 위한 공유 어휘입니다. 사용자가 module의 interface를 설계 또는 개선하거나, deepening 기회를 찾거나, seam 위치를 결정하거나, 코드를 더 테스트하기 쉽고 AI가 탐색하기 쉽게 만들고자 할 때, 또는 다른 스킬에 deep module 어휘가 필요할 때 사용합니다.
---

# 코드베이스 설계

**Deep module**을 설계한다. 작은 interface 뒤에 많은 동작을 숨기고, 깨끗한 seam에 배치하며, 그 interface를 통해 테스트할 수 있게 만든다. 코드를 설계하거나 재구조화하는 모든 곳에서 이 언어와 원칙을 사용한다. 목표는 호출자에게 leverage를, 유지보수자에게 locality를, 모두에게 테스트 용이성을 제공하는 것이다.

## 용어집

이 용어를 정확히 사용한다. "component", "service", "API", "boundary" 같은 말로 대체하지 않는다. 일관된 언어 자체가 핵심이다.

**Module** - interface와 implementation을 가진 모든 것. 의도적으로 규모에 구애받지 않는다. 함수, 클래스, 패키지, 여러 tier를 가로지르는 slice가 모두 될 수 있다. _Avoid_: unit, component, service.

**Interface** - 호출자가 module을 올바르게 사용하기 위해 알아야 하는 모든 것. 타입 signature뿐 아니라 invariant, 순서 제약, 오류 모드, 필수 설정, 성능 특성까지 포함한다. _Avoid_: API, signature(너무 좁다. 타입 수준의 표면만 가리킨다).

**Implementation** - module 안에 있는 것, 즉 코드 본문. **Adapter**와 구분된다. 어떤 것은 큰 implementation을 가진 작은 adapter(Postgres repo)일 수도 있고, 작은 implementation을 가진 큰 adapter(in-memory fake)일 수도 있다. seam이 주제일 때는 "adapter"를, 그 외에는 "implementation"을 사용한다.

**Depth** - interface에서 발생하는 leverage. 호출자 또는 테스트가 배워야 하는 interface 단위당 실행할 수 있는 동작의 양이다. 작은 interface 뒤에 많은 동작이 있을 때 module은 **deep**하고, interface가 implementation만큼 거의 복잡할 때 **shallow**하다.

**Seam** _(Michael Feathers)_ - 그 위치의 코드를 수정하지 않고도 동작을 바꿀 수 있는 지점. module의 interface가 놓이는 *위치*다. seam을 어디에 둘지는 그 뒤에 무엇을 둘지와 별개의 설계 결정이다. _Avoid_: boundary(DDD의 bounded context와 의미가 겹친다).

**Adapter** - seam에서 interface를 만족하는 구체적인 것. 실체(안에 무엇이 있는지)가 아니라 *역할*(어떤 자리를 채우는지)을 설명한다.

**Leverage** - 호출자가 depth에서 얻는 것. 배워야 하는 interface 단위당 더 많은 능력을 얻는다. 하나의 implementation이 N개의 호출 지점과 M개의 테스트에서 보답한다.

**Locality** - 유지보수자가 depth에서 얻는 것. 변경, 버그, 지식, 검증이 호출자 전체로 퍼지지 않고 한곳에 모인다. 한 번 고치면 모든 곳에서 고쳐진다.

## Deep vs shallow

**Deep module** = 작은 interface + 많은 implementation:

```
┌─────────────────────┐
│   Small Interface   │  ← 적은 method, 단순한 params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← 복잡한 logic을 숨김
│                     │
└─────────────────────┘
```

**Shallow module** = 큰 interface + 적은 implementation(피할 것):

```
┌─────────────────────────────────┐
│       Large Interface           │  ← 많은 method, 복잡한 params
├─────────────────────────────────┤
│  Thin Implementation            │  ← 단순 pass-through
└─────────────────────────────────┘
```

interface를 설계할 때 다음을 묻는다.

- 메서드 수를 줄일 수 있는가?
- 파라미터를 단순화할 수 있는가?
- 더 많은 복잡도를 안에 숨길 수 있는가?

## 원칙

- **Depth는 implementation이 아니라 interface의 속성이다.** deep module은 내부적으로 작고 mock 가능하며 교체 가능한 part들로 구성될 수 있다. 다만 그것들이 interface의 일부가 아닐 뿐이다. module은 interface에 놓인 **external seam**뿐 아니라, implementation에만 private하고 자체 테스트에서 사용하는 **internal seam**도 가질 수 있다.
- **삭제 테스트.** module을 삭제한다고 상상한다. 복잡도가 사라진다면 그것은 pass-through였다. 복잡도가 N개의 호출자에 다시 나타난다면 자기 몫을 하고 있던 것이다.
- **Interface가 테스트 표면이다.** 호출자와 테스트는 같은 seam을 지난다. interface를 *넘어* 테스트하고 싶다면 module의 형태가 잘못되었을 가능성이 높다.
- **Adapter 하나는 가설적 seam이다. Adapter 둘은 실제 seam이다.** 실제로 그 seam을 기준으로 달라지는 것이 없다면 seam을 도입하지 않는다.

## 테스트 가능성을 위한 설계

좋은 interface는 테스트를 자연스럽게 만든다.

1. **의존성은 생성하지 말고 받아들인다.**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **side effect를 만들지 말고 결과를 반환한다.**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **작은 표면적.** 메서드가 적을수록 필요한 테스트가 줄어든다. 파라미터가 적을수록 테스트 준비가 단순해진다.

## 관계

- **Module**은 정확히 하나의 **Interface**를 가진다. 이는 호출자와 테스트에 드러나는 표면이다.
- **Depth**는 **Module**의 속성이며, 그 **Interface**를 기준으로 측정된다.
- **Seam**은 **Module**의 **Interface**가 놓이는 곳이다.
- **Adapter**는 **Seam**에 위치하며 **Interface**를 만족한다.
- **Depth**는 호출자에게 **Leverage**를, 유지보수자에게 **Locality**를 만든다.

## 거부하는 관점

- **implementation line 수와 interface line 수의 비율로 보는 depth**(Ousterhout): implementation을 부풀리는 데 보상을 준다. 대신 depth-as-leverage를 사용한다.
- **"Interface"를 TypeScript `interface` 키워드나 클래스의 public method로 보는 관점**: 너무 좁다. 여기서 interface는 호출자가 알아야 하는 모든 사실을 포함한다.
- **"Boundary"**: DDD의 bounded context와 의미가 겹친다. **seam** 또는 **interface**라고 말한다.

## 더 깊게 보기

- **의존성을 고려한 cluster deepening** - [DEEPENING.md](DEEPENING.md) 참고: dependency category, seam discipline, replace-don't-layer testing.
- **대안 interface 탐색** - [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) 참고: 병렬 sub-agent를 띄워 interface를 여러 가지 완전히 다른 방식으로 설계한 뒤 depth, locality, seam placement 기준으로 비교한다.

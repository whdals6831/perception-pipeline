---
name: domain-modeling
description: 프로젝트의 도메인 모델을 만들고 다듬습니다. 사용자가 도메인 용어나 ubiquitous language를 확정하거나, 아키텍처 결정을 기록하거나, 다른 스킬이 도메인 모델을 유지해야 할 때 사용합니다.
---

# 도메인 모델링

설계하면서 프로젝트의 도메인 모델을 능동적으로 만들고 다듬는다. 이것은 *능동적* 규율이다. 용어에 이의를 제기하고, edge-case scenario를 만들어 보고, 용어와 결정이 선명해지는 순간 glossary와 decision으로 기록한다. 단순히 어휘를 확인하기 위해 `CONTEXT.md`를 *읽는 것*은 이 스킬이 아니다. 그것은 어떤 스킬도 할 수 있는 한 줄짜리 습관이다. 이 스킬은 모델을 소비하는 것이 아니라 바꿀 때 사용한다.

## 파일 구조

대부분의 repo는 단일 context를 가진다.

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

root에 `CONTEXT-MAP.md`가 있다면 repo는 여러 context를 가진다. map은 각 context가 어디에 있는지 가리킨다.

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

파일은 필요할 때만 생성한다. 쓸 것이 있을 때만 만든다. `CONTEXT.md`가 없다면 첫 번째 용어가 확정될 때 생성한다. `docs/adr/`이 없다면 첫 번째 ADR이 필요할 때 생성한다.

## 세션 중

### Glossary와 대조해 이의 제기

사용자가 `CONTEXT.md`의 기존 언어와 충돌하는 용어를 사용하면 즉시 짚는다. "glossary에서는 'cancellation'을 X로 정의하지만, 지금은 Y를 뜻하는 것 같습니다. 어느 쪽인가요?"

### 흐릿한 언어 다듬기

사용자가 모호하거나 여러 의미로 쓰이는 용어를 사용하면 정확한 canonical term을 제안한다. "account라고 하셨는데, Customer를 뜻하나요, User를 뜻하나요? 둘은 다른 것입니다."

### 구체적 scenario 논의

도메인 관계를 논의할 때는 구체적 scenario로 stress-test한다. edge case를 찌르고 개념 사이의 경계를 정확히 말하게 만드는 scenario를 만들어 낸다.

### 코드와 교차 확인

사용자가 어떤 동작 방식을 말하면 코드도 그에 동의하는지 확인한다. 모순을 발견하면 드러낸다. "코드는 전체 Order를 취소하지만, 방금 부분 취소가 가능하다고 하셨습니다. 어느 쪽이 맞나요?"

### CONTEXT.md 즉시 갱신

용어가 확정되면 그 자리에서 `CONTEXT.md`를 갱신한다. 모아서 처리하지 않는다. 발생하는 즉시 기록한다. [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)의 형식을 사용한다.

`CONTEXT.md`에는 implementation detail이 전혀 없어야 한다. `CONTEXT.md`를 spec, scratch pad, implementation decision 저장소로 취급하지 않는다. 이것은 glossary일 뿐이다.

### ADR은 아껴서 제안

다음 세 가지가 모두 참일 때만 ADR 생성을 제안한다.

1. **되돌리기 어려움** - 나중에 마음을 바꾸는 비용이 의미 있게 크다.
2. **맥락 없이는 놀라움** - 미래의 독자가 "왜 이렇게 했지?"라고 궁금해할 것이다.
3. **실제 trade-off의 결과** - 진짜 대안들이 있었고, 특정한 이유로 하나를 골랐다.

셋 중 하나라도 빠지면 ADR은 건너뛴다. [ADR-FORMAT.md](./ADR-FORMAT.md)의 형식을 사용한다.

# CONTEXT.md 형식

## 구조

```md
# {Context Name}

{이 context가 무엇이고 왜 존재하는지 한두 문장으로 설명}

## Language

**Order**:
{이 용어에 대한 한두 문장 설명}
_Avoid_: Purchase, transaction

**Invoice**:
배송 후 customer에게 보내는 payment 요청.
_Avoid_: Bill, payment request

**Customer**:
order를 생성하는 사람 또는 조직.
_Avoid_: Client, buyer, account
```

## 규칙

- **분명한 입장을 가진다.** 같은 개념에 여러 단어가 있다면 가장 좋은 하나를 고르고 나머지는 `_Avoid_` 아래에 나열한다.
- **정의는 타이트하게 유지한다.** 최대 한두 문장으로 쓴다. 그것이 무엇을 하는지가 아니라 무엇인지를 정의한다.
- **이 프로젝트 context에 특화된 용어만 포함한다.** timeout, error type, utility pattern 같은 일반 프로그래밍 개념은 프로젝트에서 널리 사용하더라도 여기에 속하지 않는다. 용어를 추가하기 전에 묻는다. 이것은 이 context에 고유한 개념인가, 아니면 일반 프로그래밍 개념인가? 전자만 포함한다.
- **자연스러운 cluster가 생기면 subheading 아래에 용어를 묶는다.** 모든 용어가 하나의 응집된 영역에 속한다면 flat list도 괜찮다.

## Single context vs multi-context repo

**Single context(대부분의 repo):** repo root에 `CONTEXT.md` 하나.

**Multiple contexts:** repo root의 `CONTEXT-MAP.md`가 context 목록, 위치, 서로의 관계를 나열한다.

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — customer order를 받고 추적한다
- [Billing](./src/billing/CONTEXT.md) — invoice를 생성하고 payment를 처리한다
- [Fulfillment](./src/fulfillment/CONTEXT.md) — warehouse picking과 shipping을 관리한다

## Relationships

- **Ordering → Fulfillment**: Ordering은 `OrderPlaced` event를 emit하고, Fulfillment는 이를 consume해 picking을 시작한다
- **Fulfillment → Billing**: Fulfillment는 `ShipmentDispatched` event를 emit하고, Billing은 이를 consume해 invoice를 생성한다
- **Ordering ↔ Billing**: `CustomerId`와 `Money`를 shared type으로 사용한다
```

이 스킬은 어떤 구조가 적용되는지 추론한다.

- `CONTEXT-MAP.md`가 있으면 읽어서 context를 찾는다.
- root `CONTEXT.md`만 있으면 single context다.
- 둘 다 없다면 첫 번째 용어가 확정될 때 root `CONTEXT.md`를 필요에 따라 생성한다.

context가 여러 개라면 현재 주제가 어느 context와 관련되는지 추론한다. 불분명하면 질문한다.

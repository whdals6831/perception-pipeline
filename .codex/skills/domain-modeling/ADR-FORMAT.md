# ADR 형식

ADR은 `docs/adr/`에 두고 `0001-slug.md`, `0002-slug.md`처럼 순차 번호를 사용한다.

`docs/adr/` 디렉터리는 첫 번째 ADR이 필요할 때만 생성한다.

## 템플릿

```md
# {결정의 짧은 제목}

{1-3문장: 맥락은 무엇이고, 무엇을 결정했으며, 왜 그렇게 결정했는지}
```

이것으로 충분하다. ADR은 단일 문단일 수 있다. 가치는 결정을 내렸다는 사실과 그 *이유*를 기록하는 데 있다. 섹션을 채우는 데 있지 않다.

## 선택 섹션

진짜 가치가 있을 때만 포함한다. 대부분의 ADR에는 필요 없다.

- **Status** frontmatter(`proposed | accepted | deprecated | superseded by ADR-NNNN`) - 결정을 다시 검토할 때 유용하다.
- **Considered Options** - 거절한 대안을 기억할 가치가 있을 때만 포함한다.
- **Consequences** - 자명하지 않은 downstream effect를 짚어야 할 때만 포함한다.

## 번호 매기기

`docs/adr/`에서 기존 가장 큰 번호를 찾아 1을 더한다.

## ADR 제안 시점

다음 세 가지가 모두 참이어야 한다.

1. **되돌리기 어려움** - 나중에 마음을 바꾸는 비용이 의미 있게 크다.
2. **맥락 없이는 놀라움** - 미래의 독자가 코드를 보고 "도대체 왜 이렇게 했지?"라고 궁금해할 것이다.
3. **실제 trade-off의 결과** - 진짜 대안들이 있었고, 특정한 이유로 하나를 골랐다.

결정을 되돌리기 쉽다면 건너뛴다. 그냥 되돌리면 된다. 놀랍지 않다면 아무도 이유를 궁금해하지 않는다. 실제 대안이 없었다면 "당연한 일을 했다" 말고 기록할 것이 없다.

### 해당하는 것

- **아키텍처 형태.** "monorepo를 사용한다." "write model은 event-sourced이고, read model은 Postgres로 projection된다."
- **context 사이의 integration pattern.** "Ordering과 Billing은 synchronous HTTP가 아니라 domain event로 통신한다."
- **lock-in을 수반하는 기술 선택.** database, message bus, auth provider, deployment target. 모든 library가 아니라, 교체에 한 분기 정도가 걸릴 만한 것만 해당한다.
- **boundary와 scope 결정.** "Customer data는 Customer context가 소유하고, 다른 context는 ID로만 참조한다." 명시적인 no는 yes만큼 가치 있다.
- **당연한 경로에서 의도적으로 벗어난 결정.** "X 때문에 ORM 대신 manual SQL을 사용한다." 합리적인 독자가 반대를 예상할 만한 모든 것. 이런 기록은 다음 engineer가 의도된 결정을 "고치지" 않게 막는다.
- **코드에 보이지 않는 제약.** "compliance requirement 때문에 AWS를 사용할 수 없다." "partner API contract 때문에 response time은 200ms 미만이어야 한다."
- **거절 이유가 자명하지 않은 대안.** GraphQL을 고려했지만 미묘한 이유로 REST를 선택했다면 기록한다. 그렇지 않으면 6개월 뒤 누군가 GraphQL을 다시 제안할 것이다.

# Design It Twice

사용자가 선택한 deepening 후보에 대해 대안 interface를 탐색하고 싶어 할 때 이 병렬 sub-agent 패턴을 사용한다. "Design It Twice"(Ousterhout)에 기반한다. 첫 번째 아이디어가 최선일 가능성은 낮다.

[SKILL.md](SKILL.md)의 어휘인 **module**, **interface**, **seam**, **adapter**, **leverage**를 사용한다.

## 절차

### 1. 문제 공간 정의

sub-agent를 띄우기 전에 선택한 후보의 문제 공간을 사용자에게 설명한다.

- 새 interface가 만족해야 하는 제약
- 의존하게 될 dependency와 그 category([DEEPENING.md](DEEPENING.md) 참고)
- 제약을 구체화하기 위한 대략적인 예시 코드 sketch. 제안이 아니라 제약을 구체적으로 만들기 위한 수단이다.

이를 사용자에게 보여 준 뒤 즉시 2단계로 진행한다. 사용자는 읽고 생각하고, sub-agent들은 병렬로 작업한다.

### 2. Sub-agent 실행

Agent 도구를 사용해 3개 이상의 sub-agent를 병렬로 실행한다. 각 sub-agent는 deepened module을 위한 **완전히 다른** interface를 만들어야 한다.

각 sub-agent에는 별도의 기술 brief를 제공한다. brief에는 file path, coupling detail, [DEEPENING.md](DEEPENING.md)의 dependency category, seam 뒤에 놓이는 것이 포함된다. 이 brief는 1단계의 사용자-facing 문제 공간 설명과 독립적이다. 각 agent에는 서로 다른 설계 제약을 준다.

- Agent 1: "interface를 최소화하라. entry point는 최대 1-3개를 목표로 한다. entry point당 leverage를 극대화하라."
- Agent 2: "유연성을 극대화하라. 많은 use case와 extension을 지원하라."
- Agent 3: "가장 흔한 caller에 최적화하라. 기본 case를 사소하게 만들라."
- Agent 4(해당하는 경우): "cross-seam dependency를 위해 ports & adapters 중심으로 설계하라."

각 sub-agent가 아키텍처 언어와 프로젝트 도메인 언어에 맞춰 일관되게 이름 붙일 수 있도록 brief에 [SKILL.md](SKILL.md) 어휘와 CONTEXT.md 어휘를 모두 포함한다.

각 sub-agent는 다음을 출력한다.

1. Interface(types, methods, params, 그리고 invariants, ordering, error modes)
2. caller가 어떻게 사용하는지 보여 주는 usage example
3. implementation이 seam 뒤에 숨기는 것
4. dependency strategy와 adapters([DEEPENING.md](DEEPENING.md) 참고)
5. trade-off. leverage가 높은 곳과 얇은 곳

### 3. 제시와 비교

사용자가 각 설계를 이해할 수 있도록 설계를 순서대로 제시한 뒤, 글로 비교한다. **depth**(interface에서의 leverage), **locality**(변경이 모이는 곳), **seam placement**를 기준으로 대조한다.

비교한 뒤 자신의 추천을 제시한다. 어떤 설계가 가장 강하고 왜 그런지 말한다. 서로 다른 설계의 요소를 잘 결합할 수 있다면 hybrid를 제안한다. 분명한 의견을 낸다. 사용자는 선택지 목록이 아니라 강한 판단을 원한다.

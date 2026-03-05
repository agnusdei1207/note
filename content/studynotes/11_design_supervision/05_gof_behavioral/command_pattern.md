+++
title = "커맨드 패턴 (Command Pattern)"
categories = ["studynotes-11_design_supervision"]
+++

# 커맨드 패턴 (Command Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 커맨드 패턴은 **요청(Action) 자체를 객체로 캡슐화**하여, 요청자(Invoker)와 수신자(Receiver)의 결합을 분리하고 실행 취소(Undo), 재실행(Redo), 로깅, 큐잉을 지원합니다.
> 2. **가치**: 요청의 발생 시점과 실행 시점을 분리할 수 있어, 스마트홈 리모컨, 워크플로 엔진, 트랜잭션 관리 등에 필수적입니다.
> 3. **융합**: 스마트폰의 알림 센터, 게임의 키 입력 처리, 그리고 CQRS의 Command 객체 설계와 연관됩니다.

---

## Ⅰ. 개요

### 1. 구성요소

| 구성요소 | 역할 |
|:---:|:---|
| **Command** | 요청 캡슐화 인터페이스 |
| **ConcreteCommand** | 실제 요청 구현 |
| **Invoker** | 명령 실행 주체 |
| **Receiver** | 실제 작업 수행 |

### 💡 비유: 스마트홈 리모컨
리모컨(Invoker)의 버튼(Command)을 누르면 TV/조명(Receiver)이 작동. **버튼 = 명령 객체**.

---

## Ⅱ. 구조

```
┌─────────────────────────────────────────────────────────────────┐
│  Client ──► Invoker ──► Command ──► Receiver                   │
│                     (버튼)   (명령)    (TV/조명)                  │
└─────────────────────────────────────────────────────────────────┘

Invoker ──holds──► Command[]
                    │
                    ├── execute()
                    └── undo()
```

---

## Ⅲ. 예시

```kotlin
interface Command { fun execute(); fun undo() }

class Light { fun on() { println("불 켜짐") }; fun off() { println("불 꺼짐") } }

class LightOnCommand(private val light: Light) : Command {
    override fun execute() { light.on() }
    override fun undo() { light.off() }
}

class RemoteControl {
    private val commands = mutableListOf<Command>()
    fun setCommand(cmd: Command) { commands.add(cmd) }
    fun pressButton() { commands.last().execute() }
    fun undo() { commands.removeLast().undo() }
}

// 사용
val remote = RemoteControl()
remote.setCommand(LightOnCommand(Light()))
remote.pressButton()  // 불 켜짐
remote.undo()         // 불 꺼짐
```

---

## Ⅳ. 활용

| 용도 | 예시 |
|:---:|:---|
| **Undo/Redo** | 텍스트 에디터 |
| **Macro** | 반복 작업 자동화 |
| **Queue** | 작업 큐, 스케줄러 |
| **Logging** | 실행 이력 기록 |

---

## 📌 관련 개념
- [옵저버 패턴](./observer_pattern.md): 상태 알림
- [책임 연쇄 패턴](./chain_of_responsibility.md): 요청 전달
- [메멘토 패턴](./memento_pattern.md): 상태 복원

---

## 👶 어린이를 위한 비유
커맨드 패턴은 **엘리베이터 버튼**과 같아요. "3층" 버튼을 누르면(Command), 엘리베이터(Receiver)가 3층으로 올라가요. 버튼은 **"3층으로 가라"는 명령을 담고 있어요!**

+++
title = "Claude Code effort를 high로 설정하는 방법"
date = "2026-04-07"
[extra]
keyword = "Claude_Code_Effort_High_Setting"
+++

# Claude Code effort를 high로 설정하는 방법

Claude Code에는 답변 속도와 추론 강도를 조절하는 `effort` 설정이 있다. 간단한 작업은 `low`나 `medium`으로도 충분하지만, 코드 구조를 길게 추적하거나 복잡한 수정 방향을 잡아야 할 때는 `high`가 더 안정적으로 동작하는 편이다.

설정 방법은 크게 세 가지다. 가장 간단한 방법은 현재 실행하는 세션에서만 `high`를 쓰는 것이다.

```bash
claude --effort high
```

이렇게 실행하면 그 세션에 한해서 `high`가 적용된다. 한 번만 집중도를 높여서 쓰고 싶을 때 적합하다.

이미 Claude Code 안에 들어와 있다면 슬래시 명령으로 바꿀 수도 있다.

```text
/effort high
```

이 방식은 현재 대화 세션에 바로 적용하는 용도다. 평소에는 기본값으로 쓰다가, 특정 작업에서만 잠깐 올리고 싶을 때 편하다.

항상 `high`로 시작하고 싶다면 사용자 설정 파일에 기본값을 넣으면 된다. Claude Code의 사용자 설정 파일은 보통 `~/.claude/settings.json`이다. 여기에 아래처럼 `effortLevel`을 추가하면 된다.

```json
{
  "skipDangerousModePermissionPrompt": true,
  "effortLevel": "high"
}
```

이미 다른 설정이 들어 있다면 지우지 말고 같은 JSON 객체 안에 `effortLevel`만 추가하면 된다. 이렇게 설정해두면 다음부터 Claude Code를 실행할 때 기본 `effort`가 `high`로 잡힌다.

여기서 자주 헷갈리는 점이 하나 있다. `effort` 설정은 Claude Code가 모델이 이 기능을 지원한다고 판단해야 화면이나 명령에서 자연스럽게 동작한다. 기본 Anthropic 모델에서는 대체로 잘 동작하지만, MiniMax M2.7처럼 커스텀 모델 경로를 쓰는 경우에는 `effort` UI나 명령이 제한적으로 보일 수 있다.

즉, 설정 방법 자체는 같지만, 커스텀 모델을 붙였을 때는 Claude Code가 그 모델의 기능 지원 범위를 완전히 인식하지 못할 수 있다. 이 경우에는 설정 파일에 `effortLevel = high` 수준으로 값을 넣어도 체감상 변화가 약하거나, 슬래시 명령이 노출되지 않을 수 있다.

정리하면, 한 번만 적용하려면 `claude --effort high`, 현재 세션에서 즉시 바꾸려면 `/effort high`, 기본값으로 고정하려면 `~/.claude/settings.json`의 `effortLevel`을 `high`로 두면 된다. 일반적인 Claude 모델에서는 이 방법이 바로 통하고, 커스텀 모델에서는 모델 지원 방식에 따라 일부 제약이 있을 수 있다.

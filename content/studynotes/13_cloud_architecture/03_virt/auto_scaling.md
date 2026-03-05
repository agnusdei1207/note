+++
title = "오토 스케일링 (Auto Scaling)"
date = 2024-05-13
description = "트래픽과 부하에 따라 컴퓨팅 자원을 자동으로 확장/축소하여 가용성을 보장하고 비용을 최적화하는 클라우드 핵심 기술"
weight = 79
[taxonomies]
categories = ["studynotes-cloud_architecture"]
tags = ["Auto Scaling", "Scale-out", "Scale-in", "Horizontal Scaling", "EC2", "Kubernetes HPA"]
+++

# 오토 스케일링 (Auto Scaling) 심층 분석

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 시스템 부하(CPU, 메모리, 네트워크 트래픽, 사용자 정의 메트릭)를 실시간 모니터링하여, 임계치 초과 시 컴퓨팅 자원(서버, 컨테이너)을 자동으로 증설(Scale-out)하고, 부하 감소 시 자원을 해제(Scale-in)하여 탄력적 운영을 실현하는 기술입니다.
> 2. **가치**: 트래픽 급증 시 **서비스 중단 0%**, 유휴 시간에는 **비용 30~70% 절감**을 동시에 달성하며, 수동 개입 없이 24/7 자동 대응으로 운영 효율을 극대화합니다.
> 3. **융합**: 로드 밸런서와 연동하여 트래픽 분산, CloudWatch/Prometheus 메트릭 기반 트리거, 쿠버네티스 HPA/VPA/CA와 결합하여 컨테이너 및 노드 레벨 스케일링을 구현합니다.

---

## Ⅰ. 개요 (Context & Background)

오토 스케일링(Auto Scaling)은 클라우드 환경에서 애플리케이션의 부하에 따라 컴퓨팅 자원을 자동으로 조절하는 기술입니다. 전통적인 온프레미스 환경에서는 트래픽 증가에 대비하여 미리 서버를 과도하게 구축(Over-provisioning)해야 했으나, 클라우드에서는 필요한 만큼만 사용하고 비용을 지불할 수 있습니다.

**💡 비유**: 오토 스케일링은 **'탄력 있는 고무줄'**과 같습니다. 고무줄을 잡아당기면(트래픽 증가) 늘어나고, 놓으면(트래픽 감소) 다시 줄어듭니다. 마찬가지로 오토 스케일링은 트래픽이 많으면 서버를 늘리고, 적으면 줄여서 딱 맞는 크기를 유지합니다. 식당으로 비유하면, 손님이 많을 때는 테이블을 늘리고 직원을 더 뽑고, 손님이 없으면 다시 줄이는 것과 같습니다.

**등장 배경 및 발전 과정**:
1. **전통적 데이터센터의 한계**: 최대 트래픽을 기준으로 서버를 구매하여 평상시 활용률이 10~20%에 불과했습니다.
2. **AWS Auto Scaling (2009)**: EC2 인스턴스 그룹을 자동으로 확장/축소하는 기능을 최초로 제공했습니다.
3. **예측 기반 스케일링 (2018~)**: 머신러닝을 활용하여 트래픽 패턴을 학습하고 선제적으로 스케일링하는 기능이 추가되었습니다.
4. **쿠버네티스 HPA/VPA**: 컨테이너 환경에서 파드와 노드를 자동으로 스케일링하는 기능이 표준화되었습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소: Auto Scaling 핵심 요소

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | AWS 서비스 | 비유 |
|---|---|---|---|---|
| **Launch Template** | 인스턴스 생성 명세 | AMI, 타입, SG, UserData | EC2 Launch Template | 직원 채용 요건 |
| **Auto Scaling Group** | 인스턴스 그룹 관리 | Min/Max/Desired 크기 | ASG | 직원 팀 |
| **Scaling Policy** | 스케일링 규칙 | Simple, Step, Target Tracking | Scaling Policy | 채용/해고 기준 |
| **CloudWatch Alarm** | 메트릭 임계치 모니터링 | CPU, 메모리, 커스텀 메트릭 | CloudWatch Alarms | 업무량 측정기 |
| **Health Check** | 인스턴스 상태 확인 | EC2/ELB 상태 검사 | Health Check Type | 건강 검진 |
| **Load Balancer** | 트래픽 분산 | ALB/NLB 연동 | ALB/NLB Target Group | 업무 분배 |
| **Cool-down** | 스케일링 안정화 | 연속 스케일링 방지 | Default 300초 | 적응 기간 |

### 정교한 구조 다이어그램: Auto Scaling 전체 아키텍처

```ascii
┌─────────────────────────────────────────────────────────────────────────────┐
│                    [ Auto Scaling Architecture ]                             │
│                     (AWS EC2 Auto Scaling + ALB)                             │
└─────────────────────────────────────────────────────────────────────────────┘

                    [ Users / Traffic ]
                          │
                          ▼
               ┌────────────────────┐
               │   Route 53 (DNS)   │
               │   or CloudFront    │
               └──────────┬─────────┘
                          │
                          ▼
               ┌────────────────────┐
               │  Application Load  │
               │     Balancer       │◄──── Target Group
               │      (ALB)         │      (Health Checks)
               └──────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────────────────────────────────────────────────────────┐
│                     Auto Scaling Group (ASG)                       │
│                                                                    │
│  Configuration:                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Min: 2   |   Desired: 4   |   Max: 10   |   Cooldown: 300s  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   EC2-1     │ │   EC2-2     │ │   EC2-3     │ │   EC2-4     │ │
│  │  (Active)   │ │  (Active)   │ │  (Active)   │ │  (Active)   │ │
│  │  AZ-a       │ │  AZ-b       │ │  AZ-a       │ │  AZ-b       │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│                                                                    │
│  [ Scaling Policies ]                                              │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ 1. Target Tracking: CPU 50%                                  │ │
│  │ 2. Step Scaling:                                             │ │
│  │    - CPU > 60%: +1 instance                                  │ │
│  │    - CPU > 70%: +2 instances                                 │ │
│  │    - CPU > 80%: +3 instances                                 │ │
│  │ 3. Predictive Scaling: (ML-based forecast)                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
               ┌────────────────────┐
               │    CloudWatch      │
               │    Metrics         │
               │  ┌──────────────┐  │
               │  │ CPU: 75%     │  │
               │  │ Memory: 60%  │  │
               │  │ Network: 40% │  │
               │  │ Request: 500 │  │
               │  └──────┬───────┘  │
               └─────────┼──────────┘
                         │
                         ▼
               ┌────────────────────┐
               │  CloudWatch Alarm  │
               │  "CPU > 70%"       │
               │  - State: ALARM    │
               │  - Action: Scale   │
               └─────────┬──────────┘
                         │
                         │ Trigger
                         ▼
               ┌────────────────────┐
               │  Scaling Policy    │
               │  Execution         │
               │  +2 instances      │
               └────────────────────┘


[ Scaling Events Timeline ]

Time    │ CPU%  │ Action                          │ Instances
────────┼───────┼─────────────────────────────────┼──────────
10:00   │ 40%   │ Normal operation                │ 2 instances
10:15   │ 55%   │ Target Tracking: Approaching    │ 2 instances
10:30   │ 68%   │ Target Tracking: Scale Out +1   │ 3 instances
10:31   │ 65%   │ Cooldown period (300s)          │ 3 instances
10:40   │ 72%   │ Step Scaling: +2 instances      │ 5 instances
10:41   │ 60%   │ Cooldown period                 │ 5 instances
11:00   │ 45%   │ Scale In: -1 instance           │ 4 instances
11:05   │ 40%   │ Normal operation                │ 4 instances
```

### 심층 동작 원리: 스케일링 정책 비교

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Auto Scaling Policy Types                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  [ 1. Simple Scaling ]                                                      │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  CPU > 70% ────► Add 1 instance                                    │   │
│  │  CPU < 30% ────► Remove 1 instance                                 │   │
│  │                                                                    │   │
│  │  특징:                                                             │   │
│  │  - 가장 단순한 정책                                                │   │
│  │  - Cooldown 필수 (연속 스케일링 방지)                              │   │
│  │  - 단점: 급격한 트래픽 변화에 대응 느림                            │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 2. Step Scaling ]                                                        │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  CPU 60-70%  ────► Add 1 instance                                  │   │
│  │  CPU 70-80%  ────► Add 2 instances                                 │   │
│  │  CPU > 80%   ────► Add 3 instances                                 │   │
│  │  CPU < 30%   ────► Remove 1 instance                               │   │
│  │                                                                    │   │
│  │  특징:                                                             │   │
│  │  - 위반 정도에 따라 다른 스케일링 크기                             │   │
│  │  - 급격한 트래픽에 더 빠른 대응                                    │   │
│  │  - CloudWatch Alarm 위반 임계값 활용                               │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 3. Target Tracking Scaling ]                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  Target: CPU = 50%                                                 │   │
│  │                                                                    │   │
│  │         100% ┤                                                     │   │
│  │          80% ┤       * (Current: 75%)                              │   │
│  │          60% ┤    *        (Scale Out)                             │   │
│  │          50% ┤─── ─ ─ ─ ─ ─ (Target)                               │   │
│  │          40% ┤                                                     │   │
│  │          20% ┤                * (Scale In)                         │   │
│  │           0% └─────────────────────────────                        │   │
│  │                                                                    │   │
│  │  특징:                                                             │   │
│  │  - 원하는 메트릭 값 유지를 자동 계산                               │   │
│  │  - 가장 권장되는 방식                                              │   │
│  │  - 복잡한 계산 불필요                                              │   │
│  │  - 예: "평균 CPU 50% 유지"                                         │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  [ 4. Predictive Scaling ]                                                  │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                                                                    │   │
│  │  Machine Learning 기반 예측                                        │   │
│  │                                                                    │   │
│  │  Historical Data ────► ML Model ────► Forecast ────► Pre-scale    │   │
│  │                                                                    │   │
│  │  Time ──────────────────────────────────────────────►             │   │
│  │         │         │         │         │         │                 │   │
│  │  00:00  Low       08:00     12:00     18:00     22:00             │   │
│  │                   High      Peak      High      Low               │   │
│  │                   ▲         ▲         ▲                           │   │
│  │                   │         │         │                           │   │
│  │             Pre-scale   Pre-scale   Pre-scale                     │   │
│  │             (7:30)      (11:30)     (17:30)                       │   │
│  │                                                                    │   │
│  │  특징:                                                             │   │
│  │  - 과거 데이터 학습으로 미리 스케일링                              │   │
│  │  - 주기적 트래픽 패턴에 최적                                       │   │
│  │  - 24시간 데이터 필요                                              │   │
│  │                                                                    │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 코드: Terraform Auto Scaling 구성

```hcl
# Production-Ready Auto Scaling Group

# 1. Launch Template (인스턴스 명세)
resource "aws_launch_template" "web" {
  name_prefix   = "web-server-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.medium"

  key_name = aws_key_pair.main.key_name

  network_interfaces {
    associate_public_ip_address = false
    security_groups             = [aws_security_group.web.id]
    delete_on_termination       = true
  }

  iam_instance_profile {
    name = aws_iam_instance_profile.web.name
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              EOF
  )

  monitoring {
    enabled = true
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "web-server"
      Environment = "production"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# 2. Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  vpc_zone_identifier = aws_subnet.private[*].id

  min_size         = 2
  max_size         = 10
  desired_capacity = 3

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  # 로드 밸런서 연결
  target_group_arns = [aws_lb_target_group.web.arn]

  # 인스턴스 보호 (Scale-in 시 삭제 방지)
  protect_from_scale_in = false

  # 초기화 지연
  initial_lifecycle_hook {
    name                 = "web-instance-launching"
    default_result       = "CONTINUE"
    heartbeat_timeout    = 300
    lifecycle_transition = "autoscaling:EC2_INSTANCE_LAUNCHING"
  }

  # 종료 정책 (어떤 인스턴스부터 종료할지)
  termination_policies = [
    "OldestInstance",      # 가장 오래된 인스턴스 우선 종료
    "ClosestToNextInstanceHour"  # 다음 청구 시간에 가까운 것
  ]

  # 인스턴스 분산 (모든 AZ에 균등 분배)
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
      instance_warmup        = 300
    }
    triggers = ["tag"]  # 태그 변경 시 롤링 업데이트
  }

  dynamic "tag" {
    for_each = {
      Name        = "web-server"
      Environment = "production"
      ManagedBy   = "terraform"
    }
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# 3. Target Tracking Scaling Policy (CPU 기반)
resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "cpu-target-tracking"
  autoscaling_group_name = aws_autoscaling_group.web.name

  policy_type = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0  # 목표 CPU 50%

    # Scale-out 후 300초 동안 추가 스케일링 대기
    scale_out_cooldown = 300

    # Scale-in 후 300초 동안 추가 스케일링 대기
    scale_in_cooldown = 300

    # Scale-in 비활성화 옵션 (선택)
    # disable_scale_in = true
  }
}

# 4. Step Scaling Policy (Request Count 기반)
resource "aws_cloudwatch_metric_alarm" "high_request_rate" {
  alarm_name          = "high-request-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "RequestCountPerTarget"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Average"
  threshold           = 1000
  treat_missing_data  = "notBreaching"

  dimensions = {
    LoadBalancer = aws_lb.web.arn_suffix
    TargetGroup  = aws_lb_target_group.web.arn_suffix
  }

  alarm_actions = [aws_autoscaling_policy.step_scale_out.arn]
}

resource "aws_autoscaling_policy" "step_scale_out" {
  name                   = "step-scale-out"
  autoscaling_group_name = aws_autoscaling_group.web.name
  policy_type            = "StepScaling"
  adjustment_type        = "ChangeInCapacity"

  step_adjustment {
    scaling_adjustment          = 1
    metric_interval_lower_bound = 0
    metric_interval_upper_bound = 500
  }

  step_adjustment {
    scaling_adjustment          = 2
    metric_interval_lower_bound = 500
    metric_interval_upper_bound = 1000
  }

  step_adjustment {
    scaling_adjustment          = 3
    metric_interval_lower_bound = 1000
  }
}

# 5. Predictive Scaling (머신러닝 기반)
resource "aws_autoscaling_policy" "predictive" {
  name                   = "predictive-scaling"
  autoscaling_group_name = aws_autoscaling_group.web.name

  policy_type = "PredictiveScaling"

  predictive_scaling_configuration {
    metric_specification {
      target_value = 50

      predefined_scaling_metric_specification {
        predefined_metric_type = "ASGAverageCPUUtilization"
      }

      predefined_load_metric_specification {
        predefined_metric_type = "ASGTotalCPUUtilization"
        resource_label         = "testLabel"
      }
    }

    # 예측 결과를 미리 적용 (분석만 할지, 실제 스케일링할지)
    mode = "ForecastAndScale"  # or "ForecastOnly"
  }
}

# 6. Scheduled Scaling (예약 스케일링)
resource "aws_autoscaling_schedule" "scale_out_morning" {
  scheduled_action_name  = "scale-out-morning"
  autoscaling_group_name = aws_autoscaling_group.web.name

  # 매일 오전 9시에 최소 5대로 증설
  recurrence             = "0 9 * * MON-FRI"
  min_size               = 5
  max_size               = 10
  desired_capacity       = 5
}

resource "aws_autoscaling_schedule" "scale_in_night" {
  scheduled_action_name  = "scale-in-night"
  autoscaling_group_name = aws_autoscaling_group.web.name

  # 매일 오후 9시에 최소 2대로 축소
  recurrence             = "0 21 * * MON-FRI"
  min_size               = 2
  max_size               = 10
  desired_capacity       = 2
}
```

### Kubernetes HPA (Horizontal Pod Autoscaler)

```yaml
# Kubernetes HPA 구성

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app

  minReplicas: 2
  maxReplicas: 20

  metrics:
  # 1. CPU 기반 스케일링
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

  # 2. 메모리 기반 스케일링
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

  # 3. 커스텀 메트릭 (Prometheus)
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"

  # 4. 외부 메트릭 (External Metrics)
  - type: External
    external:
      metric:
        name: sqs_queue_length
        selector:
          matchLabels:
            queue_name: "orders"
      target:
        type: AverageValue
        averageValue: "10"

  behavior:
    # Scale-out 동작
    scaleUp:
      stabilizationWindowSeconds: 60  # 60초 대기 후 스케일
      policies:
      - type: Percent
        value: 100  # 현재 크기의 100%까지 증가
        periodSeconds: 60
      - type: Pods
        value: 4    # 최대 4개씩 증가
        periodSeconds: 60
      selectPolicy: Max  # 두 정책 중 큰 값 선택

    # Scale-in 동작
    scaleDown:
      stabilizationWindowSeconds: 300  # 5분 대기 후 스케일인
      policies:
      - type: Percent
        value: 10   # 10%씩만 감소
        periodSeconds: 60
      - type: Pods
        value: 2    # 최대 2개씩만 감소
        periodSeconds: 60
      selectPolicy: Min  # 두 정책 중 작은 값 선택

---
# VPA (Vertical Pod Autoscaler)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app

  updatePolicy:
    updateMode: "Auto"  # or "Off" (권장사항만 표시)

  resourcePolicy:
    containerPolicies:
    - containerName: web-container
      minAllowed:
        cpu: 100m
        memory: 256Mi
      maxAllowed:
        cpu: 2000m
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: Scale-up vs Scale-out

| 비교 관점 | Scale-up (수직) | Scale-out (수평) | 상세 분석 |
|---|---|---|---|
| **방식** | 서버 사양 업그레이드 | 서버 대수 증설 | Scale-out이 Auto Scaling에 적합 |
| **중단 시간** | 일반적 (재부팅) | 없음 (무중단) | Scale-out이 고가용성에 유리 |
| **확장 한계** | 하드웨어 한계 존재 | 이론상 무제한 | Scale-out이 대규모 서비스에 필수 |
| **비용 효율** | 고가 서버 필요 | 범용 서버 활용 | Scale-out이 비용 효율적 |
| **복잡성** | 단순 | 분산 시스템 복잡성 | Scale-up이 관리 용이 |
| **적합한 워크로드** | DB, 단일 앱 | 웹, 마이크로서비스 | DB는 Scale-up, 웹은 Scale-out |

### 과목 융합 관점 분석

**운영체제(OS)와의 융합**:
- **프로세스 스케줄링**: CPU 스케줄링과 Auto Scaling의 유사성
- **메모리 관리**: OOM(Out of Memory) 방지를 위한 메모리 기반 스케일링

**네트워크와의 융합**:
- **로드 밸런싱**: Auto Scaling과 로드 밸런서의 필수 연동
- **DNS 기반 라우팅**: Route 53과 연동한 트래픽 라우팅

**데이터베이스와의 융합**:
- **Read Replica**: 읽기 트래픽을 Read Replica로 분산 (RDS Auto Scaling)
- **Connection Pooling**: 스케일링 시 DB 커넥션 관리

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 이커머스 타임세일 대응

**문제 상황**: 이커머스 기업 D사의 타임세일 이벤트 시 평소 100배 트래픽이 발생합니다. 지난번 이벤트에서 서버가 다운되었습니다.

**기술사의 전략적 의사결정**:

1. **트래픽 분석**:

   | 시간대 | 일일 트래픽 | 이벤트 트래픽 | 비고 |
   |---|---|---|---|
   | 평상시 | 1,000 RPS | - | 2대로 충분 |
   | 이벤트 10분 전 | - | 5,000 RPS |预热 필요 |
   | 이벤트 시작 | - | 100,000 RPS | Peak |
   | 이벤트 종료 | - | 10,000 RPS | 급감 |

2. **다층 스케일링 전략**:

   ```
   ┌────────────────────────────────────────────────────────┐
   │              Multi-Layer Auto Scaling Strategy          │
   ├────────────────────────────────────────────────────────┤
   │                                                        │
   │  Layer 1: CDN & Edge (CloudFront)                      │
   │  - Static Content 캐싱                                 │
   │  - Origin 부하 70% 감소                                │
   │                                                        │
   │  Layer 2: Application (EC2 ASG)                        │
   │  - Predictive Scaling: 이벤트 30분 전 Pre-scale       │
   │  - Target Tracking: CPU 60% 목표                       │
   │  - Max: 100 instances                                  │
   │                                                        │
   │  Layer 3: Database (Aurora)                            │
   │  - Read Replica: 2 → 10 Auto Scaling                  │
   │  - Serverless: 자동 스케일링                          │
   │                                                        │
   │  Layer 4: Cache (ElastiCache)                          │
   │  - Redis Cluster: 3 → 10 nodes                        │
   │  - Session & Hot Data 캐싱                            │
   │                                                        │
   └────────────────────────────────────────────────────────┘
   ```

3. **Scheduled Scaling 구성**:

   ```hcl
   # 이벤트 30분 전 스케일 아웃
   resource "aws_autoscaling_schedule" "event_prepare" {
     scheduled_action_name  = "event-prepare"
     autoscaling_group_name = aws_autoscaling_group.web.name
     recurrence             = "30 19 * * *"  # 오후 7:30
     min_size               = 20
     max_size               = 100
     desired_capacity       = 50  # 미리 50대로 증설
   }
   ```

### 도입 시 고려사항 및 안티패턴

- **안티패턴 - Over-Aggressive Scale-in**: 너무 빠르게 Scale-in 하면 썸머타임 문제(thundering herd) 발생. Scale-in은 신중하게.

- **안티패턴 - Ignoring Warm-up Time**: 애플리케이션 초기화 시간을 고려하지 않으면 트래픽을 받을 준비가 안 된 인스턴스에 요청이 들어갑니다.

- **체크리스트**:
  - [ ] Cooldown/Warm-up 시간 설정
  - [ ] Min/Max 크기 적절히 설정
  - [ ] Health Check와 연동
  - [ ] Scale-in 보호 (중요 인스턴스)
  - [ ] 메트릭 선정 (CPU만으로는 부족할 수 있음)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 수동 관리 | Auto Scaling | 개선율 |
|---|---|---|---|
| **서버 다운타임** | 연 2~3회 | 0회 | 100% 제거 |
| **운영 인력** | 24/7 대기 | 자동 대응 | 80% 절감 |
| **비용 효율** | 100% (Over-provision) | 40% | 60% 절감 |
| **장애 대응 시간** | 15~30분 | 1~3분 | 90% 단축 |

### 미래 전망 및 진화 방향

- **AI-Driven Auto Scaling**: 머신러닝이 트래픽 패턴을 학습하여 더 정확한 예측 스케일링
- **Event-Driven Scaling**: 외부 이벤트(마케팅 캠페인 등) 연동 자동 스케일링
- **Multi-Dimensional Scaling**: CPU, 메모리, 네트워크, 비용을 동시에 고려한 최적화

### ※ 참고 표준/가이드
- **AWS Auto Scaling Best Practices**: AWS 공식 가이드
- **Kubernetes HPA Documentation**: K8s 공식 문서
- **Google SRE Book**: 서비스 신뢰성 공학

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [로드 밸런서](@/studynotes/13_cloud_architecture/03_virt/load_balancer.md) : Auto Scaling과 필수 연동
- [쿠버네티스 (Kubernetes)](@/studynotes/13_cloud_architecture/01_native/kubernetes.md) : HPA/VPA/CA 구현
- [CloudWatch](@/studynotes/15_devops_sre/02_observability/observability_fundamentals.md) : 메트릭 기반 스케일링 트리거
- [무중단 배포](@/studynotes/15_devops_sre/03_cicd/deployment_strategies.md) : 스케일링과 연동한 배포
- [SRE](@/studynotes/15_devops_sre/_index.md) : 서비스 신뢰성 공학

---

### 👶 어린이를 위한 3줄 비유 설명
1. 오토 스케일링은 **'탄력 있는 고무줄'**과 같아요. 트래픽이 많으면 늘어나고, 적으면 줄어들어서 딱 맞는 크기를 유지해요.
2. **'식당 주방'**으로 비유하면, 손님이 몰리면 요리사를 더 뽑고, 한산하면 보내는 것과 같아요. 24시간 자동으로 해줘요!
3. 덕분에 **'서버가 터지지 않아요'**. 갑자기 손님이 몰려와도 자동으로 요리사를 더 뽑아서 모두를 응대할 수 있어요!

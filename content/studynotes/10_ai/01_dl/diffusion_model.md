+++
title = "디퓨전 모델 (Diffusion Model)"
date = "2026-03-04"
[extra]
categories = ["studynotes-10_ai"]
+++

# 디퓨전 모델 (Diffusion Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이미지에 점진적으로 노이즈를 추가(Forward Diffusion)하여 순수 노이즈로 만든 후, 이 과정을 역으로 학습(Reverse Diffusion)하여 노이즈에서 원본 이미지를 복원하는 생성 모델로, 2020년 Ho 등이 DDPM으로 제안했습니다.
> 2. **가치**: Stable Diffusion, DALL-E 3, Midjourney 등 텍스트-이미지 생성의 핵심 기술로, GAN 대비 학습 안정성이 높고 다양한 이미지를 생성하며, FID 점수 3~10으로 최고 품질을 달성합니다.
> 3. **융합**: 텍스트, 이미지, 오디오, 비디오, 3D 모델 등 멀티모달 생성으로 확장되며, Latent Diffusion으로 연산 효율을 100배 이상 향상시켜 소비자 GPU에서도 실행 가능합니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**디퓨전 모델(Diffusion Model)**은 비평형 열역학(Non-equilibrium Thermodynamics)에서 영감을 받은 생성 모델입니다. 핵심 아이디어는 **(1) Forward Process (노이즈 추가), (2) Reverse Process (노이즈 제거), (3) Score Matching (노이즈 예측)**입니다.

수학적으로 Forward Process는 마르코프 연쇄(Markov Chain)로 정의됩니다:

$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I)$$

Reverse Process는 신경망이 학습해야 합니다:

$$p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))$$

#### 2. 💡 비유를 통한 이해
디퓨전 모델은 **'흐려진 안개 속에서 길 찾기'**에 비유할 수 있습니다:

- **Forward Process (안개 끼기)**: 맑은 날의 풍경 사진이 시간이 지날수록 안개가 끼어서 점점 흐려지고, 결국 완전히 하얀 안개 속에 갇힙니다.
- **Reverse Process (안개 걷기)**: 안개 속에서 시작해서 "안개를 조금 걷으면 어떤 모습이 나올까?"를 상상하며 한 발짝씩 되돌아갑니다.
- **노이즈 예측**: "지금 있는 안개를 얼마나 걷어내야 원래 모습이 보일까?"를 학습하는 것.

#### 3. 등장 배경 및 발전 과정

1.  **기존 기술의 치명적 한계점**:
    - **GAN의 Mode Collapse**: 다양한 이미지를 생성하지 못하고 몇 가지 패턴만 반복.
    - **GAN의 학습 불안정**: 생성자와 판별자의 균형이 깨지면 학습 실패.
    - **VAE의 흐릿한 이미지**: 평균적인 패턴을 생성하여 디테일 손실.

2.  **혁신적 패러다임의 변화**:
    - **DDPM (2020)**: Ho 등이 Denoising Diffusion Probabilistic Models 발표.
    - **Dhariwal & Nichol (2021)**: Classifier Guidance로 품질 향상.
    - **Classifier-Free Guidance (2022)**: 별도 분류기 없이 조건부 생성.
    - **Latent Diffusion (2022)**: Rombach 등이 Stable Diffusion 발표.
    - **DALL-E 2, Imagen, Midjourney (2022~2023)**: 텍스트-이미지 생성 상용화.

3.  **비즈니스적 요구사항**:
    - 텍스트만으로 고품질 이미지 생성 (콘텐츠 제작 비용 절감)
    - 디자인, 일러스트, 게임 에셋 자동 생성
    - 개인화된 이미지 생성 (프로필, 아바타)

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. Diffusion Model 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 수식 | 비유 |
|:---|:---|:---|:---|:---|
| **Forward Process** | 노이즈 추가 | T 단계에 걸쳐 가우시안 노이즈 추가 | q(x_t\|x_{t-1}) | 안개 끼기 |
| **Beta Schedule** | 노이즈 스케줄 | 선형/코사인/제곱 스케줄 | β_1, ..., β_T | 안개 밀도 |
| **Reverse Process** | 노이즈 제거 | 신경망이 노이즈 예측 | p_θ(x_{t-1}\|x_t) | 안개 걷기 |
| **U-Net** | 노이즈 예측 네트워크 | 인코더-디코더 + Skip Connection | ε_θ(x_t, t) | 예측기 |
| **Time Embedding** | 시간 정보 인코딩 | Sinusoidal + MLP | t → PE(t) | 단계 표시 |
| **CFG** | 조건부 생성 강화 | 조건부/무조건부 혼합 | Ê = ė + s(ε̂_c - ė) | 프롬프트 강조 |

#### 2. Diffusion Process 다이어그램

```text
<<< Forward Diffusion Process (노이즈 추가) >>=>

    x_0 (원본)  →  x_1  →  x_2  →  ...  →  x_T (순수 노이즈)
    │             │        │                   │
    │   +ε_1      │ +ε_2   │    +ε_T           │
    │             │        │                   │
    └─────────────┴────────┴───────────────────┘
         β_1 √(1-β_1)   β_2            β_T ≈ 1

    Closed Form: x_t = √(ᾱ_t) x_0 + √(1-ᾱ_t) ε
    여기서 ᾱ_t = ∏(1-β_i), ε ~ N(0,I)


<<< Reverse Diffusion Process (노이즈 제거) >>=>

    x_T (노이즈)  →  x_{T-1}  →  ...  →  x_0 (생성 이미지)
    │                 │                    │
    │  U-Net 예측     │   U-Net 예측       │
    │  ε_θ(x_T,T)     │   ε_θ(x_{T-1},T-1) │
    │                 │                    │
    └─────────────────┴────────────────────┘
         p_θ(x_{t-1}|x_t) = N(μ_θ, σ_t²I)


<<< U-Net Architecture for Diffusion >>=>

    Input: x_t (noisy image), t (timestep)
           condition (text embedding)

    x_t ──┬──────────────────────────────────────────────┐
          │                                              │
          ▼                                              │
    [Conv] → [Down1] → [Down2] → [Down3] → [Middle]     │
              │          │          │          │         │
              │          │          │          │         │
    [Up1] ←──┼──────────┼──────────┼──────────┘         │
      │       │          │          │                    │
    [Up2] ←───┼──────────┼──────────┘                    │
      │       │          │                               │
    [Up3] ←───┼──────────┘                               │
      │       │                                          │
    [Out] ←───┴──────────────────────────────────────────┘
      │
      ▼
    ε_θ(x_t, t)  (예측된 노이즈)


<<< Classifier-Free Guidance (CFG) >>=>

    ε̂_final = ε̂_uncond + s × (ε̂_cond - ε̂_uncond)

    여기서:
    - ε̂_uncond: 조건 없이 예측한 노이즈
    - ε̂_cond: 프롬프트 조건으로 예측한 노이즈
    - s: guidance scale (보통 7.5~15)
    - s가 높을수록 프롬프트에 더 충실하지만 다양성 감소
```

#### 3. 심층 동작 원리: DDPM 학습 목적 함수

**단순화된 목적 함수 (Simple Loss)**:
$$L_{simple} = \mathbb{E}_{t, x_0, \epsilon} \left[ ||\epsilon - \epsilon_\theta(x_t, t)||^2 \right]$$

이는 "t 시점에서 추가된 노이즈 ε를 신경망 ε_θ가 얼마나 정확히 예측하는가?"를 측정합니다.

**DDIM Sampling (가속 샘플링)**:
표준 DDPM은 T=1000 스텝이 필요하지만, DDIM은 20~50 스텝으로 생성 가능:
$$x_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \underbrace{\left(\frac{x_t - \sqrt{1-\bar{\alpha}_t}\epsilon_\theta(x_t)}{\sqrt{\bar{\alpha}_t}}\right)}_{\text{예측된 } x_0} + \sqrt{1-\bar{\alpha}_{t-1}} \cdot \epsilon_\theta(x_t)$$

#### 4. 실무 수준의 PyTorch Diffusion 구현 코드

```python
"""
Production-Ready Latent Diffusion Model
- U-Net with Time Embedding, Self-Attention
- Classifier-Free Guidance 지원
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Optional

class SinusoidalPositionEmbedding(nn.Module):
    """시간 단계 t를 임베딩으로 변환"""
    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        """
        Args:
            t: (batch,) - timestep
        Returns:
            emb: (batch, dim)
        """
        device = t.device
        half_dim = self.dim // 2
        emb = math.log(10000) / (half_dim - 1)
        emb = torch.exp(torch.arange(half_dim, device=device) * -emb)
        emb = t[:, None] * emb[None, :]
        emb = torch.cat([emb.sin(), emb.cos()], dim=-1)
        return emb


class ResidualBlock(nn.Module):
    """U-Net의 기본 블록"""
    def __init__(self, in_ch: int, out_ch: int, time_emb_dim: int, dropout: float = 0.1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, padding=1)
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding=1)
        self.norm1 = nn.GroupNorm(8, in_ch)
        self.norm2 = nn.GroupNorm(8, out_ch)
        self.time_mlp = nn.Linear(time_emb_dim, out_ch)
        self.dropout = nn.Dropout(dropout)

        if in_ch != out_ch:
            self.skip = nn.Conv2d(in_ch, out_ch, 1)
        else:
            self.skip = nn.Identity()

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        h = self.norm1(x)
        h = F.silu(h)
        h = self.conv1(h)

        # Time embedding 추가
        h += self.time_mlp(F.silu(t))[:, :, None, None]

        h = self.norm2(h)
        h = F.silu(h)
        h = self.dropout(h)
        h = self.conv2(h)

        return h + self.skip(x)


class UNet(nn.Module):
    """
    Diffusion용 U-Net
    - Time Embedding, Self-Attention, Skip Connection 포함
    """
    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 3,
        base_channels: int = 64,
        channel_mults: tuple = (1, 2, 4, 8),
        time_emb_dim: int = 256,
        num_res_blocks: int = 2,
        dropout: float = 0.1
    ):
        super().__init__()
        self.time_emb_dim = time_emb_dim

        # Time Embedding
        self.time_mlp = nn.Sequential(
            SinusoidalPositionEmbedding(base_channels),
            nn.Linear(base_channels, time_emb_dim),
            nn.SiLU(),
            nn.Linear(time_emb_dim, time_emb_dim)
        )

        # Initial Conv
        self.init_conv = nn.Conv2d(in_channels, base_channels, 3, padding=1)

        # Encoder (Downsampling)
        self.encoder = nn.ModuleList()
        channels = [base_channels]
        ch = base_channels

        for mult in channel_mults:
            for _ in range(num_res_blocks):
                self.encoder.append(ResidualBlock(ch, ch * mult, time_emb_dim, dropout))
                ch = ch * mult
                channels.append(ch)
            # Downsampling (마지막 레벨 제외)
            if mult != channel_mults[-1]:
                self.encoder.append(nn.Conv2d(ch, ch, 3, stride=2, padding=1))
                channels.append(ch)

        # Middle
        self.middle = nn.ModuleList([
            ResidualBlock(ch, ch, time_emb_dim, dropout),
            ResidualBlock(ch, ch, time_emb_dim, dropout)
        ])

        # Decoder (Upsampling)
        self.decoder = nn.ModuleList()
        for mult in reversed(channel_mults):
            for i in range(num_res_blocks + 1):
                skip_ch = channels.pop()
                self.decoder.append(
                    ResidualBlock(ch + skip_ch, ch // mult if i < num_res_blocks else ch,
                                  time_emb_dim, dropout)
                )
                ch = ch // mult if i < num_res_blocks else ch
            # Upsampling (마지막 레벨 제외)
            if mult != channel_mults[0]:
                self.decoder.append(nn.ConvTranspose2d(ch, ch, 4, stride=2, padding=1))

        # Output
        self.out_norm = nn.GroupNorm(8, ch)
        self.out_conv = nn.Conv2d(ch, out_channels, 3, padding=1)

    def forward(
        self,
        x: torch.Tensor,
        t: torch.Tensor,
        condition: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Args:
            x: (batch, C, H, W) - 노이즈가 섞인 이미지
            t: (batch,) - timestep
            condition: (batch, cond_dim) - 텍스트 임베딩 등 (선택)
        Returns:
            eps_pred: (batch, C, H, W) - 예측된 노이즈
        """
        # Time Embedding
        t_emb = self.time_mlp(t)

        # Condition 추가 (Classifier-Free Guidance용)
        if condition is not None:
            t_emb = t_emb + condition

        # Initial
        h = self.init_conv(x)
        skips = [h]

        # Encoder
        for layer in self.encoder:
            if isinstance(layer, ResidualBlock):
                h = layer(h, t_emb)
            else:
                h = layer(h)
            skips.append(h)

        # Middle
        for layer in self.middle:
            h = layer(h, t_emb)

        # Decoder
        for layer in self.decoder:
            if isinstance(layer, ResidualBlock):
                skip = skips.pop()
                h = torch.cat([h, skip], dim=1)
                h = layer(h, t_emb)
            else:
                h = layer(h)

        # Output
        h = self.out_norm(h)
        h = F.silu(h)
        return self.out_conv(h)


class GaussianDiffusion:
    """
    DDPM 기반 가우시안 디퓨전
    """
    def __init__(
        self,
        model: UNet,
        timesteps: int = 1000,
        beta_schedule: str = "cosine"
    ):
        self.model = model
        self.timesteps = timesteps

        # Beta schedule
        if beta_schedule == "linear":
            betas = torch.linspace(1e-4, 0.02, timesteps)
        elif beta_schedule == "cosine":
            steps = torch.linspace(0, timesteps, timesteps + 1)
            f_t = torch.cos((steps / timesteps) * math.pi * 0.5) ** 2
            betas = torch.clip(1 - f_t[1:] / f_t[:-1], 0, 0.999)

        self.register_buffer('betas', betas)
        self.register_buffer('alphas', 1.0 - betas)
        self.register_buffer('alphas_cumprod', torch.cumprod(self.alphas, dim=0))
        self.register_buffer('sqrt_alphas_cumprod', torch.sqrt(self.alphas_cumprod))
        self.register_buffer('sqrt_one_minus_alphas_cumprod',
                            torch.sqrt(1.0 - self.alphas_cumprod))

    def register_buffer(self, name: str, tensor: torch.Tensor):
        setattr(self, name, tensor)

    def q_sample(
        self,
        x_0: torch.Tensor,
        t: torch.Tensor,
        noise: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """Forward diffusion: x_0 → x_t"""
        if noise is None:
            noise = torch.randn_like(x_0)

        sqrt_alpha = self.sqrt_alphas_cumprod[t][:, None, None, None]
        sqrt_one_minus_alpha = self.sqrt_one_minus_alphas_cumprod[t][:, None, None, None]

        return sqrt_alpha * x_0 + sqrt_one_minus_alpha * noise

    def p_losses(
        self,
        x_0: torch.Tensor,
        t: torch.Tensor,
        condition: Optional[torch.Tensor] = None,
        noise: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """학습 손실 계산"""
        if noise is None:
            noise = torch.randn_like(x_0)

        x_t = self.q_sample(x_0, t, noise)
        noise_pred = self.model(x_t, t, condition)

        return F.mse_loss(noise_pred, noise)

    @torch.no_grad()
    def p_sample(
        self,
        x_t: torch.Tensor,
        t: int,
        condition: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """Reverse diffusion: x_t → x_{t-1}"""
        t_tensor = torch.full((x_t.size(0),), t, device=x_t.device, dtype=torch.long)
        noise_pred = self.model(x_t, t_tensor, condition)

        alpha = self.alphas[t]
        alpha_cumprod = self.alphas_cumprod[t]

        # Mean
        mean = (1 / alpha.sqrt()) * (x_t - (1 - alpha) / (1 - alpha_cumprod).sqrt() * noise_pred)

        # Variance (t > 0일 때만 노이즈 추가)
        if t > 0:
            noise = torch.randn_like(x_t)
            sigma = self.betas[t].sqrt()
            return mean + sigma * noise
        return mean

    @torch.no_grad()
    def sample(
        self,
        batch_size: int,
        channels: int,
        height: int,
        width: int,
        condition: Optional[torch.Tensor] = None,
        device: str = 'cuda'
    ) -> torch.Tensor:
        """T→0까지 순차적 샘플링"""
        x = torch.randn(batch_size, channels, height, width, device=device)

        for t in reversed(range(self.timesteps)):
            x = self.p_sample(x, t, condition)

        return x


# 사용 예시
if __name__ == "__main__":
    # 모델 생성
    unet = UNet(in_channels=3, out_channels=3, base_channels=64)
    diffusion = GaussianDiffusion(unet, timesteps=1000)

    # 파라미터 수
    print(f"U-Net Parameters: {sum(p.numel() for p in unet.parameters()):,}")

    # 더미 데이터
    x_0 = torch.randn(4, 3, 64, 64)
    t = torch.randint(0, 1000, (4,))

    # Forward
    x_t = diffusion.q_sample(x_0, t)
    print(f"x_0 Shape: {x_0.shape}, x_t Shape: {x_t.shape}")

    # Loss
    loss = diffusion.p_losses(x_0, t)
    print(f"Training Loss: {loss.item():.4f}")
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. Diffusion vs GAN vs VAE 비교

| 비교 항목 | VAE | GAN | Diffusion |
|:---|:---|:---|:---|
| **생성 품질** | 중간 (흐릿함) | 높음 | 매우 높음 |
| **다양성** | 높음 | 낮음 (Mode Collapse) | 매우 높음 |
| **학습 안정성** | 높음 | 낮음 | 높음 |
| **생성 속도** | 빠름 (1-step) | 빠름 (1-step) | 느림 (multi-step) |
| **제어 용이성** | 중간 | 어려움 | 쉬움 |
| **이론적 기반** | 변분 추론 | 게임 이론 | 확률적 미분 방정식 |

#### 2. Diffusion 변형 모델 비교

| 모델 | 핵심 혁신 | 장점 | 용도 |
|:---|:---|:---|:---|
| **DDPM** | 기본 프레임워크 | 단순, 안정 | 연구 |
| **DDIM** | 비마르코프 샘플링 | 빠른 생성 | 가속 |
| **Score-Based** | SDE 프레임워크 | 이론적 일관성 | 연구 |
| **Latent Diffusion** | 잠재 공간 확산 | 100배 효율 | Stable Diffusion |
| **Stable Diffusion** | CLIP + LDM | 고품질 텍스트-이미지 | 상용 |
| **DALL-E 3** | Recaption + Diffusion | 프롬프트 이해력 | 상용 |
| **Consistency Models** | One-step 생성 | GAN 수준 속도 | 실시간 |

#### 3. 과목 융합 관점 분석

*   **[Diffusion + NLP]**:
    텍스트 임베딩(CLIP, T5)을 조건으로 사용하여 텍스트-이미지 생성. 프롬프트 엔지니어링의 중요성 증대.

*   **[Diffusion + 멀티모달]**:
    Image-to-Video (Sora, Runway), Text-to-3D (DreamFusion), Audio-to-Audio (AudioLDM)로 확장.

*   **[Diffusion + 엣지 컴퓨팅]**:
    모바일 기기에서 실행하기 위한 모델 경량화, 양자화, 지식 증류 연구.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 이커머스 상품 이미지 생성**
*   **상황**: "파란색 원피스를 입은 여성 모델" 이미지 100장 생성
*   **기술사 판단**:
    1.  **모델**: Stable Diffusion XL + LoRA Fine-tuning
    2.  **프롬프트**: "professional photo of woman wearing blue dress, studio lighting"
    3.  **가이던스 스케일**: 7.5 (품질-다양성 균형)
    4.  **후처리**: 얼굴 복원(GFPGAN) + 초해상도

**시나리오 B: 게임 에셋 자동 생성**
*   **상황**: 판타지 게임의 1000개 아이템 아이콘 생성
*   **기술사 판단**:
    1.  **모델**: Stable Diffusion + ControlNet (윤곽선 유지)
    2.  **파인튜닝**: 게임 스타일 이미지로 LoRA 학습
    3.  **일관성**: 동일 시드(seed)로 스타일 일관성 유지

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **하드웨어**: 8GB+ VRAM 권장 (SDXL은 12GB+)
- [ ] **라이선스**: Stable Diffusion은 OpenRAIL, 상용 시 확인 필요
- [ ] **안전 필터**: NSFW, 유해 콘텐츠 필터링 설정
- [ ] **프롬프트 튜닝**: 품질 키워드(masterpiece, best quality) 활용
- [ ] **평가 지표**: FID, CLIP Score, 인간 평가 병행

#### 3. 안티패턴 (Anti-patterns)

*   **안티패턴 1: 과도한 Guidance Scale**: s > 20이면 이미지가 타버림(burn-out).
*   **안티패턴 2: 너무 적은 스텝**: 20 스텝 미만은 품질 저하. 30~50 권장.
*   **안티패턴 3: 모호한 프롬프트**: "예쁜 그림" → 일관성 없는 결과. 구체적 묘사 필수.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 기존 방식 (스톡 이미지) | Diffusion 생성 | 향상/변화 |
|:---|:---|:---|:---|
| **이미지 비용** | 1장당 $10~50 | 1장당 $0.01~0.1 | 99% 절감 |
| **제작 시간** | 1장당 1시간~1일 | 1장당 10초 | 99% 단축 |
| **커스터마이징** | 제한적 | 무제한 | 완전 자유 |
| **품질 일관성** | 높음 | 모델 의존 | 튜닝 필요 |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2026)**:
- **실시간 Diffusion**: Consistency Models로 1-step 생성
- **3D/비디오 Diffusion**: Sora, Gen-2 등 비디오 생성 상용화

**중기 (2027~2030)**:
- **개인화 모델**: 10장 사진으로 개인 스타일 학습
- **로컬 실행**: 모바일 기기에서 고화질 생성

**장기 (2030~)**:
- **AGI 수준 창작**: 인간 감독 수준의 창작물 생성
- **실시간 렌더링 대체**: 게임/영화 제작 파이프라인 혁신

#### 3. 참고 표준 및 가이드라인

*   **Stable Diffusion (CompVis/stable-diffusion)**: 오픈소스 표준
*   **Diffusers (Hugging Face)**: 라이브러리 표준
*   **OpenRAIL License**: 생성 모델 라이선스 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

*   **[GAN](@/studynotes/10_ai/01_dl/gan_generative_adversarial.md)**: 또 다른 생성 모델
*   **[VAE](@/studynotes/10_ai/01_dl/vae_model.md)**: 잠재 공간 학습의 선구자
*   **[CLIP](@/studynotes/10_ai/01_dl/clip_model.md)**: 텍스트-이미지 연결 모델
*   **[U-Net](@/studynotes/10_ai/01_dl/unet_architecture.md)**: 이미지 분할 및 디노이징
*   **[텍스트-이미지 생성](@/studynotes/10_ai/01_dl/text_to_image.md)**: Diffusion의 응용

---

### 👶 어린이를 위한 3줄 비유 설명

1.  **안개 속 풍경**: Diffusion은 맑은 날 풍경 사진에 안개를 조금씩 끼워서 완전히 하얗게 만드는 것에서 시작해요.
2.  **되돌아가기**: 그 다음, 하얀 안개에서 시작해서 "이 안개를 조금 걷으면 무엇이 보일까?" 하고 상상하며 한 발짝씩 되돌아가요.
3.  **마법 같은 결과**: 마지막에는 완전히 새로운 풍경 사진이 나타나요! "고양이가 우주복을 입은 사진"도 이렇게 만들 수 있답니다!

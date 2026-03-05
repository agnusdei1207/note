+++
title = "맵리듀스 (MapReduce)"
date = "2026-03-04"
[extra]
categories = "studynotes-14_data_engineering"
+++

# 맵리듀스 (MapReduce)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 맵리듀스는 대용량 데이터를 분산 병렬 처리하기 위한 프로그래밍 모델로, Map(매핑/필터링) → Shuffle(데이터 재분배) → Reduce(집계)의 3단계로 처리합니다.
> 2. **가치**: 복잡한 분산 처리를 단순한 Map/Reduce 함수로 추상화하여, 개발자가 분산 시스템 세부사항을 몰라도 대용량 처리가 가능합니다.
> 3. **융합**: 구글 MapReduce 논문을 기반으로 하둡에 구현되었으나, 현재는 인메모리 기반 Spark로 대체되는 추세입니다.

---

### Ⅰ. 개요

#### 1. 개념
**MapReduce**는 구글이 2004년 발표한 분산 처리 모델입니다. 데이터를 Key-Value 쌍으로 처리하며, Map과 Reduce 두 단계로 구성됩니다.

#### 2. 처리 단계
| 단계 | 역할 | 입력 | 출력 |
|:---|:---|:---|:---|
| **Map** | 데이터 변환/필터링 | (K1, V1) | List(K2, V2) |
| **Shuffle** | 같은 Key끼리 그룹화 | List(K2, V2) | (K2, List(V2)) |
| **Reduce** | 집계/요약 | (K2, List(V2)) | (K3, V3) |

---

### Ⅱ. 처리 과정

```text
<<< MapReduce Word Count Example >>>

Input: "hello world hello hadoop"

[Map Phase]
"hello world"     → (hello,1), (world,1)
"hello hadoop"    → (hello,1), (hadoop,1)

[Shuffle & Sort]
hello  → [1, 1]
world  → [1]
hadoop → [1]

[Reduce Phase]
hello  → 2
world  → 1
hadoop → 1

Output: (hello,2), (world,1), (hadoop,1)
```

---

### Ⅲ. 핵심 원리

**데이터 지역성**:
- Map 태스크를 데이터가 있는 노드에서 실행
- 네트워크 전송 최소화

**디스크 기반 처리**:
- 각 단계 결과를 디스크에 저장
- 반복 작업에 비효율적 → Spark가 인메모리로 개선

---

### Ⅳ. 실무 적용

```java
// Word Count MapReduce (Java)
public class WordCount {
  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        word.set(itr.nextToken());
        context.write(word, one);
      }
    }
  }

  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }
}
```

---

### Ⅴ. 결론

맵리듀스는 분산 처리의 기초를 닦은 모델이며, 현재는 Spark의 RDD 연산으로 진화했습니다.

---

### 관련 개념 맵
- **[Apache Hadoop](@/studynotes/14_data_engineering/01_data_arch/apache_hadoop.md)**
- **[Apache Spark](@/studynotes/14_data_engineering/01_data_arch/apache_spark.md)**
- **[RDD](@/studynotes/14_data_engineering/01_data_arch/rdd.md)**

---

### 어린이를 위한 3줄 비유
1. **나눠서 일하기**: 숙제를 친구들과 나눠서 해요. 각자 맡은 부분을 따로따로 풀어요.
2. **모아서 합치기**: 각자 푼 답을 모아서 선생님께 냅니다.
3. **줄 세우기**: 답을 낼 때는 이름순으로 줄 세워서 정리해요!

작성일: 2026-07-29 (최종 갱신: 2026-08-05)
버전: v30 (Introduction — McDonald(2021) 실제 본문(1단락) 반영 확정,
Jia(2022) 1단락 재인용 추가. 둘 다 Shin&Park/Basu 중복 인용 완화 목적)
상태: **Introduction 완료(14편, 미확정 항목 없음) / Methods 17건(SOLWEIG
계보·Moreno 포함)+링크UTCI할당 재검증 완료 / Related Work — v5 기준
2.1~2.4절 전 문장 검증 완료 + 38°C 클러스터 4편 신규(Dijkstra 가등록
제외) / Results 2건(Hsu 사용주의, Wang 용도재검토) /
Discussion
2편 신규 등재**

---

## 이 문서의 목적과 절대 규칙

이 문서는 논문(SCI + 국문 석사논문, 주제 동일)에 실제로 인용되는 모든 선행연구를
**할루시네이션 0%로 관리**하기 위한 마스터 목록이다. 사용자는 이 목록과 별개로
동일한 논문들을 종이로 프린트하여 인용 단락·문장에 형광펜 표시하는 물리적 검증
작업을 병행한다.

### ⚠️ 등재 조건 (절대 규칙)

**어떤 논문도 다음 조건을 만족하기 전까지는 이 목록에 등재될 수 없다:**

1. Claude가 해당 논문의 PDF 원문을 직접 읽는다
2. 논문 본문에 실제로 존재하는 **정확한 문단 또는 문장**을 원문 그대로 사용자에게
   제시한다 (인용 근거가 되는 페이지 번호 포함)
3. 사용자가 그 문단/문장이 우리 논문의 어느 인용과 정확히 대응하는지 확인한다

**현재 프린트되어 있는 11편(서론 관련 10편 + Colaninno 2024)도 아직 이 검증
절차를 거치지 않았으므로 이 목록에 없다.** 검증이 완료되는 즉시 해당 섹션에
추가된다.

### 정리 원칙

- **배치 순서 = 논문 내 등장 순서** (서론 → 선행연구 → 방법론 → 결과 → 논의 → 결론)
- 논문이 **처음 등장하는 섹션**에 전체 정보(원문 인용, 페이지, 우리 논문 문장 대응)를 기재
- **같은 논문이 이후 섹션에서 재인용되면**, 그 섹션에는 (a) 재인용 시 구체적으로
  어느 부분에 어떻게 쓰였는지만 간단히 적고, (b) "최초 등장: [섹션명] 참고"로
  역참조 표시 — 전체 원문 인용을 중복해서 적지 않음
- 각 항목은 `reference_list.csv`의 id 번호와 연결

### 버전/작업로그 관리

- 파일명 형식: `YYYY-MM-DD_reference_list.md` — 내용이 갱신될 때마다 그날 날짜로
  파일명을 바꾸고(예: 2026-07-14 → 2026-07-20) 버전 번호(v1→v2…)를 올림
- 이전 버전은 git 히스토리에 남으므로 별도 백업 불필요
- 하단 "작업 로그" 섹션에 추가/수정/삭제 내역을 **날짜 필수**로 기록

---

## 1. Introduction

*(1~4단락 인용 전부 확정 완료. 검증 대기: Bröde et al. 2012(5단락),
IPCC 2022(PDF 미확보, 검증 보류) — 1편 남음)*

### [id 022] Basu et al. (2024) — 1차 등장

- **인용 위치**: 1단락 오프닝 — "도시의 보행가능성은 기후 환경의 영향을
  받으며, 폭염일수와 발생빈도의 증가는 인간의 생명에 심각한 위협을 초래할 수
  있다(Basu et al., 2024)."
- **원문 (Introduction, p.1)**:
  > "The walkability of a city is affected by its thermal environment, whereby
  > the outdoor thermal comfort for pedestrians plays a key role in determining
  > the quality of urban life... The increasing number of hot days and frequent
  > occurrences of heatwaves can cause a serious threat to human life."
- **번역**: "도시의 보행가능성은 기후 환경의 영향을 받으며, 보행자의 실외
  열쾌적성은 도시 삶의 질을 결정하는 핵심 요인이다... 폭염일 수와 발생 빈도의
  증가는 인간의 생명에 심각한 위협을 초래할 수 있다."
- **비고**: 뒤 문장("실외 활동이 필연적으로 수반되는 보행은 폭염 시 위협이
  더욱 커질 것이다")은 Basu(2024)의 "pedestrians are comparatively more exposed
  to extreme weather conditions" 구절과 유사하지만, 그대로 재서술하지 않고
  저자 본인의 논리적 추론으로 무인용 처리하기로 확정(2026-07-14). 2단락에서
  "인지 보행거리 80.8m 증가(UTCI 1°C/26°C 초과, 보스턴 GPS)" 수치로 재인용됨 —
  재인용 시 이 항목 참고. 추가로 Abstract의 "Non-White residents were observed
  to have lower accessibility levels... likely because of disparities in urban
  heat exposure"는 1단락 마지막 문장(열노출의 공간적 불균등, 현재 무인용)의
  후보로 검토했으나 인종/사회집단 기반 불균등이라 우리 문장(건조환경·수목
  분포 기반)과 결이 달라 보류.
- **동일 논문 2차 인용 (같은 1단락 내)**: "그럼에도 불구하고 도시 보행 공간은
  대체로 기능성 위주로 계획되어 기후적 쾌적성에 대한 고려가 부족한 경우가
  많다(Basu et al., 2024)."
  - **원문 (Introduction, p.2)**: "Unfortunately, most urban walking spaces are
    planned by functionality, with little consideration of thermal comfort."
  - **번역**: "안타깝게도 대부분의 도시 보행 공간은 기능성 위주로 계획되며,
    기후적 쾌적성에 대한 고려는 부족하다."
  - **위치 판단**: 이 문장은 "연구방법론 갭"(3단락, 연속 패널티의 한계)과는
    성격이 다른 "도시설계 실무 갭"이라 3단락이 아닌 1단락(동기 부여)에 배치—
    "위험 증가 + 설계 미반영 → 정확한 측정의 필요성" 인과 흐름으로 접근성
    형평성 문장(Geurs & van Wee 등)으로 자연스럽게 이어짐.
  - **향후 검토**: 같은 단락에서 Basu(2024)가 두 번 인용되는 상태 — 추후 다른
    선행연구 검토 중 이 "설계 갭" 주장을 뒷받침하거나 대체할 인용이 보이면
    교체/추가하여 인용 다양성 확보 예정(사용자 요청, 2026-07-14).
- **확인**: 사용자 확인 완료 (2026-07-14)
- **동일 논문 3차 인용(같은 1단락 내, 2026-08-04 신규 확정)**: "여러 이동
  방식 중 실외에서 신체 활동이 필연적으로 수반되는 보행의 경우 폭염 시
  직접적인 열노출로 인한 위협이 더욱 커질 것이다(Basu et al., 2024)."
  - **원문 (Introduction, p.2, "생명 위협" 문장 바로 다음)**: "Trips that
    entail physical exertion outdoors, such as walking and biking trips,
    will increase people's overall exposure to potentially dangerous
    urban microclimates."
  - **번역**: "실외에서 신체적 노력을 수반하는 이동(보행·자전거 등)은
    잠재적으로 위험한 도시 미기후에 대한 전반적 노출을 증가시킬 것이다."
  - **경위**: 2026-07-14 당시 이 문장을 다른 문구("pedestrians are
    comparatively more exposed to extreme weather conditions", p.2)와
    대조해 "유사하지만 그대로 재서술 아님 → 무인용 유지"로 결정했었음.
    2026-08-04 Claude가 원문 재확인 중 위 문장(더 직접적으로 일치)을
    추가로 발견해 사용자에게 보고, 사용자가 인용 추가로 확정.
- **확인**: 사용자 확인 완료 (2026-08-04)

### [id 030] Yoon et al. (2020)

- **인용 위치**: 1단락 — "기후변화로 인해 도시 내 폭염의 빈도와 강도는
  더욱 증가하는 추세이며(IPCC, 2022), 국내에서도 최근 폭염일수가 과거
  대비 유의하게 증가하는 것으로 확인된다(Yoon et al., 2020)."
- **서지정보**: Yoon, D. et al. (2020). Recent changes in heatwave
  characteristics over Korea. *Climate Dynamics*, 55, 1685–1696.
  DOI: 10.1007/s00382-020-05420-1
  (`references/all_papers/Yoon2020_HeatwaveKorea.pdf`)
- **원문 (Abstract)**: "Global warming and abnormal climate change have
  resulted in an increase in the frequency of severe heatwave events.
  Recently, a series of extreme heatwave events have occurred in South
  Korea, and the damage from these events has also been increasing."
- **번역**: "지구온난화와 이상기후는 심각한 폭염 사건의 빈도 증가를
  가져왔다. 최근 한국에서도 일련의 극한 폭염 사건이 발생했으며, 이로
  인한 피해도 증가하고 있다."
- **판단**: 군집분석으로 2000~2018년 한국 폭염일수가 1981~1999년 대비
  유의하게 증가함을 실증(카나차카반도 지위고도 이상과 연관된 cluster 2
  유형 증가가 원인) — IPCC(2022)의 전지구적 일반론 옆에 한국 특정
  실증 데이터를 추가해 서론 도입부를 보강.
- **확인**: 사용자 확인 완료 (2026-08-04) — 마스터 초안 반영 완료

### [id 017] Geurs & van Wee (2004)

- **인용 위치**: 1단락 — "도시 내 이동 접근성의 공평한 분배와 이에 대한 정확한
  측정은 거주민의 삶의 질 향상 및 증거 기반 도시계획의 전제가 되는 문제이나"
- **역할**: "정확한 측정 = 증거기반 도시계획의 전제" 부분의 근거
- **원문 (p.131, Section 3.1.4 "Accessibility as a social indicator")**:
  > "Accessibility measures can be used as a social indicator if they show the
  > availability of social and economic opportunities for individuals (or groups
  > of individuals), i.e. the level of access to essential sources for human
  > existence such as jobs, food, health and social services, along with the
  > potential for social interaction with family and friends. Furthermore,
  > social equity impacts, typically analysed in social impact assessments, can
  > be evaluated if the accessibility measure is spatially differentiated and
  > disaggregated."
- **번역**: "접근성 측정치는, 개인(혹은 집단)이 일자리·식품·건강·사회서비스와
  같은 인간 존립에 필수적인 자원에 접근할 수 있는 수준과 가족·친구와의 사회적
  교류 가능성을 보여준다면, 사회적 지표로 활용될 수 있다. 또한 접근성 측정치가
  공간적으로 세분화·분리되어 있다면, 사회영향평가에서 다루어지는 사회적 형평성
  영향도 평가할 수 있다."
- **보조 원문 (p.127, Section 1. Introduction)**:
  > "Accessibility... plays an important role in policy making." / "This paper
  > presents a thorough review of accessibility studies and research directions
  > to improve the current practice of land-use and transport policy appraisal."
- **비고**: "삶의 질"이라는 표현 자체는 이 논문에 그대로 없음(paraphrase). 해당
  표현의 직접 출처는 아래 Shin & Park(2026).
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 054] Shin & Park (2026)

- **인용 위치**: 1단락 — 위와 동일 문장, "삶의 질 향상" 표현의 직접 출처
- **원문 (p.1, Section 1. Introduction, 첫 문장)**:
  > "The equitable distribution of green space is a critical issue directly
  > linked to the quality of life for urban residents within the built
  > environment."
- **번역**: "녹지 공간의 공평한 분배는 건조환경 내 도시 거주자들의 삶의 질과
  직접적으로 연관된 중요한 문제다."
- **보조 원문 (같은 단락)**:
  > "Hence, it is critical for policymakers to require objective tools to
  > accurately measure this inequality and allocate limited resources
  > efficiently."
- **번역**: "따라서 정책입안자들이 이러한 불평등을 정확히 측정하고 제한된
  자원을 효율적으로 배분할 수 있는 객관적 도구를 갖추는 것이 중요하다."
- **비고**: 같은 논문이 1단락 두 번째 문장("접근성은... 환경 조성 차이에 따라
  불균등하게 분포")에서 "환경 조성 차이" 요인의 근거로도 재사용됨(아래 참고).
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 052] Kar et al. (2024)

- **인용 위치**: 1단락 — "접근성은 사회경제적 조건(Kar et al., 2024), 인프라
  차이(Park et al., 2022), 환경 조성 차이(Shin & Park, 2026)에 따라 불균등하게
  분포하는 경우가 많다" 중 "사회경제적 조건" 요인의 근거
- **원문 (p.1, Abstract)**:
  > "We find that socio-economically disadvantaged communities experience
  > higher mobility barriers and lower accessibility while walking and using
  > transit in Columbus, OH."
- **번역**: "사회경제적으로 취약한 지역사회는 콜럼버스(오하이오)에서 도보 및
  대중교통 이용 시 더 높은 이동 장벽과 더 낮은 접근성을 경험하는 것으로
  나타났다."
- **비고**: 이 논문은 "사회경제적 조건" 요인만 실증. "인프라 차이·환경 조성
  차이"까지 이 한 논문으로 커버하지 않기로 하고 요인별로 별도 인용을 붙임
  (아래 Park et al. 2022, 위 Shin & Park 2026 참고). 같은 id가 5단락에서도
  재인용되는지는 5단락 검증 시 확인 예정.
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 055] Park et al. (2022)

- **인용 위치**: 1단락 — 위 문장 중 "인프라 차이" 요인의 근거
- **원문 (p.11, Section 4.2 결과)**:
  > "Temporal cluster C (morning) had the same tendency: locations inside the
  > hotspot showed higher values, and more peripheral locations suffered from
  > insufficient accessibility (i.e. more notable cold spots). The spatial
  > inequality deteriorated in temporal clusters D and E: smaller hot spots and
  > prominent cold spots."
- **번역**: "시간대 군집 C(오전)도 같은 경향을 보였다 — 핫스팟 내부 지역은
  접근성이 높았고, 주변부 지역일수록 접근성 부족(콜드스팟)이 뚜렷했다. 시간대
  군집 D와 E에서는 공간적 불균등이 더 심화되어 핫스팟은 작아지고 콜드스팟은
  더 두드러졌다."
- **보조 원문 (p.2, Introduction)**:
  > "Low spatial accessibility identifies the spatial mismatch between supply
  > and demand, which in turn suggests spatial impedance and inequality
  > issues."
- **비고**: 지도교수(박진우) 논문. 서울 EV충전소(인프라) 접근성의 중심부-주변부
  공간적 불균등을 자체 데이터로 실증 — "인프라 차이에 따른 불균등" 근거로 적합.
  서지정보: Park, J., Kang, J.Y., Goldberg, D.W., & Hammond, T.A. (2022).
  *International Journal of Geographical Information Science*, 36(6), 1185–1204.
  DOI: 10.1080/13658816.2021.1978450 (Online 2021, 정식 게재 2022 — 인용 연도는
  2022로 확정).
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 028] Jia et al. (2022) — 1차 등장

- **인용 위치**: 2단락 — "Jia et al.(2022)은 홍콩 야외 보행로에서 337명을
  대상으로 열 스트레스가 높아질수록 보행속도가 감소함을 실증하였으며"
- **원문 (p.10, Section 3.3, Fig. 13 관련 본문)**:
  > "Obviously, the average walking speed is reduced with increased PET
  > temperature or heat stress levels. Under strong heat stress, a reduction in
  > walking speed about 10–20% from the baseline condition is expected."
- **원문 (p.2, 방법)**:
  > "A total of 337 pedestrians were monitored and interviewed at four
  > carefully chosen sites with contrasting urban morphologies in Hong Kong..."
- **번역**: "평균 보행속도는 PET 또는 열 스트레스 수준이 높아질수록 감소한다.
  강한 열 스트레스 조건에서는 기준 대비 약 10~20%의 보행속도 감소가
  나타난다." / "홍콩 내 도시형태가 대비되는 4개 지점에서 337명의 보행자를
  대상으로 관측 및 인터뷰를 진행하였다."
- **비고**: 애초 3단락 초안에 "Jia et al.(2022)에서도 언급되듯 일부 보행자는
  오히려 속도를 높인다"는 재인용이 있었으나, 3단락 검증 중 **오인용으로 판명**
  — p.2 원문 확인 결과 "일부는 속도를 높인다"는 서술은 Jia 본인들의 발견이
  아니라 **다른 설문조사 연구([25])의 미확인 믿음**을 소개한 것이며, Jia 본인은
  바로 다음 문장에서 "현장연구로 확인된 바 없다"고 선을 긋고, 실제 현장데이터는
  오히려 일관된 속도 감소(R²=0.719)를 보여줌. Aydin(2026), Azegami(2023)도
  확인했으나 "일부 속도 증가" 근거는 없음(Azegami는 오히려 Jia를 정확히
  요약 — "그늘/양지에 따라 속도 변화 양상이 다르다"까지만 언급, 속도 증가
  아님). 결론: **이 재인용은 3단락에서 삭제**, Jia(2022)는 2단락에서만 등장.
  3단락은 "속도/거리 패널티는 경로 회피라는 별개 차원을 다루지 못한다"는
  논리로 대체(인용 불요, 저자 자신의 개념적 구분).
- **확인**: 사용자 확인 완료 (2026-07-14)
- **1단락 재인용(2026-08-05 신규, 2026-08-05 사용자 최종 정리로 Basu
  단독 제거·Jia 단독 인용으로 확정)**: "실외에서 신체 활동이 수반되는
  보행의 경우 폭염 시 열노출로 인한 위협이 더욱 커질 것이다(Jia et al.,
  2022)." 원문(p.2): "Walking as a weather-exposed activity is highly
  influenced by climatic conditions [17–19]." (2026-08-05 4편 정독 시
  확인됨). 초안 단계에선 Basu(2024)와 병기했었으나, 같은 1단락 내
  Basu 3회 반복을 완화하는 과정에서 사용자가 이 자리는 Jia만 남기기로
  최종 정리(Basu는 1단락에 여전히 2회 등장: 생명위협/기능성위주계획).
- **확인**: 사용자 확인 완료 (2026-08-05)

### [id 022] Basu et al. (2024) — 2단락 재인용 (수치 표기 관련 결정 포함)

- **인용 위치**: 2단락 — "Basu et al.(2024)은 보스턴 보행 궤적 분석을 통해
  UTCI가 증가할수록 인지 보행거리가 증가함을 실증하였다." (최초 등장은 1단락
  참고)
- **원문 (p.2, Introduction 연구 요약 문단)**:
  > "Furthermore, we detected a non-linear effect of UTCI on pedestrians'
  > perceived distance. While the average effect of 1°C increase in UTCI
  > (beyond the comfort threshold of 26°C) is 80.8 meters, separating the
  > effect by heat stress categories (e.g., 26°C to 29°C, 29°C to 32°C, etc.)
  > leads to varied effects across these categories that likely resemble an
  > exponential increase."
- **번역**: "또한 UTCI가 보행자의 인지 거리에 미치는 영향은 비선형적임을
  확인하였다. UTCI가 안락 임계값(26°C)을 넘어 1°C 증가할 때 평균 효과는
  80.8m였으며, 열 스트레스 구간별로 나누면 그 효과가 지수적으로 증가하는
  양상을 보였다."
- **비고**: Results 섹션(본문 표)에는 전체 데이터셋 모델(Model 2)은 104m,
  주간 이동만 뽑은 서브셋 모델(Models 4/5, N=742)은 80.8m로 서로 다른 두
  수치가 있음 — 저자들이 서론에서는 80.8m을 헤드라인 수치로 제시하지만
  모델에 따라 값이 갈리는 상황. 이 모호함을 피하기 위해 **구체적 수치(80.8m/
  104m/26°C 임계값)를 인용하지 않고 "UTCI 증가 → 인지 보행거리 증가"라는
  정성적 결과만 서술하는 것으로 확정**(사용자 결정, 2026-07-14).
- **확인**: 사용자 확인 완료 (2026-07-14)
- **방법론 근거 (2단락 오프닝 문장 "연속적인 값으로 반영" 뒷받침)**, p.8:
  > "The third walkshed type also used perceived distance but included the
  > effect of UTCI as well... route attributes other than the UTCI (i.e.,
  > turns, sidewalk width, amenities, SVF, and NDVI) were translated to their
  > equivalent walking distance values in the calculation of perceived
  > distance... All four walkshed types were constructed using 800 meters as
  > the catchment area network radius."
  - 번역: "세 번째 walkshed 유형도 인지거리를 사용하되 UTCI 효과를 포함했다...
    UTCI 외 경로 속성들을 인지거리 계산 시 동등한 보행거리 값으로 환산했다...
    네 walkshed 유형 모두 800m를 캐치먼트 네트워크 반경으로 사용했다."
  - 판단: 네트워크 반경(800m)은 열과 무관하게 고정, UTCI는 그 안에서 경로
    비용으로 연속적으로 반영됨 — 하드컷 아님, 연속 패널티 확인(2026-07-14,
    사용자 질문으로 촉발된 방법론 재확인).

### [id 042] Aydin et al. (2026)

- **인용 위치**: 2단락 — "Aydin et al.(2026)은 싱가포르를 대상으로 UTCI를
  인지이동시간(PTT)으로 변환하여 도달 가능 거리를 줄이는 방식으로 보행
  접근성을 산출하였다."
- **원문 (p.11, Section 2.3.3.2 UTCI-adjusted reach)**:
  > "PDT = (1.0 − PTT)·d0 + d0 (2). Here, d0 represents the default search
  > distance (in meters), PTT is normalized and unitless, and PDT is measured
  > in meters."
- **번역**: "PDT = (1.0 − PTT)·d0 + d0. 여기서 d0는 기본 탐색거리(m), PTT는
  정규화된 무차원 값, PDT는 도달거리(m)로 측정된다."
- **비고 (방법론 확인, 사용자 질문으로 촉발)**: 같은 논문 p.11, Section 2.3.4에
  "RUCS"라는 별도 지표도 정의됨: "RUCSi = 1, if UTCIi < 32.0°C and
  ΔPOI.reach[i] = 0; 0, otherwise" (식 8) — 이진 분류이지만, 이미 연속식(PDT)
  으로 계산된 reach 결과를 사후에 "열 영향 없음/있음"으로 라벨링하는 평가용
  지표일 뿐, 접근성 산출 자체(핵심 방법)는 여전히 연속(PDT). 하드컷 아님.
- **확인**: 사용자 확인 완료 (2026-07-14)
- **Related Work 재인용 (2.3절, 96 CPU×72시간 CFD 주장 검증, 2026-07-21)**
  - **원문 (p.8, §2.2.1.2 "CFD simulation")**:
    > "The CFD runs were executed in OpenFOAM v2112 (OpenFOAM, 2025) on the
    > NSCC supercomputing facility, approximately 72 h on 96 CPUs."
  - **번역**: "CFD 연산은 OpenFOAM v2112(OpenFOAM, 2025)로 NSCC 슈퍼컴퓨팅
    시설에서 실행되었으며, 약 96개 CPU로 72시간이 소요되었다."
  - **판단**: 2.3절 "풍속장은 OpenFOAM CFD로 계산하나 96 CPU×72시간이 소요되어
    도시 전역급 확장에는 비현실적이다" 서술과 수치 정확히 일치. 원문 대조 확인.
  - **확인**: 사용자 확인 완료 (2026-07-21)

### [id 021] Colaninno et al. (2024)

- **인용 위치**: 2단락 — "Colaninno et al.(2024)은 보행 이동성 데이터와 도시
  미기후 모델링을 결합하여 인도(sidewalk) 단위의 열 위험도를 평가하는
  프레임워크를 제안하였다."
- **원문 (p.1, Abstract)**:
  > "This study proposes a novel heat risk assessment framework combining
  > pedestrian mobility modeling with urban microclimate modeling."
- **번역**: "이 연구는 보행 이동성 모델링과 도시 미기후 모델링을 결합한 새로운
  열위험 평가 프레임워크를 제안한다."
- **판단**: 우리 2단락 서술과 정확히 일치 — **확정**.
- **비고 (방법론 확인, 사용자 질문으로 촉발 — 다른 3편과 메커니즘이 다름)**:
  - p.6: "pedestrians being willing to walk only up to a certain distance
    threshold (e.g., a half mile or 800 m)" — 네트워크 반경은 열과 무관하게
    고정.
  - p.13: "The combined use of heat hazard (UTCI) and exposure (pedestrian
    volume) helps identify specific sidewalks that warrant prioritization for
    interventions" — 위험지수(HEI) = 위험(UTCI) × 노출(보행량)의 곱, 열을
    속도/거리로 치환하는 게 아니라 별도의 연속 위험지수로 산출.
  - 판단: 하드컷 아님. 다만 Jia/Basu/Aydin(속도·거리 치환형)과는 메커니즘이
    달라(위험지수형), 2단락 오프닝 문장을 "치환하거나 위험지수로 환산하는
    등"으로 넓혀 확정(사용자 확인, 2026-07-14).
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 023] Melnikov et al. (2022)

- **인용 위치**: 4단락 — "Melnikov et al.(2022)은 싱가포르 실험에서 그늘
  경로가 햇볕 경로보다 이동 비용이 낮게 인식되어 경로 선택이 달라짐을
  보고하였다."
- **원문 (p.1, Abstract)**:
  > "We find that the distance walked in the shade is discounted by a factor
  > of 0.86 compared to the distance walked in the sun, and that shadows cast
  > by buildings have a stronger effect than trees."
- **번역**: "그늘에서 걸은 거리는 햇볕에서 걸은 거리 대비 0.86배로 할인되어
  인식되며, 건물 그림자가 나무 그늘보다 더 강한 효과를 보인다."
- **비고**: 0.86 수치는 본문에서 생략하고 "낮게 인식되어"로만 서술하기로
  결정(2026-07-14).
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 024] Azegami et al. (2023)

- **인용 위치**: 4단락 — "Azegami et al.(2023)은 도쿄 실험에서 보행자의
  28.2%가 최단경로보다 그늘 있는 경로를 우선 선택하였으며, 일부는 그늘 있는
  측을 선택하기 위해 신호 대기까지 감수하였다고 보고하였다."
- **원문 (p.1, Abstract)**:
  > "Most participants chose shaded routes in front of a large commercial
  > facility. The most common reason given was 'because there is shade'
  > (28.2%), indicating that the presence or absence of shade is a major
  > factor in route choice under severe thermal environment."
- **원문 (p.6)**:
  > "Some participants in the 13:00 group did not choose Sidewalk D at Point G
  > but chose Sidewalk E even after waiting for the street signal."
- **번역**: "대부분의 참가자는 대형 상업시설 앞에서 그늘진 경로를 선택했다.
  가장 흔한 이유는 '그늘이 있어서'(28.2%)였다." / "13시 그룹의 일부 참가자는
  G지점에서 인도 D를 선택하지 않고, 신호를 기다린 후에도 인도 E를
  선택했다."
- **비고**: 3단락 검증 중 이 논문이 Jia(2022)를 정확히 요약한 문장("그늘/양지
  간 속도 변화 양상이 다르다", 속도 증가 언급 없음)도 확인함 — 3단락 Jia
  항목의 비고 참고.
- **확인**: 사용자 확인 완료 (2026-07-14)

### [id 037] Buo et al. (2026)

- **인용 위치**: 4단락 — "Buo et al.(2026)은 열 최적 경로 탐색 도구의
  실사용 데이터를 통해, 전체 경로의 70% 이상에서 최단경로 대신 우회가
  선택됨을 실증하였다."
- **원문 (p.1, Abstract)**:
  > "Rerouting occurred in >70% of cases, with average detours <3% longer
  > than the shortest path, reducing average route MRT by up to 3.8 °C in
  > cool months."
- **번역**: "우회는 전체 사례의 70% 이상에서 발생했으며, 평균 우회거리는
  최단경로보다 3% 미만 길었고, 서늘한 계절 기준 평균 경로 MRT를 최대
  3.8°C까지 낮췄다."
- **비고**: 구체적 우회거리(32.2m)·MRT 절감폭(3.8°C)은 서론 본문에서 생략,
  "70% 이상 우회"만 서술하기로 결정(2026-07-14). 추가로 p.6(line 229 부근)에
  "a version of Dijkstra's shortest path algorithm"이라는 명시적 서술 확인
  — **Methods 섹션에서 라우팅 방법론 선례로 재인용 시 사용**(최초 등장은
  Introduction 4단락, Methods에서는 역참조 + Dijkstra 사용 사실만 추가).
- **확인**: 사용자 확인 완료 (2026-07-14)
- **Discussion 섹션 예정 비교 메모 (2026-07-14, 사용자 요청으로 기록)**:
  Buo(2026)는 MRT+SOLWEIG(1m 해상도) + Dijkstra 변형 알고리즘으로 **두 지점
  간 최적(가장 시원한) 경로 하나를 찾아주는 실시간 내비게이션 도구**(Cool
  Routes)이며, 연구 범위는 Arizona State University 템피 캠퍼스(500 OD쌍,
  171 POI, p.5-6 확인)로 대학 캠퍼스 규모. 우리 연구는 MRT+SOLWEIG(5m, 서울
  전체 시도) + Hard Cut(임계값 초과 링크 완전 제거)으로 **특정 경로가 아니라
  도달 가능한 전체 공간 범위(캐치먼트) 자체의 변화**를 산출 — "최적 경로
  찾기"(엔지니어링/내비게이션 관점)와 "도달 가능 영역의 불평등 측정"(접근성
  이론/지리학 관점)의 차이. Discussion에서 "유사한 MRT+SOLWEIG 파이프라인을
  쓰면서도 접근 방향이 다른 선례"로 Buo를 대조할 예정 — 실제 작성 시 이
  메모를 근거로 재검증 후 사용.

### [id 007] Bröde et al. (2012)

- **인용 위치**: 5단락 — "UTCI 기준 매우 강한 더위(Very Strong Heat Stress,
  ≥38°C; Bröde et al., 2012)에 해당하는 조건의 보행 링크를 네트워크에서
  완전히 제거(Hard Cut)하여..."
- **원문 (p.9, Table 3 "UTCI equivalent temperatures categorised in terms of
  thermal stress")**:
  > "+38 to +46 → Very strong heat stress" / "+32 to +38 → Strong heat
  > stress" / "Above +46 → Extreme heat stress"
- **번역**: "UTCI 38~46°C → 매우 강한 더위" / "UTCI 32~38°C → 강한 더위" /
  "UTCI 46°C 초과 → 극심한 더위"
- **비고**: 이 Table 3이 본 연구 전체의 Hard Cut 임계값(UTCI≥38°C) 근거 —
  Methods 섹션에서도 재인용됨(최초 등장 Introduction 5단락 참고).
- **확인**: 사용자 확인 완료 (2026-07-14)

## 2. Related Work (선행연구 검토)

### "38°C 임계값 정당화" 클러스터 — 스노우볼링 확보 5편 (2026-08-05)

> 인용 목적(공통): II장§2 또는 V장§3("왜 UTCI를 직접 쓰는가")에 "임계값은
> 지역 기후에 맞춰 정하는 것이 학계 관행이며, 서울처럼 더운 여름 기후에서는
> 38°C 이상 구간이 실제로 흔하게 관측되므로 38°C를 본문 기준값으로 채택한다"
> 논거를 보강하기 위해 사용자가 다운로드 → Claude가 fork로 각각 원문 정독.
> **아직 실제 학위논문 본문에는 반영 안 됨 — 문단 작성은 별도 단계.**

#### Pantavou et al. (2018)

- **서지정보**: Pantavou, K., Lykoudis, S., Nikolopoulou, M., & Tsiros, I.X.
  (2018). Thermal sensation and climate: a comparison of UTCI and PET
  thresholds in different climates. *International Journal of
  Biometeorology*, 62, 1695–1708. DOI: 10.1007/s00484-018-1569-4
- **원문(Abstract, p.1695)**: "The results indicated that the calibrated
  UTCI and PET thresholds increase with the climate normal annual air
  temperature of the survey city... The average increase of the
  respective thresholds... was about 0.6°C for each 1°C increase of the
  normal annual air temperature for both indices."
- **번역**: 보정된 UTCI·PET 임계값은 조사도시의 평년 연평균기온에 따라
  증가하며, 연평균기온 1°C 상승마다 임계값이 약 0.6°C씩 상승한다.
- **⚠️ 오버클레임 주의(fork가 명시적으로 경고)**: 이 논문은 유럽 온대
  도시(연평균 6.9~16.7°C)의 "중립(neutral)" 등급 경계 이동을 다룬 것이지,
  우리가 쓰는 "Very Strong Heat Stress(38°C 이상)" 같은 극한 등급 자체를
  지역별로 재정의해야 한다고 직접 주장하지 않는다. "임계값은 지역 기후에
  따라 상대적"이라는 **일반 원리**의 근거로만 쓸 것 — "그러므로 서울은
  38°C를 써야 한다"는 결론까지 이 논문이 내리는 것처럼 인용하면 오귀속.
- **확인**: 원문 PDF 전체 대조 완료 (2026-08-05)

#### Krüger, Rossi & Drach (2017)

- **서지정보**: Krüger, E., Rossi, F., & Drach, P. (2017). Calibration of
  the physiological equivalent temperature index for three different
  climatic regions. *International Journal of Biometeorology*, 61,
  1323–1336. DOI: 10.1007/s00484-017-1310-8 (원문 저자 표기는 이니셜만:
  "E Krüger, F Rossi, P Drach")
- **원문(Abstract, p.1323)**: "there is a need for adjusting comfort/
  stress ranges of a given index when using it in different climatic
  contexts."
- **원문(Table 6, p.1334 — 가장 강력한 수치 근거)**: 동일한 "Strong heat
  stress" 등급의 PET 임계값이 도시마다 **Glasgow 27°C, Curitiba 37°C,
  Tianjin 40°C, Rome 45°C, Rio de Janeiro 49°C**로, 같은 스트레스 등급인데
  최대 22°C까지 차이남.
- **번역**: "지표를 다른 기후 맥락에서 사용할 때는 쾌적/스트레스 구간의
  조정이 필요하다." 표 수치는 "같은 등급이라도 도시마다 실제 온도값이
  최대 22°C 차이난다"는 실증.
- **확인**: 원문 PDF 전체 대조 완료 (2026-08-05) — 우리 논증에 가장
  강력한 정량적 근거

#### Liu & Qin (2023)

- **서지정보**: Liu, L. & Qin, X. (2023). Analysis of heatwaves based on
  the universal thermal climate index and apparent temperature over
  mainland Southeast Asia. *International Journal of Biometeorology*,
  67(12), 2055–2068. DOI: 10.1007/s00484-023-02562-9
- **원문(p.2062)**: "the area with high HWA values measured by UTCI, with
  HWA values up to 40°C for AT and **45°C for UTCI**... The significantly
  higher value of UTCI compared to other indices indicates the actual
  human perceptions during heatwave may be more heat-stressed than what
  is assessed based on air temperature alone."
- **번역**: 동남아 본토 폭염일의 UTCI가 최대 45°C까지 도달했으며, 이는
  단순 기온보다 실제 체감 스트레스가 더 큼을 보여준다.
- **판단**: 더운 몬순·아열대 기후에서는 UTCI 38°C 이상(Very Strong Heat
  Stress) 구간이 예외가 아니라 정례적으로 관측되는 범위임을 보여주는
  실측 사례 — Basu(2024, 보스턴 최댓값 37.3°C)와 정확히 대비됨. 다만 "지역별
  임계값 비교 정당화" 자체는 이 논문의 주제가 아님(Kruger·Pantavou가 그
  역할) — "우리 지역엔 38°C가 실제로 흔하다"는 사실관계 근거로만 사용.
- **확인**: 원문 PDF pp.1-8, 12-14 대조 완료 (2026-08-05). Discussion/
  Conclusion(pp.9-11 추정)은 미확인 — 필요시 추가 확인 권장.

#### Jendritzky, de Dear & Havenith (2012)

- **서지정보**: Jendritzky, G., de Dear, R., & Havenith, G. (2012). UTCI—
  why another thermal index? *International Journal of Biometeorology*,
  56(3), 421–428. DOI: 10.1007/s00484-011-0513-7
- **원문 ①(p.421)**: "ISB Commission 6 took up the idea of developing a
  Universal Thermal Climate Index (UTCI)... COST Action 730 so that
  finally over 45 scientists from 23 countries... worked together."
- **원문 ②(p.423, UTCI 설계 요구조건)**: "The UTCI must meet the following
  requirements: ... (3) **Valid in all climates, seasons, and time and
  spatial scales**"
- **원문 ③(p.422)**: "The tolerance to thermal extremes depends on
  personal characteristics (Havenith 2001, 2005): age, fitness, gender,
  acclimatisation, morphology, and fat thickness being among the most
  significant."
- **번역**: ① ISB 위원회6+COST Action 730(23개국 45명 이상 과학자)이
  UTCI를 개발했다. ② UTCI는 "모든 기후·계절·시공간 스케일에서 유효해야
  한다"는 게 공식 설계 요구조건이다. ③ 극한열 내성은 나이·체력·성별·순응도
  등 개인 특성에 좌우된다(=UTCI 자체는 이 개인차를 반영하지 못함).
- **용도**: ①은 II장§2 UTCI 채택 근거(Bröde 2012 옆) 보강. ②는 "서울
  여름처럼 더운 기후에도 UTCI를 그대로 쓸 수 있는가"에 대한 **UTCI 설계
  자체의 공식 답변**으로 강력함. ③은 **"UTCI는 연령별 차별화 안 되는
  지표"라는 우리 V장§6 한계 서술이 지금까지 근거 논문 없이 서술돼
  있었는데, 그 원 근거로 사용 가능**.
- **확인**: 원문 PDF 5페이지 전체 대조 완료 (2026-08-05)

---

### Hägerstrand (1970)

- **인용 위치**: 2.1절 — "Hägerstrand(1970)의 시공간 프리즘은 개인이 정해진
  시간 예산 내에서 이동할 수 있는 공간 범위를 3차원으로 개념화하면서, 물리적
  이동 가능성을 분석 단위로 설정하는 틀을 제시했다."
- **서지정보**: Hägerstrand, T. (1970). What about people in regional science?
  *Papers of the Regional Science Association*, 24(1), 7-24. (9차 유럽 지역과학회
  회장 연설) (`references/all_papers/Hagerstrand1970_SpaceTimePrism.pdf` — 스캔본,
  pdftotext 텍스트 추출 불가해 이미지로 직접 확인)
- **원문 (p.14)**:
  > "If we look closer at the time-space volume within reach, it turns out to
  > be not a cylinder but a prism. It not only has a geographical boundary; it
  > has time-space walls on all sides."
- **원문 (p.13)**:
  > "...there exists a definite boundary line beyond which he cannot go if he
  > has to return before a deadline. Thus, in his daily life everybody has to
  > exist spatially on an island... the effective size of an individual's
  > island is much smaller than the potential size which is delineated by his
  > ability to move."
- **번역**: "도달 범위 내 시공간 볼륨을 자세히 보면 원기둥이 아니라 프리즘임이
  드러난다. 이는 지리적 경계뿐 아니라 사방으로 시공간적 벽을 갖는다." / "...
  마감시간 전에 돌아와야 한다면 넘어설 수 없는 명확한 경계선이 존재한다.
  따라서 일상생활에서 모든 사람은 공간적으로 '섬' 위에 존재하는 셈이다..."
- **비고**: p.13 Figure 1 "Daily Prisms"에서 walker/driver/flyer별 시간예산에
  따른 최대 도달 프리즘을 실제로 도식화. 이미지 기반 확인(OCR 아님, 직접 열람).
- **확인**: 사용자 확인 완료 (2026-07-21)

### Miller (1991)

- **인용 위치**: 2.1절 — "Miller(1991)는 이를 GIS 네트워크 분석으로 구현하여
  네트워크 기반 도달 가능 영역(Potential Path Area) 개념을 정립했다."
- **서지정보**: Miller, H. J. (1991). Modelling accessibility using space-time
  prism concepts within geographical information systems. *International
  Journal of Geographical Information Systems*, 5(3), 287-301.
  DOI: 10.1080/02693799108927856
  (`references/all_papers/Miller1991_SpaceTimePrism_GI.pdf`)
- **원문 (p.291-292)**:
  > "These considerations can be addressed explicitly and in detail by
  > defining PPA structure within the format of the urban transportation
  > network. A network representation can be formulated where arcs represent
  > the individual streets in the transportation network and nodes represent
  > intersections of these streets. A PPA defined in this format shows the
  > streets (arcs) in the network that are feasible for travel and the
  > intersections (nodes) which it is feasible to reach."
- **원문 (p.292)**:
  > "...the network based PPA can be based on the assumption of the shortest
  > path through the network being used by the individual."
- **번역**: "이러한 고려사항은 PPA(잠재적 경로 영역) 구조를 도시 교통 네트워크의
  형태로 정의함으로써 다룰 수 있다. 네트워크 표현은 도로(arc)가 개별 거리를,
  노드(node)가 교차점을 나타내는 방식으로 구성한다..." / "...네트워크 기반
  PPA는 개인이 네트워크를 통해 최단경로를 이용한다는 가정에 기반할 수 있다."
- **비고**: 저널명은 1991년 당시 *...Information **Systems***(복수형)였으며,
  현재의 *...Information **Science***(단수, GIScience)와 다름 — 인용 시 연도별
  정확한 저널명 표기 필요.
- **확인**: 사용자 확인 완료 (2026-07-21)

### Miller (2007)

- **인용 위치**: 2.1절 — "접근성 측정은 분석 단위에 따라 장소기반(place-based)과
  개인기반(person-based) 측정으로 갈라져 발전해왔다(Miller, 2007)."
- **서지정보**: Miller, H. J. (2007). Place-based versus people-based geographic
  information science. *Geography Compass*, 1(3), 503-535.
  DOI: 10.1111/j.1749-8198.2007.00025.x
  (`references/all_papers/Miller2007_PlaceBasedPeopleBased_GIScience.pdf`)
- **원문 (Abstract, p.503)**:
  > "This article discusses the need to move beyond a place-based perspective
  > in geographic information science to include a people-based perspective
  > (i.e., the individual in space and time)."
- **번역**: "이 논문은 지리정보과학에서 장소기반 관점을 넘어 개인기반 관점
  (즉, 시공간 속 개인)을 포함해야 할 필요성을 논한다."
- **판단**: "장소기반/개인기반 구분이 존재한다"는 정의적 인용으로만 사용 —
  일치. **오귀속 방지 경과(2026-07-21)**: 초안 문장이 원래 이 논문을 "개인기반
  측정은 일반화가 어렵다는 한계가 지적되어 왔다"의 근거로 인용했으나, 원문
  전체에 "generaliz"라는 단어가 전혀 없고 오히려 이 논문은 **개인기반을
  옹호하고 장소기반을 비판**하는 반대 논조임을 확인 — 사용자와 논의 후 해당
  주장(일반화 한계)은 삭제하고, Miller(2007)는 "이분법이 존재한다"는 정의적
  인용으로만 축소. 이 과정에서 "PPA(Miller 1991)를 개인기반 버전의 Catchment
  Area로 볼 수 있다"는 것은 Miller가 명시한 바 없는 **본 연구의 해석**임을
  확인(원문에 "catchment" 단어 없음, grep 확인) — 본문에 "본 연구는 ~라고
  본다"로 명시해 저자 주장과 분리(사용자 지적으로 발견, 2026-07-21).
- **확인**: 사용자 확인 완료 (2026-07-21)

### 확보했으나 현재 미사용 — 향후 활용 후보 (석사논문 확장판 등)

> SCI 논문은 분량 제약으로 2.1절을 Miller(2007) 하나로 압축했으나, PDF는 이미
> 확보되어 있고 내용도 확인했으므로 버리지 않고 여기 정리해둔다. 국문
> 석사논문(분량 여유 있음)이나 추후 논의 확장 시 재검토 대상.

- **El-Geneidy & Levinson (2006)**. Access to Destinations: Development of
  Accessibility Measures. Minnesota DOT 기술보고서 #MN/RC-2006-16, University
  of Minnesota. (`references/all_papers/ElGeneidy2006_AccessToDestinations.pdf`)
  - **원문 (p.4)**: "The traditional measure of accessibility is place-based,
    and involves measurements of spatial separation of individuals and
    certain activities. Recently 'people-based accessibility' measures have
    been proposed in the literature (H. Miller, 2005)."
  - **비고**: SCI 논문이 아니라 정부 기술보고서라 SCI 저널 인용 규칙에는
    엄밀히 안 맞음(CLAUDE.md). 다만 "장소기반=전통적/표준 측정"이라는 내용
    자체는 정확하고, 국문 석사논문에서는 기술보고서 인용이 문제되지 않으므로
    후보로 유지.
- **Kwan (1999)**. Gender and individual access to urban opportunities: a
  study using space-time measures. *The Professional Geographer*, 51(2),
  211-227. DOI: 10.1111/0033-0124.00158
  (`references/all_papers/Kwan1999_GenderSpaceTimeAccess.pdf`)
  - **비고**: 아직 원문 대조 안 함(이번 2.1절 재구성으로 불필요해져 검토
    보류). 개인기반 접근성에 지각적 요소를 결합한 초기 사례로, Kar et
    al.(2023/2024)의 "soft constraint" 계보를 더 깊이 다룰 때(예: 성별·
    사회집단별 접근성 격차 논의) 후보로 재검토.

### Dijkstra (1959) — ⚠️ 검증 보류 (사용자 직접 등재 예정)

- **인용 위치**: 2.1절 — "Catchment Area는 출발 노드에서 Dijkstra 알고리즘
  (Dijkstra, 1959)으로 최단경로를 탐색하고..."
- **서지정보(추정, 미확인)**: Dijkstra, E. W. (1959). A note on two problems in
  connexion with graphs. *Numerische Mathematik*, 1, 269-271.
- **판단**: 특정 수치·주장이 아니라 "Dijkstra 알고리즘"이라는 표준 알고리즘
  명칭의 출처 표기 — PDF 미확보. 사용자 결정(2026-07-21): 원문 검증 없이
  일단 인용하고, 추후 사용자가 직접 PDF 확보해 정식 등재할 예정.
- **확인**: ⚠️ 미검증 — 사용자 직접 등재 예정, 그 전까지 이 항목은 "가등록"
  상태로만 취급.

### [id 017] Geurs & van Wee (2004) — 2.1절 재인용 ("contour measure = isochrone")

- **최초 등장**: Introduction 1단락 참고(p.131, 3.1.4절 "정확한 측정=정책 전제"
  인용, id 017)
- **인용 위치**: 2.1절 — "Catchment Area는 개념적으로 이소크론(isochrone) 분석
  및 Geurs & van Wee(2004)의 contour measure와 같은 계보 위에 있다."
- **원문 (p.134, §3.3 "Location-based accessibility measures")**:
  > "A contour measure, also known as isochronic measure, cumulative
  > opportunities, proximity count or daily accessibility, counts the number
  > of opportunities which can be reached within a given travel time, distance
  > or cost... This measure is popular in urban planning and geographical
  > studies."
- **번역**: "contour measure는 isochronic measure, 누적기회, 근접성 카운트,
  일일 접근성이라고도 불리며, 주어진 이동시간·거리·비용 내에서 도달 가능한
  기회의 수를 센다... 이 지표는 도시계획·지리학 연구에서 널리 쓰인다."
- **판단**: "contour measure = isochronic measure"라는 저자 자신의 명시적
  동일시 확인 — 2.1절 인용 정확히 부합.
- **⚠️ 오귀속 발견 및 수정(2026-07-21)**: 같은 문단의 앞 문장 "버퍼 기반 반경
  분석과 달리 실제 도로 구조를 반영하며, 도시 시설 접근성 분석에서 표준
  방법론으로 광범위하게 활용된다"에도 원래 이 논문이 인용되어 있었으나, 원문
  전체를 검색해도 Geurs & van Wee(2004)가 버퍼 기반 vs 네트워크 기반 접근성을
  구분해 서술하는 대목이 없음을 확인. 사용자 결정: 이 문장은 **인용 없이
  필자 서술로 남김**(오귀속 방지). `2026-07-21_선행연구_v5_전체판.md`에 반영
  완료.
- **확인**: 사용자 확인 완료 (2026-07-21)

### [신규] Kar et al. (2023)

- **인용 위치**: 2.1절 — "기존 연구들은 이 틀이... 이동에 대한 개인의 인지적
  제약을 소프트 제약(soft constraint)으로 통합하려는 시도를 이어왔다. Kar et
  al.(2023)은 시공간 프리즘(STP)에 이동 인식(perceived mobility)을 소프트
  제약으로 통합한 포용적 접근성(inclusive accessibility) 개념을 제안하여..."
- **서지정보**: Kar, A., Le, H.T.K., & Miller, H.J. (2023). Inclusive
  Accessibility: Integrating Heterogeneous User Mobility Perceptions into
  Space-Time Prisms. *Annals of the American Association of Geographers*,
  113(10), 2456-2479. DOI: 10.1080/24694452.2023.2236184
  (`references/all_papers/Kar2023_InclusiveAccessibility_STP.pdf`)
- **원문 (Abstract)**:
  > "We conceptualize inclusive accessibility as a subset of the classic
  > space–time prism (STP) that incorporates hard constraints (e.g., limited
  > infrastructure and services and time) and soft constraints (e.g.,
  > perceptions of safety and comfort toward the built environment and
  > infrastructure and travel time preferences)."
- **번역**: "우리는 포용적 접근성을 고전적 시공간 프리즘(STP)의 부분집합으로
  개념화하는데, 이는 하드 제약(제한된 인프라·서비스·시간)과 소프트 제약
  (건조환경·인프라에 대한 안전·편안함 인식, 이동시간 선호)을 통합한다."
- **비고**: Kar et al.(2024, id 052, Introduction 1단락 기존 등재)와는 **다른
  논문**(저자 3인 중 Kar, Miller 겹치나 공저자·저널·연도·DOI 전부 다름) —
  2026-07-17 PDF 원문 대조로 확인됨. 혼동 주의.
- **확인**: 사용자 확인 완료 (2026-07-20)

### Ali-Toudert & Mayer (2006)

- **인용 위치**: 2.2절 — "Ali-Toudert & Mayer(2006)는 사하라 기후 가로 협곡을
  ENVI-met으로 모의해, 같은 가로 내에서도 기온은 균일하지만 MRT는 햇빛 구역과
  그늘 구역 사이에 최대 40K까지 벌어짐을 확인하였다"
- **서지정보**: Ali-Toudert, F., & Mayer, H. (2006). Numerical study on the
  effects of aspect ratio and orientation of an urban street canyon on
  outdoor thermal comfort in hot and dry climate. *Building and Environment*,
  41(2), 94-108. (`references/all_papers/AliToudert2006_AspectRatio_
  StreetCanyon.pdf`)
- **원문 (p.100)**:
  > "Ta shows a uniform distribution within the street... In contrast, the
  > radiation fluxes expressed by Tmrt are very sensitive to geometrical
  > properties. Tmrt shows a totally different pattern with differences to
  > Ta reaching 40 K for the sunlit part of the street and about 6–10 K for
  > the shaded area."
- **번역**: "기온(Ta)은 가로 내에서 균일한 분포를 보인다... 반면 복사플럭스로
  표현되는 MRT(Tmrt)는 기하학적 특성에 매우 민감하다. MRT는 완전히 다른 패턴을
  보이며 기온과의 차이가 햇빛이 드는 구간에서는 40K, 그늘 구간에서는 6~10K에
  달한다."
- **판단**: 초안 인용과 페이지·수치 정확히 일치(원문 대조로 p.100 확인, 저널
  페이지 범위 94-108 중 7번째 페이지).
- **확인**: 사용자 확인 완료 (2026-07-20)

### Ali-Toudert & Mayer (2007) — 후속 연구

- **인용 위치**: 2.2절 — "후속 연구(Ali-Toudert & Mayer, 2007)는 갤러리·가로수를
  함께 적용하면 체감온도(PET)가 최대 24K까지 낮아짐을 보였다."
- **서지정보**: Ali-Toudert, F., & Mayer, H. (2007). Effects of asymmetry,
  galleries, overhanging façades and vegetation on thermal comfort in urban
  street canyons. *Solar Energy*, 81(6), 742-754.
  (`references/all_papers/AliToudert2007_VegetationFacade_Canyon.pdf`)
- **원문 (p.751, §4.3 "Use of vegetation")**:
  > "Further, Fig. 8 gives the PET values for the N-S street with H/W = 1
  > including a large central row of trees and galleries compared to a street
  > without trees or galleries. In this case, PET was up to 24 K lower than in
  > a street without trees."
- **번역**: "N-S 방향 가로(H/W=1)에 중앙 대형 가로수 열과 갤러리를 함께 적용한
  경우와 수목·갤러리가 없는 가로를 비교한 PET 값을 Fig.8에 제시한다. 이 경우
  PET는 수목이 없는 가로 대비 최대 24K 낮았다."
- **판단**: 초안 인용과 수치·조건(갤러리+가로수 병용) 정확히 일치.
- **확인**: 사용자 확인 완료 (2026-07-21)

### Kántor & Unger (2011)

- **인용 위치**: 2.2절 — "Kántor & Unger(2011)의 리뷰도 MRT가 열쾌적성 평가에서
  가장 중요하고 공간 분화가 큰 변수임을 재확인한다."
- **서지정보**: Kántor, N., & Unger, J. (2011). The most problematic variable
  in the course of human-biometeorological comfort assessment — the mean
  radiant temperature. *Central European Journal of Geosciences*, 3(1), 90-100.
  DOI: 10.2478/s13533-011-0010-x
  (`references/all_papers/Kantor2011_MRT_ProblematicVariable.pdf`)
- **원문 (Abstract, p.90)**:
  > "This paper gives a review on the topic of the mean radiant temperature
  > Tmrt, the most important parameter influencing outdoor thermal comfort
  > during sunny conditions. Tmrt summarizes all short wave and long wave
  > radiation fluxes reaching the human body, which can be very complex
  > (variable in spatial and also in temporal manner) in urban settings."
- **번역**: "이 논문은 평균복사온도(MRT)에 관한 리뷰로, MRT는 맑은 날 조건에서
  실외 열쾌적성에 영향을 미치는 가장 중요한 변수이며... 도시 환경에서
  공간적으로(시간적으로도) 매우 복잡하게 변화할 수 있다."
- **판단**: "가장 중요한 변수"·"공간적으로 복잡하게 변화"라는 표현이 초안의
  "가장 중요하고 공간 분화가 큰 변수"와 정확히 일치.
- **확인**: 사용자 확인 완료 (2026-07-21)

### Kar et al. (2024) — "Inclusive Access 1" (Hard Cut 선례, 2.4절)

- **주의**: id 052 Kar et al. (2024)와 **같은 논문, 다른 절 인용**. id 052는
  Introduction 1단락(Abstract, 사회경제적 조건 관련)에서 이미 등재됨. 이 항목은
  같은 논문의 5.3절/6.2절을 Related Work 2.4절(Hard Cut 선례)에서 인용.
- **서지정보**: Kar, A., Le, H.T.K., Miller, H.J., Ng, N., & Le, H. (2024).
  Perceived accessibility and its role in shaping equitable access to urban
  amenities. *Computers, Environment and Urban Systems*, 114, 102202.
  (`references/all_papers/Armita2024_PerceivedAccessibility.pdf`)
- **인용 위치**: 2.4절 — "Kar et al.(2024)은... 보행 인지 점수가 특정 임계값
  (≤3) 이하인 도로 링크를 네트워크에서 완전히 제거하는 'Inclusive Access 1'을
  정의하였다"
- **원문 (p.7, §5.3 "Classic and inclusive accessibility measure")**:
  > "The first inclusive access considers all hard constraints of classic
  > access mentioned above, as well as walking perception scores of social
  > groups as soft spatial constraints. To do this, we first modify the road
  > network to eliminate the streets with low walking perception scores
  > (walking perception score ≤ 3) for the respective group. Using this
  > modified road network, inclusive access 1 for a social group identifies
  > the network space that any traveler from the respective group perceives
  > as accessible as well as they can physically reach the nearby food
  > locations within the 30-min travel time budget."
- **번역**: "첫 번째 inclusive access는 위에서 언급한 classic access의 모든
  hard constraint에 더해, 사회집단별 보행 인지점수를 soft spatial constraint로
  추가한다. 이를 위해 먼저 해당 집단에 대해 보행 인지점수가 낮은(3점 이하) 도로를
  네트워크에서 제거한다. 이렇게 수정된 네트워크로, inclusive access 1은 해당
  집단의 어떤 이동자든 물리적으로 도달 가능하면서 동시에 접근 가능하다고
  인지하는 네트워크 공간을 식별한다."
- **원문 (p.12, §6.2 "Study limitations and future directions")**:
  > "Similarly, our inclusive accessibility measure treats the walking
  > perception score as a binary constraint, assuming people only walk when
  > the travel environment seems favorable. In other words, a route is
  > excluded from the inclusive accessibility measure if any link on that
  > route feels unwalkable to the traveler."
- **번역**: "마찬가지로, 우리의 inclusive accessibility 측정치는 보행
  인지점수를 binary constraint로 취급하며, 이동 환경이 호의적이라고 느낄 때만
  사람들이 보행한다고 가정한다. 다시 말해 경로 상 어떤 링크라도 이동자에게
  보행 불가능하게 느껴지면 그 경로는 측정에서 제외된다."
- **용어 주의(중요)**: 이 논문의 "soft/hard constraint"는 **제약의 성격**
  (주관적 인지 vs 객관적 물리) 기준이며, 본 연구의 "연속적 패널티 vs Hard Cut"
  이분법(**함수 형태**: 연속 vs 이진) 기준과 다른 축이다. 저자들은 인지점수를
  "soft spatial constraint"라 명명하지만 실제 구현(§5.3)은 임계값 이하 링크를
  네트워크에서 완전히 제거하는 **이진적** 방식이며, §6.2에서 스스로 "binary
  constraint"라 인정한다 — 즉 이름은 soft이나 메커니즘은 우리 Hard Cut과
  구조적으로 동일. 본문에서 Kar(2024)를 인용할 때 "soft/hard"라는 원저자
  용어를 그대로 쓰지 말고 이 차이를 명시할 것(2026-07-21, 사용자 지적으로
  발견 및 확정).
- **판단**: 5.3절 정의문·6.2절 자기한계 인정문 모두 원문 대조 확인. 섹션 번호
  (5.3, 6.2)도 pdftotext 헤더 대조로 확인(p.12 = "6.2. Study limitations and
  future directions").
- **확인**: 사용자 확인 완료 (2026-07-21)

### 백참조 확인 — 2.3절/2.4절 재인용 (Jia/Basu/Aydin/Colaninno/Melnikov/Azegami/Buo/Bröde)

2.3절·2.4절에 등장하는 아래 인용은 모두 Introduction 또는 Methods에서 이미
원문 대조 검증 완료된 것을 재인용한 것 — 각 절의 실제 텍스트와 기존 등록
인용문을 대조해 정확히 일치함을 확인(2026-07-21):

- **Jia et al. (2022)** — 2.3절 "보행속도가 10~20% 감소"는 직접 인용 없이
  정성적 서술만 사용. 최초 검증: 위 Introduction id 028 항목(p.10 원문).
- **Basu et al. (2024)** — 2.3절 "route attributes... were translated to
  their equivalent walking distance values"(p.8), "air temperature, relative
  humidity, and wind speed are spatially constant, but vary hourly"(p.6) 모두
  위 Introduction id 022 항목(2단락 재인용/기상입력 방법론 확인)과 정확히
  일치.
- **Aydin et al. (2026)** — 2.3절 "PDT = (1.0−PTT)·d0 + d0" 공식은 위 id 042
  항목(p.11)과 일치. "96 CPU×72시간" 신규 검증은 바로 위 항목 참고.
- **Colaninno et al. (2024)** — 2.3절 HEI 인용(p.13)은 위 Introduction id 021
  항목(4단락, p.13)과 일치. 800m 고정 반경(p.6)·ERA5(p.8) 인용도 위 Methods
  재인용 항목과 정확히 일치.
- **Melnikov et al. (2022) / Azegami et al. (2023) / Buo et al. (2026)** —
  2.4절에서는 직접 인용 없이 정성적 서술(0.86, 28.2%, 70% 이상 우회)만
  재사용 — 최초 검증은 위 Introduction id 023/024/037 항목 참고.
- **Bröde et al. (2012)** — 2.4절 말미 "UTCI 기준 매우 강한 더위(≥38°C)"는
  위 Introduction id 007 항목(Table 3)과 동일.

## 3. Methods (연구자료 구축 및 방법론)

### Moreno et al. (2021) — 15분 시간예산 근거

- **인용 위치**: 국문 학위논문 III장 §4 — "출발지에서 15분(Moreno et al.,
  2021) 시간 예산 내 도달 가능한 노드 집합을 산출하며..."
- **서지정보**: Moreno, C., Allam, Z., Chabaud, D., Gall, C., & Pratlong, F.
  (2021). Introducing the "15-Minute City": Sustainability, Resilience and
  Place Identity in Future Post-Pandemic Cities. *Smart Cities*, 4(1), 93–111.
  (`references/all_papers/Moreno2021_15MinuteCity.pdf`)
- **원문 (Abstract, Introduction)**: "...the re-emergence of a concept,
  initially proposed in 2016 by Carlos Moreno: the '15-Minute City'." /
  "...the 15-minute walkable neighborhood proposed by Weng et al. [9]..."
- **번역**: "...2016년 Carlos Moreno가 처음 제안한 개념인 '15분 도시'가
  재부상하였다." / "...Weng et al.이 제안한 15분 보행권 근린 개념..."
- **판단**: "15분 보행권"이라는 시간예산 자체의 개념적 출처로 적합 — 다만
  이 논문 자체는 정책·도시계획 관점의 개관 논문(perspective paper)이라
  "15분이 왜 접근성 분석의 표준 시간예산인가"를 수치적으로 증명하지는
  않음(그 성격의 논문 아님). 개념 출처 인용으로는 정당, 수치적 근거로
  오인되지 않도록 유의.
- **확인**: 사용자 확인 완료 (2026-08-04, 원문 PDF 직접 확인 — 기존에
  마스터 파일 미등재 상태로 III장에 인용되고 있었음을 발견해 시정)

### SOLWEIG 계보 4편 — Lindberg et al.(2008/2016), Lindberg & Grimmond(2011), Wallenberg et al.(2026)

- **인용 위치**: 국문 학위논문 III장 §2(MRT 산출) — SOLWEIG 성능(R²=0.94,
  RMSE=4.8K), 식생 스킴(R²=0.91, RMSE=3.1K, τ=0.05), 지표재질 스킴,
  벽면온도 스킴(±2.5°C) 4개 수치.
- **검증 경위**: 2026-08-04 III장 인용근거정리 작업 중 마스터 파일에
  formal 등재가 안 돼 있음을 발견 — 단, `references/study_note_
  Lindberg2008_SOLWEIG1.md` 등 개별 스터디노트에는 이미 원문 수치가
  확인되어 있었음(작성일 2026-06~07월경, 원문 대조 완료 상태).
- **Lindberg et al.(2008)** — SOLWEIG 1.0, *Int J Biometeorol*, 52(7),
  697–713. 예테보리 현장검증 R²=0.94, RMSE=4.8K(스터디노트 p.127-128
  확인 기록).
- **Lindberg & Grimmond(2011)** — 식생 스킴(SOLWEIG 2.0), *Theoretical
  and Applied Climatology*, 105(3), 311–323. R²=0.91, RMSE=3.1K, 캐노피
  투과율 τ=0.05 권장(완전히 잎 달린 여름 조건)(스터디노트 p.66-81 확인
  기록).
- **Lindberg et al.(2016)** — 지표재질 스킴, *Int J Biometeorol*, 60(9),
  1439–1452. 재질별 알베도·방사율 값(아스팔트 ε=0.95/α=0.18 등, Table 1)
  확인 기록.
- **Wallenberg et al.(2026)** — 벽면온도 step heating 스킴,
  *Geoscientific Model Development*, 19, 1321–1336. 새 스킴 적용 시
  T_mrt 최대 ±2.5°C 차이(스터디노트 §7.2 확인 기록, 단 CIBSE(2015) 표
  인용값이라는 점도 함께 기록돼 있음).
- **판단**: 4편 모두 스터디노트 단계에서는 원문 대조가 이미 돼 있었으나
  이 마스터 파일에는 옮겨적히지 않았던 상태 — 이번에 위치만 정식
  등재. 개별 수치의 원문 페이지·직접 인용문은 각 스터디노트 파일 참고
  (이미 확인된 내용이라 여기서 재복사하지 않음).
- **확인**: 사용자 확인 완료 (스터디노트 단계 2026-06~07월, 마스터파일
  정식 등재 2026-08-04)

### Lindberg et al. (2018) — UMEP

- **인용 위치**: III장 §2 — "SOLWEIG는 QGIS 기반 오픈소스 플랫폼
  UMEP(Lindberg et al., 2018)에 통합되어 배포되며..."
- **서지정보**: Lindberg, F. et al. (2018). Urban Multi-scale Environmental
  Predictor (UMEP). *Environmental Modelling & Software*, 99, 70–87.
  (`references/all_papers/Lindberg2018_UMEP.pdf`)
- **원문**: "...the implications of green infrastructure on runoff
  (SUEWS); microscale heat stress (**SOLWEIG**); solar energy production
  (SEBE)..." — SOLWEIG가 UMEP 플러그인의 구성 도구 중 하나임을 명시.
- **판단**: "SOLWEIG가 UMEP에 통합돼 있다"는 사실관계 확인 완료.
- **확인**: 사용자 확인 완료 (2026-08-04)

### [id 022] Basu et al. (2024) — Methods 재인용

- **최초 등장**: Introduction 1·2단락 참고
- **인용 목적**: 기상 입력 방식 근거 — "MRT만 공간적으로 산출하고, 기온·습도·풍속은
  공간적으로 균일한 단일값(시간별로만 변화)을 사용"하는 방식이 본 연구만의
  단순화가 아니라 기존 SCI 연구에서도 채택된 방식임을 뒷받침
- **원문 (p.6)**:
  > "mean radiant temperature is the only variable among the four that varies
  > both spatially and temporally; air temperature, relative humidity, and
  > wind speed are spatially constant, but vary hourly. When all four
  > components are combined, we obtain hourly UTCI values at a 2.5 meter
  > resolution."
- **번역**: "네 변수(기온·습도·풍속·MRT) 중 MRT만 공간적으로도 시간적으로도
  변화하며, 기온·상대습도·풍속은 공간적으로는 일정하되 시간별로만 변화한다.
  네 요소를 결합하여 2.5m 해상도의 시간별 UTCI 값을 얻는다."
- **비고**: 기온/습도/풍속은 ERA5(Copernicus C3S) 재분석자료에서 2m(기온·습도)
  및 1.5m(풍속) 고도 값을 사용. URock/CFD 등 별도 바람장 모델링 없음.
- **확인**: 사용자 확인 완료 (2026-07-15)

### [id 021] Colaninno et al. (2024) — Methods 재인용

- **최초 등장**: Introduction 2단락 참고
- **인용 목적**: 위와 동일 — Basu(2024)와 같은 연구팀(공저자 겹침)이 동일 방법론을
  다른 사례(LA 폭염)에서도 사용했음을 교차 확인
- **원문 (p.8)**:
  > "We then used the ERA5 dataset, produced by the Copernicus Climate Change
  > Service (C3S) at the European Center for Medium-Range Weather Forecasts
  > (ECMWF)... meteorological data, are the main inputs used to model UTCI."
- **번역**: "ECMWF의 Copernicus 기후변화서비스(C3S)가 생산하는 ERA5 데이터셋을
  사용하였다... 기상 데이터가 UTCI 모델링의 주요 입력값이다."
- **비고**: 1m 해상도 SOLWEIG로 MRT만 공간분포 산출, 기온·습도·풍속은 ERA5
  단일값. CFD/URock 언급 없음 — Basu(2024)와 동일한 팀 방법론 확인(교차검증).
- **확인**: 사용자 확인 완료 (2026-07-15)

### [id 021] Colaninno et al. (2024) — Methods 재인용 2 (링크 단위 UTCI 할당 방법)

- **인용 위치**: 국문 학위논문 III장 §3(UTCI 산출 및 기상 입력 방식) — 우리
  연구가 링크 지오메트리를 버퍼링(폭/2)한 뒤 겹치는 UTCI 픽셀의 평균값을
  그 링크에 할당하는 방식(`rasterstats.zonal_stats(..., stats=['mean'])`)의
  선례로 인용. 이 claim은 2026-08-04 이전까지 `study_note_
  Colaninno2024_SidewalkHeatRisk.md`에 원문 인용 없이 요약("세그먼트 버퍼로
  픽셀 평균")으로만 남아 있어 이번에 원문 대조로 정식 검증함.
- **원문 (p.9~10, "Heat exposure index" 절)**:
  > "We first computed the average UTCI value for each segment that
  > represents the segment-level hazard. We created a buffer around each
  > segment in the sidewalk network and overlaid it against the UTCI raster
  > layer (that we had created with a 1-meter spatial resolution). We
  > calculated the average UTCI across all the pixels that intersected with
  > the segment buffer and assigned it to that segment as its heat hazard."
- **번역**: "우리는 먼저 각 세그먼트의 위험도를 나타내는 평균 UTCI 값을
  계산했다. 사이드워크 네트워크의 각 세그먼트 주변에 버퍼를 생성하고 이를
  UTCI 래스터 레이어(1m 해상도로 제작)에 겹쳤다. 세그먼트 버퍼와 교차하는
  모든 픽셀의 평균 UTCI를 계산해 그 세그먼트의 열위험값으로 할당했다."
- **보조 원문 (p.10, "Heat risk" 절, 경로 단위 집계)**:
  > "...we obtained all feasible routes to the selected critical
  > destinations... and computed weighted averages of the segment-level
  > hazard values, with segment lengths as weights and UTCI as heat hazard."
- **번역**: "...선택된 핵심 목적지까지의 모든 가능한 경로를 구하고,
  세그먼트 길이를 가중치로 하여 세그먼트별 위험값의 가중평균을 계산했다."
- **판단**: "버퍼+픽셀 평균"·"세그먼트 길이 가중평균" 둘 다 우리 서술과
  정확히 일치. 정식 검증 완료.
- **확인**: 사용자 확인 완료 (2026-08-04)

**종합 판단**: MIT 팀(Basu·Colaninno)의 SCI 논문 2편이 모두 "MRT만 공간적으로
산출, 기온/습도/풍속은 재분석자료 기반 단일값"이라는 동일 방법론을 채택 —
본 연구가 URock 등 보행자 수준 바람장 모델링 없이 met.txt 단일값 + SOLWEIG
공간 MRT를 쓰는 것에 대한 선례로 사용 가능. Aydin et al.(2026)만 예외적으로
OpenFOAM CFD(96 CPU, 72시간)를 사용하나 이는 슈퍼컴퓨팅 자원이 필요한
예외 사례로 본 연구 규모에서는 비현실적임을 근거로 언급 가능.

### UMEP/SOLWEIG 소스코드 확인 — 풍속 높이보정 (논문 아님, 우리가 실제 사용하는 도구 원본)

- **인용 목적**: "풍속을 별도 보정 없이 그대로 썼다"는 인상을 피하고, 우리가 쓰는
  SOLWEIG 자체에 표준 풍속 높이보정이 내장되어 있으며 그 가정(10m 관측고도)이
  우리 AWS 데이터 실제 관측고도와 일치함을 Methods에서 명시하기 위함
- **원본 파일**: `/opt/miniconda3/lib/python3.13/site-packages/umep/functions/SOLWEIGpython/solweig_runner.py`,
  L539-540
  ```python
  WsPET  = (1.1  / self.params.Wind_Height.Value.magl) ** 0.2 * self.environ_data.Ws[i]
  WsUTCI = (10.0 / self.params.Wind_Height.Value.magl) ** 0.2 * self.environ_data.Ws[i]
  ```
- **기본 파라미터**: `/opt/miniconda3/lib/python3.13/site-packages/umep/parametersforsolweig.json`
  L186-191 — `"Wind_Height": {"Value": {"magl": 10.0}, "Comment": "Height of wind
  sensor for PET and UTCI calcualtions."}`
- **판단**: SOLWEIG는 관측 풍속을 거듭제곱 프로파일(지수 0.2)로 PET는 1.1m,
  UTCI는 10m 높이로 각각 보정하는 구조. 기본 관측고도 가정은 10m이며, 우리
  풍속 입력 출처(AWS 성동 421, WMO 표준 10m 관측탑 — `2026-07-09_MRT산출_
  기술노트` 참고)와 정확히 일치해 별도 보정 없이도 이 코드의 전제와 정합적.
  **논문 인용이 아니라 소프트웨어 소스코드 직접 확인**이므로 위 12편·재인용
  2건과는 성격이 다름 — Methods에서 "SOLWEIG(UMEP)의 표준 처리 방식을
  따랐다"는 서술의 근거로 사용, 참고문헌 목록에는 UMEP 자체 논문
  (Lindberg et al. 2018, id 확인 필요)으로 등재 검토.
- **확인**: 사용자 확인 완료 (2026-07-16)

### [id 007] Bröde et al. (2012) — Methods 재인용 (풍속 입력 규정)

- **최초 등장**: Introduction 5단락 참고(Hard Cut 임계값 근거)
- **인용 목적**: UTCI 계산 자체의 공식 절차와 풍속 입력 규정의 근거 — 우리가
  10m 관측 풍속을 별도 높이보정 없이 그대로 쓰는 것이 임의 처리가 아니라
  원 논문의 공식 요구사항을 그대로 만족하는 것임을 Methods에서 명시하기 위함
- **원문 (p.491, "Input of wind speed")**:
  > "Following meteorological conventions..., wind speed (va) is taken as the
  > value 10 m above the ground level. The UTCI-Fiala model of thermoregulation
  > internally applies a formula (Oke 1987) to calculate the local wind speed
  > profile at the body level. If wind speed measurements are only available
  > from a height x (m) different from 10 m, the user should apply the same
  > formula to convert the measured wind speed (va_xm) to the required input va
  > according to Eq. 3. va = va_xm · LOG(10/0.01) / LOG(x/0.01)"
- **번역**: "기상학 관례에 따라 풍속(va)은 지상 10m 높이 값을 사용한다. UTCI-Fiala
  모델은 내부적으로 Oke(1987) 공식을 적용해 신체 높이의 국소 풍속 프로파일을
  계산한다. 관측 풍속이 10m가 아닌 다른 높이(x)에서만 확보 가능하다면, 사용자는
  동일한 공식(식 3)을 적용해 관측 풍속을 요구되는 10m 입력값으로 변환해야 한다."
- **원문 (p.490, "Usage guidelines")**: "Computing UTCI values... by using the
  software and the web-based application available from the project's website
  (http://www.utci.org)... straightforward, given the user has the required
  input on air temperature, wind speed, humidity and mean radiant temperature."
  — 공식 UTCI 산출은 6차 다항 회귀식(polynomial regression)으로 근사한
  "operational procedure"이며, 이를 구현한 공식 소프트웨어/웹앱이 utci.org에
  있음. **우리가 쓰는 `pythermalcomfort.utci()`는 이 공식 회귀식의 재구현체.**
- **교차검증(2026-07-16)**: Basu et al.(2024) p.6는 ERA5 풍속을 **1.5m** 높이
  그대로 사용, Bröde(2012)의 10m 규정이나 Eq.3 변환 언급 없음(⚠️ 이유 불명 —
  ERA5 표준 변수 자체가 10m인데 왜 1.5m을 썼는지 원문에 설명 없음). 반면 본
  연구는 AWS 성동 421(WMO 표준 10m 관측탑) 데이터를 변환 없이 그대로 사용 —
  **Bröde(2012) 원 논문의 공식 절차를 Basu(2024)보다 더 엄밀하게 준수**하는
  구조임을 확인.
- **확인**: 사용자 확인 완료 (2026-07-16)

### UMEP 소스코드 확인 — 기상요인을 "보간"이 아니라 "격자 모델링"으로 공간화하는 공식 경로 존재

- **인용 목적**: "우리가 쓰는 단일값 방식이 UMEP에서 유일하게 가능한 방식인가?"에
  대한 답 — UMEP 자체에 기상요인을 공간적으로 반영하는 공식 도구가 있는지 확인
- **확인 대상**: `processing_umep/postprocessor/spatialtc_algorithm.py`
  (UMEP의 공식 "Spatial Thermal Comfort" 도구 — UTCI/PET/COMFA를 Tmrt 래스터로부터
  계산하는 바로 그 도구)
- **원본 코드 (L93, L127, L201)**:
  ```python
  UROCK_MAP = 'UROCK_MAP'
  self.addParameter(QgsProcessingParameterRasterLayer(self.UROCK_MAP, ...))
  ws = self.parameterAsRasterLayer(parameters, self.UROCK_MAP, context)
  ```
  같은 파일에서 기온·습도는 여전히 스칼라: `Ta = metdata[posMet, 11][0][0]`,
  `RH = metdata[posMet, 10][0][0]` (met.txt에서 단일 시점값 하나만 추출)
- **판단**: **UMEP의 공식 UTCI 산출 도구는 풍속만 래스터(격자)로 받고, 기온·습도는
  여전히 스칼라 단일값으로 처리하는 구조**. 이 래스터는 여러 관측소 값을 보간(IDW/
  크리깅)한 게 아니라, **URock**(별도 UMEP 도구, `urock_processing_algorithm.py`
  확인 — "calculate spatial variations of wind speed and wind direction in 3
  dimensions using 2.5D building and vegetation data", 건물·식생 형상 기반 진단형
  바람모델)이 만든 물리 기반 격자를 그대로 받는 구조. **본 연구는 이 UROCK_MAP
  경로를 쓰지 않고 커스텀 `pythermalcomfort.utci()` 스크립트로 Ta/RH/풍속 전부
  스칼라 처리** — UMEP의 "완전 공식" 경로와는 이 지점에서 갈라짐(URock을 추가
  도입할지는 별도 검토 필요, 계산비용·시간 예산 고려).
- **부가 확인**: UMEP에는 기온을 공간적으로 모델링하는 별도 도구 **TARGET**도 존재
  (`target_algorithm.py` — Broadbent et al. 2019 기반). 아래 별도 항목 참고.
- **확인**: 사용자 확인 완료 (2026-07-16)

### Broadbent et al. (2019) — TARGET 모델 (PDF 확보·직접 확인 완료)

- **서지정보**: Broadbent, A.M., Coutts, A.M., Nice, K.A., Demuzere, M.,
  Krayenhoff, E.S., Tapper, N.J., & Wouters, H. (2019). The Air-temperature
  Response to Green/blue-infrastructure Evaluation Tool (TARGET v1.0): an
  efficient and user-friendly model of city cooling. *Geoscientific Model
  Development*, 12(2), 785–803. DOI: 10.5194/gmd-12-785-2019 (오픈액세스,
  PDF 확보 완료: `references/all_papers/Broadbent2019_TARGET.pdf`)
- **인용 목적**: UMEP 생태계 안에 기온을 공간적으로(격자로) 모델링하는 공식 도구가
  실제로 존재함을 확인 — 우리가 안 쓰고 있을 뿐 "택할 수 있는 선택지"였음을 명시
- **원문 확인 (본문)**: "...spatial resolution of 100 m for air temperature
  simulations..." / "TARGET treats each model grid point..." / 검증 시
  "27 AWSs"(호주 애들레이드 Mawson Lakes 실제 관측소 27개망)를 대조 지점으로 사용
- **판단**: TARGET은 여러 관측소 값을 단순 보간하는 게 아니라, 토지피복(수목·수역·
  포장 비율)을 입력으로 한 **에너지수지 기반 물리모델**로 100m 격자 기온을 산출하고,
  27개 실측망으로 검증한 도구. UMEP의 `target_algorithm.py` 소스코드에도 "Possibilities
  to model multiple grids or a single location is available"라고 명시됨(오늘 소스
  코드 확인). 이 역시 URock과 마찬가지로 본 연구는 도입하지 않은 경로.
- **확인**: 사용자 확인 완료 (2026-07-16, PDF 직접 확인)

### Lee, Park & Mayer (2025) — PDF 확보·직접 확인 완료

- **서지정보**: Lee, H., Park, S., & Mayer, H. (2025). Approach for the vertical
  wind speed profile implemented in the UTCI basics blocks UTCI applications at
  the urban pedestrian level. *International Journal of Biometeorology*, 69(3),
  567–580. DOI: 10.1007/s00484-024-02835-x
  (`references/all_papers/Lee2025_UTCI_VerticalWindProfile.pdf`)
- **인용 목적**: 우리가 AWS 10m 풍속을 그대로 쓰는 것(변환 없이)이 Bröde(2012)
  공식 절차와는 정합적이지만, **UTCI 자체의 풍속 프로파일 가정이 도시환경에서
  구조적 한계를 갖는다**는 점을 Methods/Discussion에서 명시하기 위함
- **원문 (Abstract, p.1)**:
  > "the VWSP is implemented in the UTCI basics, but only for neutral atmospheric
  > stability and a roughness length (z0) for short-cut grassland (z0 = 0.01 m).
  > This methodological approach cannot be changed in the UTCI basics so far...
  > [UTCI] cannot be applied [with log law] within the urban canopy layer (UCL).
  > If the UTCI is nevertheless applied at the urban pedestrian level,
  > inaccuracies in the UTCI values will occur. With reference to z0 = 0.80 m,
  > which is more typical for the UCL, they can be **up to 7 K**"
- **번역**: "풍속수직프로파일(VWSP)은 UTCI 기초에 구현되어 있으나 중립대기조건과
  짧은잔디밭 조도길이(z0=0.01m)에 대해서만 성립하며, 이 방법론적 접근은 UTCI
  기초에서 현재 변경 불가능하다... UTCI가 그럼에도 도시 보행자 수준에 적용되면
  UTCI 값에 오차가 발생한다. 도시캐노피층에 더 전형적인 z0=0.80m을 기준으로 하면
  그 오차는 최대 7K에 이를 수 있다."
- **판단**: 우리가 지금 쓰는 표준 UTCI(Bröde 2012 공식 그대로, z0=0.01m 암묵
  가정)는 도시캐노피층 내부(즉 건물 사이 보행자 수준)에서 최대 7K의 오차 가능성을
  내포함 — 이는 우리 연구의 **명시적 한계(limitation)**로 Discussion에 서술
  필요. 동시에 이 논문이 인용하는 Brecht et al.(2020)의 스케일 구분(아래 참고)은
  오히려 "그렇다면 어느 스케일에 UTCI를 적용하는 게 맞는가"에 대한 답을 제공 —
  우리의 단일값+MRT공간화 방식을 정당화하는 근거로 반전 활용 가능.
- **확인**: 사용자 확인 완료 (2026-07-16, PDF 직접 확인)

### Brecht, Schädler & Schipper (2020) — PDF 확보·직접 확인 완료

- **서지정보**: Brecht, B.M., Schädler, G., & Schipper, J.W. (2020). UTCI
  climatology and its future change in Germany – an RCM ensemble approach.
  *Meteorologische Zeitschrift*, 29(2), 97–116. DOI: 10.1127/metz/2020/1010
  (`references/all_papers/Brecht2020_UTCIClimatologyGermany.pdf`)
- **인용 목적**: "UTCI가 적합한 공간 스케일"에 대한 1차 출처 직접 확인(Lee et
  al. 2025의 재인용이 정확한지 대조) — 본 연구의 도메인 전체 단일 기상값 채택을
  뒷받침하는 핵심 근거
- **원문 (p.2, Introduction)**:
  > "the UTCI uses the wind speed at a height of 10 m above ground level, making
  > it well suited for operational data and applications at **spatial scales
  > from city quarters onwards**, whereas indices using the wind speed at the
  > biometeorological reference height of 1.1 m above ground level are more
  > suitable for **building and street resolving simulations**."
- **번역**: "UTCI는 지상 10m 높이의 풍속을 사용하며, 이 때문에 **동(city quarter)
  단위 이상의 공간 스케일**에서의 운영 데이터·적용에 적합하다. 반면 생체기상학
  기준높이(1.1m)의 풍속을 직접 쓰는 지수들은 **건물·거리 단위의 정밀 시뮬레이션**에
  더 적합하다."
- **판단**: Lee et al.(2025)의 재인용과 원문이 정확히 일치함을 확인(교차검증
  완료). **본 연구가 URock(건물 해상도 풍속장)을 도입하지 않고 도메인 단일
  기상값 + MRT만 5m 공간화하는 방식이, "UTCI는 애초에 동 단위 이상 스케일에
  맞게 설계됐다"는 이 원 논문의 명시적 진술과 정합적** — Aydin(2026)의 CFD
  풍속장(건물 해상도)을 UTCI에 결합하는 방식이 오히려 이 논문 기준으로는 스케일
  부정합일 수 있음을 시사.
- **확인**: 사용자 확인 완료 (2026-07-16, PDF 직접 확인)

### Krüger & Di Napoli (2022) — PDF 확보·직접 확인 완료

- **서지정보**: Krüger, E.L., & Di Napoli, C. (2022). Feasibility of climate
  reanalysis data as a proxy for onsite weather measurements in outdoor thermal
  comfort surveys. *Theoretical and Applied Climatology*. DOI:
  10.1007/s00704-022-04129-x
  (`references/all_papers/Kruger2022_ReanalysisProxy.pdf`)
- **인용 목적**: 재분석자료(단일값의 한 종류) 사용 시 발생하는 오차를 정량적으로
  보여줌 — 단, 우리는 재분석자료가 아니라 실측 AWS를 쓰므로 이 오차가 그대로
  적용되지 않는다는 점을 명확히 구분하기 위함(과잉 적용 방지)
  ERA5-HEAT는 31×31km 격자.
- **원문 (Table 3, p.348 / 373)**:
  > "Mean bias −0.81 [1h] ... Standard deviation 4.13" / Summer(N=171) "mean
  > bias −3.65 °C UTCI, whereas in winter, they overestimate it by [+1.10]"
- **번역**: "전체 평균편향 −0.81°C(표준편차 4.13), 여름철만 보면 −3.65°C 과소
  추정, 겨울철은 반대로 과대추정."
- **판단**: PDF 원문 대조 결과 어제 WebFetch 요약과 수치 일치(교차검증 완료).
  **이 오차는 ERA5(31×31km 저해상도 재분석자료) 고유의 문제이지, "단일값
  자체"의 문제가 아님** — 본 연구는 실측 AWS(성동 421) 지점값을 쓰므로 이
  논문의 오차 규모를 그대로 인용하면 과장이 됨. Methods/Limitation에서 "재분석
  자료 기반 단일값과 실측 기반 단일값은 오차 성격이 다르다"는 구분 문장의
  근거로만 활용.
- **확인**: 사용자 확인 완료 (2026-07-16, PDF 직접 확인)

- **참고(등재 대상 아님)**: Gallacher & Boehnke (2025), *Int J Biometeorol*,
  DOI: 10.1007/s00484-024-02830-2 (드레스덴 모바일 열쾌적성 매핑) — 여러 관측소
  보간 없이 이동측정 경로 자체를 시계열로 씀, 풍속은 아예 측정 안 함("negligible
  wind conditions"). 우리 연구에 직접 참고할 방법론은 아니라 등재 보류.

### Hard Cut 임계값 근거 — 나이대별 열스트레스 내성 (몬테카를로 임계값 방어, 2026-07-29 착수)

> 배경: 지도교수(박진우 교수님) 문제제기 — Bröde et al.(2012) UTCI 급간표를 그대로
> Hard Cut 임계값(38°C)의 근거로 쓰는 건 "왜 하필 38°C인가"라는 질문에 취약함.
> 나이대별 열스트레스 내성 차이를 반영한 임계값 분포를 문헌에서 확보해 몬테카를로
> 시뮬레이션(1000회, UTCI 30~48°C 히스토그램의 최빈값을 임계값으로 채택)으로
> 임계값을 재도출하려는 시도. 아래 3편은 이 목적을 위해 확보·확인.

#### Thorsson et al. (2014) — 핵심 근거, 나이대별 Tmrt 임계값 수치 제공

- **서지정보**: Thorsson, S., Rocklöv, J., Konarska, J., Lindberg, F., Holmer, B.,
  Dousset, B., & Rayner, D. (2014). Mean radiant temperature – A predictor of
  heat related mortality. *Urban Climate*, 10, 332-345.
  (`references/all_papers/Thorsson2014_MRT_HeatMortality.pdf`)
- **원문 (Table 2, p.339, "Risk classification, short-term effects of daily
  maximum mean radiant temperature (Tmrt) over lag 0–1")**:

  | 위험단계 | 위험증가율 | 전연령 | 45–79세 | 80세 이상 |
  |---|---|---|---|---|
  | 0 | 0% | 47.4°C | 46.7°C | 47.6°C |
  | 1 | 5% | 57.1°C | 58.8°C | 55.5°C |
  | 2 | 10% | — | — | 59.4°C |

- **번역**: "표 2. 일일 최대 평균복사온도(Tmrt)의 단기 영향에 따른 위험 분류(lag
  0–1일)." — 위험증가율(%)별로 전연령/45–79세/80세 이상 각각의 Tmrt 임계값을
  제시.
- **비고**: 이 논문 자체는 **Tmrt(MRT) 기준**이지 UTCI 기준이 아니다. 저희 연구는
  최종적으로 UTCI를 쓰므로, 이 임계값들을 그대로 쓰려면 (a) UTCI 대신 MRT를
  몬테카를로 축으로 쓰거나 (b) 동일 기상조건 하에서 MRT→UTCI 변환식을 적용해
  등가 UTCI 임계값으로 환산하는 절차가 필요함 — 아직 미확정, 방법론 설계 시
  결정할 것.
- **확인**: 사용자 확인 완료 (2026-07-29)

#### Tousi(Evgenia), Mela & Tseliou (2024) — 제한적 활용(UTCI는 나이 무관 동일값 확인)

- **서지정보**: Tousi, E., Mela, A., & Tseliou, A. (2024). Thermal Stress in
  Outdoor Spaces During Mediterranean Heatwaves: A PET and UTCI Analysis of
  Different Demographics. *Urban Science*, 8(4), 193.
  DOI: 10.3390/urbansci8040193
  (`references/all_papers/Evgenia2024_PET_UTCI_AgeDemographics.pdf`)
- **원문 (§3.4.1, p.17-18)**:
  > "At 10 a.m., the UTCI values for four distinct demographic groups—35-year-old
  > males, 35-year-old females, 80-year-old males, and 8-year-old children—range
  > between 28.94 °C (No thermal stress) and 51.36 °C (extreme heat stress)...
  > While the UTCI values for all four demographic groups fall within the same
  > range, the implications of these values vary significantly."
- **번역**: "오전 10시, 35세 남성·35세 여성·80세 남성·8세 아동 네 집단의 UTCI
  값은 28.94°C(무스트레스)~51.36°C(극심한 열스트레스) 사이였다... 네 집단 모두
  UTCI 값 자체는 같은 범위 안에 있지만, 그 값이 의미하는 위험도는 집단별로
  크게 다르다."
- **판단**: 이 논문은 PET는 나이·체구에 따라 다른 값을 산출하지만, **UTCI 공식
  자체에는 나이 변수가 없어 모든 집단이 동일한 UTCI 값을 받는다**는 것을
  명시적으로 확인해준다 — 즉 "왜 UTCI 자체가 아니라 Thorsson(2014) 같은 외부
  문헌에서 나이대별 임계값을 따로 가져와야 하는가"를 정당화하는 근거로 활용
  (UTCI 수식이 나이를 반영 못 하므로 사후적으로 임계값을 나이대별로 조정해야
  한다는 논리).
- **확인**: 사용자 확인 완료 (2026-07-29)

#### Wolf et al. (2023) — 일반적 근거(단위 불일치로 수치 직접 활용 불가)

- **서지정보**: Wolf, S. T., Cottle, R. M., Fisher, K. G., Vecellio, D. J., &
  Kenney, W. L. (2023). Heat stress vulnerability and critical environmental
  limits for older adults. *Communications Earth & Environment*, 4, 386.
  DOI: 10.1038/s43247-023-01159-9
  (`references/all_papers/Wolf2023_HeatStress_ElderlyLimits.pdf`)
- **원문 (Abstract)**:
  > "We exposed fifty-one young (23 ± 4 yrs) and 49 older (71 ± 6 yrs) adults to
  > progressive heat stress across a wide range of environments in an
  > environmental chamber... Heat compensability curves were shifted leftward
  > for older adults indicating age-dependent heat vulnerability (p < 0.01).
  > During Minimal Activity, critical environmental limits were lower in older
  > compared to young adults (p < 0.0001)."
- **번역**: "청년(23±4세) 51명과 고령자(71±6세) 49명을 환경챔버에서 다양한
  환경조건의 점증적 열스트레스에 노출시켰다... 고령자의 열보상곡선이 좌측으로
  이동해 나이에 따른 열취약성을 보였다(p<0.01). 최소활동 조건에서 임계
  환경한계는 고령자가 청년보다 낮았다(p<0.0001)."
- **판단**: 실내 챔버 실험으로 건조구온도(Tdb)+수증기압(mmHg) 단위의 임계
  환경한계를 실측 — **UTCI/MRT/PET 단위가 아니라 직접 수치 활용은 어려움**.
  "나이에 따른 열내성 차이가 실측으로 확인된 사실"이라는 일반적 근거로만 활용.
- **확인**: 사용자 확인 완료 (2026-07-29)

## 4. Results

### McDonald et al. (2021) — 스노우볼링 신규 확보(2026-08-05)

- **실제 용도(2026-08-05 갱신, 같은 날 재조정)**: 원래 IV장 §4.2 후보로
  검토했으나, **실제로는 I장 서론 1단락에 반영됨** — 최종: "환경 조성
  차이(McDonald et al., 2021)에 따라 공간적으로 불균등하게 분포하는
  경우가 많다." 처음엔 Shin & Park(2026)과 병기했으나, 사용자가 최종
  정리하며 Shin & Park는 "삶의 질" 문장에만 남기고 이 자리는 McDonald
  단독으로 확정(1단락 내 Shin & Park 반복을 1회로 완전히 줄임). IV장
  §4.2 용도는 보류(추후 검토).
- **서지정보**: McDonald, R.I., Biswas, T., Sachar, C., Housman, I.,
  Boucher, T.M., Balk, D., Nowak, D., Spotswood, E., Stanley, C.K., &
  Leyk, S. (2021). The tree cover and temperature disparity in US
  urbanized areas: Quantifying the association with income across 5,723
  communities. *PLoS ONE*, 16(4), e0249715.
  DOI: 10.1371/journal.pone.0249715
  (`references/all_papers/McDonald2021_TreeCoverTemperatureDisparity.pdf`
  — Colaninno(2024)의 스노우볼링 참고문헌에서 발견, PLoS ONE 오픈액세스라
  Claude가 직접 확보)
- **원문 (Abstract)**: "In 92% of the urbanized areas surveyed, low-income
  blocks have less tree cover than high-income blocks. On average,
  low-income blocks have 15.2% less tree cover and are 1.5°C hotter than
  high-income blocks. The greatest difference between low- and
  high-income blocks was found in urbanized areas in the Northeast of
  the United States, where low-income blocks in some urbanized areas
  have 30% less tree cover and are 4.0°C hotter."
- **번역**: "조사된 도시화지역의 92%에서 저소득 블록이 고소득 블록보다
  수목피복이 적었다. 평균적으로 저소득 블록은 수목피복이 15.2% 적고
  1.5°C 더 더웠다. 저소득-고소득 블록 간 차이가 가장 큰 지역은 미국
  북동부로, 일부 도시화지역에서 저소득 블록은 수목피복이 30% 적고
  4.0°C 더 더웠다."
- **확인**: 원문 PDF 1페이지(Abstract) 직접 확인 완료(2026-08-05). 본문
  전체 대조는 아직 안 함 — IV장§4.2에 실제로 인용하기로 결정되면 추가
  검증 필요.

### Hsu et al. (2021) — ⚠️ 사용 주의 (2026-08-05 원문 확인)

- **후보 용도(원래 기대)**: IV장§4.2 보강 — 인종/소득별 열섬노출 격차.
- **서지정보**: Hsu, A., Sheriff, G., Chakraborty, T., & Manya, D.
  (2021). Disproportionate exposure to urban heat island intensity
  across major US cities. *Nature Communications*, 12, 2721.
  DOI: 10.1038/s41467-021-22799-5 (오픈액세스, CC BY)
- **원문(Abstract)**: "the average person of color lives in a census
  tract with higher SUHI intensity than non-Hispanic whites in all but
  6 of the 175 largest urbanized areas... A similar pattern emerges for
  people living in households below the poverty line."
- **⚠️ 핵심 경고 — 우리 상관관계와 반대 방향**: 이 논문 본문(p.2, p.4)은
  "**연령 자체는 SUHI 노출 격차의 강한 설명변수가 아니며, 오히려 65세
  이상 인구가 86%의 미국 도시에서 65세 미만보다 SUHI 노출이 낮다**"고
  명시한다("people over 65 have lower SUHI exposure than those under 65
  in 86% of US cities", p.4). 우리 IV장§4.2는 "09시 감소율이 고령인구
  비율과 양의 상관(r=0.39)"이라고 서술하는데, 이 논문을 그대로 병치
  인용하면 **오귀속** — 지표(SUHI 강도 vs 우리의 TCA 감소율)와 메커니즘
  (거주지 패턴 vs 네트워크 위상)이 다르다는 점을 명시하지 않고 인용하면
  독자가 "선행연구와 반대 결과"로 오인할 위험.
- **권고**: 인종/소득 부분(핵심 결과)은 우리 IV장§4.2가 다루는 변수
  (고령인구·녹지비율)와 정확히 일치하지 않아 직접 인용 가치가 낮음.
  **연령 관련 부분은 인용하지 않거나, 인용 시 반드시 지표 차이를 명시할
  것.** 전반적으로 이 논문은 우리 IV§4.2 보강용으로 McDonald(2021)보다
  적합성이 낮다고 판단.
- **확인**: 원문 PDF 대조 완료 (2026-08-05)

### Wang et al. (2022) — 15분 근거 대체 실패, 별도 용도로 재검토

- **후보 용도(원래 기대)**: III장§4 "15분 시간예산"을 Moreno(2021)보다
  정밀하게 뒷받침 — **원문 확인 결과 기대에 못 미침**.
- **서지정보**: Wang, Y., He, B-J., Kang, C., Yan, L., Chen, X., Yin, M.,
  Liu, X., & Zhou, T. (2022). Assessment of walkability and walkable
  routes of a 15-min city for heat adaptation: Development of a dynamic
  attenuation model of heat stress. *Frontiers in Public Health*, 10,
  1011391. DOI: 10.3389/fpubh.2022.1011391 (오픈액세스, CC BY)
- **원문 확인 결과**: "왜 15분인가"에 대한 별도의 수치적 도출/정당화는
  이 논문에도 없음 — Moreno(2021)와 마찬가지로 "15분 도시" 개념(citation
  36)을 전제로 받아들일 뿐. 다만 이 논문 고유의 실험(128명, 4단계
  열스트레스, 15분 도보)에서는 15분을 실제 프로토콜로 사용:
  "a 15-min walkability experiment was conducted... A total of 128
  residents attended... requested to walk for 15 min at four levels of
  heat stress" (p.8).
- **판단**: **III장§4의 15분 근거는 Moreno(2021) 그대로 유지 — 이 논문으로
  교체/보강 불필요.** 다만 이 논문 고유의 DAM(Dynamic Attenuation Model,
  R_t = H − S_t, Eq.3, p.8) 방법론은 "잔여 열내성"이라는 개념이 흥미로워
  V장(향후연구, 개인별 열내성 반영 확장) 참고자료로는 남겨둘 만함 — 우선
  순위 낮음.
- **확인**: 원문 PDF 대조 완료 (2026-08-05)

## 5. Discussion

### Jenelius, Petersen & Mattsson (2006)

- **인용 위치**: 국문 학위논문 V장 §2(정책적 함의) — "도로망 취약성 분석의
  기존 표준 방법론(Jenelius, Petersen & Mattsson, 2006 — 링크를 하나씩
  복구/폐쇄했을 때 접근성이 얼마나 회복/감소하는지로 링크의 '중요도'를
  정의하는 전체망 스캔 방식)을 그대로 적용하였다" 및 결론·초록 등 총 8곳
  재인용(전부 같은 근거).
- **서지정보**: Jenelius, E., Petersen, T., & Mattsson, L.-G. (2006).
  Importance and exposure in road network vulnerability analysis.
  *Transportation Research Part A: Policy and Practice*, 40(7), 537–560.
  (`references/all_papers/Jenelius2006_rodenetwork_vulnerability.pdf`)
- **원문 (p.537~538, Abstract/Introduction)**:
  > "The concepts of link importance and site exposure are introduced. In
  > this paper, several link importance indices and site exposure indices
  > are derived, based on the increase in generalised travel cost when
  > links are closed."
  > "...following Nicholson and Du (1994), we call the consequences for a
  > collection of sites of a failing link or group of links the importance
  > of that link/group of links. As a measure of the consequences of
  > failure we use the increase in generalised travel cost."
- **번역**: "링크 중요도와 지점 노출이라는 개념을 도입한다. 본 논문에서는
  링크가 폐쇄되었을 때 일반화된 통행비용이 얼마나 증가하는지를 기반으로
  여러 링크 중요도 지수와 지점 노출 지수를 도출한다." / "...Nicholson과
  Du(1994)를 따라, 하나의 링크(또는 링크 집합)의 고장이 여러 지점에
  미치는 결과를 그 링크(집합)의 '중요도'라 부른다. 고장의 결과를 측정하는
  척도로는 일반화된 통행비용의 증가를 사용한다."
- **판단**: "링크 제거/복구 → 접근성 변화로 중요도를 정의"라는 우리 서술과
  정확히 일치. "일반화된 비용(generalised cost)"이라는 표현도 우리가 V장
  §2에서 "누적 길이(m)"를 개입 규모 단위로 쓰는 근거("일반화된 비용으로
  중요도를 정의하는 관행")와 정확히 부합 — 원문에 그대로 있는 용어였음.
- **확인**: 사용자 확인 완료 (2026-08-04, 사용자가 PDF 직접 다운받아 제공)

### Nemhauser, Fisher & Wolsey (1978)

- **인용 위치**: 국문 학위논문 V장 §2 — "Nemhauser, Fisher & Wolsey(1978)의
  탐욕적 집합함수 최적화 방식(매 단계 한계이득이 가장 큰 후보를 선택)을
  그대로 유지하되, 이득이 동점일 때는 출발지로부터의 거리가 가까운 후보를
  우선하는 지연 규칙(tie-breaking)을 추가하여 재계산하였다."
- **서지정보**: Nemhauser, G.L., Wolsey, L.A., & Fisher, M.L. (1978). An
  analysis of approximations for maximizing submodular set functions—I.
  *Mathematical Programming*, 14(1), 265–294.
  (`references/all_papers/Nemhauser1978_approximations.pdf`)
- **원문 (p.276, §4 "The greedy heuristic for submodular set functions")**:
  > "A natural way to find solutions to problem (1.6) quickly is to start
  > from the null set and add elements one at a time, taking at each step
  > that element which increases z the most. The resulting solution is
  > called a 'greedy' solution..."
- **번역**: "문제(1.6)의 해를 빠르게 찾는 자연스러운 방법은, 공집합에서
  시작해 원소를 하나씩 추가하되 매 단계 z를 가장 많이 증가시키는 원소를
  선택하는 것이다. 이렇게 구해진 해를 '탐욕적(greedy)' 해라고 부른다..."
- **판단**: 저자명 표기 주의 — 원문 표지의 저자 순서는 **Nemhauser, Wolsey,
  Fisher**이나(논문 헤더 확인), 국문 학위논문·본 목록 모두 관행적으로
  통용되는 "Nemhauser, Fisher & Wolsey"로 표기해왔음 — 실제로는 저자 3인
  동일 논문이라 인용 자체는 문제없으나, 정확한 원문 저자 순서와 다르다는
  점은 기록해둠(추후 참고문헌 목록 표기 시 원문 순서로 통일할지 사용자
  결정 필요). "매 단계 한계이득 최대 원소 선택"이라는 우리 서술과 원문의
  greedy heuristic 정의가 정확히 일치.
- **확인**: 사용자 확인 완료 (2026-08-04, 사용자가 PDF 직접 다운받아 제공)

### Jenelius (2010) — 참고용 보조 자료(직접 인용 아님)

- **성격**: Jenelius, Petersen & Mattsson(2006)의 1저자 Erik Jenelius의
  박사학위논문(KTH, *Large-Scale Road Network Vulnerability Analysis*,
  2010) — 위 2006년 논문을 본인 학위논문의 "Paper I"로 명시하며 동일한
  importance/exposure 개념을 더 상세히 정식화함
  (`references/all_papers/Jenelius2010_PhDThesis_RoadNetworkVulnerability.pdf`).
- **용도**: 2026-08-04 당시 2006년 원논문(페이월) 접근 전, 같은 개념을
  가진 대체 자료로 먼저 확인했던 것. 2006년 원논문을 사용자가 직접
  확보해준 뒤로는 본 학위논문은 더 이상 인용에 쓰지 않음 — 기록만 남김.

## 6. Conclusion

*(검증 완료 항목 없음)*

---

## 7. 데이터·법령 출처 (원본 자료 제공기관·다운로드 시점·요소)

> 선행연구(논문)와 별개로, 우리가 실제로 다운로드해서 쓰는 원본 데이터·법령도
> 같은 원칙(추정 금지, 확인된 사실만 기록)으로 여기 등재한다. "이 숫자/변수
> 어디서 왔지?"를 추후 바로 추적하기 위함. **날짜는 다음 우선순위로 기록**:
> (1) 파일명에 포함된 다운로드 타임스탬프(가장 신뢰), (2) 다운로드 스크립트에
> 명시된 작성일, (3) 파일시스템 생성일(추정치, ⚠️ 표시) — 정확한 날짜를 셋 다
> 확인 못한 항목은 "⚠️ 사용자 확인 필요"로 남김.

### 7.1 보행 네트워크

- **OpenStreetMap (OSM)** — osmnx로 다운로드(`data/network/01_download_seoul_network.py`).
  `ox.graph_from_place("Seoul, South Korea", network_type="walk")`, motorway/
  motorway_link 링크는 후처리로 제거. 저장: `seoul_walk_network.graphml/.gpkg`.
  ⚠️ **정확한 다운로드 일자 미확인** — 스크립트에 날짜 미기재, 파일 자체도
  이후 여러 차례 재처리됨.
- **서울 열린데이터광장 — TbTraficWlkNet API** (자치구별 도보 네트워크 공간정보).
  다운로드: **2026-08-02**(스크립트 작성일=실행일, `03_Method_C/code/
  download_seoul_walk_api_network.py` 헤더 명시). 저장:
  `data/network/2026-08-02_seoul_walk_api_network.gpkg`. **받은 필드**:
  LNKG_ID, LNKG_WKT, LNKG_TYPE_CD, BGNG_LNKG_ID, END_LNKG_ID, LNKG_LEN,
  SGG_NM, EMD_NM, EXPN_CAR_RD, SBWY_NTW, BRG, TNL, OVRP, CRSWK, PARK, BLDG
  (스크립트 `FIELDS` 리스트 그대로). API 키 발급 기관: 서울특별시
  (data.seoul.go.kr).

### 7.2 지형·건물·수목

- **지면(DEM)**: Copernicus GLO-30(30m, 오픈소스, ESA). 서울 영역
  `N37_E126.tif`, `N37_E127.tif` → `GLO30_Seoul_EPSG5186_30m.tif`로 병합.
  파일 생성일 2026-07-01(⚠️ 추정 — 다운로드 스크립트 미확인).
- **건물 높이**: 건축물대장 통합정보 `F_FAC_BUILDING`(국토교통부/
  국가공간정보포털 계열로 추정) — HEIGHT·지상층수(GRND_FLR) 필드 실측값
  사용, 결측 시 도로명주소 건물자료(TL_SPBD_BULD)로 층수 보완(BD_MGT_SN
  키 조인). 파일: `data/F_FAC_BUILDING_서울.zip`(생성일 2026-07-07, ⚠️ 추정).
  **제공기관명 정확한 표기 사용자 확인 필요**(국토교통부 vs 각 자치구
  등록 여부).
- **도시숲 캐노피**: 산림청 임상도(1:5,000, 서울시) — `HEIGHT`(임분고,
  00~28m 2m 간격 실측), `FRTP_NM`(임상명), `KOFTR_NM`(수종구성) 필드 사용.
  파일: `data/녹지데이터 복사본/임상도/11_서울시/`. ⚠️ 다운로드 일자
  미확인 — 갱신년도가 폴리곤별로 2015~2023 혼재(기술노트 §2.3, 한계 항목
  이미 명시됨).
- **토지피복도**: 환경부 세분류(1:5,000, 41클래스) — 국가공간정보포털
  또는 환경공간정보서비스(egis.me.go.kr)로 추정. 파일: `data/토지피복도/
  SG05_*.zip`(다수), 파일명에 **다운로드일 20251113 = 2025-11-13**로
  명시되어 있어 신뢰도 높음. UMEP 5클래스(building/paved/grass/bare_soil/
  water)로 재분류(`landcover_crosswalk_L3_to_UMEP.csv`).

### 7.3 기상

- **일사량**: ASOS 서울(108) 실측 전천일사(MJ/m²) → W/m² 환산. 기상청
  기상자료개방포털(data.kma.go.kr) 추정. 파일: `data/OBS_ASOS_TIM_
  20260702021244.csv` — **파일명 타임스탬프 = 다운로드 시점 2026-07-02
  02:12:44**(포털 자동 생성 파일명 규칙, 신뢰도 높음).
- **풍속**: AWS 성동(관측소 421) 10m 관측탑 실측. 기상청 기상자료개방포털
  추정. 파일: `data/OBS_AWS_TIM_20260707154958.csv` — **다운로드 시점
  2026-07-07 15:49:58**(위와 동일 근거로 신뢰도 높음).
- **체감온도(STCS)**: `data/STCS_체감온도_20260701211159.csv` — **다운로드
  시점 2026-07-01 21:11:59**(파일명 타임스탬프). 현재 파이프라인에서 실제
  사용 여부 ⚠️ 확인 필요(직접 UTCI 산출은 Bröde 2012 공식으로 자체 계산,
  이 파일은 대조/검증용으로 추정).
- **기온·습도**: 서울 스마트도시데이터 센서(S-DoT) NATURE 항목. 서울
  열린데이터광장 추정. 폴더명 데이터 커버리지: 2025-01-01~2026-01-04
  (주간 단위 csv 분할). 파일 생성일(=다운로드 추정) **2026-05-20**. ⚠️
  정확한 다운로드 신청일·기관명(서울시 스마트도시정책관실 등) 사용자
  확인 필요. 참고: CLAUDE.md에 "S-DoT 관련 KCI 논문은 서울시 공공포털
  공식 출처로 대체"라는 기존 결정 있음(reference_list.csv id 041/043).

### 7.4 시설(기회) 및 인구

- **지하철역**: `data/facilities/seoul_subway_stations.gpkg`. ⚠️ **출처
  기관·다운로드일 미확인** — 스크립트/메타데이터 미발견, 사용자 확인 필요.
- **버스정류장(GTFS)**: `/Users/jin/석사논문/TAVI/GTFS_Korea/GTFS_creation/
  gtfs_KTDB/stops.txt`. 폴더명의 "KTDB"로 미루어 국가교통DB(국토교통부
  산하)로 추정되나 ⚠️ **정확한 제공기관·다운로드일 미확인** — 사용자
  확인 필요.
- **등록인구(연령별·동별)**: `data/등록인구/등록인구(연령별_동별)_
  20260729224302.csv` — **다운로드 시점 2026-07-29 22:43:02**(파일명
  타임스탬프, 행정안전부 주민등록인구통계 또는 통계청 KOSIS 추정, ⚠️
  정확한 제공기관 사용자 확인 필요). 현재 파이프라인 실사용 여부도 확인
  필요(2SFCA 거주인구 추정 관련 메모리 참고).

### 7.5 행정·통계 경계

- **집계구/행정구역 경계**: 통계청 통계지리정보서비스(SGIS,
  sgis.kostat.go.kr) — `data/_tmp_boundary/readme.txt` 원문 확인:
  "https://sgis.kostat.go.kr/contents/shortcut/shortcut_05.jsp", 좌표계
  UTM-K(GRS80). 파일: `집계구.shp`(2026-07-07 생성, ⚠️ 추정),
  `data/통계지역경계(2016년+기준)/`도 동일 출처(2016년 기준 경계).

### 7.6 법령

- **「도시·군계획시설의 결정·구조 및 설치기준에 관한 규칙」 제9조**(도로
  폭 법정 등급 — 소로~광로) — 국가법령정보센터(law.go.kr) 확인. 본 연구
  도로 폭 근사값(OSM 도로유형별 통상값)이 이 규칙의 법정 범위 내에
  있음을 사후 확인하는 용도로만 사용(개별 링크를 법정 등급에 직접
  매칭한 것은 아님 — V장 §6 한계 항목에 이미 명시됨). 정식 조문 URL·
  확인일 ⚠️ 세션 로그에는 있으나 이 파일에는 아직 미등재 — 추후 정리
  필요.

**종합 상태**: 다운로드일이 파일명에 정확히 남아있는 4건(API네트워크
2026-08-02, ASOS 2026-07-02, AWS 2026-07-07, 등록인구 2026-07-29, 토지피복
2025-11-13, STCS 2026-07-01)은 신뢰도 높음. 나머지(OSM, DEM, 건물높이,
임상도, S-DoT, 지하철역, 버스정류장, 집계구)는 제공기관명 또는 정확한
다운로드일 중 하나 이상이 ⚠️ 미확인 상태 — 사용자가 직접 다운로드
당시 신청 이력(공공데이터포털 "내 활용신청" 등)을 확인해 채워주시면
바로 반영하겠음.

---

## 작업 로그

- **2026-07-14**: 문서 최초 생성(v1). 등재 규칙 확정(PDF 원문 직접 확인 전까지
  등재 불가). 서론 v4 기준 검증 대상 11편 식별(프린트 완료, 검증 작업은 미착수).
  `references/reference_list.ris` 동시 생성(EndNote 서지정보 일괄 가져오기용,
  PDF 첨부는 EndNote 내에서 수동 진행 필요).
- **2026-07-14 (추가)**: RIS 최초 버전에서 저자 필드 오류 발견 — `reference_list.csv`의
  "저자1 et al." 축약 문자열이 그대로 AU 필드 하나에 통째로 들어가 EndNote에서
  "et al."이 이름의 일부처럼 표시됨(총 27건). PDF 보유 25건은 논문 1페이지 저자
  목록을 직접 열어 전원 확인 후 개별 AU 라인으로 분리(Lindberg2018 UMEP 20인 저자
  포함). PDF 미보유 2건(Thorsson 2011, Fitzpatrick 2006)은 최초 저자만 남기고
  "et al." 텍스트 제거. 추가로 "&"로 2인 저자를 붙여쓴 13건(예: Lindberg F. &
  Grimmond C.S.B.)도 동일 문제이므로 개별 AU 라인으로 분리(이 13건은 CSV에 이미
  검증된 전체 이름이 있어 PDF 재확인 없이 포맷만 수정). `reference_list.ris` 재생성
  완료(54개 항목, 172개 AU 라인). 사용자가 EndNote 기존 라이브러리 전체 삭제 후
  재import 예정.
- **2026-07-14 (추가, v2)**: 서론 1단락 인용 검증 착수. Geurs & van Wee(2004)
  p.131(3.1.4절) 확인 — "정확한 측정=정책 전제" 근거. Shin & Park(2026) p.1
  확인 — "삶의 질" 표현의 실제 출처(원문에 동일 문구 존재). 두 인용 모두 1단락
  같은 문장에 함께 배치하는 것으로 사용자 확정. 서론 전체 12편(+ 인용 미정 2곳)
  중 2편 검증 완료, 10편 남음.
- **2026-07-14 (추가, v3)**: 1단락 두 번째 문장("사회경제적 조건/인프라 차이/
  환경 조성 차이에 따른 불균등 분포") 검증. Kar et al.(2024) p.1 Abstract 확인
  — "사회경제적 조건" 요인만 커버함을 확인, 인프라·환경 조성 차이는 별도 인용
  필요 판단. "인프라 차이" 근거로 신규 문헌 Park et al.(2022, 지도교수 논문,
  EV충전소 접근성) 발굴 및 p.11 결과 확인 — `reference_list.csv`에 id 055로
  신규 등재. "환경 조성 차이"는 기존 Shin & Park(2026, id 054) 재사용. 세 요인
  모두 요인별 개별 인용으로 확정. 서론 12편 중 4편 검증 완료, 9편 남음.
- **2026-07-14 (추가, v4)**: 1단락 오프닝 재구성. 기존 "보행=기상제약 직접
  받는 이동방식"[인용 필요] + "폭염 시 보행자 위협 증가"[인용 필요, IPCC 아님]
  2곳의 빈 인용을 Basu et al.(2024) Introduction(p.1, "walkability... affected
  by thermal environment" / "increasing hot days... serious threat to human
  life")로 대체 — 새 논문을 찾는 대신 기존에 검증된 Basu(2024) 인용을 재배치.
  단, "보행자가 폭염에 더 노출된다"는 후속 절은 Basu 원문을 그대로 재서술하지
  않고 저자 본인의 논리적 추론(무인용)으로 처리하기로 확정 — Basu(2024)는
  1단락에서 "폭염-생명 위협" 절 하나만 뒷받침하는 것으로 정정. **1단락 인용
  전체 확정 완료(빈 인용 0곳)**. 서론 12편 중 5편 검증 완료, 8편 남음(2~5단락
  대상).
- **2026-07-14 (추가, v6)**: 사용자가 Basu(2024)를 읽으며 발견한 통찰("폭염
  위험 증가 vs 도시 보행공간은 기능성 위주 설계, 기후 고려 부족")을 1단락에
  반영. Basu(2024) p.2 "Unfortunately, most urban walking spaces are planned by
  functionality, with little consideration of thermal comfort" 확인. 위치는
  3단락(연구방법론 갭)이 아닌 1단락(동기)으로 확정 — 도시설계 실무 갭과
  학술적 측정방법 갭은 성격이 달라 분리. 문장 위치는 "폭염 위협 커짐" 문장
  뒤, "접근성 형평성" 문장 앞 — "위험↑+설계 미흡 → 정확한 측정 필요"라는
  인과 흐름 형성. Basu(2024)가 1단락 내에서 2회 인용되는 상태이며, 추후 다른
  선행연구 검토 중 대체/추가 인용을 찾아 다양성을 확보하기로 함(사용자 요청).
  **1단락 최종 확정.**
- **2026-07-14 (추가, v7)**: 2단락 검증 진행. Jia et al.(2022) p.10(Fig. 13
  본문) "강한 열 스트레스 시 보행속도 10~20% 감소", p.2 "337명 대상" 확인 —
  확정. Basu et al.(2024) 2단락 재인용 검증 중 수치 불일치 발견: 서론 요약
  문단(p.2)은 80.8m를 헤드라인으로 제시하지만, Results 표에서는 전체모델
  104m/주간이동 서브셋 80.8m로 값이 갈림. 모호함을 피하기 위해 구체적 수치
  없이 "UTCI 증가 → 인지 보행거리 증가"라는 정성적 서술로 단순화하기로
  사용자 확정. 서론 2단락 진행 중(Colaninno, Aydin 남음).
- **2026-07-14 (추가, v8)**: 사용자 질문("지금까지 본 논문들 정말 연속패널티
  맞아? 하드컷 아녀?")을 계기로 2단락 4편 전체의 실제 방법론 재확인. Jia(2022,
  연속회귀)·Basu(2024, p.8 800m 고정반경+UTCI를 경로비용으로 연속 환산)·
  Aydin(2026, p.11 PDT 연속식 + RUCS는 사후 라벨링용 이진지표일 뿐 핵심계산
  아님)·Colaninno(2024, p.1 서론문장 재확인 일치 + p.6/p.13 위험지수형 메커니즘
  — 속도/거리 치환이 아니라 UTCI×보행량의 연속 위험지수)까지 4편 모두 확인한
  결과 **네 편 다 하드컷 아님, 우리 Hard Cut의 방법론적 차별성 재확인**. 2단락
  오프닝 문장을 "치환하거나 위험지수로 환산하는 등, 연속적인 값으로 반영하는
  방식"으로 수정 확정. **1~2단락 인용 전체 확정 완료.** 서론 12편 중 9편
  검증 완료, 4편 남음(Bröde, Melnikov, Azegami, Buo — 4~5단락 대상).
- **2026-07-14 (추가, v9)**: 3단락 검증 중 **오인용 발견** — "Jia et al.(2022)
  에서도 언급되듯 일부 보행자는 오히려 속도를 높인다"는 문장이 실제로는 Jia
  본인의 발견이 아니라 Jia가 인용한 별개의 미확인 설문조사([25])의 내용이었고,
  Jia 본인 데이터는 오히려 일관된 속도 감소를 보임(2단락 항목 참고). 대체
  근거를 찾기 위해 Aydin(2026), Azegami(2023)를 추가로 확인했으나 "속도 증가"
  관련 내용 없음(Azegami는 Jia를 정확히 인용 — 그늘/양지 간 속도 변화 폭
  차이만 언급). 사용자와 논의 후 **이 재인용을 3단락에서 완전히 삭제**하고,
  "속도/거리 패널티는 경로 회피라는 별개의 행동 차원을 다루지 못한다"는
  무인용 개념적 논증으로 대체하기로 확정. 3단락은 인용 없음(모두 저자 자신의
  논리 전개), **검증 완료**. 서론 12편 중 9편 검증 유지(3단락에 새 인용 없음),
  4단락(Melnikov, Azegami, Buo)·5단락(Bröde) 대기.
- **2026-07-14 (추가, v10)**: 4단락 3편 검증 완료. Melnikov et al.(2022) p.1
  Abstract "0.86배 할인 인식" 확인(본문엔 수치 생략, "낮게 인식" 서술만 사용).
  Azegami et al.(2023) p.1 Abstract(28.2%) + p.6("신호 대기 후에도 그늘 선택")
  확인. Buo et al.(2026) p.1 Abstract "70% 이상 우회" 확인(구체 수치 32.2m/
  3.8°C는 서론에서 생략) — 추가로 p.6 부근에서 "a version of Dijkstra's
  shortest path algorithm" 명시 확인, Methods 섹션 라우팅 방법론 인용 시
  활용 예정(역참조). **4단락 검증 완료.** 서론 12편 중 11편 검증 완료(IPCC
  제외), 5단락 Bröde et al.(2012) 1편만 남음.
- **2026-07-14 (추가, v11)**: 5단락 Bröde et al.(2012) 검증. p.9 Table 3에서
  "+38 to +46 → Very strong heat stress" 확인 — 본 연구 Hard Cut 임계값
  (UTCI≥38°C)의 직접 근거이자 Methods에서도 재인용될 핵심 수치. **서론
  (Introduction) 1~5단락 전체 인용 검증 완료** — 총 12편 확인(IPCC 2022는
  사용자 승인으로 검증 생략). 이 과정에서 발견/결정된 주요 사항: (1) Kar(2024)
  는 사회경제적 요인만 커버 → Park et al.(2022, 신규 발굴) 추가로 인프라
  요인 보강, (2) Basu(2024)는 1단락에서 2회 인용(설계갭 통찰 포함), (3) 2단락
  4편 모두 실제로는 비-하드컷 방식임을 재확인(우리 방법론 차별성 강화),
  (4) 3단락 Jia 재인용이 오인용이었음을 발견해 삭제 및 무인용 논리로 대체,
  (5) Buo(2026)와의 Discussion 비교 메모 기록. 다음 단계는 Related Work
  섹션 집필 및 동일한 검증 절차 적용.
- **2026-07-15 (추가, v12)**: 사용자 질문("URock까지 필요한 건가?")을 계기로
  UMEP `Spatial Thermal Comfort` 알고리즘 소스코드 확인 — UTCI 계산 시
  Age/Activity/Clothing 등 개인변수는 미사용(PET/COMFA 전용), UROCK_MAP은
  필수 파라미터. 이를 계기로 선행연구 4편의 실제 풍속 처리 방식 재조사: Basu
  (2024) p.6, Colaninno(2024) p.8 — 둘 다 ERA5 재분석자료로 기온·습도·풍속을
  공간적으로 균일한 단일값(시간별 변화만)으로 처리하고 MRT만 SOLWEIG로
  공간분포 산출. Aydin(2026)만 예외적으로 OpenFOAM CFD(96 CPU, 72시간)
  사용. Jia(2022)는 현장실측(공간모델링 없음). **결론: 본 연구가 URock 없이
  met.txt 단일값 + SOLWEIG 공간 MRT를 쓰는 것은 MIT팀(Basu·Colaninno) SCI
  논문의 선례를 따르는 것으로 방법론적으로 방어 가능** — Methods 섹션에
  Basu(2024)·Colaninno(2024) 재인용으로 근거 등재.
- **파일명 변경**: 2026-07-14 → 2026-07-15 (내용 갱신에 따른 날짜 갱신, 규칙에
  따름).
- **2026-07-16 (추가, v13)**: 지도교수 논의로 MRT 채택 → UTCI 직접 채택으로
  방법론 대전환 후, UTCI 오피셜 산출 준비 차 기상요인(특히 풍속) 반영 방식을
  재조사. 논문 PDF가 아니라 우리가 실제 쓰는 UMEP `solweig_runner.py`
  L539-540과 `parametersforsolweig.json` L186-191을 직접 열어 확인 — 풍속
  높이보정이 거듭제곱 프로파일(지수 0.2)로 이미 내장되어 있고 기본 관측고도
  가정(10m)이 우리 AWS 풍속 출처(WMO 표준 10m 관측탑)와 일치함을 확인. Methods
  섹션 신규 항목으로 등재(논문 재인용 2건과 별도 — 소스코드 직접 확인). 이
  조사를 촉발한 질문("12편이 원래 기상요인 확인용이었나?")에 대한 답: 아니오
  — 12편은 서론 인용 검증용이었고, 기상요인 반영방식 확인은 그중 실제 UTCI/MRT
  공간모델링을 수행하는 5편(Basu·Colaninno·Aydin·Jia·Buo)에 한정된 별도
  작업이었음을 명확히 함. 나머지 7편은 모델링을 하지 않는 논문이라 확인 대상이
  아님.
- **2026-07-16 (추가, v14)**: Bröde et al.(2012) p.491 "Input of wind speed"
  절 재확인 — UTCI는 공식적으로 10m 높이 풍속을 입력으로 요구하며(Oke 1987
  공식으로 내부 자동 변환), 관측고도가 다르면 사용자가 로그프로파일(Eq.3)로
  10m로 변환해야 함을 명시. 이를 계기로 Basu(2024)의 실제 풍속 처리를
  교차검증한 결과 Basu는 ERA5 1.5m 풍속을 변환 없이 그대로 사용 —
  Bröde(2012) 공식 규정과 다름(사유 불명, ⚠️). 반면 본 연구의 AWS 10m 관측탑
  데이터는 변환 없이도 Bröde(2012) 규정을 그대로 만족 — 오히려 선례(Basu)보다
  더 엄밀한 준수임을 확인. Methods 섹션 신규 항목(Bröde 2012 재인용)으로 등재.
- **2026-07-16 (추가, v15)**: 사용자 질문("보간해서 반영한 UTCI 산출은 없나? UMEP은
  격자로 받나?")에 답하기 위해 UMEP 소스코드를 더 파봄. `postprocessor/
  spatialtc_algorithm.py`(UMEP 공식 UTCI 산출 도구) 확인 결과 **풍속은
  `UROCK_MAP`이라는 래스터 파라미터로 받고(L93/127/201), 기온·습도는 여전히
  met.txt 스칼라 단일값**임을 확인 — 우리가 안 쓰고 있는 URock(건물·식생 기반
  진단형 바람모델) 경로가 공식적으로 존재. 추가로 기온을 공간 모델링하는 별도
  도구 TARGET(`target_algorithm.py`, Broadbent et al. 2019)도 발견 — 이 논문은
  오픈액세스라 PDF 확보·직접 확인 완료(100m 격자, 27개 AWS망 검증). 웹서치로
  Lee et al.(2025, IJB)·Krüger & Di Napoli(2022)·Brecht et al.(2020) 3편을
  추가 발견했으나 PMC 자동다운로드 차단으로 PDF 미확보 — WebFetch 요약만 잠정
  기록, DOI·권장 파일명을 사용자에게 전달해 수동 다운로드 요청. 등재 규칙(PDF
  직접 확인)을 아직 충족 못했음을 표에 명시.
- **2026-07-16 (추가, v16)**: 사용자가 3편 PDF를 모두 다운로드해 제공. 전부 직접
  열어 어제 WebFetch 요약과 원문 대조 — 3편 모두 수치·인용 정확히 일치(교차검증
  통과). Lee et al.(2025) p.1에서 z0=0.80m 기준 UTCI 오차가 **최대 7K**까지
  가능함을 원문으로 추가 확인(어제는 몰랐던 구체 수치). Brecht et al.(2020) p.2
  원문에서 "spatial scales from city quarters onwards" 문장을 직접 확인 —
  Lee et al.(2025)의 재인용이 정확했음을 검증. Krüger & Di Napoli(2022)는
  ERA5(31×31km) 재분석자료 고유의 오차이며 우리(실측 AWS)와는 성격이 다르다는
  점을 명시해 과잉 인용 방지. 3편 모두 정식 등재 완료(임시 표 형식에서 정식
  항목으로 전환). 사용자 질문("TARGET/URock 도구를 실제로 UTCI 산출에 써야
  하나?")에 대한 답변은 별도 대화로 진행 — Brecht(2020)의 스케일 구분에 따르면
  URock(건물 해상도)은 오히려 표준 UTCI와 스케일 부정합 가능성이 있고, TARGET
  (100m, city quarter급)이 상대적으로 더 정합적이라는 판단.
- **2026-07-20/21 (v17)**: Related Work 검증 착수. `writing/03_논문구조/
  2026-07-17_논문전체구조_v3.md`의 Section 2가 `writing/02_선행연구/
  2026-07-17_선행연구_v2_SCI_별도섹션안.md`(압축판)보다 최신·상세함을 사용자가
  발견 — Section 2를 그대로 추출해 `writing/02_선행연구/
  2026-07-20_선행연구_v4_전체판.md`(v4) 신규 생성, 이후 이 문서를 검증 기준
  원본으로 사용. **Kar et al.(2023)** Abstract(hard/soft constraint 개념)
  원문 대조 확인 후 등재. **Ali-Toudert & Mayer(2006)** p.100(MRT 40K 차이)
  원문 대조 확인 후 등재. **Kar et al.(2024)**의 "Inclusive Access 1"(같은
  논문의 id 052와 다른 절 인용, p.7 §5.3 정의문 + p.12 §6.2 자기한계 인정문)
  원문 대조 확인 후 등재 — 이 과정에서 Kar(2023/2024)의 "soft/hard constraint"
  (제약의 성격 축)가 본 연구의 "연속적 패널티 vs Hard Cut"(함수 형태 축)와
  다른 개념임을 발견, `CLAUDE.md`에서 "소프트 패널티" 표현을 전부 "연속적
  패널티"로 교체(용어 혼동 방지 확정). 2.3/2.4절의 Jia/Basu/Aydin/Colaninno/
  Melnikov/Azegami/Buo/Bröde 재인용은 Introduction·Methods 기존 등록 인용문과
  전수 대조해 일치 확인(백참조 블록 추가). Aydin et al.(2026) p.8 §2.2.1.2
  "72 h on 96 CPUs" 원문 위치 확인했으나 **사용자 확인 대기 중**(등재 보류).
  파일명 규칙(§"버전/작업로그 관리")에 따라 `2026-07-16_reference_list.md` →
  `2026-07-21_reference_list.md`로 리네임, v16→v17.
- **2026-07-21 (v18)**: v4 기준 2.1절을 위에서부터 순서대로 검증 진행.
  **Hägerstrand(1970)**(p.13-14, "Daily Prisms" — 스캔본이라 이미지로 직접
  확인) 등록. **Miller(1991)**(p.291-292, network-based PPA 정의 — 저널명이
  1991년 당시 "...Information **Systems**"였음을 확인, 현재의 "...Science"와
  다름 주의) 등록. **Dijkstra(1959)**는 PDF 미확보 상태에서 사용자가 "표준
  알고리즘 명칭 인용이라 검증 없이 진행, 추후 직접 등재하겠다"고 결정 —
  가등록 상태로 표시. 사용자가 "Kar(2024)의 계보 서술을 그대로 가져다 써도
  되지 않냐"고 질문 — **Kar의 요약을 차용하지 않고 직접 원문 검증한다는
  원칙을 재확인**(El-Geneidy & Levinson 2006, Miller 2007, Kwan 1999는 아직
  PDF 미확보 상태이므로 인용 보류, `2026-07-21_선행연구_v5_전체판.md`에 TODO로
  명시). v4를 이어받아 2.1절에 place-based/person-based 이분법 보강 문단을
  추가한 **v5** 신규 생성 — 이후 검증 기준 문서를 v5로 이전, v4 상단에 대체
  안내 추가.
- **2026-07-21 (v19)**: 사용자가 Aydin(2026) "96 CPU×72시간" 재확인 —
  등재 확정. 이어서 2.1절 "Catchment Area는... contour measure와 같은 계보
  위에 있다" 문장을 사용자가 재검증 요청 — Geurs & van Wee(2004) p.134에서
  "A contour measure, also known as isochronic measure... is popular in urban
  planning and geographical studies" 확인, 저자 자신이 "contour=isochronic"을
  명시함을 확인. **동시에 오귀속 발견**: 같은 문단 앞 문장("버퍼 기반 반경
  분석과 달리 실제 도로 구조를 반영...표준 방법론으로 광범위하게 활용된다")도
  Geurs & van Wee(2004)를 인용하고 있었으나, 원문 전체 검색 결과 이 논문이
  버퍼 vs 네트워크 기반 구분을 다루는 대목이 없음을 확인 — 사용자 결정으로
  이 문장의 인용을 제거하고 필자 서술로 전환(`v5` 반영 완료). **결과: v5
  기준 2.1~2.4절 전 문장 검증 완료**(Dijkstra 가등록, El-Geneidy&Levinson/
  Miller2007/Kwan1999 TODO 제외).
- **2026-07-21 (v20)**: 사용자가 El-Geneidy & Levinson(2006)/Miller(2007)/
  Kwan(1999) 3편 PDF를 직접 확보(Kar et al.2024 참고문헌에서 정확한 서지정보
  확인 후 안내). El-Geneidy & Levinson(2006)은 SCI 논문이 아니라 Minnesota
  DOT 기술보고서임을 이유로 미채택 결정. Miller(2007) 원문 확인 중 **오귀속
  재발견**: 초안이 "개인기반은 일반화가 어렵다"의 근거로 이 논문을 인용했으나
  원문에 "generaliz" 단어 자체가 없고 논지가 오히려 반대(개인기반 옹호, 장소
  기반 비판)임을 확인 — 문단을 "장소기반/개인기반은 우열이 아니라 각자 쓰임이
  다르다"는 중립 서술로 재구성, Miller(2007)는 "이분법이 존재한다"는 정의적
  인용으로만 사용. 이 과정에서 사용자가 "PPA(Miller 1991)가 개인기반 버전의
  Catchment Area 아니냐"는 통찰을 제시 — Miller(1991) 원문에 "catchment"
  단어가 없음을 재확인해 이건 저자 주장이 아니라 **본 연구의 해석**임을
  명시("본 연구는 ~라고 본다"로 문장 구분). 사용자 요청으로 미사용 2편도
  삭제하지 않고 "확보했으나 현재 미사용 — 향후 활용 후보(석사논문 확장판 등)"
  섹션으로 분리 보관(El-Geneidy&Levinson p.4 인용문 포함, Kwan은 원문 미대조
  상태로 서지정보만).
- **2026-07-21 (v21)**: 사용자가 2.2절을 보고 "인용 문헌이 너무 적은 거
  아니냐"고 질문 — 확인 결과 이미 4개 문헌(Bröde 2012, Ali-Toudert & Mayer
  2006/2007, Kántor & Unger 2011)이 인용되어 있었으나 (2006)만 검증 완료
  상태였음을 발견. 나머지 2편의 PDF가 이미 로컬에 있어 검증 진행. **Ali-
  Toudert & Mayer(2007)** p.751 "PET was up to 24 K lower than in a street
  without trees"(갤러리+가로수 병용) 확인. **Kántor & Unger(2011)** Abstract
  "the most important parameter... variable in spatial... manner" 확인 —
  둘 다 초안 인용과 정확히 일치. **결과: 2.2절 4개 인용 전부 검증 완료.**
- **2026-08-04 (v23)**: 국문 학위논문 V장 §2(정책적 함의 — 병목 링크 분석)에서
  이번 세션 동안 여러 차례 인용해온 **Jenelius, Petersen & Mattsson(2006)**·
  **Nemhauser, Fisher & Wolsey(1978)** 두 편이 이 마스터 목록에 등재는커녕
  PDF조차 읽지 않은 채(WebSearch 서지정보만으로) 본문에 8회+1회 인용되어
  있었음을 사용자가 지적해 발견. 즉시 시정: (1) WebSearch로 오픈액세스 대체
  자료(Jenelius의 2010년 박사학위논문, KTH)를 먼저 확보해 개념을 교차확인했으나
  원논문 자체는 아니었음을 사용자에게 보고, (2) 사용자가 원논문 2편을 직접
  다운로드해 제공, (3) 두 편 모두 원문 PDF 대조 완료 — Jenelius(2006) p.537
  "importance"·"generalised cost" 정의, Nemhauser et al.(1978) p.276 greedy
  heuristic 정의 확인, 초안 서술과 정확히 일치. 5. Discussion 섹션에 정식
  등재(기존 이 섹션은 공란이었음). **동시에 별도로 발견된 문제**: 국문
  학위논문 서론 1단락의 "여러 이동 방식 중 실외에서 신체 활동이... 위협이
  더욱 커질 것이다" 문장에 Claude가 세션 중 임의로 (Basu et al., 2024)
  인용을 추가했으나, 이 파일(1단락 Basu 항목, 65~68행)에 **이미 2026-07-14에
  "유사하지만 저자 본인의 논리적 추론으로 무인용 처리하기로 확정"**된 기록이
  있었음이 드러나 즉시 원복(마스터 초안 및 본 파일 미변경, 결정 유지) — 단,
  당시 대조했던 문구("pedestrians are comparatively more exposed to extreme
  weather conditions")와 별개로, 같은 단락 바로 앞의 "Trips that entail
  physical exertion outdoors, such as walking and biking trips, will
  increase people's overall exposure to potentially dangerous urban
  microclimates"(p.2)라는 더 직접적으로 일치하는 문장을 추가로 발견 — 재인용
  여부는 사용자 재확인 필요 항목으로 남겨둠(미확정, 아래 참고).
  **교훈**: 이 세션에서 Claude가 원문을 확인하지 않고 "방법론적 근거가
  있습니다"라고 서술한 경우, 이 마스터 목록에 즉시 반영하지 않고 넘어가는
  일이 반복됐음 — 앞으로는 이 목록 확인·갱신을 원문 검증과 동시에 처리할 것.
- **2026-08-04 (v24, 이어서)**: 사용자가 "더 찾을 거 없냐"고 재질문 —
  같은 방식으로 이번 세션에서 언급된 다른 방법론 근거도 점검. **Colaninno
  et al.(2024)**의 "링크 버퍼+픽셀 평균 UTCI 할당" 방법(III장 §3에서
  우리 방법의 선례로 서술)이 `study_note_Colaninno2024_SidewalkHeatRisk.md`
  에 원문 인용 없이 요약("세그먼트 버퍼로 픽셀 평균")으로만 남아 있었음을
  발견 — 원문(p.9~10) 대조 후 Methods 섹션에 정식 등재(위 참고). **Yoon et
  al.(2020)**은 서론 인용 후보로 원문(Abstract) 확인까지는 완료했으나
  아직 마스터 초안에 반영은 안 한 상태 — "미확정" 섹션에 추가. **점검
  결과**: Jenelius/Nemhauser/Colaninno 3건 원문 미검증 상태 발견·시정,
  Basu/Yoon 2건은 사용자 결정 대기. 다른 인용은 기존 로그(v1~v23) 기준
  전부 원문 대조 완료 상태로 확인됨.

### 미확정 — 사용자 재확인 필요 (2026-08-04)

- **2026-08-04 (v25)**: 사용자가 (1) Basu(2024) 3차 인용 확정 지시 — 마스터
  초안 반영 + 이 파일 1단락 항목을 "미확정"에서 확정으로 이전. (2) 이 마스터
  파일을 논문 전체의 "0번" 근거로 삼되, 별도로 각 파트(서론 등)마다 "인용
  근거정리" 요약 파일도 유지하기로 확정(용도 구분: 마스터=원문 검증 로그,
  파트별 파일=완성된 문장과 인용의 1:1 대조표) — `writing/01_서론/
  2026-08-04_서론_인용근거정리.md`는 삭제하지 않고 유지, 향후 다른 장
  작성 시에도 같은 패턴 적용 예정. (3) 논문에 등장하는 선행연구 외에
  **원본 데이터·법령 출처도 전부 이 마스터 파일에 기록**하라는 지시 —
  7절(데이터·법령 출처) 신설, 데이터 폴더 전수 조사(파일명 타임스탬프,
  다운로드 스크립트 헤더, readme 파일 대조)로 12개 데이터군의 제공기관·
  다운로드일·수집 요소를 1차 정리. 파일명에 다운로드 타임스탬프가 남아있는
  6건(API네트워크·ASOS·AWS·등록인구·토지피복·STCS)은 신뢰도 높게 확정,
  나머지 8건(OSM·DEM·건물높이·임상도·S-DoT·지하철역·버스정류장·집계구)은
  제공기관명 또는 정확한 다운로드일 중 최소 하나가 미확인 상태로 남아
  사용자 확인 대기 표시. 법령(도로폭 규칙)도 항목 신설, 정식 조문 URL은
  추후 보강 필요.
- **원칙 재확인**: "마스터 파일에 없는 논문은 인용하지 않는다" — 이후
  모든 신규 인용은 이 파일에 원문 검증 없이 본문에 먼저 쓰지 않기로
  확정(사용자 지시, 2026-08-04).
- **2026-08-04 (v26)**: 사용자가 "다른 장도 같은 패턴으로 다 만들어놔"
  지시 — II~VI장 전체를 마스터 파일과 대조하며 인용근거정리 보조 파일
  5개 신규 생성(`writing/02_선행연구/`, `04_방법론_결정노트/`,
  `05_결과/`, `06_논의/`(신규 폴더), `07_결론/`(신규 폴더)). 이 과정에서
  III장 §2·§4에서 추가로 미검증 인용 6건 발견·시정: **Moreno et
  al.(2021)**(15분 시간예산 근거, 마스터파일에 아예 없었음), **Lindberg
  et al.(2008/2016/2018)·Lindberg & Grimmond(2011)·Wallenberg et
  al.(2026)**(SOLWEIG 계보 5편 — 스터디노트 단계에서는 이미 원문 검증돼
  있었으나 마스터 파일 Methods 섹션에 옮겨지지 않은 상태였음, 뒤늦게
  정식 등재). II장·IV장·V장·VI장은 기존 인용이 전부 이미 검증된 상태로
  확인됨(IV장은 선행연구 인용이 3건뿐이라 논문 인용보다 "수치가 어느
  스크립트에서 나왔는지" 대응표 형태로 작성). CLAUDE.md 최상단에 이
  마스터 파일 확인 원칙을 명문화(사용자 지시).
- **잔여 미확정 항목(2026-08-04 기준)**: Yoon et al.(2020) 서론 추가
  인용 여부, 데이터·법령 출처 중 8건의 정확한 다운로드일/제공기관명,
  IV장 수치 중 6건의 정확한 생성 스크립트 경로.
- **2026-08-05**: Yoon et al.(2020) 확정 반영(위 Introduction 섹션 참고,
  미확정 목록에서 해소). 사용자 지시로 Jia(2022)·Basu(2024)·Aydin(2026)·
  Colaninno(2024) 4편을 fork 4개로 병렬 전체 정독(본문+참고문헌) —
  스노우볼링(후방 인용 추적) 방식으로 각 논문이 인용하는 문헌 중 우리
  연구에 필요해 보이는 것 추출. 핵심 발견: "38°C 임계값 정당화" 논증
  클러스터 — Basu(2024) Conclusion이 스스로 "임계값은 기후마다 다를
  것으로 예상되며 다른 기후권 비교연구가 필요하다"고 요청한 문장 발견,
  Aydin(2026)도 32°C를 싱가포르 현지 실측 평균에 맞춰 채택했음을 확인.
  스노우볼링 후보 중 McDonald et al.(2021, PLoS ONE, 오픈액세스)은 직접
  PDF 확보해 Abstract 검증 후 Results 섹션에 등재(위 참고) — Colaninno
  (2024)의 참고문헌에서 발견. Wang et al.(2022, Frontiers)는 PMC 자동
  차단으로 요약만 확보, 원문 PDF는 미확보. Hsu et al.(2021, Nature
  Comms)는 로그인장벽으로 확보 실패. 나머지 상세(채굴 문장 전체, 다운로드
  요청 목록 6편의 정확한 서지정보·제안 파일명)는 `writing/02_선행연구/
  2026-08-05_4편_정독_스노우볼링_결과.md` 참고 — **이 파일의 내용은 전부
  아직 "후보" 단계이며 본문에 반영되지 않음**.
- **2026-08-05 (v29)**: 사용자가 다운로드 요청 6편을 전부 받아 제공 —
  fork 6개로 병렬 원문 타겟검증(각자 특정 주장에 필요한 정확한 문구만
  확인). 결과: Pantavou(2018)·Kruger(2017)·Liu&Qin(2023)·Jendritzky
  (2012) 4편은 "38°C 임계값 정당화" 논증에 유효 확인, Related Work
  섹션 최상단에 전용 클러스터로 등재(Kruger의 Table 6 도시별 임계값
  비교가 가장 강력한 수치 근거). McDonald(2021)는 Results에 등재
  (후보 단계). **Hsu(2021)는 확인 결과 우리 IV장§4.2 상관관계(고령인구
  비율과 양의 상관)와 반대 방향(고령층이 SUHI 노출 더 낮음)임을
  fork가 발견 — ⚠️사용주의로 등재, 오귀속 위험 명시**. Wang(2022)도
  기대(15분 근거 보강)와 달리 원문에 "왜 15분인가"의 수치적 근거가
  없어 **III장§4는 Moreno(2021) 그대로 유지하기로 판정**. 6편 모두
  원문 PDF 전체 또는 목표 구간 대조 완료.
- **2026-08-05 (v30)**: 사용자가 서론 1단락 직접 편집 중 Basu(3회)·
  Shin&Park(2회) 중복 인용을 지적 — 오늘 스노우볼링으로 확보한 재료
  활용해 완화. (1) "실외 신체활동 보행 위협" 문장에 **Jia et
  al.(2022)** 추가(원문 p.2 "Walking as a weather-exposed activity..." —
  이미 확보된 PDF에서 신규 발견). (2) "환경 조성 차이" 클레임에
  **McDonald et al.(2021)** 추가, Shin&Park 중복 완화. 두 문헌 모두
  마스터 초안 참고문헌 목록에도 추가 완료. 사용자가 별도로 편집 중이던
  텍스트에서 Yoon(2020) 인용이 빠져있어 확인한 결과 실제 파일에는 이상
  없음 확인(로컬 워드 파일이 최신 md 갱신을 반영 못 하고 있었던 것으로
  판명 — 파일 동기화 문제였을 뿐 실제 인용 손실 아님).

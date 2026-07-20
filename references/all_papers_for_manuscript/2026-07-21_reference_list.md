작성일: 2026-07-21
버전: v20 (2.1절 place-based/person-based 문단 재구성 — Miller(2007) 등록,
El-Geneidy&Levinson 2006/Kwan 1999는 확보만 하고 "미사용 후보 풀"로 분리 보관)
상태: **Introduction 완료(12편) / Methods 8건 완료 / Related Work — v5 기준
2.1~2.4절 전 문장 검증 완료(Dijkstra 가등록 제외)**

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

## 4. Results

*(검증 완료 항목 없음)*

## 5. Discussion

*(검증 완료 항목 없음)*

## 6. Conclusion

*(검증 완료 항목 없음)*

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

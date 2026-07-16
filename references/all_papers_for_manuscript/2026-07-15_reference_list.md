작성일: 2026-07-15
버전: v12 (Methods 방법론 근거 2건 추가 — 기상입력 단일값 정당화)
상태: **Introduction 완료(12편) / Methods 2건(재인용) 추가 / Related Work 대기**

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

*(검증 완료 항목 없음)*

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

# 사용자 행동 기반의 실시간 이슈트렌드 분석; 그래프DB를 활용하여

> 연세대학교 컴퓨터과학과 2021-2 소프트웨어종합설계(1) 프로젝트

## 1. Overview

이 프로젝트는 다양한 온라인 플랫폼에서 수집한 사용자 행동 데이터를 바탕으로 **실시간 이슈 트렌드**를 분석하고 시각화하는 시스템을 구축하는 것을 목표로 합니다. 이를 통해 개인의 가치 판단을 도와줄 수 있는 **객관적인 지표**를 제시하고자 하였습니다.

- **기간**: 2021.03 - 2021.06
- **주요 플랫폼**: 네이버 뉴스, 다음 뉴스, 유튜브 동영상
- **특징**: Pororo(NER)을 이용한 실시간 키워드 추출, 그래프DB(Neo4j)를 통한 데이터 관계 분석 및 시각화
- **Report**: [사용자 행동 기반의 실시간 이슈트렌드 분석; 그래프DB를 활용하여](https://2hwayoung.notion.site/DB-e85b2cdd78624fa2a7ced1e62b4f51ba?pvs=4)

  
## 2. Team
- Team name: GentleGraph
- **T.M** 김대현 컴퓨터과학과
- **T.M** 이화영 산업공학과
- **T.M** 유승수 산업공학과

## 3. Skills
- Python Crawling
- Kafka
- Airflow (with PostgresDB)
- Neo4j
- AWS EC2 4대

## 4. Structure
<img src="https://github.com/user-attachments/assets/c578abcd-f684-44da-bb55-15b6519ecbae" height="400"/>


## 5. Flow
1) **데이터 수집**: 네이버뉴스, 다음뉴스, 유튜브 동영상 데이터 수집 (댓글수, 평가(반응)수, 조회수, 좋아요/싫어요수 등)
3) **데이터 처리**: Kafka 실시간 데이터 처리(5분 간격)
4) **실시간 인기 검색어 추출**: KakaoBrain의 Pororo(NER)을 이용하여 실시간 이슈 검색어 추출
5) **그래프 DB**: Neo4j 그래프 데이터베이스 구축


   <img src="https://github.com/user-attachments/assets/61d183fd-2dc3-4a98-af76-9dc1b4d5d642" height="300"/>

6) **키워드 분석 모델**: 키워드 분석 Decision tree 모델 설계 및 학습
7) **워크플로우 관리**: Airflow Scheduler 구축
8) **그래프 시각화 및 웹서비스**: Neo4j Bloom 그래프 시각화와 Flask로 웹서비스 구현

  <img src="https://github.com/user-attachments/assets/303941bf-2ce0-4612-886f-405690315a4b" height="300"/>


## 6. Report

- **Report |** [사용자 행동 기반의 실시간 이슈트렌드 분석; 그래프DB를 활용하여](https://2hwayoung.notion.site/DB-e85b2cdd78624fa2a7ced1e62b4f51ba?pvs=4)

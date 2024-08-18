# fastapi

# 폴더 구조 주요 구성 요소 설명

- app/: 애플리케이션의 메인 패키지입니다.
- main.py: FastAPI 애플리케이션을 초기화하고 실행합니다.
- api/: API 라우트와 엔드포인트를 정의합니다.
- core/: 애플리케이션의 핵심 기능과 설정을 관리합니다.
- db/: 데이터베이스 연결 및 세션 관리를 담당합니다.
- models/: SQLAlchemy ORM 모델을 정의합니다.
- schemas/: Pydantic 모델을 사용하여 요청 및 응답 데이터의 구조를 정의합니다.
- tests/: 단위 테스트와 통합 테스트 코드를 포함합니다.
- alembic/: 데이터베이스 스키마 변경을 관리하는 마이그레이션 도구입니다.
- .env: 환경 변수를 저장합니다. 이 파일은 버전 관리에서 제외해야 합니다.
- requirements.txt: 프로젝트의 Python 패키지 의존성을 명시합니다.

~~~
myproject/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션의 진입점
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/          # API 엔드포인트 정의
│   │   │   ├── __init__.py
│   │   │   ├── items.py
│   │   │   └── users.py
│   │   └── dependencies.py     # API 의존성 (예: 인증)
│   │
│   ├── core/                   # 핵심 기능 및 설정
│   │   ├── __init__.py
│   │   ├── config.py           # 환경 설정
│   │   └── security.py         # 보안 관련 기능
│   │
│   ├── db/                     # 데이터베이스 관련
│   │   ├── __init__.py
│   │   ├── base.py             # 데이터베이스 기본 설정
│   │   └── session.py          # 데이터베이스 세션 관리
│   │
│   ├── models/                 # 데이터베이스 모델
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   │
│   └── schemas/                # Pydantic 모델 (요청/응답 스키마)
│       ├── __init__.py
│       ├── item.py
│       └── user.py
│
├── tests/                      # 테스트 코드
│   ├── __init__.py
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_items.py
│   │   └── test_users.py
│   └── conftest.py             # pytest 설정 및 픽스처
│
├── alembic/                    # 데이터베이스 마이그레이션
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .env                        # 환경 변수
├── .gitignore
├── requirements.txt            # 프로젝트 의존성
└── README.md                   # 프로젝트 설명 (현재 파일)
~~~

## 시작하기

- 가상 환경을 생성하고 활성화합니다.
~~~
# 프로젝트의 의존성을 관리하고 시스템 전체 Python 환경과 분리하기 위해 가상환경을 사용합니다. 아래는 운영체제별 가상환경 생성 및 활성화 방법입니다.

# window:

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate

macOS 및 Linux:
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

~~~
- 필요한 패키지를 설치합니다: 

~~~
pip install -r requirements.txt
~~~

- .env 파일을 설정합니다.

- 애플리케이션을 실행합니다: 

~~~
# fastapi 실행
uvicorn app.main:app --reload
~~~

## 개발 가이드라인

- 새로운 API 엔드포인트를 추가할 때는 app/api/endpoints/ 디렉토리에 새 파일을 생성하세요.
- 데이터베이스 모델을 변경할 때는 app/models/ 디렉토리에서 작업하고, Alembic을 사용하여 마이그레이션을 생성하세요.
- 모든 설정은 app/core/config.py에서 관리합니다.
- 테스트 코드는 tests/ 디렉토리에 작성하며, pytest를 사용하여 실행합니다.
- 항상 가상환경 내에서 작업하세요. 

~~~
# 새 패키지를 설치할 때
 pip install <package_name>

# 파이선 설치 환경 파일 업데이트(requirements.txt)
pip freeze > requirements.txt
~~~

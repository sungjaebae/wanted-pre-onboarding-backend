### 1. 지원자의 성명

배성재

### 2. 애플리케이션의 실행 방법

로컬 데이터베이스의 계정: root, 비밀번호: 12341234, db:intership  
연결 문자열 수정이 필요한 경우 connect.py에서 수정

python -m pip install -r ./requirements.txt  
python create_tables.py //데이터베이스 및 테이블 생성  
python app.py

엔드포인트 호출 방법 : http://localhost:5000/api/register 등의 라우트로 호출

### 3. 데이터베이스 테이블 구조

Users

- id : INT[10]
- email : VARCHAR[25]
- password : VARCHAR[44]

Articles

- id : INT[10]
- user_id : INT[10]
- title : VARCHAR[100]
- body : TEXT

### 4. 데모 영상 링크

https://youtu.be/jaTpMIxkxTk

### 5. 구현 방법 및 이유

- flask를 기반으로 구현
- sqlalchemy와 pydantic을 하나의 모델로 구현한 sqlmodel 사용
- 로그인 여부, 게시글 소유 여부를 데코레이션으로 구현하여 재사용성 있음

### 6. API 명세

1 사용자 회원가입 엔드포인트

    라우트 : POST /api/register
    요청(json) : email, password
    응답(json) : result, message

2 사용자 로그인 엔드포인트

    라우트 : POST /api/login
    요청(json) : email, password
    응답(json) : result, message, token

3 새로운 게시글을 생성하는 엔드포인트

    라우트 : POST /api/article
    헤더 : Authorization: Bearer token
    요청(json) : title, body
    응답(json) : result, message

4 게시글 목록을 조회하는 엔드포인트

    라우트 : GET /api/article
    쿼리 파타리터 : page (1부터 시작)
    요청(json) : 불필요
    응답(json) : result, message, articles

5 특정 게시글을 조회하는 엔드포인트

    라우트 : GET /api/article/<article_id>
    요청(json) : 불필요
    응답(json) : result, message, article

6 특정 게시글을 수정하는 엔드포인트

    라우트 : PUT /api/article/<article_id>
    헤더 : Authorization: Bearer token
    요청(json) : title, body
    응답(json) : result, message

7 특정 게시글을 삭제하는 엔드포인트

    라우트 : DELETE /api/article/<article_id>
    헤더 : Authorization: Bearer token
    요청(json) : 불필요
    응답(json) : result, message

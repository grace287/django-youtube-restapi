FROM python:3.11-alpine3.19
LABEL maintainer="grace287"

ENV PYTHONUNBUFFERED=1

# 빌드 도구 및 의존성 설치
RUN apk add --no-cache \
      gcc \
      musl-dev \
      python3-dev \
      libffi-dev \
      openssl-dev \
      mariadb-dev \
      postgresql-dev \
      build-base \
      py3-virtualenv

# requirements.txt 복사 & 설치
COPY ./requirements.txt /tmp/requirements.txt

# 가상환경 생성 및 패키지 설치
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r /tmp/requirements.txt

# 애플리케이션 코드 복사
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false
ENV PATH="/app/venv/bin:$PATH"
ENV DEV=$DEV

# 일반 사용자 추가
RUN adduser --disabled-password --no-create-home django-user
USER django-user

# 실행 커맨드
CMD ["sh", "-c", "if [ $DEV = 'true' ]; then python manage.py runserver 0.0.0.0:8000; else gunicorn app.wsgi:application --bind 0.0.0.0:8000; fi"]

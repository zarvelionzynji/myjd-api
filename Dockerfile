FROM python:3.11-slim AS build
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY app.py .


FROM python:3.11-alpine
WORKDIR /app

COPY --from=build /install /usr/local
COPY --from=build /app /app

ENV JD_EMAIL=""
ENV JD_PASSWORD=""
ENV JD_DEVICE=""
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]

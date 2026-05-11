# ML CI/CD Pipeline — Homework 7

## Описание проекта

ML-сервис с настроенным CI/CD пайплайном, реализацией стратегии Blue-Green деплоя и A/B-тестированием моделей. Проект выполнен в рамках модуля «Автоматизированное развертывание с помощью CI/CD».

## Структура репозитория

```
ml-cicd-hw7/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI пайплайн — тестирование и обучение модели
│       └── deploy.yml       # CD пайплайн — сборка и деплой Docker-образа
├── ml_pipeline.py           # Обучение модели (RandomForest на датасете Iris)
├── save_artifacts.py        # Сохранение модели и метрик
├── app.py                   # Flask-сервис (/health, /predict)
├── Dockerfile               # Сборка Docker-образа
├── docker-compose.blue.yml  # Blue окружение (v1.0.0)
├── docker-compose.green.yml # Green окружение (v1.1.0)
├── nginx.conf               # Балансировщик трафика
└── requirements.txt         # Зависимости проекта
```

## Стратегия деплоя — Blue-Green

Выбрана стратегия **Blue-Green Deployment** как наиболее подходящая при отсутствии обработки ошибок в коде модели.

| | Blue (v1.0.0) | Green (v1.1.0) |
|---|---|---|
| Статус | Стабильная версия | Новая версия |
| Порт | 8001 | 8002 |
| Откат | Мгновенный | — |

**Принцип работы:**
- Blue и Green окружения работают параллельно
- Nginx перенаправляет весь трафик на активную версию
- При ошибках новой версии — мгновенный откат на Blue одной командой

### Запуск окружений

```bash
# Запуск Blue (v1.0.0)
docker-compose -f docker-compose.blue.yml up -d

# Запуск Green (v1.1.0)
docker-compose -f docker-compose.green.yml up -d

# Проверка health
curl http://localhost:8001/health
# {"status": "ok", "version": "v1.0.0"}

# Предсказание
curl http://localhost:8001/predict -d '{"x": [5.1, 3.5, 1.4, 0.2]}'
# {"prediction": [0], "version": "v1.0.0"}
```

## CI/CD пайплайн

Пайплайн запускается автоматически при каждом `push` в ветку `main`.

### ML Pipeline CI (`ci.yml`)

```
push → checkout → setup Python → install deps → train model → save artifacts
```

Сохраняемые артефакты:
- `model.pkl` — обученная модель
- `metrics.json` — точность и гиперпараметры
- `requirements.txt` — зафиксированные версии зависимостей

### Model Deployment (`deploy.yml`)

```
push → checkout → build Docker image → health check simulation
```

## A/B-тестирование моделей

Проведено статистическое сравнение двух версий модели на датасете Iris с добавленным шумом.

| Параметр | Значение |
|---|---|
| Модель A (v1.0) | DecisionTreeClassifier, max_depth=3 |
| Модель B (v1.1) | RandomForestClassifier, n_estimators=100 |
| Тестовая выборка | 30% (45 наблюдений) |
| Статистический тест | z-тест для пропорций |
| Уровень значимости | α = 0.05 |

**Результаты:**
- Accuracy A: 0.7778
- Accuracy B: 0.7333
- P-value: 0.6237 > 0.05

**Вывод:** различия статистически незначимы, модель A (v1.0) остаётся основной.

## Архитектурное решение (ADR-001)

**Статус:** Принято

**Контекст:** Код модели не содержит обработки ошибок, что повышает риск при деплое новой версии.

**Решение:** Blue-Green Deployment — простота реализации, мгновенный откат, полная изоляция версий.

**Альтернатива:** Canary Deployment — безопаснее для пользователей, но требует зрелой системы мониторинга.

## Ссылки

- [GitHub Actions](https://github.com/shadoww6/ml-cicd-hw7/actions)
- [Репозиторий](https://github.com/shadoww6/ml-cicd-hw7)

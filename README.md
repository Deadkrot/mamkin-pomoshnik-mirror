# Мамкин помощник — Telegram бот (ИВ: кормления и сон)!

Минимально рабочий бот: онбординг → план дня → фиксация фактов → напоминания (каркас).

## 1) Быстрый старт локально (без Docker)
1. Создайте бота у @BotFather, получите `BOT_TOKEN`.
2. Скопируйте `.env.example` в `.env` и вставьте токен.
3. Установите Python 3.11+.
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. Запустите:
   ```bash
   python -m app.main
   ```

## 2) Развёртывание на VPS (Docker)
1. Скопируйте репозиторий на сервер.
2. Создайте `.env` на VPS (никогда не коммитьте):
   ```env
   BOT_TOKEN=123456:ABC...
   TZ=Europe/Amsterdam
   ```
3. Запустите:
   ```bash
   docker compose up -d --build
   ```
4. Откройте бот, введите `/start`.

## 3) Структура
```
app/
  handlers/ (onboarding, plan, facts)
  services/ (age_rules, planner)
  models.py (User, Event, Job)
  db.py (SQLite)
  scheduler.py (APScheduler каркас)
  main.py (вход)
  config.py, keyboards.py, states.py, utils_time.py
```

## 4) Настройка безопасного зеркала (GitHub)
Есть 2 варианта:
- **Ветка `mirror` в том же репо** (проще).
- **Отдельный публичный mirror-репозиторий**.

### А) Ветка `mirror` в том же репо
1. В приватном репо добавьте GitHub Actions из `.github/workflows/mirror.yml`.
2. Любой push в `main` создаст/обновит ветку `mirror`, удалив секреты/данные.
3. Деплой делайте **только** из `main`. `mirror` — для просмотра кода мной.

### Б) Отдельный mirror-репозиторий
1. Создайте пустой публичный репозиторий, например `yourname/mamkin-bot-mirror`.
2. В приватном репо настройте секрет `MIRROR_REPO_URL` вида:
   `https://<TOKEN>@github.com/yourname/mamkin-bot-mirror.git`
   (токен GitHub с правом **repo:public_repo** или эквивалент).
3. Включите `.github/workflows/mirror.yml` — он будет пушить в mirror-репо лишь безопасные файлы.

## 5) Команды VPS-шпаргалка
```bash
# Первичный запуск
docker compose up -d --build

# Перезапуск после обновления кода
docker compose pull || true       # если используете образы
docker compose up -d --build

# Логи
docker compose logs -f --tail=100

# Обновление .env (после правки)
docker compose down && docker compose up -d --build

# Резервная копия БД
tar czf backup_$(date +%F).tgz data/
```

## 6) Что дальше (патчи)
- Автонагрузка напоминаний при генерации плана и после фактов.
- /settings для быстрой правки параметров.
- Экспорт/импорт конфигурации из `config/config.local.yml`.

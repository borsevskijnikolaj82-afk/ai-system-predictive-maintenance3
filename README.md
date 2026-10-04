# Лабораторная работа №3 — Predictive Maintenance

Реализация изолированного AI-компонента системы предиктивного обслуживания оборудования.

Компонент принимает телеметрию, валидирует вход, подготавливает признаки, рассчитывает риск компактным baseline-алгоритмом и применяет правило ручной проверки.

## Структура

app/
- __init__.py
- schemas.py — входной и выходной контракт
- preprocessing.py — подготовка признаков
- inference.py — интеллектуальная функция
- service.py — прикладное правило

tests/
- test_component.py

docs/
- lab3_report.md

## Запуск

Требуется Python 3.11+.

    python -m venv .venv
    python -m pip install -r requirements.txt
    python -m pytest -q

Для Windows PowerShell активируйте .venv\Scripts\Activate.ps1. Для Linux/macOS используйте source .venv/bin/activate.

API и веб-сервер для ЛР3 не требуются: компонент тестируется напрямую.

## Контракт

Вход: item_id, temperature, vibration_amplitude, operating_hours, error_code_last_24h.

Выход: prediction, probability, model_version и manual_review_required.

probability является нормированным risk score baseline-алгоритма, а не калиброванной вероятностью.

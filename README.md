# Транзакционное тестирование

Репозиторий для статьи: https://habr.com/ru/company/selectel/blog/598499/

- Способ 0: нет тестирования
- Способ 1: [app/test_1_mock_db.py](app/test_1_mock_db.py) — тестирование через заглушки;
- Способ 2: [app/test_2_embedded_db.py](app/test_2_embedded_db.py) — тестирование через встраиваемую БД, тестировалось через SQLite.
- Способ 3: [app/test_3_nested_transactions.py](app/test_3_nested_transactions.py) — тестирование через вложенные транзакции. Тестировалось на postgresql.

Для тестов с бд необходимо определить переменную окружения `HABR_TEST_DB_URL`.
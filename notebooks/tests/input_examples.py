from app.core.states.api import UserContext
from app.core.states.sql_schema import SQLTables, SQLTableWithColumns, SQLColumn
from app.core.states.agents.terms_explainer import TermEntry, TermsGlossary
from app.core.states.agents.tables_selector import SelectedSQLTables, SelectedSQLTable
from app.core.states.agents.columns_selector import (
    SQLTablesWithSelectedColumns,
    SQLTableWithSelectedColumns,
    SelectedSQLColumn,
)
from app.core.states.agents.sql_executor import SQLExecutionFeedback
from app.core.states.agents.context_intent_classifier import ContextIntentClassification


SESSION_ID = "1"

USER_MESSAGE = "Опиши процесс П1838"

USER_CONTEXT = UserContext(
    block="",
    org_unit="",
    process_name="",
    kp_id="109",
)

NEED_CUR_KP = False
CONTEXT_INTENT_CLASSIFICATION = ContextIntentClassification(
    info_class="common",
    process_ids=[],
    kp_ids=[],
)

COMMON_RULES = """
-----
# Документ с заголовком 'Общее описание домена 'бизнес-процессы'' и подзаголовком 'Клиентские пути':
Вся логика пользовательского взаимодействия в нашем банке строится по следующей иерархии:
1. Клиентский путь (client_path/kp_id), например, "Работа с брокерским счетом"
2. Процесс (process) - составляющая клиентского пути, например:
- Открытие брокерского счета
- Зачисление средств на брокерский счет  
**Замечание:** пользователь не обязан проходить все процессы, входящие в клиентский путь.
3. Действие (action) - действие в рамках процесса, например:
1) Создание заявки (для открытия брокерского счета)
2) Отправка заявки (для открытия брокерского счета)
3) ...
4. Поддействие (action_detailed) - атомарное действие, например:
1) Открытие экрана (для создания заявки)
2) Ввод данных (для создания заявки)

-----
# Документ с заголовком 'Общее описание домена 'бизнес-процессы'' и подзаголовком 'Ошибки':
- Пользователь не обязан проходить все процессы в рамках клиентского пути
- Однако для корректного прохождания процесса желательно пройти все действия и поддействия
- На последнем поддействии сессии должно стоять is_final_step = true. Если на той же строке стоит is_success = true, то сессия выполнена успешно, иначе - сессия выполнена с ошибкой.

-----
# Документ с заголовком 'Общее описание домена 'бизнес-процессы'' и подзаголовком 'Сессии':
Экземпляры клиентских путей - сессии (process_item_id).
Пользователь инициирует сессию, связанную с конкретным процессом (process) в клиентском пути (по kp_id).
Все действия и поддействия логируются в универсальной таблице.
"""

KP_INFO = """
-----
# Документ с заголовком 'Описание клиентского пути "Открытие/редактирование брокерского счета /ИИС". KP ID 1002'
и подзаголовком 'Процессы и действия':
1. Открытие брокерского счета:
1.1 Переход в лендинг открытия брокерского счета
1.2 Заполнение параметров тарифа брокерского счёта
1.3 Заполнение контактных данных
1.4 Вывод средств
1.5 Предложение открытия ИИС к брокерскому счёту
1.6 Подтверждение Клиентом
1.7 Потверждение сотрудником
1.8 Заявка на открытие брокерского счёта оформлена  
2. Зачисление средств на счет
2.1 Зачисление средств на счет

-----
# Документ с заголовком 'Описание клиентского пути "Открытие/редактирование брокерского счета /ИИС". KP ID 1002'
и подзаголовком 'Фильтры':
filter1 - название территориального банка
filter2 - название региона, в котором расположен тербанк
"""

DB_SCHEMA = SQLTables(
    tables=[
        SQLTableWithColumns(
            name="s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai",
            columns=[
                SQLColumn(
                    name="channel",
                    type="text",
                    comment="",
                    first_rows=["vsp", "vsp", "vsp"],
                ),
                SQLColumn(
                    name="month_num",
                    type="text",
                    comment="",
                    first_rows=["2024-12", "2025-07", "2025-07"],
                ),
                SQLColumn(
                    name="week_num",
                    type="text",
                    comment="",
                    first_rows=["2024_51", "2025_28", "2025_28"],
                ),
                SQLColumn(
                    name="filter1",
                    type="text",
                    comment="",
                    first_rows=[
                        "Юго-Западный банк",
                        "Московский банк",
                        "Волго - Вятский банк",
                    ],
                ),
                SQLColumn(
                    name="filter2",
                    type="text",
                    comment="",
                    first_rows=[
                        "Краснодарский край",
                        "г.Москва",
                        "Республика Татарстан",
                    ],
                ),
                SQLColumn(
                    name="filter3",
                    type="text",
                    comment="",
                    first_rows=["", "None", "None"],
                ),
                SQLColumn(
                    name="filter4",
                    type="text",
                    comment="",
                    first_rows=["", "None", "None"],
                ),
                SQLColumn(
                    name="filter5",
                    type="text",
                    comment="",
                    first_rows=["", "None", "None"],
                ),
                SQLColumn(
                    name="kp_id",
                    type="integer",
                    comment="",
                    first_rows=["239", "1002", "1002"],
                ),
                SQLColumn(
                    name="process_date",
                    type="date",
                    comment="",
                    first_rows=["2024-12-21", "2025-07-07", "2025-07-08"],
                ),
                SQLColumn(
                    name="process_item_id",
                    type="text",
                    comment="",
                    first_rows=[
                        "04YpX5ihTI-PKJFZ01t3kCWTskBtzcT2JpKOxDiMBsCO4CBVtgzHnrlSTOcGkDZR | 2024-12-21 13:50:14.672+03",
                        "ArYD8GD-SEi9KrHB8ZkD9AR2_vPiFAEVo0uKW54Lk6gSS_tIgmmBW5hg06kU2oK- | 2025-07-08 17:25:40.676+03",
                        "-1FaesHvRUCx3tYkmSxGUB4ttfXLIWfV6sRJ0Hnf5URj-ppWIxKWbNnZvr2rd6Wm | 2025-07-09 14:27:33.839+03",
                    ],
                ),
                SQLColumn(
                    name="client_id",
                    type="text",
                    comment="",
                    first_rows=[
                        "1130222181587568926",
                        "1130159386625079547",
                        "1127796686208118268",
                    ],
                ),
                SQLColumn(
                    name="process_num",
                    type="text",
                    comment="",
                    first_rows=["1", "1", "1"],
                ),
                SQLColumn(
                    name="process",
                    type="text",
                    comment="",
                    first_rows=[
                        "Снятие наличных со вклада/счёта",
                        "Открытие брокерского счета",
                        "Открытие брокерского счета",
                    ],
                ),
                SQLColumn(
                    name="action_num",
                    type="text",
                    comment="",
                    first_rows=["1.2", "1.1", "1.2"],
                ),
                SQLColumn(
                    name="action",
                    type="text",
                    comment="",
                    first_rows=[
                        "Ознакомление Клиента  с документами",
                        "Переход в лендинг открытия брокерского счета",
                        "Заполнение параметров тарифа брокерского счёта",
                    ],
                ),
                SQLColumn(
                    name="object_num",
                    type="text",
                    comment="",
                    first_rows=["", "None", "1.2.Б"],
                ),
                SQLColumn(
                    name="object",
                    type="text",
                    comment="",
                    first_rows=["", "None", "Заполнение параметров "],
                ),
                SQLColumn(
                    name="action_detailed",
                    type="text",
                    comment="",
                    first_rows=[
                        "subflow.confirmation/Ознакомление с документами/Подтверждение/Виджет проверки документов/Открытие/Снятие наличных",
                        "brokerage.management/Открытие брокерского счета/Лендинг/Открытие экрана",
                        "brokerage.management/Открытие брокерского счета/Открытие брокерского счета/Параметры счета/Открытие экрана",
                    ],
                ),
                SQLColumn(
                    name="is_employee",
                    type="integer",
                    comment="",
                    first_rows=["1", "1", "1"],
                ),
                SQLColumn(
                    name="is_tech_error",
                    type="integer",
                    comment="",
                    first_rows=["0", "0", "0"],
                ),
                SQLColumn(
                    name="is_success",
                    type="integer",
                    comment="",
                    first_rows=["0", "0", "0"],
                ),
                SQLColumn(
                    name="cost_per_minute",
                    type="numeric",
                    comment="",
                    first_rows=["43.110585", "43.110585", "43.110585"],
                ),
                SQLColumn(
                    name="csi",
                    type="numeric",
                    comment="",
                    first_rows=["None", "None", "None"],
                ),
                SQLColumn(
                    name="dt",
                    type="timestamp with time zone",
                    comment="",
                    first_rows=[
                        "2024-12-21 10:51:46.231000+00:00",
                        "2025-07-08 14:25:40.676000+00:00",
                        "2025-07-09 11:27:56.146000+00:00",
                    ],
                ),
                SQLColumn(
                    name="duration",
                    type="double precision",
                    comment="",
                    first_rows=["11.355", "0.0", "22.307"],
                ),
                SQLColumn(
                    name="step_detailed",
                    type="text",
                    comment="",
                    first_rows=[
                        "accounts.withdrawal/Снятие наличных со вклада/Выбор счета и суммы списания/Открытие экрана --> subflow.confirmation/Ознакомление с документами/Подтверждение/Виджет проверки документов/Открытие/Снятие наличных",
                        "None",
                        "brokerage.management/Открытие брокерского счета/Лендинг/Открытие экрана --> brokerage.management/Открытие брокерского счета/Открытие брокерского счета/Параметры счета/Открытие экрана",
                    ],
                ),
                SQLColumn(
                    name="cost",
                    type="double precision",
                    comment="",
                    first_rows=["8.15867821125", "0.0", "16.02779699325"],
                ),
                SQLColumn(
                    name="loop_duration",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "22.307"],
                ),
                SQLColumn(
                    name="loop_cost",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "16.02779699325"],
                ),
                SQLColumn(
                    name="error_duration",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "0.0"],
                ),
                SQLColumn(
                    name="error_cost",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "0.0"],
                ),
                SQLColumn(
                    name="is_final_step",
                    type="integer",
                    comment="",
                    first_rows=["0", "0", "0"],
                ),
                SQLColumn(
                    name="duration_3m",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "22.307"],
                ),
                SQLColumn(
                    name="cost_3m",
                    type="double precision",
                    comment="",
                    first_rows=["0.0", "0.0", "16.02779699325"],
                ),
                SQLColumn(
                    name="report_date",
                    type="date",
                    comment="",
                    first_rows=["2024-12-21", "2025-07-07", "2025-07-08"],
                ),
                SQLColumn(
                    name="load_dttm",
                    type="character varying(50)",
                    comment="",
                    first_rows=[
                        "2025-06-25 11:01:49.887124",
                        "2025-08-01 13:10:00.254674",
                        "2025-08-01 13:10:00.254674",
                    ],
                ),
                SQLColumn(
                    name="is_business_error",
                    type="integer",
                    comment="",
                    first_rows=["None", "None", "None"],
                ),
            ],
        )
    ]
)

TERMS_GLOSSARY = TermsGlossary(
    glossary=[
        TermEntry(
            term="Тербанк",
            meaning="Территориальное подразделение банка, например, Уральский банк.",
        )
    ]
)

TABLE_NAMES = ["s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai"]

SELECTED_TABLES = SelectedSQLTables(
    tables=[
        SelectedSQLTable(
            name="s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai",
            reason="Таблица содержит данные обо всех сессиях клиентов, что может включать информацию о тербанках и уникальных клиентах.",
        )
    ]
)

SQL_EXAMPLES = """
-----
# Документ с заголовком 'Примеры SQL-запросов для метрики 'длительность (duration)''
и подзаголовком 'Пример 2':
- Самый медленный тербанк в Брянской области:
```
SELECT bank_name, AVG(total_duration) AS avg_total_duration
FROM (
SELECT bank_name, process_item_id, SUM(duration) AS total_duration
FROM your_table
WHERE region = "Брянская область"
GROUP BY bank_name, process_item_id
) t
GROUP BY bank_name
ORDER BY avg_total_duration DESC
LIMIT 1;
```

-----
# Документ с заголовком 'Примеры SQL-запросов для метрики 'длительность (duration)''
и подзаголовком 'Пример 1':
- Средняя длительность клиентского пути 121:
```
SELECT AVG(total_duration) AS avg_total_duration
FROM (
SELECT process_item_id, SUM(duration) AS total_duration
FROM your_table
WHERE kp_id = 121
GROUP BY process_item_id
) t;
```
"""

TABLES_WITH_SELECTED_COLUMNS = SQLTablesWithSelectedColumns(
    tables=[
        SQLTableWithSelectedColumns(
            name="s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai",
            columns=[
                SelectedSQLColumn(
                    name="client_id",
                    reason="Уникальный ID клиента, необходим для подсчета числа уникальных клиентов.",
                ),
                SelectedSQLColumn(
                    name="filter1",
                    reason="Название территориального банка, необходимо для группировки по тербанкам.",
                ),
            ],
        )
    ]
)

# SQL_DECOMPOSER_PLAN = SQLDecompositionResult(
#     initial_plan="1. Извлечь данные из таблицы sw_v2_summary_channels_2_3_ai\n2. Сгруппировать по тербанкам (filter1)\n3. Посчитать число уникальных клиентов (client_id)\n4. Отсортировать по убыванию числа уникальных клиентов\n5. Ограничить вывод до 20 строк",
#     entities=SQLEntityExtraction(
#         selected_tables=["s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai"],
#         selected_columns=["filter1", "client_id"],
#         condition=[],
#         joins=[],
#     ),
#     reasoning=[
#         SQLReasoningStep(
#             step_id=1,
#             description="Выбор таблицы и необходимых колонок. Нужны колонки filter1 (тербанк) и client_id (клиент).",
#             partial_query="SELECT filter1, COUNT(DISTINCT client_id) AS unique_clients FROM s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai",
#         ),
#         SQLReasoningStep(
#             step_id=2,
#             description="Группировка по тербанкам (filter1).",
#             partial_query="GROUP BY filter1",
#         ),
#         SQLReasoningStep(
#             step_id=3,
#             description="Сортировка по числу уникальных клиентов в порядке убывания.",
#             partial_query="ORDER BY unique_clients DESC",
#         ),
#         SQLReasoningStep(
#             step_id=4,
#             description="Ограничение вывода до 20 строк.",
#             partial_query="LIMIT 20",
#         ),
#     ],
#     something_forgotten="Нет, ничего не забыл. Все шаги учтены и корректны.",
#     final_sql_query="SELECT filter1, COUNT(DISTINCT client_id) AS unique_clients FROM s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai GROUP BY filter1 ORDER BY unique_clients DESC LIMIT 20",
# )

SQL_EXECUTION_FEEDBACK = SQLExecutionFeedback(
    status="ok",
    sql_query="SELECT\n  filter1,\n  COUNT(DISTINCT client_id) AS unique_clients\nFROM s_grnplm_as_bsr_ds_raw.sw_v2_summary_channels_2_3_ai\nGROUP BY\n  filter1\nORDER BY\n  unique_clients DESC\nLIMIT 20",
    error=None,
)

SQL_RESULT = {
    "filter1": {
        0: "Сибирский банк",
        1: "Московский банк",
        2: "Среднерусский банк",
        3: "Волго - Вятский банк",
        4: "Северо-Западный банк",
        5: "Уральский банк",
        6: "Не определено",
        7: "Юго-Западный банк",
        8: "Центрально-Черноземный банк",
        9: "Поволжский банк",
        10: "Дальневосточный банк",
        11: "Байкальский банк",
    },
    "unique_clients": {
        0: 89,
        1: 44,
        2: 34,
        3: 33,
        4: 24,
        5: 24,
        6: 24,
        7: 22,
        8: 21,
        9: 15,
        10: 12,
        11: 8,
    },
}

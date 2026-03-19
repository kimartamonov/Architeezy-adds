# Журнал релиза документации по метамоделям

Этот файл управляет последовательной разработкой документации по структуре из `meta-doc-structure.md`.

## Как пользоваться

1. Для запуска очередного шага вызывай одну и ту же команду: `Реализуй DocCurrentTask.md`.
2. `DocCurrentTask.md` должен взять текущую задачу из раздела `Текущая задача` этого журнала.
3. После подготовки документа `DocCurrentTask.md` должен:
   - создать или обновить файл документа в `metadoc-pages/`;
   - создать отчёт о выполнении в `metadoc-reports/`;
   - перенести завершённую задачу в раздел `Реализованные документы`;
   - назначить следующую задачу из очереди как текущую;
   - обновить таблицу очереди.
4. Если все документы реализованы, в `Текущая задача` должно быть явно написано, что очередь завершена.

## Текущая задача

- Статус: `COMPLETED`
- Порядок: `18/18`
- Раздел документации: `Очередь завершена`
- Страница документации: `Все документы из текущей структуры реализованы`
- Файл требований: `N/A`
- Целевой файл документа: `N/A`
- Файл отчёта: `N/A`
- Следующая задача после завершения: `QUEUE_COMPLETE`

## Очередь документов

| Порядок | Статус | Раздел | Страница | Файл требований | Целевой документ | Отчёт |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | DONE | Введение | Что такое метамодель в Architeezy и когда она нужна | metadoc-req/Introduction-WhatIsMetamodelAndWhenNeeded.md | metadoc-pages/Introduction-WhatIsMetamodelAndWhenNeeded.md | metadoc-reports/Introduction-WhatIsMetamodelAndWhenNeeded-report.md |
| 02 | DONE | Введение | Маршруты чтения по ролям и сценариям | metadoc-req/Introduction-ReadingPathsByRoleAndScenario.md | metadoc-pages/Introduction-ReadingPathsByRoleAndScenario.md | metadoc-reports/Introduction-ReadingPathsByRoleAndScenario-report.md |
| 03 | DONE | От идеи к языку | Как выбрать границы предметной области и пилотный кейс | metadoc-req/Discovery-DomainScopeAndPilotCase.md | metadoc-pages/Discovery-DomainScopeAndPilotCase.md | metadoc-reports/Discovery-DomainScopeAndPilotCase-report.md |
| 04 | DONE | От идеи к языку | Как выделить сущности из практики и собрать минимально достаточную метамодель | metadoc-req/Discovery-ExtractConceptsAndBuildMinimalMetamodel.md | metadoc-pages/Discovery-ExtractConceptsAndBuildMinimalMetamodel.md | metadoc-reports/Discovery-ExtractConceptsAndBuildMinimalMetamodel-report.md |
| 05 | DONE | Конструкция метамодели | Как проектировать типы объектов и атрибуты | metadoc-req/Language-ObjectTypesAndAttributes.md | metadoc-pages/Language-ObjectTypesAndAttributes.md | metadoc-reports/Language-ObjectTypesAndAttributes-report.md |
| 06 | DONE | Конструкция метамодели | Как проектировать связи, иерархии и переиспользуемые справочники | metadoc-req/Language-RelationsHierarchiesAndReferenceObjects.md | metadoc-pages/Language-RelationsHierarchiesAndReferenceObjects.md | metadoc-reports/Language-RelationsHierarchiesAndReferenceObjects-report.md |
| 07 | DONE | Конструкция метамодели | Как задавать статусы, жизненные циклы, версии и обязательные правила | metadoc-req/Language-LifecyclesStatusesVersionsAndRules.md | metadoc-pages/Language-LifecyclesStatusesVersionsAndRules.md | metadoc-reports/Language-LifecyclesStatusesVersionsAndRules-report.md |
| 08 | DONE | Представления и публикация | Как делать диаграммы, таблицы и несколько представлений одной модели | metadoc-req/Views-DiagramTableAndMultipleViews.md | metadoc-pages/Views-DiagramTableAndMultipleViews.md | metadoc-reports/Views-DiagramTableAndMultipleViews-report.md |
| 09 | DONE | Представления и публикация | Как делать карточки объектов, паспорта и документы на базе модели | metadoc-req/Views-ObjectCardsPassportsAndDocuments.md | metadoc-pages/Views-ObjectCardsPassportsAndDocuments.md | metadoc-reports/Views-ObjectCardsPassportsAndDocuments-report.md |
| 10 | DONE | Проверка и развитие | Как проверить метамодель на пилоте и не переусложнить язык | metadoc-req/Validation-PilotValidationAndAvoidOvermodeling.md | metadoc-pages/Validation-PilotValidationAndAvoidOvermodeling.md | metadoc-reports/Validation-PilotValidationAndAvoidOvermodeling-report.md |
| 11 | DONE | Проверка и развитие | Как масштабировать и сопровождать метамодель в командах | metadoc-req/Validation-ScalingAndMetamodelGovernance.md | metadoc-pages/Validation-ScalingAndMetamodelGovernance.md | metadoc-reports/Validation-ScalingAndMetamodelGovernance-report.md |
| 12 | DONE | Интеграция и автоматизация | Как использовать REST API, MCP и AI поверх кастомной метамодели | metadoc-req/Integrations-RestApiMcpAndAi.md | metadoc-pages/Integrations-RestApiMcpAndAi.md | metadoc-reports/Integrations-RestApiMcpAndAi-report.md |
| 13 | DONE | Интеграция и автоматизация | Как встроить модель в governance, review и операционные процессы | metadoc-req/Integrations-ModelInGovernanceReviewAndOperations.md | metadoc-pages/Integrations-ModelInGovernanceReviewAndOperations.md | metadoc-reports/Integrations-ModelInGovernanceReviewAndOperations-report.md |
| 14 | DONE | Прикладные паттерны | Паттерн: каталоги и управленческие реестры | metadoc-req/Patterns-CatalogsAndManagementRegisters.md | metadoc-pages/Patterns-CatalogsAndManagementRegisters.md | metadoc-reports/Patterns-CatalogsAndManagementRegisters-report.md |
| 15 | DONE | Прикладные паттерны | Паттерн: процессы, требования и traceability | metadoc-req/Patterns-ProcessesRequirementsAndTraceability.md | metadoc-pages/Patterns-ProcessesRequirementsAndTraceability.md | metadoc-reports/Patterns-ProcessesRequirementsAndTraceability-report.md |
| 16 | DONE | Прикладные паттерны | Паттерн: интеграции, события и технические контракты | metadoc-req/Patterns-IntegrationsEventsAndTechnicalContracts.md | metadoc-pages/Patterns-IntegrationsEventsAndTechnicalContracts.md | metadoc-reports/Patterns-IntegrationsEventsAndTechnicalContracts-report.md |
| 17 | DONE | Прикладные паттерны | Паттерн: data governance, глоссарии и compliance обмена данными | metadoc-req/Patterns-DataGovernanceGlossariesAndCompliance.md | metadoc-pages/Patterns-DataGovernanceGlossariesAndCompliance.md | metadoc-reports/Patterns-DataGovernanceGlossariesAndCompliance-report.md |
| 18 | DONE | Прикладные паттерны | Паттерн: инфраструктура, платформа и эксплуатационные зависимости | metadoc-req/Patterns-InfrastructurePlatformAndOperations.md | metadoc-pages/Patterns-InfrastructurePlatformAndOperations.md | metadoc-reports/Patterns-InfrastructurePlatformAndOperations-report.md |

## Реализованные документы

| Дата | Порядок | Страница | Документ | Отчёт |
| --- | --- | --- | --- | --- |
| 2026-03-19 | 01 | Что такое метамодель в Architeezy и когда она нужна | metadoc-pages/Introduction-WhatIsMetamodelAndWhenNeeded.md | metadoc-reports/Introduction-WhatIsMetamodelAndWhenNeeded-report.md |
| 2026-03-19 | 02 | Маршруты чтения по ролям и сценариям | metadoc-pages/Introduction-ReadingPathsByRoleAndScenario.md | metadoc-reports/Introduction-ReadingPathsByRoleAndScenario-report.md |
| 2026-03-19 | 03 | Как выбрать границы предметной области и пилотный кейс | metadoc-pages/Discovery-DomainScopeAndPilotCase.md | metadoc-reports/Discovery-DomainScopeAndPilotCase-report.md |
| 2026-03-19 | 04 | Как выделить сущности из практики и собрать минимально достаточную метамодель | metadoc-pages/Discovery-ExtractConceptsAndBuildMinimalMetamodel.md | metadoc-reports/Discovery-ExtractConceptsAndBuildMinimalMetamodel-report.md |
| 2026-03-19 | 05 | Как проектировать типы объектов и атрибуты | metadoc-pages/Language-ObjectTypesAndAttributes.md | metadoc-reports/Language-ObjectTypesAndAttributes-report.md |
| 2026-03-19 | 06 | Как проектировать связи, иерархии и переиспользуемые справочники | metadoc-pages/Language-RelationsHierarchiesAndReferenceObjects.md | metadoc-reports/Language-RelationsHierarchiesAndReferenceObjects-report.md |
| 2026-03-19 | 07 | Как задавать статусы, жизненные циклы, версии и обязательные правила | metadoc-pages/Language-LifecyclesStatusesVersionsAndRules.md | metadoc-reports/Language-LifecyclesStatusesVersionsAndRules-report.md |
| 2026-03-19 | 08 | Как делать диаграммы, таблицы и несколько представлений одной модели | metadoc-pages/Views-DiagramTableAndMultipleViews.md | metadoc-reports/Views-DiagramTableAndMultipleViews-report.md |
| 2026-03-19 | 09 | Как делать карточки объектов, паспорта и документы на базе модели | metadoc-pages/Views-ObjectCardsPassportsAndDocuments.md | metadoc-reports/Views-ObjectCardsPassportsAndDocuments-report.md |
| 2026-03-19 | 10 | Как проверить метамодель на пилоте и не переусложнить язык | metadoc-pages/Validation-PilotValidationAndAvoidOvermodeling.md | metadoc-reports/Validation-PilotValidationAndAvoidOvermodeling-report.md |
| 2026-03-19 | 11 | Как масштабировать и сопровождать метамодель в командах | metadoc-pages/Validation-ScalingAndMetamodelGovernance.md | metadoc-reports/Validation-ScalingAndMetamodelGovernance-report.md |
| 2026-03-19 | 12 | Как использовать REST API, MCP и AI поверх кастомной метамодели | metadoc-pages/Integrations-RestApiMcpAndAi.md | metadoc-reports/Integrations-RestApiMcpAndAi-report.md |
| 2026-03-19 | 13 | Как встроить модель в governance, review и операционные процессы | metadoc-pages/Integrations-ModelInGovernanceReviewAndOperations.md | metadoc-reports/Integrations-ModelInGovernanceReviewAndOperations-report.md |
| 2026-03-19 | 14 | Паттерн: каталоги и управленческие реестры | metadoc-pages/Patterns-CatalogsAndManagementRegisters.md | metadoc-reports/Patterns-CatalogsAndManagementRegisters-report.md |
| 2026-03-19 | 15 | Паттерн: процессы, требования и traceability | metadoc-pages/Patterns-ProcessesRequirementsAndTraceability.md | metadoc-reports/Patterns-ProcessesRequirementsAndTraceability-report.md |
| 2026-03-19 | 16 | Паттерн: интеграции, события и технические контракты | metadoc-pages/Patterns-IntegrationsEventsAndTechnicalContracts.md | metadoc-reports/Patterns-IntegrationsEventsAndTechnicalContracts-report.md |
| 2026-03-19 | 17 | Паттерн: data governance, глоссарии и compliance обмена данными | metadoc-pages/Patterns-DataGovernanceGlossariesAndCompliance.md | metadoc-reports/Patterns-DataGovernanceGlossariesAndCompliance-report.md |
| 2026-03-19 | 18 | Паттерн: инфраструктура, платформа и эксплуатационные зависимости | metadoc-pages/Patterns-InfrastructurePlatformAndOperations.md | metadoc-reports/Patterns-InfrastructurePlatformAndOperations-report.md |
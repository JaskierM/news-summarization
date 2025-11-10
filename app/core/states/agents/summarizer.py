from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Topic(str, Enum):
    """Классификация новости для выбора ветки суммаризации."""

    DEFAULT = "default"
    DUMA_BILL = "duma_bill"
    JUDGE_IVANOV = "judge_ivanov"


class DumaBillDetails(BaseModel):
    """
    Детализация новости о законопроекте/обсуждении в Госдуме.
    Заполняется, если topic == 'duma_bill'.
    """

    norm: Optional[str] = Field(
        None,
        description="Норма/статья закона, к которой относится инициатива (например: 'ст. 446 ГПК РФ').",
    )
    number: Optional[str] = Field(
        None,
        description="Номер законопроекта (например: '№ 123456-8'). Если в тексте не указан — оставь null.",
    )
    initiator: Optional[str] = Field(
        None,
        description="Инициатор(ы) законопроекта (например: 'Минюст', 'фракция ЛДПР', конкретные депутаты).",
    )
    search_keys: List[str] = Field(
        default_factory=list,
        description="Технические ключи для поиска карточки законопроекта (3–6 фраз/ключевых слов).",
    )


class JudgeIvanovDetails(BaseModel):
    """
    Детализация в случае, если в новости фигурирует судья Иванов.
    Заполняется, если topic == 'judge_ivanov'.
    """

    full_name: Optional[str] = Field(
        None,
        description="Полное имя судьи, если указано в тексте (например: 'Иванов Пётр Сергеевич').",
    )
    role: Optional[str] = Field(
        None,
        description="Роль/должность в контексте новости (обычно: 'судья').",
    )
    instance: Optional[str] = Field(
        None,
        description="Инстанция/уровень (например: 'первая инстанция', 'апелляция'), если явно указано.",
    )
    action: Optional[str] = Field(
        None,
        description="Что сделал/предложил/решил судья в контексте новости (краткая формулировка).",
    )


class NewsSummarization(BaseModel):
    """
    Унифицированный ответ агента-суммаризатора.
    Поддерживает общий случай и два специальных сценария.
    """

    thinking: Optional[str] = Field(
        None,
        description="Опциональные рабочие заметки/ход рассуждений модели. Можно не заполнять.",
    )

    topic: Topic = Field(
        ...,
        description="Классификация новости: 'default' | 'duma_bill' | 'judge_ivanov'.",
    )

    summary: str = Field(
        ...,
        description=(
            "Краткий или расширенный пересказ (в зависимости от topic). "
            "Строго фактический, без оценок и домыслов."
        ),
    )

    bill: Optional[DumaBillDetails] = Field(
        None, description="Детали по законопроекту, если тема 'duma_bill'; иначе null."
    )

    judge_ivanov: Optional[JudgeIvanovDetails] = Field(
        None,
        description="Детали при упоминании судьи Иванова, если тема 'judge_ivanov'; иначе null.",
    )
    
    def to_bullet_list(self) -> str:
        lines = [f"Тема: {self.topic.value}", f"Краткое содержание: {self.summary}"]

        if self.topic == Topic.DUMA_BILL and self.bill:
            lines.append("\nДетали законопроекта:")
            if self.bill.norm:
                lines.append(f"\tНорма закона: {self.bill.norm}")
            if self.bill.number:
                lines.append(f"\tНомер законопроекта: {self.bill.number}")
            if self.bill.initiator:
                lines.append(f"\tИнициатор: {self.bill.initiator}")
            if self.bill.search_keys:
                keys = ", ".join(self.bill.search_keys)
                lines.append(f"\tКлючевые слова для поиска: {keys}")

        elif self.topic == Topic.JUDGE_IVANOV and self.judge_ivanov:
            lines.append("\nДетали по судье Иванову:")
            if self.judge_ivanov.full_name:
                lines.append(f"\tИмя судьи: {self.judge_ivanov.full_name}")
            if self.judge_ivanov.role:
                lines.append(f"\tРоль: {self.judge_ivanov.role}")
            if self.judge_ivanov.instance:
                lines.append(f"\tИнстанция: {self.judge_ivanov.instance}")
            if self.judge_ivanov.action:
                lines.append(f"\tДействие/решение: {self.judge_ivanov.action}")

        return "\n".join(lines)

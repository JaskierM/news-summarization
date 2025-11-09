from typing import Optional

from pydantic import BaseModel, Field


class NERPersonEntity(BaseModel):
    """JSON-схема для представления именованной персоны, извлечённой из новости."""

    full_name: str = Field(
        ...,
        description="Полное имя человека (ФИО) так, как оно указано в тексте",
    )

    role: Optional[str] = Field(
        None,
        description=(
            "Роль, должность или статус человека, если они явно указаны в тексте. "
            "Примеры: 'лидер ЛДПР', 'судья', 'министр'. "
        ),
    )

    addresses: Optional[list[str]] = Field(
        default_factory=list,
        description=(
            "Список адресов или мест, связанных с этим человеком, если они упомянуты в тексте. "
            "Например: ['Москва', 'Здание Государственной Думы на Охотном Ряду']. "
            "Если связи по месту нет — список пуст."
        ),
    )


class NERExtraction(BaseModel):
    """Контейнер для списка персон, найденных в тексте новости."""

    thinking: Optional[str] = Field(
        None,
        description="Опциональные рабочие заметки/ход рассуждений модели. Можно не заполнять.",
    )

    ner_persons: list[NERPersonEntity] = Field(
        default_factory=list,
        description=(
            "Список всех выделенных персон (объектов NERPersonEntity), "
            "упомянутых в новостном тексте."
        ),
    )

    def to_bullet_list(self) -> str:
        return "\n".join(
            f"ФИО: {ner_person.full_name}; Роль: {ner_person.role}; Адреса: {ner_person.addresses}"
            for ner_person in self.ner_persons
        )

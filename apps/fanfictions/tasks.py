from typing import Sequence

from django.conf import settings

import openai
from celery import shared_task

from apps.characters.models import Character
from apps.users.models import User

from .models import FanFiction, Genre

openai.api_key = settings.OPENAI_API_KEY

CHATGPT_REQUEST_TEXT = """
    Write me a fanfiction in the '{genre_name}' genre with title '{title}' with
    participation of these heroes: {characters}
"""


@shared_task
def create_fanfiction_with_chatgpt(
    title: str,
    genre_id: int,
    user_id: int,
    character_ids: Sequence[int],
):
    """Request text from ChatGPT and create fanfiction."""
    genre = Genre.objects.get(pk=genre_id)
    user = User.objects.get(pk=user_id)
    characters = Character.objects.filter(
        id__in=character_ids,
    ).values(
        "id",
        "name",
    )
    response = get_response_from_chatgpt(title, genre, characters)
    create_fanfiction(
        title=title,
        genre=genre,
        user=user,
        text=response["choices"][0]["message"]["content"],
        characters=characters,
    )


def get_response_from_chatgpt(
    title: str,
    genre: Genre,
    characters: Sequence[Character],
):
    """Request data to create fanfiction from ChatGPT."""
    return openai.ChatCompletion.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": CHATGPT_REQUEST_TEXT.format(
                    genre_name=genre.name,
                    title=title,
                    characters=", ".join(
                        character["name"] for character in characters
                    ),
                ),
            },
        ],
        max_tokens=settings.OPENAI_MAX_TOKENS,
    )


def create_fanfiction(
    title: str,
    genre: Genre,
    user: User,
    text: str,
    characters: Sequence[Character],
):
    """Create new fanfiction with prepared data."""
    fanfiction = FanFiction.objects.create(
        title=title,
        genre=genre,
        user=user,
        text=text,
    )
    fanfiction.save()
    fanfiction.characters.add(
        *(character["id"] for character in characters),
    )


@shared_task
def publish(fanfiction_id: int):
    """Set fanfiction `is_published` attribute to True."""
    fanfiction = FanFiction.objects.get(pk=fanfiction_id)
    fanfiction.is_published = True
    fanfiction.save()

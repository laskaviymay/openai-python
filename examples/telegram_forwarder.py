"""Forward news posts from subscribed Telegram channels to a chat.

The script runs using a personal account and listens to all new posts on
channels you are subscribed to. When a post contains any of the defined
keywords, it is forwarded to ``TARGET_CHAT``. Reposts are forwarded too but
duplicates are skipped.

Usage::

    python examples/telegram_forwarder.py

You will be asked to sign in on the first run and a ``forwarder.session`` file
will be created to persist your login.
"""

import asyncio
from typing import Set, Tuple

from telethon import TelegramClient, events

# Replace with your own API credentials
API_ID = 29824150
API_HASH = '6f733b4d95b6058e145ea7c6658c7025'

# ID or username of the chat to forward matching posts to
TARGET_CHAT = 'your_target_chat_username_or_id'

# List of keywords to watch for in new posts
KEYWORDS = [
    'фк краснодар',
    'футбольный клуб краснодар',
    'быки',
    'краснодарцы',
    'краснодарский клуб',
    'черно-зеленые',
    'галлицкий',
    'сергей галлицкий',
    'краснодар арена',
    'академия краснодара',
    'молодёжка краснодара',
    'краснодар-2',
    'сперцян',
    'кордоба',
    'сафарян',
    'черников',
    'иванович',
    'ильин',
    'кадио',
    'алейшандре',
    'жоаозиньо',
    'рамирес',
    'берг',
    'вандерсон',
    'классон',
    'мусаев',
    'ивич',
    'торбинский',
    'гончаренко',
    'шалимов',
    'трансфер краснодара',
    'игра краснодара',
    'матч краснодара',
    'результат матча',
    'поражение краснодара',
    'победа краснодара',
    'тур рпл',
    'кубок россии',
    'лига европы',
    'лига конференций',
    'чемпионат россии',
    'судья матча',
    'удаление краснодар',
    'гол краснодар',
    'пенальти краснодар',
    'стадион краснодар',
    'арена краснодар',
    'академия галлицкого',
    'краснодарский край футбол',
]


async def main() -> None:
    # Create the client and connect. The session will be stored in 'forwarder.session'.
    client = TelegramClient('forwarder', API_ID, API_HASH)

    processed: Set[Tuple[int, int]] = set()

    @client.on(events.NewMessage)
    async def handler(event: events.NewMessage.Event) -> None:
        """Forward channel posts containing the keywords."""
        # Only consider posts from broadcast channels (not groups or comments)
        if not event.is_channel or event.is_group:
            return

        text = event.raw_text.lower()
        if not any(keyword in text for keyword in KEYWORDS):
            return

        if event.message.forward:
            # Use original post information to avoid duplicates from reposts
            unique_id = (
                event.message.forward.chat_id,
                event.message.forward.channel_post,
            )
        else:
            unique_id = (event.chat_id, event.id)

        if unique_id in processed:
            return
        processed.add(unique_id)

        await event.message.forward_to(TARGET_CHAT)
        print(f"Forwarded message {unique_id}")

    async with client:
        print("Forwarder is running. Press Ctrl+C to stop.")
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())

from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event


@local_handler.register(event_name="on_discord_get_user")
async def discord_get_user(event: Event):
    event_name, payload = event

    # TODO: Using The Payload, we're going to do some DB checks to see if the user is blacklisted from the bot, or do any other sort of necessary checks depending on the user id

    pass

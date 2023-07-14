from fastapi import APIRouter, Request, BackgroundTasks
from app.services.generate_data import send_generator
from app.utils.logging import log
from sse_starlette.sse import EventSourceResponse
import asyncio
import datetime
from app.utils.notification_helper import send_webhook


MESSAGE_STREAM_DELAY = 15  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

router = APIRouter(prefix="/v1")


@router.get("/events", tags=['Events'])
async def get_events(request: Request,  background_tasks: BackgroundTasks):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.info('Client Discount...')
                break

            item = await send_generator()
            if item:
                # current_datetime = datetime.datetime.now()
                # notice = {'time': str(current_datetime),
                #           'action': 'Data Sent Successfully'}
                # background_tasks.add_task(send_webhook, notice)
                yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": item,
                }
            else:
                yield {
                    "event": "end_event",
                    "id": "message_id",
                    "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                    "data": "End of the stream",
                }

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

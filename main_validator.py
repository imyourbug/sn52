import asyncio
from contextlib import asynccontextmanager

import uvicorn
import wandb
from commons.api.middleware import LimitContentLengthMiddleware
from commons.api.reward_route import reward_router
from commons.human_feedback.dojo import DojoAPI
from commons.objects import ObjectManager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from neurons.validator import DojoTaskTracker

load_dotenv()


validator = ObjectManager.get_validator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Performing startup tasks...")
    yield
    logger.info("Performing shutdown tasks...")
    validator._should_exit = True
    DojoTaskTracker()._should_exit = True
    wandb.finish()
    validator.save_state()
    await DojoAPI._http_client.aclose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
)
app.add_middleware(LimitContentLengthMiddleware)
app.include_router(reward_router)


async def main():
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=ObjectManager.get_config().api.port,
        workers=1,
        log_level="info",
        reload=False,
    )
    server = uvicorn.Server(config)
    running_tasks = [
        asyncio.create_task(validator.log_validator_status()),
        asyncio.create_task(validator.run()),
        asyncio.create_task(validator.update_score_and_send_feedback()),
        asyncio.create_task(DojoTaskTracker.monitor_task_completions()),
    ]

    await server.serve()

    for task in running_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info(f"Cancelled task {task.get_name()}")
        except Exception as e:
            logger.error(f"Task {task.get_name()} raised an exception: {e}")
            pass

    logger.info("Exiting main function.")


if __name__ == "__main__":
    asyncio.run(main())

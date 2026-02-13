"""
Background task to cleanup expired sessions from the database

This can be run as a scheduled task (e.g., using cron, celery, or APScheduler)
to periodically remove expired sessions from the sessions table.
"""

import asyncio
from datetime import datetime, timezone
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete
from .db import main
from .api.sessions import models


async def cleanup_expired_sessions():
    """Remove expired sessions from the sessions table"""
    async with main.get_session_context() as session:
        # Delete all sessions where expires_at is in the past
        statement = delete(models.Session).where(
            models.Session.expires_at < datetime.now(timezone.utc) # type: ignore
        )
        result = await session.exec(statement)
        await session.commit()
        
        deleted_count = result.rowcount
        print(f"Cleaned up {deleted_count} expired sessions at {datetime.now()}")
        return deleted_count


# Example using APScheduler
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# Run cleanup every day at 2 AM
scheduler.add_job(
    cleanup_expired_sessions,
    'cron',
    hour=2,
    minute=0
)

scheduler.start()
"""

# Example using simple asyncio loop (for testing)
async def run_periodic_cleanup(interval_hours: int = 24):
    """Run cleanup periodically"""
    while True:
        try:
            await cleanup_expired_sessions()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        # Wait for the specified interval
        await asyncio.sleep(interval_hours * 3600)


if __name__ == "__main__":
    # Run cleanup immediately and then exit
    asyncio.run(cleanup_expired_sessions())
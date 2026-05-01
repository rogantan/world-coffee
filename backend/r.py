from utils.storage_sync import storage_sync
import asyncio

if __name__ == "__main__":
  asyncio.run(storage_sync.start_synchronization())
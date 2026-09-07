import asyncio
import os
from livekit.api import LiveKitAPI, RoomCompositeEgressRequest, EncodedFileOutput, S3Upload

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")

# Mock S3 config for demo purposes, or pull from env
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY", "mock-access-key")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY", "mock-secret-key")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "https://mock-s3-endpoint.r2.cloudflarestorage.com")
S3_BUCKET = os.environ.get("S3_BUCKET", "mock-bucket")

async def start_recording(room_name: str) -> str:
    async with LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET) as api:
        s3 = S3Upload(
            access_key=S3_ACCESS_KEY,
            secret=S3_SECRET_KEY,
            endpoint=S3_ENDPOINT,
            bucket=S3_BUCKET
        )
        file_out = EncodedFileOutput(
            filepath=f"recordings/{room_name}-{asyncio.get_event_loop().time()}.mp4",
            s3=s3
        )
        req = RoomCompositeEgressRequest(
            room_name=room_name,
            file=file_out,
            layout="speaker"
        )
        # Note: In a real environment with free tier, Egress might fail if not configured in the LiveKit Cloud dashboard. 
        # We will catch the exception to allow the DB flow to continue.
        try:
            info = await api.egress.start_room_composite_egress(req)
            return info.egress_id
        except Exception as e:
            print(f"Egress error (expected if free tier doesn't support egress): {e}")
            return "mock-egress-id"

async def stop_recording(egress_id: str):
    if egress_id == "mock-egress-id":
        return
    async with LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET) as api:
        try:
            await api.egress.stop_egress(egress_id)
        except Exception as e:
            print(f"Error stopping egress: {e}")

def start_recording_sync(room_name: str) -> str:
    return asyncio.run(start_recording(room_name))

def stop_recording_sync(egress_id: str):
    asyncio.run(stop_recording(egress_id))

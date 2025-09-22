"""
Audio API endpoints for streaming Google Drive audio files.

Provides proxy endpoints to serve audio files from Google Drive,
bypassing CORS and iframe restrictions.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
import logging
import httpx

# Note: Authentication removed for streaming endpoint to allow HTML audio element access
from app.services.audio_service import audio_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/stream")
async def stream_audio(
    target_date: Optional[str] = Query(
        default=None, description="Specific date for audio file (YYYY-MM-DD format)"
    ),
):
    """
    Stream audio file directly from Google Drive through backend proxy.

    This endpoint acts as a proxy to serve Google Drive audio files directly
    to the frontend, bypassing CORS restrictions and iframe blocking issues.

    Args:
        target_date: Optional specific date. If not provided, returns today's audio.

    Returns:
        Streaming audio file response

    Raises:
        HTTPException: If audio file not found or streaming fails
    """
    try:
        # Parse date if provided
        parsed_date = None
        if target_date:
            try:
                parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
                )

        # Get audio file info from service
        result = await audio_service._get_audio_file_info(parsed_date)

        if not result:
            # Provide helpful error message
            date_str = (
                parsed_date.strftime("%Y-%m-%d")
                if parsed_date
                else datetime.now().strftime("%Y-%m-%d")
            )
            filename_base = f"{(parsed_date or datetime.now().date()).strftime('%Y%m%d')}-CompassAudio"
            raise HTTPException(
                status_code=404,
                detail=f"Audio file not found for date {date_str}. Looking for: {filename_base}.wav, {filename_base}.m4a, or {filename_base}.mp4",
            )

        # The audio service should already return the correct download URL
        file_url = result["url"]

        # Double-check that we have the right format
        if "uc?id=" not in file_url or "export=download" not in file_url:
            logger.warning(
                f"DEBUG: Unexpected URL format from audio service: {file_url}"
            )
            # Try to extract file ID and create proper download URL
            if "/d/" in file_url:
                file_id = file_url.split("/d/")[1].split("/")[0]
                file_url = f"https://drive.google.com/uc?id={file_id}&export=download"
                logger.info(f"DEBUG: Converted to download URL: {file_url}")
            else:
                raise HTTPException(
                    status_code=500, detail="Unable to generate download URL"
                )

        logger.info(f"Proxying audio stream from: {file_url}")

        # Stream the file from Google Drive
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                logger.info(f"DEBUG: Fetching audio from Google Drive: {file_url}")
                response = await client.get(file_url, follow_redirects=True)
                logger.info(
                    f"DEBUG: Google Drive response status: {response.status_code}"
                )
                logger.info(
                    f"DEBUG: Google Drive response headers: {dict(response.headers)}"
                )

                response.raise_for_status()

                # Check if we got actual audio content
                content_type_header = response.headers.get("content-type", "")
                content_length = response.headers.get("content-length", "unknown")
                logger.info(
                    f"DEBUG: Content-Type from Google Drive: {content_type_header}"
                )
                logger.info(
                    f"DEBUG: Content-Length from Google Drive: {content_length}"
                )

                # Determine content type based on filename
                filename = result["filename"]
                if filename.endswith(".wav"):
                    content_type = "audio/wav"
                elif filename.endswith(".m4a"):
                    content_type = "audio/mp4"
                elif filename.endswith(".mp4"):
                    content_type = "audio/mp4"
                else:
                    content_type = "audio/mpeg"  # fallback

                logger.info(f"DEBUG: Using content type: {content_type}")

                # Create streaming response
                def generate():
                    bytes_streamed = 0
                    for chunk in response.iter_bytes(chunk_size=8192):
                        bytes_streamed += len(chunk)
                        yield chunk
                    logger.info(f"DEBUG: Streamed {bytes_streamed} bytes total")

                return StreamingResponse(
                    generate(),
                    media_type=content_type,
                    headers={
                        "Accept-Ranges": "bytes",
                        "Content-Disposition": f'inline; filename="{filename}"',
                        "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
                        "Content-Length": content_length
                        if content_length != "unknown"
                        else None,
                    },
                )

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error fetching audio from Google Drive: {e}")
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to fetch audio from Google Drive: {e.response.status_code}",
                )
            except httpx.RequestError as e:
                logger.error(f"Request error fetching audio from Google Drive: {e}")
                raise HTTPException(
                    status_code=502, detail="Failed to connect to Google Drive"
                )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error streaming audio file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/info")
async def get_audio_info(
    target_date: Optional[str] = Query(
        default=None, description="Specific date for audio file (YYYY-MM-DD format)"
    ),
):
    """
    Get audio file information without streaming the file.

    Returns metadata about the audio file including the backend streaming URL.

    Args:
        target_date: Optional specific date. If not provided, returns today's audio.

    Returns:
        Audio file metadata with backend streaming URL
    """
    try:
        # Parse date if provided
        parsed_date = None
        if target_date:
            try:
                parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
                )

        # Get audio metadata from service
        audio_metadata = await audio_service.get_audio_metadata(parsed_date)

        if not audio_metadata:
            # Provide helpful error message
            date_str = (
                parsed_date.strftime("%Y-%m-%d")
                if parsed_date
                else datetime.now().strftime("%Y-%m-%d")
            )
            filename_base = f"{(parsed_date or datetime.now().date()).strftime('%Y%m%d')}-CompassAudio"
            raise HTTPException(
                status_code=404,
                detail=f"Audio file not found for date {date_str}. Looking for: {filename_base}.wav, {filename_base}.m4a, or {filename_base}.mp4",
            )

        # Replace the Google Drive URL with our backend streaming URL
        stream_url = "/v1/audio/stream"
        if target_date:
            stream_url += f"?target_date={target_date}"

        return {
            "url": stream_url,  # Backend streaming URL
            "title": audio_metadata["title"],
            "date": audio_metadata["date"],
            "filename": audio_metadata["filename"],
            "google_drive_url": audio_metadata[
                "url"
            ],  # Original Google Drive URL for reference
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audio info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

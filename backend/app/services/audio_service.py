"""
Audio service for Google Drive integration.

Handles fetching audio files from Google Drive and generating download links.
"""

from datetime import date, datetime
from typing import Optional
import logging
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.config import settings
from app.utils.date_utils import get_business_date

logger = logging.getLogger(__name__)


class AudioService:
    """Service for handling audio files from Google Drive."""

    def __init__(self):
        """Initialize Google Drive service."""
        self.drive_service = None
        self._initialize_drive_service()

    def _initialize_drive_service(self):
        """Initialize Google Drive API service."""
        try:
            # Check if folder ID is configured
            if not settings.GOOGLE_DRIVE_AUDIO_FOLDER_ID:
                error_msg = (
                    "GOOGLE_DRIVE_AUDIO_FOLDER_ID is required but not configured. \n"
                    "To find your folder ID:\n"
                    "1. Open Google Drive in your browser\n"
                    "2. Navigate to the folder containing your audio files\n"
                    "3. Look at the URL - it will be something like: \n"
                    "   https://drive.google.com/drive/folders/YOUR_FOLDER_ID\n"
                    "4. Copy the folder ID (the part after 'folders/')\n"
                    "5. Add it to your .env file as GOOGLE_DRIVE_AUDIO_FOLDER_ID"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            if not settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
                raise ValueError("Google Drive credentials not configured")

            credentials_dict = json.loads(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=["https://www.googleapis.com/auth/drive.readonly"],
            )

            self.drive_service = build("drive", "v3", credentials=credentials)

            # Test basic API access
            try:
                self.drive_service.about().get(fields="user").execute()
                logger.info("Google Drive service initialized successfully")
            except Exception as api_test_error:
                logger.warning(
                    f"API test failed but service may still work: {api_test_error}"
                )

        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {e}")
            self.drive_service = None
            raise

    async def get_audio_metadata(
        self, target_date: Optional[date] = None
    ) -> Optional[dict]:
        """
        Get metadata for audio file including URL and title.

        Args:
            target_date: The date to get audio for

        Returns:
            Dictionary with audio metadata or None if not found
        """
        result = await self._get_audio_file_info(target_date)

        if not result:
            return None

        # Format date for display
        display_date = target_date if target_date else datetime.now().date()

        return {
            "url": result["url"],
            "title": f"Compass Bulletin - {display_date.strftime('%B %d, %Y')}",
            "date": display_date.isoformat(),
            "filename": result["filename"],
        }

    async def _get_audio_file_info(
        self, target_date: Optional[date] = None
    ) -> Optional[dict]:
        """
        Internal method to get audio file info including URL and actual filename.

        Args:
            target_date: The date to get audio for

        Returns:
            Dictionary with url and filename, or None if not found
        """
        if not self.drive_service:
            logger.error("Google Drive service not initialized")
            return None

        # Use current date if not provided
        if target_date is None:
            target_date = datetime.now().date()

        # Convert to business date (follows same pattern as dashboard services)
        business_date = get_business_date(target_date)

        # Format filename base according to pattern: 20250709-CompassAudio
        filename_base = f"{business_date.strftime('%Y%m%d')}-CompassAudio"

        try:
            # Search for both .wav and .m4a files in Google Drive
            # Note: Google Drive uses 'audio/x-wav' and 'audio/x-m4a' MIME types
            query = (
                f"(name='{filename_base}.wav' or name='{filename_base}.m4a') and "
                f"(mimeType='audio/wav' or mimeType='audio/x-wav' or mimeType='audio/x-m4a' or mimeType='audio/mp4' or mimeType='audio/mpeg') and "
                f"trashed=false and "
                f"'{settings.GOOGLE_DRIVE_AUDIO_FOLDER_ID}' in parents"
            )

            # Verify folder access first
            try:
                self.drive_service.files().get(
                    fileId=settings.GOOGLE_DRIVE_AUDIO_FOLDER_ID, fields="id, name"
                ).execute()
            except HttpError as folder_error:
                if folder_error.resp.status == 404:
                    logger.error(
                        "Folder not found! Check if the folder ID is correct and the service account has access."
                    )
                elif folder_error.resp.status == 403:
                    logger.error(
                        "Permission denied! The service account doesn't have access to this folder."
                    )
                return None

            # Search for the audio file
            response = (
                self.drive_service.files()
                .list(
                    q=query,
                    fields="files(id, name, mimeType)",
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )

            files = response.get("files", [])

            if not files:
                logger.warning(
                    f"Audio file not found: {filename_base}.wav or {filename_base}.m4a"
                )
                return None

            # Use the first matching file
            file = files[0]
            file_id = file.get("id")
            actual_filename = file.get("name")

            logger.info(f"Found audio file: {actual_filename}")

            # Generate download URL for backend proxy
            audio_url = f"https://drive.google.com/uc?id={file_id}&export=download"

            return {"url": audio_url, "filename": actual_filename}

        except HttpError as e:
            logger.error(f"Google Drive API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving audio file: {e}")
            return None


# Singleton instance
audio_service = AudioService()

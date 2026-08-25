"""
Canva API Client
Core module for interacting with Canva Connect API
"""

import os
import json
import time
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("Required packages not installed. Run: pip install requests python-dotenv")
    raise

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('canva_client')


class CanvaClient:
    """Client for Canva Connect API"""

    BASE_URL = os.getenv('CANVA_API_BASE_URL', 'https://api.canva.com/rest')

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Canva client

        Args:
            access_token: OAuth access token (uses env var if not provided)
        """
        self.access_token = access_token or os.getenv('CANVA_ACCESS_TOKEN')
        self.client_id = os.getenv('CANVA_CLIENT_ID')
        self.client_secret = os.getenv('CANVA_CLIENT_SECRET')
        self.timeout = int(os.getenv('CANVA_API_TIMEOUT', '30'))
        self.rate_limit_delay = int(os.getenv('CANVA_RATE_LIMIT_DELAY', '100')) / 1000

        if not self.access_token:
            logger.warning("No access token configured. Run OAuth flow first.")

    @property
    def headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make API request

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON data
        """
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=self.timeout
            )

            # Rate limiting
            time.sleep(self.rate_limit_delay)

            response.raise_for_status()

            if response.content:
                return response.json()
            return {}

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Response: {response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            raise

    # ===========================================
    # USER ENDPOINTS
    # ===========================================

    def get_user_info(self) -> Dict[str, Any]:
        """Get authenticated user information"""
        return self._request('GET', '/v1/users/me')

    def get_user_profile(self) -> Dict[str, Any]:
        """Get user profile (display name)"""
        return self._request('GET', '/v1/users/me/profile')

    def get_user_capabilities(self) -> Dict[str, Any]:
        """Get user's API capabilities"""
        return self._request('GET', '/v1/users/me/capabilities')

    # ===========================================
    # DESIGN ENDPOINTS
    # ===========================================

    def list_designs(
        self,
        limit: int = 50,
        continuation: Optional[str] = None,
        ownership: Optional[str] = None,
        sort_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all designs

        Args:
            limit: Max number of results
            continuation: Pagination token
            ownership: Filter by ownership (owned, shared)
            sort_by: Sort field (created_at, modified_at, title)
        """
        params = {'limit': limit}
        if continuation:
            params['continuation'] = continuation
        if ownership:
            params['ownership'] = ownership
        if sort_by:
            params['sort_by'] = sort_by

        return self._request('GET', '/v1/designs', params=params)

    def get_design(self, design_id: str) -> Dict[str, Any]:
        """Get design metadata"""
        return self._request('GET', f'/v1/designs/{design_id}')

    def get_design_pages(self, design_id: str) -> Dict[str, Any]:
        """Get design pages with thumbnails"""
        return self._request('GET', f'/v1/designs/{design_id}/pages')

    def get_export_formats(self, design_id: str) -> Dict[str, Any]:
        """Get available export formats for a design"""
        return self._request('GET', f'/v1/designs/{design_id}/export-formats')

    def create_design(
        self,
        design_type: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new design

        Args:
            design_type: Preset type (e.g., 'instagram_post', 'presentation')
            width: Custom width (if not using preset)
            height: Custom height (if not using preset)
            title: Design title
        """
        data = {}
        if design_type:
            data['design_type'] = {'type': design_type}
        elif width and height:
            data['design_type'] = {
                'type': 'custom',
                'width': width,
                'height': height
            }
        if title:
            data['title'] = title

        return self._request('POST', '/v1/designs', data=data)

    # ===========================================
    # EXPORT ENDPOINTS
    # ===========================================

    def create_export(
        self,
        design_id: str,
        format_type: str,
        pages: Optional[List[int]] = None,
        quality: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create export job

        Args:
            design_id: Design to export
            format_type: Export format (pdf, png, jpg, pptx, mp4, gif)
            pages: Specific pages to export (1-indexed)
            quality: Export quality (standard, high)
        """
        data = {
            'design_id': design_id,
            'format': {'type': format_type}
        }
        if pages:
            data['pages'] = pages
        if quality:
            data['format']['quality'] = quality

        return self._request('POST', '/v1/exports', data=data)

    def get_export(self, export_id: str) -> Dict[str, Any]:
        """Get export job status and download URL"""
        return self._request('GET', f'/v1/exports/{export_id}')

    def wait_for_export(
        self,
        export_id: str,
        timeout: int = 300,
        poll_interval: int = 2
    ) -> Dict[str, Any]:
        """
        Wait for export to complete

        Args:
            export_id: Export job ID
            timeout: Max wait time in seconds
            poll_interval: Seconds between status checks
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.get_export(export_id)
            status = result.get('job', {}).get('status')

            if status == 'completed':
                return result
            elif status == 'failed':
                raise Exception(f"Export failed: {result}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Export timed out after {timeout} seconds")

    # ===========================================
    # FOLDER ENDPOINTS
    # ===========================================

    def create_folder(
        self,
        name: str,
        parent_folder_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new folder

        Args:
            name: Folder name
            parent_folder_id: Parent folder ID (use 'root' for Projects)
        """
        data = {'name': name}
        if parent_folder_id:
            data['parent_folder_id'] = parent_folder_id

        return self._request('POST', '/v1/folders', data=data)

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """Get folder details"""
        return self._request('GET', f'/v1/folders/{folder_id}')

    def update_folder(self, folder_id: str, name: str) -> Dict[str, Any]:
        """Rename a folder"""
        return self._request('PATCH', f'/v1/folders/{folder_id}', data={'name': name})

    def delete_folder(self, folder_id: str) -> Dict[str, Any]:
        """Delete a folder (moves to trash)"""
        return self._request('DELETE', f'/v1/folders/{folder_id}')

    def list_folder_items(
        self,
        folder_id: str,
        limit: int = 50,
        continuation: Optional[str] = None,
        item_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List items in a folder

        Args:
            folder_id: Folder ID ('root' for Projects, 'uploads' for Uploads)
            limit: Max results
            continuation: Pagination token
            item_type: Filter by type (design, folder, image)
        """
        params = {'limit': limit}
        if continuation:
            params['continuation'] = continuation
        if item_type:
            params['item_type'] = item_type

        return self._request('GET', f'/v1/folders/{folder_id}/items', params=params)

    def move_items(
        self,
        item_ids: List[str],
        target_folder_id: str
    ) -> Dict[str, Any]:
        """
        Move items to a folder

        Args:
            item_ids: List of item IDs to move
            target_folder_id: Destination folder ID
        """
        data = {
            'item_ids': item_ids,
            'to_folder_id': target_folder_id
        }
        return self._request('POST', '/v1/folders/move', data=data)

    # ===========================================
    # ASSET ENDPOINTS
    # ===========================================

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """Get asset metadata"""
        return self._request('GET', f'/v1/assets/{asset_id}')

    def update_asset(
        self,
        asset_id: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update asset name and/or tags"""
        data = {}
        if name:
            data['name'] = name
        if tags is not None:
            data['tags'] = tags
        return self._request('PATCH', f'/v1/assets/{asset_id}', data=data)

    def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """Delete an asset (moves to trash)"""
        return self._request('DELETE', f'/v1/assets/{asset_id}')

    def create_asset_upload(
        self,
        name: str,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Upload an asset from file

        Args:
            name: Asset name
            file_path: Path to file
        """
        # Get file info
        path = Path(file_path)
        content_type = self._get_content_type(path.suffix)

        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Create upload job
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': content_type,
            'Asset-Upload-Metadata': json.dumps({'name': name})
        }

        response = requests.post(
            f"{self.BASE_URL}/v1/asset-uploads",
            headers=headers,
            data=file_data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def get_asset_upload_status(self, job_id: str) -> Dict[str, Any]:
        """Check asset upload job status"""
        return self._request('GET', f'/v1/asset-uploads/{job_id}')

    def create_url_asset_upload(
        self,
        name: str,
        url: str
    ) -> Dict[str, Any]:
        """
        Upload an asset from URL

        Args:
            name: Asset name
            url: Source URL (max 100MB)
        """
        data = {'name': name, 'url': url}
        return self._request('POST', '/v1/url-asset-uploads', data=data)

    @staticmethod
    def _get_content_type(extension: str) -> str:
        """Get MIME type for file extension"""
        types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.webp': 'image/webp',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
        }
        return types.get(extension.lower(), 'application/octet-stream')


def get_client() -> CanvaClient:
    """Get configured Canva client instance"""
    return CanvaClient()


if __name__ == '__main__':
    # Test connection
    client = get_client()
    try:
        user = client.get_user_info()
        print(f"Connected as: {user}")
    except Exception as e:
        print(f"Connection failed: {e}")

import requests
import time
from typing import Dict, Any, Optional

class JulesAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._source_cache = {}

    def get_source_name(self, api_key: str, repo_name: str) -> Optional[str]:
        """Fetches the Jules Source Name for a given GitHub repo."""
        cache_key = f"{api_key}:{repo_name}"
        if cache_key in self._source_cache:
            return self._source_cache[cache_key]

        headers = {"x-goog-api-key": api_key}
        url = f"{self.base_url}/sources"

        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()

            for source in data.get("sources", []):
                gh_repo = source.get("githubRepo", {})
                full_name = f"{gh_repo.get('owner')}/{gh_repo.get('repo')}"
                if full_name.lower() == repo_name.lower():
                    self._source_cache[cache_key] = source['name']
                    return source['name']
            
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ API Error listing sources: {e}")
            return None

    def create_session(self, api_key: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Creates a new Jules session."""
        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/sessions"

        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            # Simple retry logic could be added here if needed, but handled by caller usually
            print(f"❌ Error creating session: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print(e.response.json())
                except:
                    pass
            return None

    def get_session_details(self, api_key: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Fetches session details from Jules API."""
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"
            
        headers = {"x-goog-api-key": api_key}
        url = f"{self.base_url}/{session_id}"
        
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching session {session_id}: {e}")
            return None

    def get_session_resource(self, api_key: str, session_id: str, resource: str) -> Optional[Dict[str, Any]]:
        """Fetches a specific resource (history, turns, etc) for a session."""
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"
            
        headers = {"x-goog-api-key": api_key}
        url = f"{self.base_url}/{session_id}/{resource}"
        
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None

    def send_input(self, api_key: str, session_id: str, text: str) -> Optional[Dict[str, Any]]:
        """Sends text input to a session."""
        if not session_id.startswith("sessions/"):
            session_id = f"sessions/{session_id}"

        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{session_id}:sendInput"
        
        payload = {"input": {"text": text}}
        
        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error sending input: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    print(e.response.json())
                except:
                    pass
            return None

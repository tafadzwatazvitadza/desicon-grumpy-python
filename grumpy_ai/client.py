import sys
import os
import traceback
import requests

class GrumpyClient:
    def __init__(self):
        self.api_key = None
        self.environment = "development"
        self.app_name = "unknown_app"
        self._original_excepthook = None
        self.ingest_url = "https://grumpy-backend-production.up.railway.app/api/v1/ingest"

    def init(self, api_key: str, app_name: str, environment: str = "production", ingest_url: str = None):
        self.api_key = api_key
        self.app_name = app_name
        self.environment = environment
        if ingest_url:
            self.ingest_url = ingest_url
        
        # Override the global exception hook
        self._original_excepthook = sys.excepthook
        sys.excepthook = self._grumpy_excepthook
        
        # Ping the backend to auto-resolve old errors on deployment/startup
        try:
            import requests
            headers = {"X-API-Key": self.api_key}
            requests.post(f"{self.host}/api/v1/ingest/ping", headers=headers, timeout=3)
        except Exception as e:
            # Silently fail so we don't break the host app if the network is down
            pass
            
        print(f"Grumpy.ai initialized for {self.app_name} ({self.environment}). We are watching you.")

    def _extract_code_context(self, tb):
        """Walks the stack trace to find the last file and extracts the surrounding lines."""
        try:
            # Extract the raw traceback
            extracted = traceback.extract_tb(tb)
            if not extracted:
                return "No traceback available."
            
            # Find the last frame that is actually in our project code
            last_frame = extracted[-1]
            filename = last_frame.filename
            lineno = last_frame.lineno
            
            if not os.path.exists(filename):
                return f"Could not locate {filename} on disk."
                
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Grab 5 lines before and 5 lines after the error
            start_idx = max(0, lineno - 6)
            end_idx = min(len(lines), lineno + 5)
            
            context = ""
            for i in range(start_idx, end_idx):
                prefix = ">> " if i == (lineno - 1) else "   "
                context += f"{prefix}{i + 1}: {lines[i]}"
                
            return context
        except Exception as e:
            return f"Failed to extract context: {str(e)}"

    def _grumpy_excepthook(self, exc_type, exc_value, exc_traceback):
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        context_str = self._extract_code_context(exc_traceback)
        
        payload = {
            "app_name": self.app_name,
            "error_type": exc_type.__name__,
            "error_message": str(exc_value),
            "stack_trace": tb_str,
            "code_context": context_str,
            "environment": self.environment
        }
        headers = {
            "X-API-Key": self.api_key
        }
        
        try:
            print(f"\n[Grumpy.ai] Catching {exc_type.__name__}... shipping to SRE engine.")
            resp = requests.post(self.ingest_url, json=payload, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "deduplicated":
                    print(f"[Grumpy.ai] Deduped (seen {data.get('count')} times).")
                else:
                    print(f"\n🔔 GRUMPY'S ANALYSIS:\n{data.get('analysis')}\n")
        except Exception as e:
            print(f"[Grumpy.ai] Failed to contact server: {e}")
            
        # Let it crash normally so we don't break the actual application
        if self._original_excepthook:
            self._original_excepthook(exc_type, exc_value, exc_traceback)

# Global singleton
grumpy = GrumpyClient()

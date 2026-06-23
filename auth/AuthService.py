class AuthService:
    def __init__(self, scanner, api):
        self.scanner = scanner
        self.api = api

    def authenticate(self):
        qr_data = self.scanner.scan()

        if not qr_data:
            return None
        
        result = self.api.verify_user(qr_data)

        if not result.get("valid"):
            return None
        
        return result["user"]
class AuthService:
    def __init__(self, scanner, api):
        self.scanner = scanner
        self.api = api

    def authenticate(self):
        print("Starting authentication process...")
        qr_data = self.scanner.scan()

        if not qr_data:
            return None
        
        result = self.api.verify_user(qr_data)

        if not result.get("valid"):
            return None
        
        print(f"User authenticated: {result['user']}")
        return result["user"]
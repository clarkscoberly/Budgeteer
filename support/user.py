class User:
    
    def __init__(self):
        self.user_id = None
        self.current_envelope = None
        self.current_item = None


    def log_out(self):
        self.user_id = None
        self.current_envelope = None
        self.current_item = None
        print("Successfully Logged Out")

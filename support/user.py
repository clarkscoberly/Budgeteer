class User:
    
    def __init__(self):
        self.user_id = None
        self.current_item = None
        self.current_envelope = None
        self.envelopes_df = None

    def log_out(self):
        self.user_id = None
        self.current_item = None
        self.current_envelope = None
        self.envelopes_df = None
        print("Successfully Logged Out")

user = User()
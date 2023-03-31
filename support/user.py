class User:
    
    def __init__(self):
        self.user_id = None
        self.current_item = None
        self.current_envelope = None
        self.envelopes_df = None
        self.envelope_current_budget = None

    def log_out(self):
        self.user_id = None
        self.current_item = None
        self.current_envelope = None
        self.envelopes_df = None
        self.envelope_current_budget = None
        print("Successfully Logged Out")

user = User()
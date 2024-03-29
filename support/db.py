import firebase_admin
from firebase_admin import credentials, db, firestore, auth

from support.user import user

import pandas as pd

cred = credentials.Certificate('C:\\Users\\cober\\Desktop\\Budgeteer\\support\\budgeteer-4c866-firebase-adminsdk-4zcz1-75e8230e72.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://budgeteer-4c866-default-rtdb.firebaseio.com'
})

db = firestore.client()

class Database:

    def __init__(self):
        self.user = user # A blank user that will carry the user's id for the duration of the application. IF THEY LOG OUT THE USER NEEDS TO GET WIPED.
        pass

    def create_user(self, username, password):
        # check if the username already exists
        user_ref = db.collection('users').where('username', '==', username).get()
        if user_ref:
            print('Username already exists')
            return None
        
        # create a new user
        new_user_ref = db.collection('users').document()
        new_user_ref.set({
            "username": username,
            "password": password
        })
        print('User created successfully')
        self.user.user_id = new_user_ref.id

        return new_user_ref.id

    def login_user(self, username, password):
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).where('password', '==', password).limit(1)
        results = query.get()
        
        for user_ref in results:
            print("User exists")
            # self.user.
            
            self.user.user_id = user_ref.id

            self.user.envelopes_df = self.get_envelopes_for_user()
            return user_ref.id
        
        return None


    def create_envelope(self, envelope_name, budget, frequency, note):
        # check if the user exists
        user_ref = db.collection('users').document(self.user.user_id)
        if not user_ref.get().exists:
            print('User does not exist')
            return
        
        # create a new envelope
        new_envelope_ref = user_ref.collection('envelopes').document()
        new_envelope_ref.set({
            "name": envelope_name,
            "budget": budget,
            "frequency": frequency,
            "note": note,
            "items": {},
            "created_at": firestore.SERVER_TIMESTAMP
        })
        print('Envelope created successfully')
        return new_envelope_ref.id

    def get_envelope_id_by_name(self, envelope_name):
        envelope_ref = db.collection('users').document(self.user.user_id).collection('envelopes').where('name', '==', envelope_name).stream()
        for doc in envelope_ref:
            return doc.id

    def add_item_to_envelope(self, envelope_name, item_name, cost, note):
        # check if the user and envelope exist
        envelope_id = self.get_envelope_id_by_name(envelope_name)
        
        envelope_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id)
        if not envelope_ref.get().exists:
            print('User or envelope does not exist')
            return
        
        # add the new item to the envelope
        item_ref = envelope_ref.collection('items').document()
        item_ref.set({
            "name": item_name,
            "cost": cost,
            "note": note,
            "date": firestore.SERVER_TIMESTAMP
        })
        print('Item added successfully')
        return item_ref.id


    def update_envelope_budget(self, envelope_name, new_budget):

        # check if the user and envelope exist
        envelope_id = self.get_envelope_id_by_name(envelope_name)

        envelope_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id)
        if not envelope_ref.get().exists:
            print('User or envelope does not exist')
            return
        
        # update the budget of the envelope
        envelope_ref.update({
            "budget": new_budget
        })
        print('Envelope budget updated successfully')


    def update_item_cost(self, envelope_name, item_id, new_cost):
        # check if the user, envelope and item exist
        envelope_id = self.get_envelope_id_by_name(envelope_name)

        item_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id).collection('items').document(item_id)
        if not item_ref.get().exists:
            print('User, envelope or item does not exist')
            return
        
        # update the cost of the item
        item_ref.update({
            "cost": new_cost
        })
        print('Item cost updated successfully')


    def delete_item(self, envelope_name, item_id):
        # check if the user, envelope and item exist
        envelope_id = self.get_envelope_id_by_name(envelope_name)

        item_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id).collection('items').document(item_id)
        if not item_ref.get().exists:
            print('User, envelope or item does not exist')
            return
        
        # delete the item
        item_ref.delete()
        print('Item deleted successfully')

    def delete_envelope(self, envelope_name):
        # check if the user and envelope exist
        envelope_id = self.get_envelope_id_by_name(envelope_name)


        envelope_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id)
        if not envelope_ref.get().exists:
            print('User or envelope does not exist')
            return
        
        # delete the envelope
        envelope_ref.delete()
        print('Envelope deleted successfully')

    def delete_user_profile(self):
        # check if the user exists
        user_ref = db.collection('users').document(self.user.user_id)
        if not user_ref.get().exists:
            print('User does not exist')
            return
        
        # delete all envelopes for the user
        envelopes = user_ref.collection('envelopes').get()
        for envelope in envelopes:
            envelope_name = envelope.to_dict()['name']
            self.delete_envelope(envelope_name)
        
        # delete the user
        user_ref.delete()
        print('User profile deleted successfully')


    def _get_envelope_data(self, envelope_id):
        # check if the user and envelope exist
        envelope_ref = db.collection('users').document(self.user.user_id).collection('envelopes').document(envelope_id)
        if not envelope_ref.get().exists:
            print('User or envelope does not exist')
            return
        
        # retrieve envelope data
        envelope_data = envelope_ref.get().to_dict()
        
        # retrieve items for the envelope
        items = envelope_ref.collection('items').get()
        item_data = []
        for item in items:
            item_data.append({
                "id": item.id,
                "name": item.get('name'),
                "date": item.get('date'),
                "cost": item.get('cost'),
                "note": item.get('note')
            })
        
        # add items data to envelope data
        envelope_data['items'] = item_data
        
        return envelope_data

    def get_envelopes_for_user(self):

        try:
            # check if the user exists
            user_ref = db.collection('users').document(self.user.user_id)
            if not user_ref.get().exists:
                print('User does not exist')
                return
            
            # get all envelopes for the user
            envelopes_ref = user_ref.collection('envelopes').get()
            envelopes_data = []
            for envelope in envelopes_ref:
                envelope_data = self._get_envelope_data(envelope.id)
                envelopes_data.append(envelope_data)

            envelopes_df = pd.DataFrame(envelopes_data)

        except Exception as e:
            print("There was an error", e)
            
        return envelopes_df
    
    def reload_db(self):
        user.envelopes_df = self.get_envelopes_for_user()

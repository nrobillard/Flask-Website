from asyncio.windows_events import NULL
import hashlib
from Money_Manager.Entities import User
import pandas as pd

class LoginVerification:

    def __init__(self, some_uname_entered: str, some_pass_entered:str) -> None:
        """Class that performs verification of user
        :param some_uname_entered: Username of user trying to login
        :some_pass_entered: Plaintext password that gets hashed and compared against the password hash of an instance of the User Class)
        :return: None
        """
        
        self.un_and_pws = pd.read_csv("userfile.csv")
        
        self.username_entered = some_uname_entered

        self.password_entered = some_pass_entered
        
        self.user_authentic = LoginVerification.authenticate_user()


    def authenicate_user(self) -> bool:
        """Method to authenticate user
        :return: boolean value
        """
        unames = self.un_and_pws['Usernames']
        username = unames.str.match(self.username_entered)
        if username[0] == None:
            return False
        else:
            auth_pass = self.un_and_pws[username][1]
            entered_hash = hashlib.sha256(self.password_entered.encode('utf-8')).hexdigest()

            if auth_pass == entered_hash:
                return True
            else:
                return False

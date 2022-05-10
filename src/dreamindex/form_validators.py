"""
form_validators.py
------------------
Defines custom validators for use in FlaskForms.
"""
import abc
from string import ascii_letters
from dreamindex import db
from wtforms.validators import ValidationError

@abc
class BaseValidator:
    @abc.abstractmethod
    def __init__(self, message=None):
        pass

    @abc.abstractmethod
    def __call__(self, form, field):
        pass

class UserNotExists(BaseValidator):
    def __init__(self, data_type, message=None):
        assert data_type in ('username', 'user_id'), f'UserNotExists only accepts "username" or "user_id" as possible data types. Got {data_type}.' 
        self.data_type = data_type
        if not message:
            self.message = 'User {data} already exists!'
        else:
            self.message = message
    
    def __call__(self, form, field):
        if not field.data: return
        data = field.data
        if (self.data_type == 'username' and db.user_exists(user_name=data)) or\
            (self.data_type == 'user_id' and db.user_exists(user_id=data)):
            raise ValidationError(self.message.format(data))

class UserExists(BaseValidator):
    def __init__(self, data_type, message=None):
        assert data_type in ('username', 'user_id'), f'UserExists only accepts "username" or "user_id" as possible data types. Got {data_type}.' 
        self.data_type = data_type
        if not message:
            self.message = 'User {data} does not exist!'
        else:
            self.message = message
    
    def __call__(self, form, field):
        if not field.data: return
        data = field.data
        if (self.data_type == 'username' and not db.user_exists(user_name=data)) and\
            (self.data_type == 'user_id' and not db.user_exists(user_id=data)):
            raise ValidationError(self.message.format(data))

class StrongPassword(BaseValidator):
    def __init__(self, message=None):
        if not message:
            self.message = 'Password is not strong enough!'
        else:
            self.message = message
    
    def __call__(self, form, field):
        password = field.data
        if not (any([l in ascii_letters for l in password]) and any([l in '12345667890' for l in password])) or\
            len(password) <= 6:
            raise ValidationError(self.message)
from models.fields import Field, FloatField, IntField, StringField, JsonField, ForeignKey
from models.database import Database, db_init
from models.models import Model
import sys
import inspect

def change_db_settings(db_type: str, infos: dict):
    Model.database = db_init(db_type=db_type, infos=infos)

def init_models(mod):
    for name, obj in inspect.getmembers(sys.modules[mod]):
        if type(obj) == type:
            if issubclass(obj, models.Model) and obj != models.Model:
                print(f'Class {name} :')
                for key, field in obj.__dict__.items():
                    if isinstance(field, Field):
                        print(f'    - {key} -> {field.field_type}')




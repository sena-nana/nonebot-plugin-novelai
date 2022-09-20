from piccolo.table import Table,create_db_tables
from piccolo.columns import Text,Varchar,Boolean
from piccolo.engine.sqlite import SQLiteEngine
import asyncio
from pathlib import Path
path=Path.cwd()/'data'/'model'
DB= SQLiteEngine(path=path/'githubpush.sqlite')
class Repolink(Table,db=DB):
    isgroup = Boolean(default=True)
    userid=Varchar(required=True,length=10)
    repo=Text(required=True)
    owner=Text(required=True)
    iscommitspush=Boolean(default=True)
    isreleasepush=Boolean(default=True)
    isissuepush=Boolean(default=True)
    atall=Boolean(default=False)
    
class Ownersub(Table,db=DB):
    isgroup=Boolean(default=True)
    userid=Varchar(required=True,length=10)
    owner=Text(required=True)
    isstarpush=Boolean(default=False)
    atall=Boolean(default=False)
async def init():
    await create_db_tables(Repolink,Ownersub,if_not_exists=True)
asyncio.run(init())
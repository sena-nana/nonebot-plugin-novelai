from ...model import Repolink
from githubkit import UnauthAuthStrategy,Response,GitHub
async def getcommit():
    async with GitHub(UnauthAuthStrategy()) as github:
        commit=await github.rest.repos.async_list_commits(owner='sena-nana',repo='sena-nana.github.io')
        repo=commit.parsed_data
        commitstr=repo[0].commit.message
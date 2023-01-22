import mistune

async def markdown(text):
    ast=mistune.markdown(text,renderer="ast")
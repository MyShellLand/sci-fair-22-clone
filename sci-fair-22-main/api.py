import requests, json, asyncio

# callig 1063068

class Foldapi:
    def __init__(self):
        pass
    async def new_request(self, uri, param=None):
        response = await asyncio.get_event_loop().run_in_executor(None, requests.get, uri, param)
        return response.json()

    async def team_info(self, id):
        if not id.isdigit():
            return await self.find_team_id(id, returnall=True)
        return await self.new_request(f'https://api2.foldingathome.org/team/{id}')
    async def find_team_id(self, name, returnall=False):
        rsp =  await self.new_request("https://api.foldingathome.org/team/find", {"name": name})
        if returnall:
            return rsp
        else:
            return rsp["id"]
    async def get_members(self, id):
        if not id.isdigit():
            id =  await self.find_team_id(id)
        return await self.new_request(f'https://api.foldingathome.org/team/{id}/members')
    async def user_info(self, id):
        return await self.new_request(f'https://api.foldingathome.org/uid/{id}')

    # this is the stupid ones

    async def miners_and_units(self,id):
        data = await self.new_request(f'https://api.foldingathome.org/team/{id}/members')
        name_n_units = []
        for row in data:
            name_n_units.append(row[0])
        #probably wont need this later
        return "this doesn't matter"
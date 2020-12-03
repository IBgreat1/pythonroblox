import urllib.request
import json
class group_post:
    def __init__(self , jsonformat):
        self.poster_id = jsonformat['poster']['userId']
        self.poster_name = jsonformat['poster']['username']
        self.body = jsonformat['body']
        self.post_displayName  = jsonformat['poster']['displayName']
        self.created = jsonformat['created']
        self.updated = jsonformat['updated']
def group_datas(url , id , search=False):
    try:
        if search == True:
            open = urllib.request.urlopen(url=url)
            open = json.load(open)['data'][0]['id']
            open =  urllib.request.urlopen(url='https://groups.roblox.com/v1/groups/'+str(open))
            open = json.load(open)
        else:
            open = urllib.request.urlopen(url=url)
            open = json.load(open)
        name = open['name']
        description = open['description']
        owner_name = open['owner']['username']
        owner_displayName = open['owner']['displayName']
        owner_id = open['owner']['userId']
        shout = open['shout']
        member_count =  open['memberCount']
        public_entry_allowed = open['publicEntryAllowed']
        return name , description , owner_name , owner_displayName , owner_id , shout , member_count , public_entry_allowed
    except Exception as e:
        raise BaseException('HTTP Error 404 - Invalid Group ID/No Results')
def get_user_data(url , url2 , id):
    try:
        open = urllib.request.urlopen(url=url)
        open = json.load(open)
        banned = open['isBanned']
        name = open['name']
        displayName = open['displayName']
        created_date = open['created']
        description = open['description']
        status = json.load(urllib.request.urlopen(url + '/status'))['status']
        groups_data = json.load(urllib.request.urlopen(url2 + '/groups/roles'))
        number_groups = len(groups_data['data'])
        #badges = json.load(urllib.request.urlopen(f'https://badges.roblox.com/v1/users/{id}/badges?limit=100&sortOrder=Asc'))
        friends_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/friends/count'))['count']
        followers_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followers/count'))['count']
        following_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followings/count'))['count']
        return [banned, name ,created_date, displayName,description,status,number_groups,friends_count,followers_count,following_count]
    except Exception as e:
        print(e)
        raise BaseException('HTTP Error 404: Not Found - No User with Such Name / ID Found.')
class group_data:
    def __init__(self,sequence,id):
        base2 = 'https://groups.roblox.com/v2/users/'
        url2 = base2 + str(id)
        groups_data = json.load(urllib.request.urlopen(url2 + '/groups/roles'))
        group_raw = groups_data['data'][sequence]['group']
        self.group_name = group_raw['name']
        self.group_id = group_raw['id']
        self.group_member_count = group_raw['memberCount']
        roles = groups_data['data'][sequence]['role']
        self.role_name = roles['name']
        self.role_id = roles['id']
        self.role_rank = roles['rank']

class User:
    class search_id:
        def __init__(self,id:int=1):
            self.id = id
            base = 'https://users.roblox.com/v1/users/'
            base2 = 'https://groups.roblox.com/v2/users/'
            url = base+str(id)
            self.url2 = base2+str(id)
            tab =  get_user_data(url , self.url2 , self.id)
            self.banned = tab[0]
            self.name = tab[1]
            self.created_date = tab[2]
            self.displayName = tab[3]
            self.description = tab[4]
            self.status = tab[5]
            self.number_groups = tab[6]
            self.friends_count = tab[7]
            self.followers_count=tab[8]
            self.following_count=tab[9]
            if self.name != None:
                self.avatar_url = 'https://web.roblox.com/Thumbs/Avatar.ashx?x=100&y=100&Format=Png&userid='+str(self.id)
            else:
                self.avatar_url = None
        def get_groups_data(self,sequence:int):
            if not sequence > self.number_groups-1:
                return  group_data(sequence,self.id)
            else:
                raise IndexError('Sequence Is Higher than Number of Groups of the Player is In or Lower than 0')
        def get_all_groups_data(self):
            base2 = 'https://groups.roblox.com/v2/users/'
            url2 = base2 + str(self.id)
            groups_data = json.load(urllib.request.urlopen(url2 + '/groups/roles'))
            return groups_data['data']
    class search_name:
        def __init__(self,name):
            try:
                base = 'https://users.roblox.com/v1/users/search?keyword='
                url = base+name+'&limit=100'
                opened = urllib.request.urlopen(url=url)
                opened = json.load(opened)
                self.opened = opened
                best_result = opened['data'][0]
                self.results = len(opened['data'])
                self.name = best_result['name']
                self.id = best_result['id']
                self.displayName = best_result['displayName']
                base = 'https://users.roblox.com/v1/users/'
                base2 = 'https://groups.roblox.com/v2/users/'
                url = base + str(self.id)
                self.url2 = base2 + str(self.id)
                bestopen = urllib.request.urlopen(url=url)
                bestopen = json.load(bestopen)
                tab = get_user_data(url, self.url2, self.id)
                self.banned = tab[0]
                self.name = tab[1]
                self.created_date = tab[2]
                self.displayName = tab[3]
                self.description = tab[4]
                self.status = tab[5]
                self.number_groups = tab[6]
                self.friends_count = tab[7]
                self.followers_count = tab[8]
                self.following_count = tab[9]
                if self.name != None:
                    self.avatar_url = 'https://web.roblox.com/Thumbs/Avatar.ashx?x=100&y=100&Format=Png&userid=' + str(self.id)
                else:
                    self.avatar_url = None
            except:
                raise BaseException('HTTP Error 404: Not Found - Not Results Found')
        def get_groups_data(self, sequence: int):
            if not sequence > self.number_groups - 1:
                return group_data(sequence, self.id)
            else:
                raise IndexError('Sequence Is Higher than Number of Groups of the Player is In or Lower than 0')
        def get_total_search_results(self):
            return self.opened['data']
        def get_all_groups_data(self):
            base2 = 'https://groups.roblox.com/v2/users/'
            url2 = base2 + str(self.id)
            groups_data = json.load(urllib.request.urlopen(url2 + '/groups/roles'))
            return groups_data['data']
class Groups:
    class search_id:
        def __init__(self , id:int):
            base  = 'https://groups.roblox.com/v1/groups/'
            url = base + str(id)
            self.name , self.description , self.owner_name , self.owner_displayName , self.owner_id  ,self.shout_details , self.member_count , self.public_entry_allowed=  group_datas(url , id=id)
        def get_shout_details(self):
            if self.shout_details != None:
                return  group_post(jsonformat=self.shout_details)
    class search_name:
        def __init__(self , id:str):
            base  = 'https://groups.roblox.com/v1/groups/search?keyword='
            url = base + str(id) + '&limit=100'
            self.url = url
            self.name , self.description , self.owner_name , self.owner_displayName , self.owner_id  ,self.shout_details , self.member_count , self.public_entry_allowed=  group_datas(url , id=id,search=True)
        def get_shout_details(self):
            if self.shout_details != None:
                return  group_post(jsonformat=self.shout_details)
        def get_total_results(self):
            try:
                data = json.load(urllib.request.urlopen(self.url))
                return data
            except:
                raise BaseException('HTTP Error 404 - Invalid Group ID/No Results')




import urllib.request
import json
import  requests
import re
from urllib import parse
class Error(Exception):
    pass
class HTTP404Error(Error):
    pass

class primary_group:
    def __init__(self,id):
        url = f"https://groups.roblox.com/v1/users/{id}/groups/primary/role"
        data = json.load(urllib.request.urlopen(url))
        open = data['group']
        self.name = open['name']
        self.description = open['description']
        self.owner_name = open['owner']['username']
        self.owner_displayName = open['owner']['displayName']
        self.owner_id = open['owner']['userId']
        self.shout_details = group_post(open['shout'])
        self.member_count = open['memberCount']
        self.public_entry_allowed = open['publicEntryAllowed']
        self.post = group_post(open['shout'])
        roles = data['role']
        self.role_name = roles['name']
        self.role_id = roles['id']
        self.role_rank = roles['rank']
class group_post:
    def __init__(self , jsonformat):
        self.poster_id = jsonformat['poster']['userId']
        self.poster_name = jsonformat['poster']['username']
        self.body = jsonformat['body']
        self.post_displayName  = jsonformat['poster']['displayName']
        self.created = jsonformat['created']
        self.updated = jsonformat['updated']


class ClassGroup:
    def __init__(self,url , id , search=False):
        try:
            if search == True:
                open = urllib.request.urlopen(url=url)
                open = json.load(open)['data'][0]['id']
                self.id_group = open
                open = urllib.request.urlopen(url='https://groups.roblox.com/v1/groups/' + str(open))
                open = json.load(open)
            else:
                self.id_group = id
                open = urllib.request.urlopen(url=url)
                open = json.load(open)

            self.name = open['name']
            self.description = open['description']
            self.owner_name = open['owner']['username']
            self.owner_displayName = open['owner']['displayName']
            self.owner_id = open['owner']['userId']
            self.shout_details = open['shout']
            self.member_count = open['memberCount']
            self.public_entry_allowed = open['publicEntryAllowed']

        except Exception as e:
            raise HTTP404Error('HTTP Error 404 - Invalid Group ID/No Results')
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
        friends_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/friends/count'))['count']
        followers_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followers/count'))['count']
        following_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followings/count'))['count']
    except Exception as e:
        raise HTTP404Error('HTTP Error 404: Not Found - No User with Such Name / ID Found.')
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
class Player:
    def __init__(self,url,url2,id):
        try:
            open = urllib.request.urlopen(url=url)
            open = json.load(open)
            self.banned = open['isBanned']
            self.name = open['name']
            self.displayName = open['displayName']
            self.created_date = open['created']
            self.description = open['description']
            self.status = json.load(urllib.request.urlopen(url + '/status'))['status']
            self.groups_data = json.load(urllib.request.urlopen(url2 + '/groups/roles'))
            self.number_groups = len(self.groups_data['data'])
            self.friends_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/friends/count'))['count']
            self.followers_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followers/count'))['count']
            self.following_count = json.load(urllib.request.urlopen(f'https://friends.roblox.com/v1/users/{id}/followings/count'))['count']
            rap_rul = f'https://data.rbxcity.com/user-inventories/fetch/{id}/'
            print(rap_rul)
            rap_data = requests.get(rap_rul)
            self.RAP = 0
            #print(rap_data.text)
            for i in rap_data.json()['data']['Inventory']:
                if i['recentAveragePrice'] != None:
                    self.RAP += i['recentAveragePrice']
        except:
            raise HTTP404Error('HTTP Error 404: Not Found - No User with Such Name / ID Found.')
class User:
    class search_id(Player):
        def __init__(self,id:int=1):
            self.id = id
            base = 'https://users.roblox.com/v1/users/'
            base2 = 'https://groups.roblox.com/v2/users/'
            url = base+str(id)
            self.url2 = base2+str(id)
            super().__init__(url , self.url2 , self.id)
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
        def roblox_badges(self):
            try:
                badge_url = f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges"
                badges = json.load(urllib.request.urlopen(badge_url))
                return badges
            except:
                return None
        def get_username_history(self):
            try:
                history_url = f'https://users.roblox.com/v1/users/{self.id}/username-history'
                history = json.load(urllib.request.urlopen(history_url))
                return history['data']
            except:
                return None
        def get_primary_group(self):
            try:
                primary_url  = f'https://groups.roblox.com/v1/users/{self.id}/groups/primary/role'
                primary = json.load(urllib.request.urlopen(primary_url))
                return primary_group(self.id)
            except Exception as e:
                return None
    class search_name(Player):
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
                super().__init__(url, self.url2, self.id)
                if self.name != None:
                    self.avatar_url = 'https://web.roblox.com/Thumbs/Avatar.ashx?x=100&y=100&Format=Png&userid=' + str(self.id)
                else:
                    self.avatar_url = None
            except:
                raise HTTP404Error('HTTP Error 404: Not Found - Not Results Found')
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
        def roblox_badges(self):
            badge_url = f"https://accountinformation.roblox.com/v1/users/{self.id}/roblox-badges"
            badges = json.load(urllib.request.urlopen(badge_url))
            return badges
        def get_username_history(self):
            try:
                history_url = f'https://users.roblox.com/v1/users/{self.id}/username-history'
                history = json.load(urllib.request.urlopen(history_url))
                return history['data']
            except:
                return None
        def get_primary_group(self):
            try:
                primary_url  = f'https://groups.roblox.com/v1/users/{self.id}/groups/primary/role'
                primary = json.load(urllib.request.urlopen(primary_url))
                return primary_group(self.id)
            except Exception as e:
                return None

class Groups:
    class search_id(ClassGroup):
        def __init__(self , id:int):
            base  = 'https://groups.roblox.com/v1/groups/'
            url = base + str(id)
            self.id = id
            super().__init__(url , id=id)
        def get_shout_details(self):
            if self.shout_details != None:
                return  group_post(jsonformat=self.shout_details)
    class search_name(ClassGroup):
        def __init__(self , id:str):
            base  = 'https://groups.roblox.com/v1/groups/search?keyword='
            url = base + str(id) + '&limit=100'
            super().__init__(url , id=id,search=True)

        def get_shout_details(self):
            if self.shout_details != None:
                return  group_post(jsonformat=self.shout_details)
        def get_total_results(self):
            try:
                data = json.load(urllib.request.urlopen(self.url))
                return data
            except:
                raise HTTP404Error('HTTP Error 404 - Invalid Group ID/No Results')
class _DummyMarketPlace:
 def __init__(self,id):
     url  = 'https://api.roblox.com/marketplace/productinfo?assetId='
     url += id
     try:
         opened = json.load(urllib.request.urlopen(url))
         self.asset_type_id = opened['AssetTypeId']
         if self.asset_type_id != 9 :
             self.product_type = opened['ProductType']
             self.asset_id = opened['AssetId']
             self.product_id = opened['ProductId']
             self.name = opened['Name']
             self.creator_name  = opened['Creator']['Name']
             self.creator_id = opened['Creator']['Id']
             self.creator_type = opened['Creator']['CreatorType']
             self.creator_target_id = opened['Creator']['CreatorTargetId']
             self.description  = opened['Description']
             if int(opened['IconImageAssetId']) == 0:
                 try:
                     ok = requests.get(url=f'https://www.roblox.com/catalog/{self.asset_id}/', headers={
                         "User-Agent": "Mozilla/5.0 (Windows NT6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"})

                     a = re.search('<span class="thumbnail-span" data-3d-url="(.*?)</span', ok.text)
                     b = re.search("<img  class='' src='(.*?)'/>", a.group(1))
                     self.icon_image_url  = b.group(1)
                 except:
                     self.icon_image_url = None
             else:
                 try:
                     ok = requests.get(url=f'https://www.roblox.com/library/{opened["IconImageAssetId"]}/', headers={
                         "User-Agent": "Mozilla/5.0 (Windows NT6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"})

                     a = re.search('<span class="thumbnail-span"(.*?)</span', ok.text)
                     b = re.search("<img  class='' src='(.*?)'/>", a.group(1))
                     self.icon_image_url = b.group(1)
                 except Exception as e:
                     self.icon_image_url = None

             self.created_date = opened['Created']
             self.updated_date = opened['Updated']
             self.price_in_robux = opened['PriceInRobux']
             self.sales = opened['Sales']
             self.is_public = opened['IsPublicDomain']
             self.is_limited = opened['IsLimited']
             self.is_limited_unique = opened['IsLimitedUnique']
             self.remaining = opened['Remaining']
             self.minimum_membership_level = opened['MinimumMembershipLevel']
             self.content_rating_type_id = opened['ContentRatingTypeId']
             if self.is_limited == True:
                limited_data = json.load(urllib.request.urlopen(f'https://economy.roblox.com/v1/assets/{self.asset_id}/resale-data'))
                self.assetStock = limited_data['assetStock']
                self.RAP = limited_data['recentAveragePrice']
                self.originalPrice = limited_data['originalPrice']
                self.numberRemaining= limited_data['numberRemaining']
         else:
             raise HTTP404Error("Invalid Asset ID")
     except:
         raise HTTP404Error("Invalid Asset ID/No Search Results")
class _Game:
    def __init__(self,id:int):
        url= 'https://games.roblox.com/v1/games?universeIds='
        url += str(id)
        opened = json.load(urllib.request.urlopen(url))
        data = opened['data'][0]
        self.place_id = data['rootPlaceId']
        self.name= data['name']
        self.description = data['description']
        creator = data['creator']
        self.creator_name = creator['name']
        self.creator_type = creator['type']
        self.creator_id = creator['id']
        self.price = data['price']
        self.allowedGearGenres = data['allowedGearGenres']
        self.playing = data['playing']
        self.visits = data['visits']
        self.created = data['created']
        self.updated = data['updated']
        self.studioAccessToApisAllowed = data['studioAccessToApisAllowed']
        self.createVipServersAllowed = data['createVipServersAllowed']
        self.universeAvatarType = data['universeAvatarType']
        self.genre = data['genre']
        self.favorites =  json.load(urllib.request.urlopen(f'https://games.roblox.com/v1/games/{id}/favorites/count'))
        votes = json.load(urllib.request.urlopen(f'https://games.roblox.com/v1/games/votes?universeIds={id}'))['data'][0]
        self.likes =votes['upVotes']
        self.dislikes = votes['downVotes']

class _Catalog:
    pass
class MarketPlace:
    class Game:
        class search_id(_Game):
            def __init__(self,id:int):
                try:
                    url = 'https://www.roblox.com/games/'
                    url += str(id)
                    opened = requests.get(url,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'})
                    self.universe_id = re.search(f'<div id=game-detail-meta-data data-universe-id=(.*?) data-place-id={id}',opened.text)
                    super().__init__(self.universe_id.group(1))
                except:
                    raise HTTP404Error("Invalid Place ID")
        class search_name(_Game):
            def __init__(self,query:str):
                try:
                    url = 'https://www.roblox.com/games/list-json?&Keyword='
                    url += query
                    opened=json.load(urllib.request.urlopen(url))
                    super().__init__(opened[0]['UniverseID'])
                except:
                    raise HTTP404Error("No Results.")
    class Catalog:
        class search_id(_DummyMarketPlace):
            def __init__(self, id: int):
                super().__init__(str(id))
                pass

        class search_name(_DummyMarketPlace):
            def __init__(self, query: str):
                self.__openedgame = None
                self.__openedcatalog = None
                url = 'https://catalog.roblox.com/v1/search/items/details?Keyword='
                url += parse.quote(query) + "&Category=1"
                a = json.load(urllib.request.urlopen(url))
                self.__opened = a
                super().__init__(str(a['data'][0]['id']))






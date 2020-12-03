# pythonroblox
A Python Module for Roblox API. Easy Useable User and Group Classes.

#User - Class
**Intializing**
```py
import pythonroblox
user = pythonroblox.User()
```
**Searching Username**
```py
import pythonroblox
user = pythonroblox.User()
user.search_name("Roblox")
```
**Searching User ID**
```py
import pythonroblox
user = pythonroblox.User()
user.search_name(1)
```

**Searching user ID and Name returns the Given Below list of Attributes:**
```
banned
name
created_date
displayName
description
status
number_groups
friends_count
followers_count
following_count
avatar_url
```
**And Functions :**
```
get_groups_data()
get_all_groups_data
```

import pickle, os, random, string

class User():
    def __init__(self):
        self.data_dir="./auth/"
    def _randomstr(self, n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
    def mkauth(self, guild_id, member_id):
        temp={}
        temp.update(id=self._randomstr(10))
        temp.update(gid=guild_id)
        temp.update(mid=member_id)
        pickle.dump(temp, open(self.data_dir+temp["id"]+".queue","wb"))
        return temp["id"]
    def readauth(self, id):
        temp=pickle.load(open(self.data_dir+str(id)+".queue","rb"))
        try:
            temp.update(rid=pickle.load(open(self.data_dir+"role","rb"))[temp["gid"]])
            return temp
        except:
            return False
    def delauth(self, id):
        os.remove(self.data_dir+str(id)+".queue")
    def setrole(self, guild_id, role_id):
        if os.path.exists(self.data_dir+"role"):
            temp=pickle.load(open(self.data_dir+"role","rb"))
        else:
            temp={}
        temp[guild_id]=role_id
        pickle.dump(temp, open(self.data_dir+"role","wb"))
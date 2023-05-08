import json, hashlib, fnmatch

class NonExistentUserError(Exception): pass
class WrongPasswordError(Exception): pass
class UnknownPermissionError(Exception): pass

def parse_perm_script(script: str, data: dict):
    args = script.split(' ')

    if args[0].startswith('@'):
        args[0] = data[args[0][1:]]
    
    if args[2].startswith('@'):
        args[2] = data[args[2][1:]]
    
    match args[1]:
        case 'eq':
            return args[0] == args[2]
        case 'ne':
            return args[0] != args[2]
        case 'lt':
            return args[0] < args[2]
        case 'gt':
            return args[0] > args[2]
        case 'le':
            return args[0] <= args[2]
        case 'ge':
            return args[0] >= args[2]

class LoginManager:
    def __init__(self):
        with open('storage/users/_usr.json', 'r') as f:
            cfg = json.loads(f.read())
        
        self.users = cfg['users']
        self.perm_groups = cfg['perm_groups']

        self.user = None
    
    def login(self, user, password):
        if not user in self.users:
            raise NonExistentUserError(f'User "{user}" does not exist.')
        
        if hashlib.sha256(password.encode('utf-8')).hexdigest() != self.users[user]['password']:
            raise WrongPasswordError(f'Wrong password for "{user}".')
        
        self.user = user
        return user, self.users[user]['folder']
    
    def logout(self):
        self.user = None
    
    def has_perm(self, permission, data=None):
        for group in self.users[self.user]['perm_groups']:
            match permission:
                case 'FSREAD':
                    if fnmatch.fnmatch(data, self.perm_groups[group][permission]):
                        return True
                    
                case 'FSWRITE':
                    if fnmatch.fnmatch(data, self.perm_groups[group][permission]):
                        return True
                    
                case 'MANAGEACCOUNTS':
                    if self.perm_groups[group][permission]:
                        return True
                 
                case 'MANAGEPERMS':
                    if self.perm_groups[group][permission].startswith('$') and parse_perm_script(self.perm_groups[group][permission][1:], {'user': data}):
                        return True
                    
        return False
    
if __name__ == '__main__':
    lmgr = LoginManager()
    try:
        lmgr.login('root', 'root')
    except WrongPasswordError as e:
        print(e)
    lmgr.login('root', 'toor')
    print(lmgr.has_perm('MANAGEPERMS', 'root'))
    print(lmgr.has_perm('MANAGEPERMS', 'toor'))
    print(lmgr.has_perm('FSREAD', '~'))
    print(lmgr.has_perm('MANAGEACCOUNTS'))

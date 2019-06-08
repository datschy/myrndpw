import hashlib, random, string, sys, urllib.request


PWND_API = 'https://api.pwnedpasswords.com/range/'
DEF_LENGTH = 12
MIN_LENGTH = 10


def generate_pw(pwlength):
    charset = string.printable[0:84]
    charlist = [random.choice(charset) for _ in range(0, pwlength)]
    pw = ''.join(charlist)

    return pw

def check_pwnd(pw):
    hash_first_five, hash_rest = get_splitted_hexhash(pw, 5)
    pwnd_list = get_pwnd_list(hash_first_five)

    isPwnd = hash_rest in pwnd_list

    return isPwnd 

def get_pwnd_list(short_hash):
    url = PWND_API + short_hash
    response = urllib.request.urlopen(url)

    raw_list = response.read().decode().splitlines()
    hash_list = [x.split(':')[0].lower() for x in raw_list]

    return hash_list

def get_splitted_hexhash(pw, first_n):
    return split_hexhash(get_hexhash(pw), first_n)

def get_hexhash(pw):
    pw_hash = hashlib.sha1(pw.encode())

    return pw_hash.hexdigest()

def split_hexhash(whole_hash, first_n):
    return whole_hash[0:first_n], whole_hash[first_n:]


if __name__ == '__main__':

    wanted_pw_length = int(sys.argv[1]) if len(sys.argv) > 1 else DEF_LENGTH
    pw_length = wanted_pw_length if (
        wanted_pw_length >= MIN_LENGTH) else MIN_LENGTH

    password = ''
    pwnd = True
    while pwnd:
        password = generate_pw(pw_length)
        pwnd = check_pwnd(password)

    print(password)
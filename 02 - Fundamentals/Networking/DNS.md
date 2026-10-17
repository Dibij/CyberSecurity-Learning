---
title: "DNS (Domain Name System)"
type: concept
category: networking
status: in-progress
tags:
  - networking
  - dns
  - fundamentals
aliases:
  - DNS
---

# DNS (Domain Name System)

## 1. What is DNS?

DNS, or Domain Name System, is a distributed system made up of rules (transfer protocols) and IPs (IPv4 and IPv6).

DNS is used to translate domain names, such as [www.google.com](https://www.google.com) or [www.yahoo.com](https://www.yahoo.com), into IP addresses.

---

## 2. How Does the Translation Work?

1. When you look up a domain name in your browser, let's say [www.google.com](https://www.google.com), the browser checks its cache to see if it already knows the domain.

2. If it does, it points you to the numerical IP address of the domain. If not, the OS picks up the request for `www.google.com` and checks its cache.
   
   - Both the OS and the browser check their caches and store results so the lookup does not happen repeatedly.
   - In my preliminary understanding, this is to make sure the Top-Level Domains are not overrun with requests for commonly visited sites.

3. If the OS does not have that domain cached, the request gets passed to a **Recursive Resolver**. The Recursive Resolver then moves this request to a **Root-Level Nameserver**.
   
   - It is usually hidden in the URL of the domain. For example, `www.google.com` leads to a server, but browsers ignore that there is a `.` in `www.google.com.` at the end. That is the Root-Level Namespace.

4. The Root-Level Nameserver then passes the request from the device to a Top-Level Domain (TLD), like `.com` or `.org`.

5. The TLD then hands over the request to the **Authoritative Nameserver**, which passes along the numerical IP address associated with the domain.

6. As the IP address comes back to the device, it is then stored in almost every layer of the network path: browser, OS, Resolver DNS, and also the local network router.

---

## 3. Where Could DNS Translation Fail?

At this point, I honestly don't know where exactly DNS translation could fail.

I know it could fail if:

- There is a mismatch in the cache between the OS and browser.
- The DNS server is down.
- There is interference or overload in the TLD or Authoritative Nameservers.

To investigate DNS failures 
we first try this: 
```bash
dig example.com
; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12233
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		204	IN	A	104.20.23.154
example.com.		204	IN	A	172.66.147.243

;; Query time: 77 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Oct 17 08:12:57 +0545 2026
;; MSG SIZE  rcvd: 72

```
I don't understand anything, lets investigate:
- So, the ip(v4) of `example.com` seems to be `104.20.23.154` and `172.66.147.243`.
- `dig` also shows the success/failure of the request
- 204 in the Answer Section is the *Time-To-Live or TTL* measured in seconds.
- It used [[UDP]] protocol.
- It used port 53 - the standard DNS port.
- 127.0.0.53 is the [[Loopback Address]].
> `dig` always starts by using the system default loopback address regardless of whether the domain is cached or not 

So apparently, dig here used the local cached ip for example.com. We know this because the TTL came out to be only 204. Here is the output from bypassing local cache and running `dig`.
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ dig @8.8.8.8 example.com

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> @8.8.8.8 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40647
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		300	IN	A	172.66.147.243
example.com.		300	IN	A	104.20.23.154

;; Query time: 110 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Sat Oct 17 08:36:46 +0545 2026
;; MSG SIZE  rcvd: 72
```
Here the TTL comes out to 300, but if ran the first command again:
```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ dig example.com

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 11600
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		240	IN	A	104.20.23.154
example.com.		240	IN	A	172.66.147.243

;; Query time: 52 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Oct 17 08:37:30 +0545 2026
;; MSG SIZE  rcvd: 72

```

#### Huh? it should have taken shorter so why did it take longer?
Let me try that command again.
```bash 
dibij@Dibij:~/projects/CyberSecurity-Learning$ dig example.com

; <<>> DiG 9.20.24-1ubuntu0.4-Ubuntu <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20297
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		199	IN	A	104.20.23.154
example.com.		199	IN	A	172.66.147.243

;; Query time: 0 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Oct 17 08:38:10 +0545 2026
;; MSG SIZE  rcvd: 72

dibij@Dibij:~/projects/CyberSecurity-Learning$ 

```
So as we can see, once the ip address and the domain name is cached in local nameserver, the lookup is faster. Running the command again got TTL to 14, 126,119,112 and so on....
### Common causes

- **NXDOMAIN:** The DNS response indicates that the requested name does not exist.
- **SERVFAIL:** The resolver could not complete the resolution.
- **Timeout:** A DNS server did not respond before the request timed out.
- **REFUSED:** A DNS server refused the query.
- **Incorrect or stale records:** A cached answer points to an old or incorrect IP.
- **Delegation problems:** The DNS hierarchy points to unavailable or
  incorrectly configured nameservers.
- **DNSSEC validation failure:** A validating resolver cannot authenticate
  the DNS response.
- **Network problems:** DNS traffic is blocked, packets are lost, or the
  upstream resolver is unreachable.
- **Resolver misconfiguration:** The device is using an incorrect DNS server
  or has incorrect DNS settings.

### Important distinction

A DNS resolution failure does not necessarily mean the website is down.

The web server may be operational while the client is unable to resolve
the domain name to an IP address.

Similarly, a DNS lookup may succeed but return an incorrect or stale IP,
causing a different kind of connectivity problem.

### Initial investigation

Inspect the system's DNS configuration:

```bash
resolvectl status
```

Query the system resolver:

```bash
dig example.com
```

Query Cloudflare's public resolver directly:

```bash
dig @1.1.1.1 example.com
```

Inspect the local resolver's statistics:

```bash
resolvectl statistics
```

Check the response status, answer records, TTL, query time, and DNS server.
Do not assume that a successful DNS response proves the website itself
is reachable.

---

Now i got three questions
### 1. What are the real upstream DNS servers for my device?
I ran this command `resolvectl status`
```bash
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 2 (enp7s0)
    Current Scopes: none
         Protocols: -DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
     Default Route: no

Link 3 (wlp8s0)
    Current Scopes: DNS
         Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 2400:1a00:8000:4::73
       DNS Servers: 100.127.255.165 100.127.255.73 2400:1a00:0:32::165 2400:1a00:8000:4::73
        DNS Domain: worldlink.com.np
     Default Route: yes

```
Not going to lie, this seems too complex. But here is what i know now.
> Since i am using a worldlink internet, it'd definitely connect to a worldlink DNS server and their ips are printed in the command.
> Why is the closest connection Link 3? 
> What is `wlp8s0`  or `enp7s0` ? 
> What is this? `+DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported`

Will Come back to it

---
### 2. Can you manually delete a stored DNS resolved cache ? If so how ?
So, there is this command called flushdns. That probably works. But i also wanna see how DNS is saved? where is it saved? and several other curiosities.
To view the cache you have to  run a few commands:

```bash
dibij@Dibij:~/projects/CyberSecurity-Learning$ resolvectl statistics
Transactions                                     
                       Current Transactions:    0
                         Total Transactions: 2161
                                                 
Cache                                            
                         Current Cache Size:   79
                                 Cache Hits:  817
                               Cache Misses: 1395
                                                 
Failure Transactions                             
                             Total Timeouts:   51
         Total Timeouts (Stale Data Served):    0
                    Total Failure Responses:    0
Total Failure Responses (Stale Data Served):    0
                                                 
DNSSEC Verdicts                                  
                                     Secure:    0
                                   Insecure:    0
                                      Bogus:    0
                              Indeterminate:    0
dibij@Dibij:~/projects/CyberSecurity-Learning$ sudo resolvectl flush-caches
[sudo: authenticate] Password:         
dibij@Dibij:~/projects/CyberSecurity-Learning$ resolvectl query example.com
example.com: 2606:4700:10::ac42:93f3           -- link: wlp8s0
             2606:4700:10::6814:179a           -- link: wlp8s0
             172.66.147.243                    -- link: wlp8s0
             104.20.23.154                     -- link: wlp8s0

-- Information acquired via protocol DNS in 31.8ms.
-- Data is authenticated: no; Data was acquired via local or encrypted transport: no
-- Data from: network
dibij@Dibij:~/projects/CyberSecurity-Learning$ resolvectl statistics
Transactions                                     
                       Current Transactions:    0
                         Total Transactions: 2170
                                                 
Cache                                            
                         Current Cache Size:    4
                                 Cache Hits:  822
                               Cache Misses: 1399
                                                 
Failure Transactions                             
                             Total Timeouts:   51
         Total Timeouts (Stale Data Served):    0
                    Total Failure Responses:    0
Total Failure Responses (Stale Data Served):    0
                                                 
DNSSEC Verdicts                                  
                                     Secure:    0
                                   Insecure:    0
                                      Bogus:    0
                              Indeterminate:    0
dibij@Dibij:~/projects/CyberSecurity-Learning$ resolvectl query example.com
example.com: 2606:4700:10::6814:179a           -- link: wlp8s0
             2606:4700:10::ac42:93f3           -- link: wlp8s0
             172.66.147.243                    -- link: wlp8s0
             104.20.23.154                     -- link: wlp8s0

-- Information acquired via protocol DNS in 1.6ms.
-- Data is authenticated: no; Data was acquired via local or encrypted transport: no
-- Data from: cache
dibij@Dibij:~/projects/CyberSecurity-Learning$ resolvectl statistics
Transactions                                     
                       Current Transactions:    0
                         Total Transactions: 2174
                                                 
Cache                                            
                         Current Cache Size:    6
                                 Cache Hits:  824
                               Cache Misses: 1401
                                                 
Failure Transactions                             
                             Total Timeouts:   51
         Total Timeouts (Stale Data Served):    0
                    Total Failure Responses:    0
Total Failure Responses (Stale Data Served):    0
                                                 
DNSSEC Verdicts                                  
                                     Secure:    0
                                   Insecure:    0
                                      Bogus:    0
                              Indeterminate:    0
dibij@Dibij:~/projects/CyberSecurity-Learning$ 
```

It shows that we got the IP address from the network after flushing the DNS (`Data from: network`). 
When queried a second time, it resolved in 1.6ms directly from local memory (`Data from: cache`).

> [!tip] Technical Note: Latency vs. TTL
> - **Query Latency (31.8ms vs 1.6ms):** The round-trip time spent waiting for packets to travel across the network vs reading from local RAM cache.
> - **TTL (Time To Live in Seconds):** The expiration timer set by the authoritative nameserver (e.g., 300s) telling the resolver how long it may safely cache the answer.
> - **Cache Stats Counter:** `resolvectl statistics` maintains cumulative totals for the `systemd-resolved` service since boot, which is why flushing cache entries does not reset the lifetime hit/miss numbers to 0.

### 3. What will the effects of having the mismatch in cache be ?
I was unable to reproduce cache mismatch of DNS because it required either my own domain or docker, and I don't have docker in my Linux system. But, apparently with cache mismatch, there will be:
- Downtime
- Broken APIs and app crashes
- SSL/TLS certificate warnings (mismatched domain/CN)
- Routing traffic to the wrong tenant or old host
- Cache poisoning and hijacking risks

--- 

> [!note]
> Apparently one domain can have multiple IPs.

## Why would a domain need multiple IPs?
1. If a website receives tons of requests, having multiple IPs helps in **Load Balancing** (DNS Round-Robin).
2. If one server becomes unavailable, another **redundant** server can fill the gap.
3. Geo-DNS / Content Delivery Networks (CDNs) return IPs closest to the user's geographic location.
4. To separate legacy vs new namespaces or dual-stack IPv4 (`A` record) and IPv6 (`AAAA` record).

---

## 4. Questions to Investigate

- [ ] **What do `wlp8s0` and `enp7s0` mean?** (Predictable Network Interface Device Names: `wl` = wireless LAN, `en` = ethernet, `p8s0` = PCI bus 8 slot 0).
- [ ] **Why does `dig` report `SERVER: 127.0.0.53#53`?** How does `systemd-resolved` act as a local stub resolver on Ubuntu/Linux?
- [ ] **What are the other essential DNS Record Types?**
  - `A` (IPv4) vs `AAAA` (IPv6)
  - `CNAME` (Canonical Name / Alias)
  - `MX` (Mail Exchange for email routing)
  - `TXT` (Text records used for domain ownership verification, SPF, and DKIM)
- [ ] **What happens during a full recursive trace?** What does `dig +trace example.com` show compared to a standard query?
- [ ] **How does DNS Cache Poisoning (Kaminsky Attack) work?** Why was DNSSEC created to stop fake responses?
- [ ] **What is DNS Tunneling?** How can attackers exfiltrate data hidden inside DNS queries even when firewalls block all web browsing?

---

## 5. Practical Experiments

- [ ] **Experiment 1 (Trace the Root-to-Leaf path):** Run `dig +trace google.com` and watch your terminal query the root servers (`.`), then `.com` servers, then Google's authoritative nameservers.
- [ ] **Experiment 2 (Inspect TXT records):** Run `dig TXT google.com` to inspect real security verification records (SPF, Google Site Verification).
- [ ] **Experiment 3 (Local `/etc/hosts` override):** Add `127.0.0.1 myfaketestdomain.local` to `/etc/hosts` and observe how the OS resolves it before touching DNS.
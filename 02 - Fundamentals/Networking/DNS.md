# 1. What is DNS ?

DNS or Domain Name Server is a distributed system made up of rules (Transfer protocols), IPs(ipv4 and ipv6). DNS is used to translate domain names ( www.google.com or www.yahoo.com) to IP addresses. 
- ### How does the translation work ? 
	- When you look up a domain name in your browser, lets say www.google.com, the browser checks it cache to see if it already knows the domain. 
	- If it does, it points you to the numerical ip address of the domain "www.google.com". If not, then the OS picks up the request to www.google.com and checks its cache. 
		- Both OS and the browser check their cache, or better yet store in cache, so the lookup does not happen many times. In my preliminary understanding its to make sure the <u>Top level domains</u> are not overrun with requests for commonly visited sites.
	 - If OS does not have that domain then that request get passed to a <u>Recursive Resolver</u>. Recursive Resolver then moves this request to a Root Level Namespace. 
		 - It is usually hidden in the url of the domain, for example, www.google.com leads to a server, but browsers ignore that there is a "." in www.google.com. at the end. That is the Root level Namespace
	 - Root level Namespace then passes the request from the device to a Top level Domain like .com or .org
	 - Top level Domain then hands over the request to the Authoritative Nameserver which then passes along the numeric ip address in regards to the domain.
	 - As the ip comes back to the device, it is then stored in almost every layer of the [[Network Path]]  in Browser, OS, Resolver DNS and also the local network router.
- # Where could the translation fail ?
- 
		

# 2. Questions to investigate

# 3. Practical Experiments

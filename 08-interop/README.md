Task #03 - ICMPv6 echo between RIOT and Contiki-NG
ICMPv6 echo request/reply exchange between a node running RIOT and a Contiki node.
This assummes Docker is installed and configured. The steps for configuring
Contiki-NG are based on the [official documentation](https://docs.contiki-ng.org/en/master/doc/getting-started/index.html)

1. Clone Contiki-NG

```bash
git clone https://github.com/contiki-ng/contiki-ng.git
cd contiki-ng
git submodule update --init --recursive

```

2. Pull the Contiki-NG Docker image

```bash
docker pull contiker/contiki-ng
```

3. Create a `contiker` alias to start the Contiki-NG environment
```bash

export CNG_PATH=<absolute-path-to-your-contiki-ng>
alias contiker="docker run --privileged --sysctl net.ipv6.conf.all.disable_ipv6=0 --mount type=bind,source=$CNG_PATH,destination=/home/user/contiki-ng -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/bus/usb:/dev/bus/usb -ti contiker/contiki-ng"
```
4. Add the `shell` service to the `examples/hello-world` application.
```diff
diff --git a/examples/hello-world/Makefile b/examples/hello-world/Makefile
index 0a79167ae..710496368 100644
--- a/examples/hello-world/Makefile
+++ b/examples/hello-world/Makefile
@@ -1,5 +1,7 @@
 CONTIKI_PROJECT = hello-world
 all: $(CONTIKI_PROJECT)
 
+MODULES += os/services/shell
+
 CONTIKI = ../..
 include $(CONTIKI)/Makefile.include
```
5. Run the Contiki-NG environment using the `contiker` alias.
```bash
contiker
```
6. Compile the `hello-world` application for your target platform. Check the
[platform documentation](https://docs.contiki-ng.org/en/master/doc/platforms/index.html)
for board specific steps. E.g for `nrf52840dk`:
```
make -C examples/hello-world TARGET=nrf52840 hello-world
make -C examples/hello-world TARGET=nrf52840 hello-world.upload
```
7. Use any serial terminal (e.g `pyterm`) to get the link-local IP address of
the Contiki-NG node:
```
ip-addr
2023-04-14 15:23:36,732 # #f4ce.36c6.d8d1.e340> Node IPv6 addresses:
2023-04-14 15:23:36,735 # -- fe80::f6ce:36c6:d8d1:e340
```
8. For the RIOT side just use [gnrc_networking](https://github.com/RIOT-OS/RIOT/tree/master/examples/gnrc_networking). Get the link-local IP address with `ifconfig`:
```
2023-04-14 15:11:12,614 # ifconfig
2023-04-14 15:11:12,620 # Iface  6  HWaddr: 06:EE  Channel: 26  NID: 0xabcd  PHY: O-QPSK 
2023-04-14 15:11:12,622 #           
2023-04-14 15:11:12,626 #           Long HWaddr: 00:04:25:19:18:01:86:EE 
2023-04-14 15:11:12,633 #            TX-Power: 0dBm  State: IDLE  max. Retrans.: 3  CSMA Retries: 4 
2023-04-14 15:11:12,640 #           AUTOACK  ACK_REQ  CSMA  L2-PDU:102  MTU:1280  HL:64  RTR  
2023-04-14 15:11:12,643 #           RTR_ADV  6LO  IPHC  
2023-04-14 15:11:12,646 #           Source address length: 8
2023-04-14 15:11:12,649 #           Link type: wireless
2023-04-14 15:11:12,655 #           inet6 addr: fe80::204:2519:1801:86ee  scope: link  VAL
2023-04-14 15:11:12,665 #           inet6 group: ff02::2
2023-04-14 15:11:12,668 #           inet6 group: ff02::1
2023-04-14 15:11:12,672 #           inet6 group: ff02::1:ff01:86ee
2023-04-14 15:11:12,674 #           inet6 group: ff02::1a
2023-04-14 15:11:12,675 #           
2023-04-14 15:11:12,678 #           Statistics for Layer 2
2023-04-14 15:11:12,682 #             RX packets 16174  bytes 1812690
2023-04-14 15:11:12,688 #             TX packets 14824 (Multicast: 82)  bytes 1715052
2023-04-14 15:11:12,692 #             TX succeeded 14694 errors 130
2023-04-14 15:11:12,694 #           Statistics for IPv6
2023-04-14 15:11:12,698 #             RX packets 3194  bytes 1453638
2023-04-14 15:11:12,704 #             TX packets 2545 (Multicast: 82)  bytes 1430068
2023-04-14 15:11:12,707 #             TX succeeded 2545 errors 0
2023-04-14 15:11:12,707 # 
```
9. Set the PAN ID of the RIOT node to `abcd` (default PAN ID of Contiki)
```
ifconfig 6 set pan_id abcd
```

10. Run the `ping` command on both the RIOT and the Contiki-NG node:

Contiki-NG:
```
ping fe80::204:2519:1801:86ee
2023-04-14 15:23:29,960 # #f4ce.36c6.d8d1.e340> Pinging fe80::204:2519:1801:86ee
2023-04-14 15:23:29,974 # Received ping reply from fe80::204:2519:1801:86ee, len 4, ttl 64, delay 15 ms
```

RIOT
```
ping fe80::f6ce:36c6:d8d1:e340
2023-04-14 15:30:20,415 # ping fe80::f6ce:36c6:d8d1:e340
2023-04-14 15:30:20,449 # 12 bytes from fe80::f6ce:36c6:d8d1:e340%6: icmp_seq=0 ttl=64 rssi=-46 dBm time=24.320 ms
2023-04-14 15:30:21,441 # 12 bytes from fe80::f6ce:36c6:d8d1:e340%6: icmp_seq=1 ttl=64 rssi=-46 dBm time=6.031 ms
2023-04-14 15:30:22,455 # 12 bytes from fe80::f6ce:36c6:d8d1:e340%6: icmp_seq=2 ttl=64 rssi=-46 dBm time=8.237 ms
2023-04-14 15:30:22,455 # 
2023-04-14 15:30:22,460 # --- fe80::f6ce:36c6:d8d1:e340 PING statistics ---
2023-04-14 15:30:22,465 # 3 packets transmitted, 3 packets received, 0% packet loss
2023-04-14 15:30:22,469 # round-trip min/avg/max = 6.031/12.862/24.320 ms
```
Every packet should be echoed by the target node and printed to the console.
<div id="main-page"></div>
<div class="divider" id="ntp-server"></div>
## Setarea serverului de Timp 

Mai întâi, în consolă, ca root :

~~~  
apt-cache search ntp  
apt-get update && apt-get install ntp ntp-doc  
update-rc.d -f ntp defaults  
run update-rc.d later,after doing some configgering  
~~~

Găsiţi documentaţia în computerul dumneavoastră la adresa 

~~~  
/usr/share/doc/ntp-doc/html/index.html  
şi puneţi-i semn !  
~~~

este un document mare, nu tot este folosit aici, dar îl aveţi.

ntp nu se va activa decât după reboot, dar trebuie să setaţi data şi ora cât mai exact posibil dinainte 

ntp va lua datele din lista de servere din /etc/ntp.conf, care este principalul fişier editabil.

Ambele, ntpdate şi demonul ntpd [numit ntp], plasează lista timeserverelor aproape de începutul fişierului /etc/ntp.conf. iată un exemplu de listă :

~~~  
pool.ntp.org maps to more than 100 low-stratum NTP servers.  
# Your server will pick a different set every time it starts up.  
# *** Please consider joining the pool! ***  
# ***  [http://www.pool.ntp.org/#join](http://www.pool.ntp.org/#join)  ***  
server 192.168.3.24  
server ntp.blueyonder.co.uk  
server uk.pool.ntp.org  
server 1.uk.pool.ntp.org  
server 2.uk.pool.ntp.org  
server 0.europe.pool.ntp.org  
server 1.europe.pool.ntp.org  
server 2.europe.pool.ntp.org  
~~~

Primul din listă este un alt computer din aceaşi reţea care rulează deasemeni ntp [aici el este 'server 192.168.3.1']

Al doilea este timeserverul providerului de internet la care sunteţi conectat (ISP) .

Mai departe sunt cateva dintre serverele uk.pool.ntp.org , apoi câteva din Europa. Apropo , însuşi serverul providerului dumneavoastră poate fi timeserver, puteţi verifica asta rulând:

~~~  
ntpdate -v  
~~~

Aceasta nu va schimba nimic, dar va întoarce un mesaj de genul :

~~~  
# ntpdate -v 192.168.3.24  
19 Sep 19:09:27 ntpdate[13329]: ntpdate 4.2.2@1.1532-o Wed Aug 9 12:08:54 UTC 2006 (1)  
~~~

 [O listă completă de timeservere este la http://www.pool.ntp.org/](http://www.pool.ntp.org) 

Apoi va trebui să permiteţi accesul către computerele locale :

~~~  
# Local users may interrogate the ntp server more closely.  
restrict 127.0.0.1 nomodify  
restrict 192.168.3.0/24  
~~~

Acum pentru a transmite :

~~~  
# If you want to provide time to your local subnet, change the next line.  
# (Again, the address is an example only.)  
broadcast 192.168.3.255  
~~~

Fişierul ntp.conf este un pic diferit şi va fi tratat diferit dacă doar daţi clic pe el, oricum , înainte de a porni ntp va trebui să setaţi ora , ex. :

~~~  
# ntpdate -u -b uk.pool.ntp.org  
19 Sep 19:19:33 ntpdate[15641]: step time server 62.3.200.116 offset 0.001523 sec  
~~~

Porniţi ntp ca serviciu , pentru pornire la fiecare boot [sau reboot] după ce ntp a rulat câtva timp, faceţi :

~~~  
ntpq -pn  
~~~

Dacă totul a mers cum trebuie veţi vedea ceva de genul :

~~~  
# ntpq -pn  
remote refid st t when poll reach delay offset jitter  
----------------------------------------------------------------------------  
192.168.3.24 .INIT. 16 u - 1024 0 0.000 0.000 0.000  
+194.117.157.4 192.5.41.40 2 u 97 128 377 7.849 1.548 30.157  
82.219.3.1 195.66.241.2 2 u 101 128 377 17.755 0.794 24.722  
82.133.58.132 .INIT. 16 u - 1024 0 0.000 0.000 0.000  
+194.153.168.75 195.66.241.3 2 u 37 128 377 23.475 3.259 12.203  
+82.68.126.114 209.81.9.7 2 u 101 128 377 44.567 -1.366 46.922  
+194.88.2.88 194.159.73.44 3 u 90 128 377 17.208 -5.569 27.527  
+130.226.232.145 213.112.52.151 3 u 89 128 377 62.130 -0.797 39.999  
127.127.1.0 .LOCL. 10 l 18 64 377 0.000 0.000 0.001  
192.168.3.255 .BCST. 16 u - 64 0 0.000 0.000 0.001  
~~~

Asteriscul de pe linia a treia , în acest exemplu : *82.219.3.1 , arată timeserverul activ , considerat cel mai de încredere . Înseamnă că acum data şi ora sunt setate bine şi foloseşte portul 123. Exemplul liniei din iptables :

~~~  
# Network Time Protocol (NTP) Server  
$IPT -A udp_inbound -p UDP -s 0/0 --destination-port 123 -j ACCEPT  
$IPT -A INPUT -j ACCEPT -p tcp --dport 123  
~~~

<div id="rev">Content last revised 30/11/2012 0100 UTC</div>

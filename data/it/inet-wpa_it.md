<div id="main-page"></div>
<div class="divider" id="wpa-basic"></div>
## Come ottenere una rete wireless funzionante - WiFi

`A causa della complessità della legge, siduction fornisce solo software dfsg-free.  [Si controlli attentamente questo collegamento per ulteriori informazioni sulle sorgenti non-free aggiuntive per i firmware](nf-firm-it.htm#non-free-firmware) .`

Per far funzionare una wlan WiFi avrete bisogno per alcuni minuti di una connessione via cavo sì da poter scaricare il firmware appropriato.

Se questa non è disponibile dovrete mettere il firmware in una periferica rimovibile (ad es., una chiavetta USB) e installarlo da lì come root utilizzando:

~~~  
#dpkg -i <firmware.deb>  
~~~

Non conoscendo il produttore o la marca del chip wireless, per trovare il firmware appropriato potrete usare il comando:

~~~  
#fw-detect  
~~~

il quale vi fornirà le seguenti informazioni:

~~~  
#apt-get update  
#apt-get install <nome_del_firmware>  
#modprobe -r <nome_del_modulo>  
#modprobe <nome_del_modulo>  
~~~

Usate il nome che il comando fw-detect vi ha fornito nella linea apt-get install. Dopo averlo fatto, dovrete scrivere alcuni comandi nella console prima di configurare la periferica.

Poi dovrete caricare il modulo per poter essere in grado di configurare la periferica.

Come root eseguite nella console:

~~~  
modprobe -r <nome_del_modulo>  
modprobe <nome_del_modulo>  
~~~

Sostituite &lt;nome_del_modulo&gt; con quello fornitovi in precedenza da fw-detect. Potete qui utilizzare un'utile funzione di Konsole, il completamento della bash:  
se, ad esempio, scrivete solo le prime lettere di &lt;nome_del_modulo&gt; e quindi premete il tasto TAB, il nome verrà automaticamente completato (ad es., modprobe ipw e tasto TAB). Ciò evita anche errori di battitura.

Entrambi i comandi modprobe non danno nessun output se non ci sono errori: quindi, se compare il prompt normale il modulo è stato caricato correttamente.

Si può controllare con:

~~~  
#lsmod | grep <module>  
~~~

Avviate adesso come root ceni da console o Ceni dal Menu K - Internet con  [Attivare una connessione di rete con "Ceni"](inet-ceni-it.htm#netcardconfig) . La periferica wireless WiFi dovrebbe ora essere visualizzata e pronta per essere configurata.

Per configurare Wlan WiFi GUI si veda  [WiFi - roaming WPA-GUI](inet-wpagui-it.htm) 

<div class="divider" id="wpa"></div>
## Modalità Operative in wpa_supplicant per Debian

`A causa della complessità della legge, siduction fornisce solo software dfsg-libero.  [Si controlli attentamente il link seguente per informazioni addizionali sulle fonti di software non-libero per il firmware](nf-firm-it.htm#non-free-firmware) .`

Il pacchetto Debian di wpa_supplicant fornisce due convenienti modalità operative strettamente integrate nel nucleo della struttura di rete, ifupdown.

#### Argomenti trattati

###### 1. Modo #1: Managed Mode

* Esempi  
* Tabella delle opzioni comuni  
* Note importanti riguardo a Managed Mode  
* Come funziona

###### 2. Modo #2: Roaming Mode

* wpa_supplicant.conf  
* /etc/network/interfaces  
* Controllare il Roaming Daemon con wpa_action  
* Regolare con precisione le impostazioni di Roaming  
* Il file di log  
* Usare gli External Mapping Scripts (ad esempio, guessnet)  
* /etc/network/interfaces con mappatura esterna

###### 3. Soluzioni di problemi

* ssid nascosti

###### 4. Considerazioni sulla sicurezza

* Configurazione dei permessi dei file

## 1. Modo #1: Managed Mode

Questa modalità permette di stabilire una connessione via wpa_supplicant a una rete conosciuta. Lavora in modo simile al pacchetto wireless-tools. Ogni elemento richiesto per stabilire la connessione con wpa_supplicant ha quale prefisso "wpa-", seguito dal valore che sarà usato per quell'elemento.

###### Esempi di un file wpa.conf in Modo #1 - Esempio 1.

~~~  
Esempio di un file wpa.conf in Modo #1 - Esempio 1.  
NOTA: Il valore "wpa-psk" è valido solo se:  
1. è una stringa di puro testo (ASCII) contenente da 8 a 63 caratteri  
2. è una stringa esadecimale di 64 caratteri  
# Si connette all'access point con ssid "NETBEER" con criptazione  
# WPA-PSK/WPA2-PSK. Presuppone che il driver usi il driver backend "wext"  
# di wpa_supplicant in quanto non è specificata nessuna opzione wpa-driver.  
# La password o passphrase è data come stringa di puro testo ASCII. Per ottenere un indirizzo di rete è usato DHCP.  
#  
#  
iface wlan0 inet dhcp  
wpa-ssid NETBEER  
# passphrase in solo testo  
wpa-psk FraseOccultaInSoloTesto  
# Si connette a un access point con ssid "homezone" con tipo di criptazione  
# WPA-PSK/WPA2-PSK, usando il driver backend "wext" di wpa_supplicant.  
# Il psk è dato come stringa esadecimale codificata.  
# Per ottenere un indirizzo di rete è usato DHCP.  
#  
iface wlan0 inet dhcp  
wpa-driver wext  
wpa-ssid homezone  
# il psk esadecimale è codificato da una passphrase in puro testo  
wpa-psk 000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f  
# Si connette a un access point con ssid "HotSpot1" e bssid "00:1a:2b:3c:4d:5e"  
# con criptazione WPA-PSK/WPA2-PSK, usando il backend driver "madwifi"  
# di wpa_supplicant. La password o passphrase è data come stringa di puro testo.  
# È usato un indirizzo statico di rete.  
#  
iface ath0 inet static  
wpa-driver madwifi  
wpa-ssid HotSpot1  
wpa-bssid 00:1a:2b:3c:4d:5e  
# plaintext passphrase  
wpa-psk madhotspot  
wpa-key-mgmt WPA-PSK  
wpa-pairwise TKIP CCMP  
wpa-group TKIP CCMP  
wpa-proto WPA RSN  
# static ip settings  
address 192.168.0.100  
netmask 255.255.255.0  
network 192.168.0.0  
broadcast 192.168.0.255  
gateway 192.168.0.1  
# Per eth1 è usato un file wpa_supplicant.conf fornito dall'utente. Tutte le informazioni sulla rete  
# sono contenute nel file wpa_supplicant.conf fornito dall'utente. Se non è specificato  
# nessun tipo di wpa-driver, verrà usato wext. Per ottenere un indirizzo di rete è usato DHCP.  
#  
iface eth1 inet dhcp  
wpa-conf /path/to/wpa_supplicant.conf  
~~~

<div class="divider" id="wpa1"></div>
## Tabella delle opzioni comuni

Ecco un breve riassunto delle opzioni comuni di "wpa-" che possono essere usate nel file "/etc/network/interfaces" per un dispositivo wireless. Si veda la sezione "Note importanti riguardo al Managed Mode" per informazioni sui valori di "wpa-" validi e non validi.

**`NOTA: TUTTI i valori sono sensibili al maiuscolo/minuscolo`**

~~~  
Elemento Valore d'esempio Descrizione  
======== ================ ===========  
wpa-ssid nomeinpurotesto imposta il ssid della rete  
wpa-bssid 00:1a:2b:3c:4d:5e è il bssid dell'access point  
wpa-psk 0123456789...... la chiave wpa (preshared). Usare  
wpa_passphrase(8) per generare l'accoppiata psk  
passphrase e ssid  
wpa-key-mgmt NONE, WPA-PSK, WPA-EAP, lista delle chiavi di autenticazione accettate  
IEEE8021X protocolli di gestione  
wpa-group CCMP, TKIP, WEP104, lista dei gruppi ciphers accettati per WPA  
WEP40  
wpa-pairwise CCMP, TKIP, NONE lista dei pairwise ciphers accettati per WPA  
wpa-auth-alg OPEN, SHARED, LEAP lista degli algoritmi di autenticazione  
IEEE 802.11 permessi  
wpa-proto WPA, RSN lista dei protocolli accettati  
wpa-identity mionomeinpurotesto lo username dell'amministratore  
(autenticazione EAP)  
wpa-password miapasswordinpurotesto la password (autenticazione EAP)  
wpa-scan-ssid 0 o 1 Commuta la scansione di una ssid con specifici  
Probe Request frames  
wpa-ap-scan 0 o 1 o 2 regola la logica di scansione di  
wpa_supplicant  
~~~

Dovrebbe essere implementata la completa funzionalità di wpa_cli(8). Qualsiasi mancanza è considerata un errore e dovrebbe essere segnalata come tale. Eventuali patch di correzione sono sempre benvenute.

## Note importanti riguardo al Managed Mode

Quasi tutte le opzioni "wpa-" richiedono che si sia specificato almeno un ssid. Solo poche opzioni hanno un effetto globale. Queste sono: "wpa-ap-scan" e "wpa-preauthenticate".

Ogni opzione "wpa-" offerta per un dispositivo nel file interfaces(5) è sufficiente a far scattare in azione il demone di wpa_supplicant.

Lo script ifupdown di wpa_supplicant fa delle supposizioni riguardo al "tipo" di input valido per ciascuna opzione. Ad esempio, presuppone che alcuni input siano in testo puro e vi pone attorno le virgolette prima di passarli al wpa_cli, che a questo punto aggiunge l'input al blocco di rete in formazione con il socket ctrl_interface di wpa_supplicant.

L'avvio manuale di ifup con l'opzione "--verbose" mostrerà tutti i comandi usati per formare il blocco di rete mediante wpa_cli. Se il valore usato per una qualunque opzione "wpa-*" nel file "/etc/network/interfaces" ha attorno le virgolette, ciò significa che è stato ritenuto un input di tipo "puro testo" o "ASCII".

Alcuni input sono presupposti stringhe esadecimali (ad esempio, la chiave wpa-wep*). Il "tipo" di valore dell'opzione "wpa-psk", comunque, è determinato tramite un semplice controllo su più di un carattere non esadecimale.

## Come funziona

Come già menzionato, ogni specifico elemento di wpa_supplicant è prefissato con "wpa-". Ogni elemento è correlato a una proprietà di wpa_supplicant descritta nelle pagine "man" di wpa_supplicant.conf(5), wpa_supplicant(8) e wpa_cli(8).

Il supplicant è lanciato senza alcuna pre-configurazione, e wpa_cli forma una configurazione di rete a partire dall'input fornito dalle righe di "wpa-*". Inizialmente, wpa_supplicant/wpa_cli non imposta direttamente le proprietà del dispositivo (come, ad esempio, l'essid con iwconfig), ma piuttosto informa il dispositivo su quale access point è disponibile ad associarsi. Una volta che il dispositivo ha eseguito la scansione dell'area e trovato che è disponibile all'uso un certo access point, quelle proprietà verranno impostate.

Lo script che fa tutto il lavoro è localizzato in:

~~~  
/etc/wpa_supplicant/ifupdown.sh  
/etc/wpa_supplicant/functions.sh  
~~~

ifupdown.sh viene eseguito da run-parts, a sua volta invocato da ifupdown durante le fasi "pre-up", "pre-down" e "post-down".

Nella fase "pre-up", viene lanciato un demone wpa_supplicant seguito da una serie di comandi wpa_cli che impostano la configurazione di rete in base alle opzioni "wpa-" che sono state usate in /etc/network/interfaces per il dispositivo fisico.

Se è usato wpa-roam, viene lanciato una demone wpa_cli nella fase "post-up".

Nella fase "pre-down", il demone wpa_cli - se esiste - è rimosso.

Nella fase "post-down", è rimosso il demone wpa_supplicant.

## 2. Modo #2: Roaming Mode

In questo pacchetto viene fornito un meccanismo di roaming autocontenente, semplicistico. È in forma di uno script d'azione wpa_cli, /sbin/wpa_action, e assume il controllo di ifupdown quando attivato. La manpage di wpa_action(8) ne descrive a fondo i dettagli tecnici.

Per attivare una interfaccia roaming, adattate la seguente sezione interfaces(5) d'esempio:

~~~  
iface eth1 inet manual  
wpa-driver wext  
wpa-roam /percorso/verso/wpa_supplicant.conf  
~~~

In questo esempio vengono richiamati due demoni: wpa_supplicant e wpa_cli. È necessario fornire un wpa_supplicant.conf. Un buon punto di partenza è fornito da un file di configurazione d'esempio:

~~~  
# copiate il modello in /etc/wpa_supplicant/  
cp /usr/share/doc/wpasupplicant/examples/wpa-roam.conf \  
/etc/wpa_supplicant/wpa_supplicant.conf  
# impostate i permessi perché solo root possa leggere e scrivere il file  
chmod 0600 /etc/wpa_supplicant/wpa_supplicant.conf  
NOTE: è criticamente importante che il wpa_supplicant.conf usato definisca la locazione di  
"ctrl_interface" cosicché un socket per la comunicazione possa essere creato per il  
wpa_cli (demone wpa-roam). L'esempio di configurazione menzionato,  
/usr/share/doc/wpasupplicant/examples/wpa-roam.conf, è stato impostato  
come ragionevole default.  
~~~

È necessario modificare questo file di configurazione e aggiungere i blocchi di rete per tutte le reti note. Se non sapete cosa significa, cominciate con il leggere la manpage di wpa_supplicant.conf(5).

Per ogni rete dovrete specificare un'opzione speciale chiamata "id_str". Dovrebbe essere impostata come stringa di testo puro. Questa stringa forma le basi per i profili di rete: si correla a un'interfaccia logica definita nel file interfaces(5). Se nessuna id_str viene data per una rete, wpa_action presume che usi l'interfaccia logica di "default". L'interfaccia fallback può essere scelta mediante l'opzione "wpa-default-iface".

Che significa tutto ciò? Illustriamolo con un piccolo esempio preso dalla manpage di wpa_action(8).

###### Esempio di wpa_supplicant.conf

~~~  
esempio di wpa_supplicant.conf:  
network={  
ssid="foo"  
key_mgmt=NONE  
# questa id_str notificherà a /sbin/wpa_action di fare "ifup uni"  
id_str="uni"  
}  
network={  
ssid="bar"  
psk=123456789...  
# questa id_str notificherà a /sbin/wpa_action di fare "ifup home_static"  
id_str="home_static"  
}  
network={  
ssid=""  
key_mgmt=NONE  
# se non viene dato nessun parametro id_str, /sbin/wpa_action farà "ifup default"  
}  
~~~

<div class="divider" id="wpa2"></div>
###### Esempio di /etc/network/interfaces

~~~  
esempio di /etc/network/interfaces:  
# l'interfaccia roaming DEVE usare il metodo inet manuale  
# "allow-hotplug" o "auto" assicura la partenza automatica del demone  
allow-hotplug eth1  
iface eth1 inet manual  
wpa-driver wext  
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf  
# se non è specificato un id_str, verrà utilizzato "default"  
iface default inet dhcp  
# id_str="uni"  
iface uni inet dhcp  
# id_str="home_static"  
iface home_static inet static  
address 192.168.0.20  
netmask 255.255.255.0  
network 192.168.0.0  
broadcast 192.168.0.255  
gateway 192.168.0.1  
~~~

Un'interfaccia logica viene acquisita con ifup ed eliminata con ifdown, in quanto wpa_supplicant associa e deassocia la rete ad esso associata tramite l'opzione "id_str" usata nel file di configurazione di wpa_supplicant.conf.

Un log delle attività di /sbin/wpa_action viene creato in /var/log/wpa_action.log: quindi, aggiungete questo log quando inviate un rapporto su eventuali problemi.

## Interagire con wpa_supplicant con wpa_cli e wpa_gui

I membri del gruppo "netdev" (o qualsiasi gruppo di utenti specificato dai parametri GROUP= crtl_interface) possono interagire con il processo di wpa_supplicant se l'esempio di file di configurazione roaming viene usato così com'è .

~~~  
# L'opzione di default ctrl_interface usata nel file d'esempio  
# /usr/share/doc/wpasupplicant/examples/wpa-roam.conf  
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev  
Per interagire con supplicant, sono stati forniti wpa_cli (linea di comando) e wpa_gui (QT).  
Con questi potete connettervi, disconnettervi, aggiungere/eliminare nuovi  
blocchi di rete, fornire le informazioni di sicurezza interattive richieste, e così via.  
~~~

## Controllare il Roaming Daemon con wpa_action

Una volta avviato, il demone roaming assume il controllo di ifupdown; wpa_cli chiama ifup quando wpa_supplicant è associato con successo a un access point e chiama ifdown quando la connessione viene persa o terminata. Mentre il demone roaming è attivo, ifupdown non dovrebbe venire controllato direttamente mediante immissione di comandi manuali, piuttosto viene fornito /sbin/wpa_action per fermare e ricaricare il demone roaming. Per esempio, per fermare il demone roaming sul dispositivo "eth1":

~~~  
wpa_action eth1 stop  
~~~

Si può anche, quando richiesto, aggiornare il demone roaming con nuovi dettagli delle reti senza bisogno di fermarlo. Modificate il file wpa_supplicant.conf che viene usato dal demone con i nuovi dettagli delle reti, aggiungete le impostazioni opzionali della rete in /etc/network/interfaces specifiche della nuova rete (collegate mediante l'indicazione "id_str") e poi ricaricate il demone come segue:

~~~  
wpa_action eth1 reload  
~~~

Per i dettagli tecnici completi di quello che wpa_action può fare, leggete la manpage di wpa_action(8).

<div class="divider" id="wpa3"></div>
## Regolare con precisione le impostazioni di Roaming

Potete trovarvi in situazioni nelle quali diversi e conosciuti access point sono in stretta vicinanza. Potete scegliere manualmente il preferito con wpa_cli o wpa_gui, o dare a ogni rete la propria priorità. Questa possibilità è consentita dall'opzione "priority" di wpa_supplicant.conf.

<div class="divider" id="wpa4"></div>
## Il Logfile

Tutte le attività del demone roaming sono scritte in /var/log/wpa_action.log. Vengono scritte le seguenti informazioni:

*ora e data  
* nome dell'interfaccia e dell'evento in corso  
* valori delle variabili di ambiente (WPA_ID, WPA_ID_STR, WPA_CTRL_DIR)  
* ifupdown eseguito  
* stato di wpa_cli (basato su WPA-PSK, la rete può visualizzare informazioni diverse)  
* bssid  
* ssid  
* id  
* id_str  
* pairwise_cipher  
* group_cipher  
* key_mgmt  
* wpa_state  
* ip_address

<div class="divider" id="wpa5"></div>
## Usare script di mappatura esterni (ad esempio, guessnet)

In aggiunta alla mappatura interna delle interfacce logiche via "id_str", wpa_action può chiamare degli script esterni di mappatura. Uno script di mappatura dovrebbe mostrare il nome dell'interfaccia logica che dovrebbe essere avviata. Qualsiasi script di mappatura che lavori dal meccanismo di mappatura di ifupdown (vedasi man interfaces) dovrebbe lavorare anche quando viene chiamato da wpa_action.

Per chiamare uno script di mappatura aggiungere una linea "wpa-mapping-script nome_dello_script" alla sezione interfaces del dispositivo fisico di roaming (potrebbe essere necessario specificare il percorso assoluto che porta allo script di mappatura).

Il contenuto delle stringhe che iniziano con wpa-map viene passato a stdin dello script di mappatura. Poiché ifupdown permette solo una linea wpa-map si può aggiungere qualsiasi numero al wpa-map per linee addizionali. Per esempio:

~~~  
iface wlan0 inet manual  
wpa-driver wext  
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf  
wpa-mapping-script guessnet-ifupdown  
wpa-map0 home  
wpa-map1 work  
wpa-map2 school  
# ...linee wpa-mapX aggiuntive se necessarie  
~~~

Per default lo script di mappatura sarà usato solo quando non è disponibile un "id_str" per la rete corrente. Se volete disabilitare completamente la funzione "id_str" e usare solo uno script di mappatura esterno, usate l'opzione "wpa-mapping-script-priority 1" per sovrascrivere il comportamento di default.

Se lo script di mappatura emette una stringa vuota, wpa_action tornerà a usare l'interfaccia di default, a meno che sia definita un'alternativa dall'opzione "wpa-roam-default-iface".

Qui i seguito è mostrato un esempio di uso di guessnet-ifupdown come script di mappatura esterno.

###### /etc/network/interfaces con esempio di mappatura esterna

~~~  
/etc/network/interfaces con esempio di mappatura esterna:  
allow-hotplug wlan0  
iface wlan0 inet manual  
wpa-driver wext  
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf  
wpa-roam-default-iface default-wparoam  
wpa-mapping-script guessnet-ifupdown  
wpa-map default: default-guessnet  
wpa-map0 home_static  
wpa-map1 work_static  
# school può essere scelta attraverso un confronto con "id_str"  
iface school inet dhcp  
# resolvconf  
dns-nameservers 11.22.33.44 55.66.77.88  
iface home_static inet static  
address 192.168.0.20  
netmask 255.255.255.0  
network 192.168.0.0  
broadcast 192.168.0.255  
gateway 192.168.0.1  
test peer address 192.168.0.1 mac 00:01:02:03:04:05  
iface work_static inet static  
address 192.168.3.200  
netmask 255.255.255.0  
network 192.168.3.0  
broadcast 192.168.3.255  
gateway 192.168.3.1  
test peer address 192.168.3.1 mac 00:01:02:03:04:05  
iface default-guessnet inet dhcp  
iface default-wparoam inet dhcp  
~~~

In questo esempio wpa_action userà lo script guessnet per la selezione di una interfaccia logica disponibile solo quando nessuna opzione "id_str" viene fornita per la rete corrente nel file wpa_supplicant.conf.

Le linee "wpa-map" forniscono a guessnet le interfacce logiche che devono essere provate, oltre all'interfaccia di default che deve essere usata se tutte le prove falliscono. Le linee "test" di ogni interfaccia logica sono usate da guessnet per determinare se sono realmente connesse alla rete. Per esempio, guessnet sceglierà l'interfaccia logica "home_static" se c'è un dispositivo con un indirizzo IP di 192.168.0.1 e MAC di 00:01:02:03:04:05 sulla rete corrente. Se tutte le prove falliscono, verrà configurata l'interfaccia "default-guessnet".

Per maggiori informazioni leggete la manpage guessnet(8).

## 4. Soluzione di problemi

Per risolvere problemi di connessione, associazione e autenticazione, suggeriamo di avviare "wpa_cli -i &lt;interfaccia&gt;" in una console differente, prima di avviare l'interfaccia. Usare il comando "level 0" per primo, per ottenere tutti i messaggi di debug. Poi usate "ifup --verbose &lt;interfaccia&gt;" per ottenere messaggi completi di debug da parte dello script che avvia wpasupplicant.

<div class="divider" id="wpa6"></div>
## ssid nascosti

Come riferimento si veda #358137. Per riuscire ad associarvi a una rete con ssid nascosto, cercate di impostare l'opzione "ap_scan=1" nella sezione global e "scan_ssid=1" nella sezione del blocco di rete del file wpa_supplicant.conf. Se state usando il managed mode, potete farlo con queste sezioni:

~~~  
iface eth1 inet dhcp  
wpa-conf managed  
wpa-ap-scan 1  
wpa-scan-ssid 1  
# opzioni aggiuntive per la configurazione  
~~~

In accordo a #368770, può essere necessario un tempo lungo per associarsi a reti protette con WEP. In alcuni casi, impostare il parametro "ap_scan=2" nel config file (o usare una sezione "wpa-ap-scan 2", che è equivalente) può velocizzare molto il processo di associazione.

Notate che impostare "ap_scan" al valore 2 richiede anche che tutte le reti abbiano norme di sicurezza precisamente definite per le variabili key_mgmt, pairwise, group e proto network.

<div class="divider" id="wpa7"></div>
## 5. Considerazioni sulla sicurezza

##### Configurazione dei permessi dei file

È importante tenere riservate le informazioni PSK e le altre di tipo sensibile riguardanti le impostazioni della rete: assicuratevi quindi che i file importanti che contengono questi dati siano leggibili solo dal proprietario. Per esempio:

~~~  
chmod 0600 /etc/network/interfaces  
# sostituite i permessi del file wpa_supplicant.conf  
chmod 0600 /etc/wpa_supplicant/wpa_supplicant.conf  
~~~

Per default il file "/etc/network/interfaces" è leggibile da tutti e quindi non è idoneo a contenere chiavi segrete e password.

<div id="rev">Page last revised 03/03/2012 2100 UTC</div>

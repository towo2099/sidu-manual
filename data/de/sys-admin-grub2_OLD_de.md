<div class="divider" id="grub2"></div>

## GRUB 2

#### Zusammenfassung der wesentlichen Unterschiede zwischen GRUB 1 (jetzt grub-legacy) und GRUB2:

+ `Die Datei menu.lst existiert nicht mehr.` 

+ Die Datei `grub.cfg`  steuert nun den Grub-Bildschirm.

+ grub.cfg wird automatisch von Skripten in `/etc/grub.d`  erstellt.

+ Die Bezeichnung der Partitionen ändert sich ebenfalls. Die Nummerierung der Partitionen beginnt mit 1, nicht mit 0 (Laufwerksnummerierungen beginnen weiterhin mit 0):      
    ~~~
    Linux grub1 grub2
    /dev/sda1 (hd0,0) (hd0,1)
    /dev/sda2 (hd0,1) (hd0,2)
    /dev/sda3 (hd0,2) (hd0,3)
    
    /dev/sdb1 (hd1,0) (hd1,1)
    /dev/sdb2 (hd1,1) (hd1,2)
    /dev/sdb3 (hd1,2) (hd1,3)
    ~~~

+ Die Stanzas in grub.cfg folgen einer anderen Syntax als in menu.lst und können nicht direkt von der menu.lst von Grub 1 nach grub.cfg von Grub2 kopiert werden. **`Die Datei grub.cfg darf nie manuell geändert werden.`** 

<div class="divider" id="grub2-files"></div>

### Konfigurationsdatei von Grub2

Die Datei `/etc/default/grub`  enthält die variablen Einstellungen für Grub2, zum Beispiel Timeout, Basiseinstellungen des Menüs, Kernel-Parameter, graphische Oberfläche von Grub u.a.

###  Die Skripte von Grub2

`/etc/grub.d`  steuert die Zieldatei `grub.cfg` , die sich in `/boot/grub/`  befindet.

**`Die Datei grub.cfg sollte nie manuell geändert werden`** .   Die &Auml;nderungen w&uuml;rden beim n&auml;chsten update von grub &uuml;berschrieben, da die Datei mit Werten aus /etc/default/grub durch Scripte in /etc/grub.d erzeugt wird. Daher müssen alle &Auml;nderungen in den Skriptdateien im Ordner `/etc/grub.d`  durchgeführt werden. os-prober sollte 90% der Fälle korrekt lösen:

~~~
00_header:
05_debian_theme: Setzt Hintergrund, Textfarben, Grafikthema
10_hurd: Sucht einen Hurd-Kernel
10_linux: Sucht einen Linux-Kernel auf Grundlage des Befehls lsb_release
20_memtest86+: Falls die Datei /boot/memtest86+.bin existiert, wird sie ins Boot-Menü integriert
30_os-prober: Sucht in allen Partitionen nach Betriebssystemen (Linux und andere) und integriert sie in das Boot-Menü
40_custom: Eine Vorlage, um benutzerdefinierte Menü-Einträge für weitere Betriebssysteme anzulegen
60_fll-fromiso: Eine Vorlage, um benutzerdefinierte Menü-Einträge für fromiso auf eine/n USB-Stick/SSD-Karte anzulegen
<span class="highlight-2">60_fll-fromiso darf nicht manuell geändert werden. Für Anpassungen steht /etc/default/grub2-fll-fromiso zur Verfügung
Weitere Informationen unter [fromiso' mit Grub 2](hd-install-opts-de.htm#grub2-fromiso) </span>
~~~

Nachdem Änderungen durchgeführt wurden, muss grub.cfg diese kennen. Nach einer Aktualisierung des siduction-Kernels, werden die Aktualisierung von Grub automatisch durchgeführt. Änderungen, die manuell durchgeführt wurden, erfordern diesen Befehl:

~~~
update-grub
~~~

`Das Debianpaket von Grub2 ist so gestaltet, dass eine manuelle Änderung selten erforderlich ist.` 

<div class="divider" id="grub1-grub2"></div>

## Aktualisierung von Grub Legacy auf Grub2

**`Wir empfehlen eine saubere Aktualisierung auf Grub2 und die gänzliche Entfernung von Grub 1`** . Man sollte sich dessen bewusst sein, dass man bei fehlerhaftem Vorgehen das Bootsystem zerstören kann und daher sehr umsichtig vorgehen soll.

#### Schritt 1: 

Stelle sicher, dass Dein ganzes System aktualisiert ist: `dist-upgrade in Runlevel 3 (init 3)` .

~~~
apt-get update
Ctrl+alt+F1
init 3
apt-get dist-upgrade
init 5 && exit
~~~

#### Schritt 2:

Vollständige Entfernung von Grub 1:

~~~
rm -rf /boot/grub
apt-get purge grub-gfxboot
~~~

Als Folge werden `fll-iso2usb* grub-gfxboot* install-usb-gui*`  entfernt. Gebe `Y`  zur Bestätigung ein.

#### Schritt 3:

~~~
apt-get install grub2 os-prober
~~~

![Grub2](../images-common/images-grub2/grub2-2.png "Grub2") 

Verwende die TAB-Taste, um OK zu wählen

![Grub2](../images-common/images-grub2/grub2-3.png "Grub2") 

Verwende die TAB-Taste, um OK zu wählen

![Grub2-conversion 1](../images-common/images-grub2/grub2-convert-1.png "Grub2-conversion 1") 

Verwende die Tastaturpfeile und die Leertaste, um einen `* (Stern)`  zu setzen, auf welcher Festplatte Grub2 in den MBR geschrieben werden soll.  *(Das folgende Beispiel zeigt eine Installation auf ein USB-Laufwerk)* .

#### Schritt 4:

~~~
update-grub
~~~

#### Schritt 5:

~~~
apt-get install install-usb-gui fll-iso2usb
~~~

#### Schritt 6:

 Starte Deinen PC neu und menu.cfg zeigt Kernel und Betriebssystem wie in diesem Beispiel an:

![Grub2-OS list](../images-common/images-grub2/grub2-os-list.jpg "Grub2-OS list") 

Sollte etwas falsch gelaufen und Grub2 korrumpiert sein, lese [Überschriebener oder korrumpierter Grub2 im MBR](sys-admin-grub2-de.htm#chroot)  

### Eingabe von Grub2-Bootoptionen mit Hilfe des Bearbeitungsmodus

![Grub2-Edit](../images-common/images-grub2/grub2-e-1.JPG "Grub2-Edit") 

Falls temporäre Änderungen bei den Boot-Optionen eines in Grub 2 gelisteten Kernels nötig sind, kann man die Kerneloptionen bearbeiten, indem die Taste **`e`**  gedrückt wird. Mit den Pfeiltasten geht man zu dem Kernel, der bearbeitet werden soll. Noch im Bearbeitungsmodus wird mit `Ctrl+x`  der Computer mit den neuen Optionen neu gestartet.

Ein Beispiel: um direkt in den Runlevel 3 zu starten, wird eine `3`  an das Ende der Zeile `linux /boot/vmlinuz`  gesetzt.

Änderungen, die im Bearbeitungsmodus durchgeführt werden, sind nicht dauerhaft. Für dauerhafte Änderungen müssen die jeweiligen Konfigurationsdateien angepasst werden. Siehe: [Konfigurationsdateien und Skripte von Grub 2](sys-admin-grub2-de.htm#grub2-files) .

<div class="divider" id="multi-os"></div>

## Dualboot und Multiboot mit Grub2

Grub2 besitzt eine modulare Konfiguration und erlaubt daher einen einfachen Befehl, um neu installierte Betriebssysteme zu finden, die automatisch in die Datei menu.cfg integriert werden. Der einfache Befehl lautet:

~~~
update-grub
~~~

Sollte ein benutzerdefinierter Eintrag in menu.cfg erwünscht sein oder falls 30_os-prober nicht die benötigten Chainload-Einträge durchführt, können Ergänzungen mit Hilfe eines Texteditors in der Datei `/etc/grub.d/40_custom`  durchgeführt werden.

Beispiele für eine Adaptierung der Datei 40_custom:

~~~
menuentry "second mbr"{
set root=(hd1)
chainloader +1
}
~~~

~~~
menuentry "second partition"{
set root=(hd0,2)
chainloader +1
}
~~~

Nach Abspeicherung der Ändertungen müssen diese Grub übergeben werden:

~~~
update-grub
~~~

Sollte die Fehlermeldung auftreten, dass Grub auf einem Laufwerk nicht erkannt wird, muss die devicemap neu erstellt werden.

`Stelle bei der Installation eines weiteren Betriebssystems sicher, dass Grub nicht in den MBR, sondern in die Partition des neuen Betriebssystems geschrieben wird:` 

~~~
grub-mkdevicemap --no-floppy
update-grub
~~~

Warnhinweise können ignoriert werden.

Bei einem Fehler überschreibt die Aktualisierung vermutlich den MBR. Wie dies repariert wird, findest Du in [Grub2 - MBR überschrieben](sys-admin-grub2-de.htm#mbr-over-grub2) .

<div class="divider" id="mbr-over-grub2"></div>

## Nur grub2 neu von der Fesplatte in den MBR schreiben

~~~
/usr/sbin/grub-install --recheck --no-floppy /dev/sda
~~~

Es kann sein, dass dieser Befehl mehrfach ausgeführt werden muss, bis er "überzeugt" ist, dass dies wirklich durchgeführt werden soll.

## MBR von Windows überschrieben - MBR korrumpiert - Wiederherstellung von Grub2

**`ANMERKUNG: zur Wiederherstellung von Grub2 benötigt man ein siduction.iso.`**  [Alternativ kann ein chroot mit jeder live.iso verwendet werden](sys-admin-grub2-de.htm#chroot) .

Um grub2 neu zu schreiben oder wiederherzustellen, muss in eine `siduction.iso`  gestartet werden:

1. Um die Partitionen ([h,s]d[a..]X) zu identifizieren und bestätigen, muss man root (#) werden:      
    ~~~
    $ suxterm
    ~~~

2. Als root wird Folgendes eingegeben:      
    ~~~
    fdisk -l
    cat /etc/fstab
    ~~~

  Auf diese Weise erhält man die korrekten Benennungen. 

3. Wenn die korrekte Partitionsbezeichnung gefunden ist, wird ein Einhängepunkt erstellt:      
    ~~~
    mkdir -p /media/[hdxx,sdxx,diskx]
    ~~~

4. Danach wird die Partition eingebunden:      
    ~~~
    mount /dev/xdxx /media/xdxx
    ~~~

5. Jetzt kann Grub in den MBR der ersten Festplatte geschrieben werden:      
    ~~~
    /usr/sbin/grub-install --recheck --no-floppy --root-directory=/media/xdxx /dev/sda
    ~~~

<div class="divider" id="chroot"></div>

## Verwendung einer chroot-Umgebung zur Wiederherstellung eines überschriebenen oder korrumpierten Grub in MBR

Um Grub wiederherzustellen, falls er im MBR überschrieben oder korrumpiert wurde, muss eine `chroot` -Umgebung aufgesetzt werden. `Es kann jede live.iso verwendet werden, da die Chroot-Umgebung die Festplatteninstallation anspricht, sodass die gewünschte Grub-Version wiederhergestellt werden kann: grub1 (grub-legacy) oder grub2.` 

Man bootet in eine Deinem System entsprechende siduction.iso (32 oder 64 bit CD, DVD, USB-Stick oder SSD-Karte) und öffnet eine Konsole. Man tippt `suxterm`  und drückt die Eingabetaste, um root-Rechte zu erhalten.

Mit `fdisk -l oder blkid`  stellt man sicher, welche Partition die Boot-Partition ist, und erhält die korrekten Bezeichnungen (falls eine graphische Oberfläche gewünscht ist, verwendet man `Gparted` ):

~~~
blkid
~~~

Jetzt überprüft man, ob die Einträge in der Datei fstab mit der Ausgabe von blkid identisch sind:

~~~
cat /etc/fstab
~~~

Hier wird angenommen, dass das root-Dateisystem sich auf `/dev/sda2`  befindet:

~~~
mkdir /mnt/siduction-chroot
mount /dev/sda2 /mnt/siduction-chroot
~~~

Als nächstes müssen /proc, /run, /dev und /sys wie folgt eingebunden werden:

~~~
mount --bind /proc /mnt/siduction-chroot/proc
mount --bind /run /mnt/siduction-chroot/run
mount --bind /sys /mnt/siduction-chroot/sys
mount --bind /dev /mnt/siduction-chroot/dev
mount --bind /dev/pts /mnt/siduction-chroot/dev/pts
~~~

Wenn in eine EFI-Systempartition gebootet wird, muss diese auch eingebunden werden. In diesem Beispiel ist sie /dev/sda1:

~~~
mount /dev/sda1 /mnt/siduction-chroot/boot/efi
~~~

Die chroot-Umgebung ist nun aufgesetzt und es kann auf diese Weise darauf zugegriffen werden:

~~~
chroot /mnt/siduction-chroot /bin/bash
~~~

Es kann nun auf den lokalen Cache von apt zugegriffen werden bzw. in Dateien, die geändert werden müssen, geschrieben werden. Das Verhalten entspricht demjenigen, als ob Du im zu reparierenden System selbst arbeiten würdest. In folgendem Beispiel wird Grub neu in den MBR geschrieben.

`Wiederherstellung von Grub 2` 

~~~
apt-get install --reinstall grub-pc
~~~

Um sicherzustellen, dass Grub auf dem richtigen Gerät bzw. der richtigen Partition installiert wurde, wird dieser Konfigurationsbefehl ausgeführt:

~~~
dpkg-reconfigure grub-pc
~~~

`Wiederherstellung von Grub 2 EFI` 

~~~
apt-get install reinstall grub-efi-amd64
~~~

`Wiederherstellung von Grub 1 (grub-legacy)` 

~~~
apt-get install --reinstall grub-legacy
~~~

Folge den Anweisungen des Installationsprogramms.

Mit diesem Befehl wird die chroot-Umgebung wieder frei gegeben:

~~~
Ctrl+d
~~~

Starte Deinen PC neu.

<div id="rev">Page last revised 15/01/2012 1545 UTC</div>

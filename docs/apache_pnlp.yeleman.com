<VirtualHost *:80>
    ServerName pnlp.yeleman.com
    Redirect permanent / https://pnlp.yeleman.com
</VirtualHost>

<VirtualHost pnlp.yeleman.com:443>
    ServerName pnlp.yeleman.com

    DocumentRoot /home/pnlp/src/pnlp2011

    ErrorDocument 404 /media/apache_404.html
    ErrorDocument 500 /media/apache_500.html

    WSGIDaemonProcess prod user=pnlp group=pnlp threads=25 display-name=pnlp-wsgi
    WSGIProcessGroup prod

    Alias /robots.txt /home/pnlp/src/pnlp2011/pnlp_web/static/robots.txt
    Alias /favicon.ico /home/pnlp/src/pnlp2011/pnlp_web/static/images/favicon.ico
    Alias /static/ /home/pnlp/src/pnlp2011/pnlp_web/static/

    Alias /admin_static/ /home/pnlp/src/envs/pnlp/lib/python2.6/site-packages/django/contrib/admin/media/
    Alias /media/ /home/pnlp/src/pnlp2011/media/

    <Directory "/home/pnlp/src/pnlp2011/media/">
        AllowOverride All
        Order allow,deny
        Allow from all

        <IfModule mod_autoindex.c>
            Options Indexes FollowSymLinks
            IndexOrderDefault Descending Name
            IndexOptions IgnoreCase FancyIndexing FoldersFirst NameWidth=* DescriptionWidth=* SuppressHTMLPreamble HTMLTable SuppressIcon SuppressRules
            DefaultIcon /static/images/bullet.png
            HeaderName /media/header.html
            ReadmeName /media/footer.html
            IndexIgnore header.html footer.html apache_404.html apache_500.html favicon.ico .htaccess .ftpquota .DS_Store icons *.log *,v *,t .??* *~ *#

            AddDescription "MPEG Layer 3 Format" .mp3
            AddDescription "GZIP compressed TAR archive" .tgz .tar.gz
            AddDescription "GZIP compressed archive" .Z .z .gz .zip
            AddDescription "RAR compressed archive" .rar
            AddDescription "TAR compressed archive" .tar
            AddDescription "ZIP compressed archive" .zip 
            AddDescription "Windows executable file" .exe
            AddDescription "Common Gateway Interface" .cgi
            AddDescription "Joint Photographics Experts Group" .jpg .jpeg .jpe
            AddDescription "Graphic Interchange Format" .gif
            AddDescription "Portable Network Graphic" .png
            AddDescription "Vector graphic" .ps .ai .eps
            AddDescription "Hypertext Markup Language" .html .shtml .htm
            AddDescription "Cascading Style Sheet" .css
            AddDescription "DocType Definition" .dtd
            AddDescription "Extensible Markup Language" .xml
            AddDescription "Win32 compressed HTML help" .chm
            AddDescription "Adobe Portable Document Format" .pdf
            AddDescription "Plain text file" .txt .nfo .faq .readme
            AddDescription "Unix man page" .man
            AddDescription "Email data" .eml .mbox
            AddDescription "Open Document Text document" .odt
            AddDescription "Open Document Calc document" .odc
            AddDescription "Open Document Presentation document" .odp
            AddDescription "Microsoft Word document" .doc .docx
            AddDescription "Microsoft Excel document" .xls .xlsx
            AddDescription "Microsoft PowerPoint document" .ppt .pptx
            AddDescription "PHP: Hypertext Preprocessor script" .php  .php3 .php4
            AddDescription "PHP: Hypertext Preprocessor source code" .phps
            AddDescription "Javascript" .js
            AddDescription "Java code"  .java
            AddDescription "Unix shell script" .sh .shar .csh .ksh .command
            AddDescription "Mac OS X shell script" .command
            AddDescription "Configuration file" .conf
            AddDescription "Mac OS X terminal" .term
            AddDescription "BitTorrent file" .torrent
            AddDescription "Windows link" .lnk .url
        </ifModule>

    </Directory>

    <Directory /home/pnlp/src/pnlp2011/pnlp_web/static/>
        AllowOverride All
        Order deny,allow
        Allow from all
    </Directory>

    <Location /static>
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Location>

    <Location /raw_data/excel>
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
        ExpiresByType application/vnd.ms-excel "access plus 1 year"
    </Location>

    ## COMPRESSION
    <Location />
    # Insert filter
    SetOutputFilter DEFLATE

    # Netscape 4.x has some problems...
    BrowserMatch ^Mozilla/4 gzip-only-text/html

    # Netscape 4.06-4.08 have some more problems
    BrowserMatch ^Mozilla/4\.0[678] no-gzip

    # MSIE masquerades as Netscape, but it is fine
    # BrowserMatch \bMSIE !no-gzip !gzip-only-text/html

    # NOTE: Due to a bug in mod_setenvif up to Apache 2.0.48
    # the above regex won't work. You can use the following
    # workaround to get the desired effect:
    BrowserMatch \bMSI[E] !no-gzip !gzip-only-text/html

    # Don't compress images
    SetEnvIfNoCase Request_URI \
    \.(?:gif|jpe?g|png)$ no-gzip dont-vary

    # Make sure proxies don't deliver the wrong content
    Header append Vary User-Agent env=!dont-vary
    </Location> 

    # main mod_wsgi directive
    WSGIScriptAlias / /home/pnlp/src/pnlp2011/django.wsgi

    # allow apache to manage access on the directory
    <Directory /home/pnlp/src/pnlp2011>
        DirectoryIndex maintenance.html
        Order allow,deny
        Allow from all
    </Directory>

    SSLEngine On
    SSLCertificateFile /etc/apache2/ssl/pnlp.crt
    SSLCertificateKeyFile /etc/apache2/ssl/pnlp.key
    SSLCertificateChainFile /etc/apache2/ssl/pnlp.ca

</VirtualHost>

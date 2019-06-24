import filetype


def detect():
    kind = filetype.guess('tests/fixtures/sample.jpg')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)


def isImage(fpath):
    """
    -----Image-----
    jpg - image/jpeg
    jpx - image/jpx
    png - image/png
    gif - image/gif
    webp - image/webp
    cr2 - image/x-canon-cr2
    tif - image/tiff
    bmp - image/bmp
    jxr - image/vnd.ms-photo
    psd - image/vnd.adobe.photoshop
    ico - image/x-icon
    heic - image/heic
        """
    kind = filetype.guess(fpath)

    return False if kind == None else kind.extension in ['jpg',
                                                         'jpx',
                                                         'png',
                                                         'gif',
                                                         'webp',
                                                         'cr2',
                                                         'tif',
                                                         'bmp',
                                                         'jxr',
                                                         'psd',
                                                         'ico',
                                                         'heic'] or kind.mime in ['image/jpeg', 'image/jpx',
                                                                                  'image/png',
                                                                                  'image/gif',
                                                                                  'image/webp',
                                                                                  'image/x-canon-cr2',
                                                                                  'image/tiff',
                                                                                  'image/bmp',
                                                                                  'image/vnd.ms-photo',
                                                                                  'image/vnd.adobe.photoshop',
                                                                                  'image/x-icon',
                                                                                  'image/heic']


def isVideo(fpath):
    """
    -----Video-----
    mp4 - video/mp4
    m4v - video/x-m4v
    mkv - video/x-matroska
    webm - video/webm
    mov - video/quicktime
    avi - video/x-msvideo
    wmv - video/x-ms-wmv
    mpg - video/mpeg
    flv - video/x-flv
    """
    kind = filetype.guess(fpath)
    return False if kind == None else kind.extension in ['mp4',
                                                         'm4v',
                                                         'mkv',
                                                         'webm',
                                                         'mov',
                                                         'avi',
                                                         'wmv',
                                                         'mpg',
                                                         'flv'] or kind.mime in['video/mp4',
                                                                                'video/x-m4v',
                                                                                'video/x-matroska',
                                                                                'video/webm',
                                                                                'video/quicktime',
                                                                                'video/x-msvideo',
                                                                                'video/x-ms-wmv',
                                                                                'video/mpeg',
                                                                                'video/x-flv']

def isAudio(fpath):
    """
    -----Audio-----
    mid - audio/midi
    mp3 - audio/mpeg
    m4a - audio/m4a
    ogg - audio/ogg
    flac - audio/x-flac
    wav - audio/x-wav
    amr - audio/amr
    """
    kind = filetype.guess(fpath)
    return False if kind == None else kind.extension in ['mid',
                                                         'mp3',
                                                         'm4a',
                                                         'ogg',
                                                         'flac',
                                                         'wav',
                                                         'amr'] or kind.mime in['audio/midi',
                                                                                'audio/mpeg',
                                                                                'audio/m4a',
                                                                                'audio/ogg',
                                                                                'audio/x-flac',
                                                                                'audio/x-wav',
                                                                                'audio/amr']


"""
-----Archive-----
epub - application/epub+zip
zip - application/zip
tar - application/x-tar
rar - application/x-rar-compressed
gz - application/gzip
bz2 - application/x-bzip2
7z - application/x-7z-compressed
xz - application/x-xz
pdf - application/pdf
exe - application/x-msdownload
swf - application/x-shockwave-flash
rtf - application/rtf
eot - application/octet-stream
ps - application/postscript
sqlite - application/x-sqlite3
nes - application/x-nintendo-nes-rom
crx - application/x-google-chrome-extension
cab - application/vnd.ms-cab-compressed
deb - application/x-deb
ar - application/x-unix-archive
Z - application/x-compress
lz - application/x-lzip
"""
"""
-----Font-----
woff - application/font-woff
woff2 - application/font-woff
ttf - application/font-sfnt
otf - application/font-sfnt
"""

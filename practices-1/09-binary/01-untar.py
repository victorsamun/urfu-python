#!/usr/bin/env python3

import argparse
import os.path
import time
import struct
import sys


class TarParser:
    _HEADER_FMT1 = '100s8s8s8s12s12s8sc100s255s'
    _HEADER_FMT2 = '6s2s32s32s8s8s155s12s'
    _HEADER_FMT3 = '6s2s32s32s8s8s12s12s112s31x'
    _READ_BLOCK = 16 * 2**20

    _FILE_TYPES = {
        b'0': 'Regular file',
        b'1': 'Hard link',
        b'2': 'Symbolic link',
        b'3': 'Character device node',
        b'4': 'Block device node',
        b'5': 'Directory',
        b'6': 'FIFO node',
        b'7': 'Reserved',
        b'D': 'Directory entry',
        b'K': 'Long linkname',
        b'L': 'Long pathname',
        b'M': 'Continue of last file',
        b'N': 'Rename/symlink command',
        b'S': "`sparse' regular file",
        b'V': "`name' is tape/volume header name"
    }

    @staticmethod
    def _parse_header(hdr):
        header1 = struct.unpack(TarParser._HEADER_FMT1, hdr)

        header2 = (header1[-1],)
        if header1[9].startswith(b'ustar\x00'):
            header2 = struct.unpack(TarParser._HEADER_FMT2, header1[-1])
        elif header1[9].startswith(b'ustar '):
            header2 = struct.unpack(TarParser._HEADER_FMT3, header1[-1])

        header = header1[:-1] + header2

        name = header[0]
        if len(header) > 16 and header[15]:
            name = b'/'.join((header[15], name))
        name = name.strip(b'\x00').decode()

        file_size = int(b'0' + header[4].strip(b'\x00'), 8)
        return (header, name, file_size)

    def _preprocess(self):
        self._files = {}
        self._fpts = []

        with open(self._fn, mode='rb') as f:
            hdr = f.read(512)
            while hdr:
                header, name, file_size = TarParser._parse_header(hdr)
                if header[7] == b'L':
                    name = f.read(512)[:file_size - 1].decode()
                    header, _, file_size = TarParser._parse_header(f.read(512))

                rest_bytes = (512 - file_size) % 512
                if name:
                    fdesc = (header, file_size, f.tell(), name)
                    self._files[name] = fdesc
                    self._fpts.append(fdesc)

                f.seek(file_size + rest_bytes, 1)
                hdr = f.read(512)

    @staticmethod
    def _parse_time(t):
        return time.strftime('%d %b %Y %H:%M:%S', time.localtime(int(t, 8)))

    @staticmethod
    def _try_extract(f, filename, fileinfo, dest):
        try:
            fn = os.path.join(dest, filename.lstrip('/'))
            os.makedirs(os.path.dirname(fn), exist_ok=True)

            with open(fn, mode='wb') as out_file:
                f.seek(fileinfo[2], 0)
                rest = fileinfo[1]
                while rest > 0:
                    out_file.write(f.read(min(rest, TarParser._READ_BLOCK)))
                    rest -= TarParser._READ_BLOCK

            os.chmod(fn, int(fileinfo[0][1].strip(b'\x00'), 8))
        except Exception as e:
            print("Error while extracting '{}'".format(e), file=sys.stderr)

    def __init__(self, filename):
        self._fn = filename
        self._preprocess()

    def extract(self, dest=os.getcwd()):
        with open(self._fn, mode='rb') as f:
            for finfo in self._fpts:
                fname = finfo[-1]
                if finfo[0][7] == b'5':
                    os.makedirs(os.path.join(dest, fname.lstrip('/')),
                                exist_ok=True)
                else:
                    TarParser._try_extract(f, fname, finfo, dest)

    def files(self):
        yield from self._files.keys()

    def file_stat(self, filename):
        if filename not in self._files:
            raise ValueError(filename)

        finfo = [x.strip(b'\x00') for x in self._files[filename][0]]
        info = [
            ('Filename', filename),
            ('Type', TarParser._FILE_TYPES.get(finfo[7],
                                              TarParser._FILE_TYPES[b'0'])),
            ('Mode', finfo[1].decode()),
            ('UID', int(b'0' + finfo[2], 8)),
            ('GID', int(b'0' + finfo[3], 8)),
            ('Size', int(b'0' + finfo[4], 8)),
            ('Modification time', TarParser._parse_time(finfo[5])),
            ('Checksum', int(b'0' + finfo[6].strip(b'\x00 '), 8))
        ]

        if finfo[8]:
            info.append(('Link', finfo[8].decode()))

        if len(finfo) > 9:
            if finfo[11]:
                info.append(('User name', finfo[11].decode()))
            if finfo[12]:
                info.append(('Group name', finfo[12].decode()))
            if finfo[7] in b'34':
                info.append(('Device minor', finfo[13]))
                info.append(('Device major', finfo[14]))

        if len(finfo) > 16:
            if finfo[15]:
                info.append(('Last access time',
                             TarParser._parse_time(finfo[15])))
            if finfo[16]:
                info.append(('Last change time',
                             TarParser._parse_time(finfo[16])))
        return info


def print_file_info(stat, f=sys.stdout):
    max_width = max(map(lambda s: len(s[0]), stat))
    for field in stat:
        print("{{:>{}}} : {{}}".format(max_width).format(*field), file=f)


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] FILE'.format(os.path.basename(sys.argv[0])),
        description='Tar extractor')
    parser.add_argument('-l', '--list', action='store_true', dest='ls',
                        help='list the contents of an archive')
    parser.add_argument('-x', '--extract', action='store_true', dest='extract',
                        help='extract files from an archive')
    parser.add_argument('-i', '--info', action='store_true', dest='info',
                        help='get information about files in an archive')
    parser.add_argument('fn', metavar='FILE',
                        help='name of an archive')

    args = parser.parse_args()
    if not (args.ls or args.extract or args.info):
        sys.exit("Error: action must be specified")

    try:
        tar = TarParser(args.fn)

        if args.info:
            for fn in sorted(tar.files()):
                print_file_info(tar.file_stat(fn))
                print()
        elif args.ls:
            for fn in sorted(tar.files()):
                print(fn)

        if args.extract:
            tar.extract()
    except Exception as e:
        sys.exit(e)

if __name__ == '__main__':
    main()

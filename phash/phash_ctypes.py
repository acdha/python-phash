# encoding: utf-8

from __future__ import absolute_import

import ctypes
import sys
from ctypes import byref, pointer
from ctypes.util import find_library

ALL = ['ph_dct_imagehash', 'ph_dct_videohash', 'ph_image_digest', 'image_digest', 'cross_correlation']

FS_ENCODING = sys.getfilesystemencoding()

libphash_path = find_library('pHash')

if not libphash_path:
    raise ImportError('Cannot find libpHash!')

try:
    libphash = ctypes.cdll.LoadLibrary(libphash_path)
except OSError as exc:
    raise RuntimeError('Cannot load libpHash: %s' % exc)


class PHashError(Exception):
    pass


def _phash_errcheck(rc, func, args):
    """
    ctypes errcheck function which raises RuntimeError if the wrapped function returns -1
    """

    if rc == -1:
        raise PHashError('%s %r returned %s' % (func, args, rc))
    else:
        return rc


class Digest(ctypes.Structure):
    _fields_ = [
        ('id', ctypes.c_char_p),
        ('coeffs', ctypes.POINTER(ctypes.c_byte)),
        ('size', ctypes.c_int),
    ]


DIGEST_P = ctypes.POINTER(Digest)

ph_dct_imagehash = libphash.ph_dct_imagehash
ph_dct_imagehash.restype = ctypes.c_int
ph_dct_imagehash.argtypes = [ctypes.c_char_p, ctypes.c_ulong]

ph_dct_videohash = libphash.ph_dct_videohash
ph_dct_videohash.restype = ctypes.POINTER(ctypes.c_ulonglong)
ph_dct_videohash.argtypes = [ctypes.c_char_p, ctypes.c_int]

# ph_audiohash = libphash.ph_dct_audiohash
# ph_audiohash.restype = ctypes.POINTER(ctypes.c_int32)
# ph_audiohash.argtypes = [ctypes.c_float_p, ctypes.c_int]

# ph_readaudio = libphash.ph_readaudio
# ph_readaudio.restype = ctypes.POINTER(ctypes.c_float)
# ph_readaudio.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]


# int ph_hamming_distance(ulong64 hasha, ulong64 hashb);
# double* ph_audio_distance_ber(uint32_t *hasha, int Na, uint32_t *hashb, int Nb, float threshold, int block_size, int &Nc);

# ph_image_digest(const char *file, double sigma, double gamma, Digest &dig, N);
ph_image_digest = libphash.ph_image_digest
ph_image_digest.err_check = _phash_errcheck
ph_image_digest.restype = ctypes.c_int
ph_image_digest.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_double, DIGEST_P, ctypes.c_int]


def image_digest(filename, sigma=1.0, gamma=1.0, lines=180):
    """
    Use values sigma=1.0 and gamma=1.0 for now. N indicates the number of lines to project through the center for
    0 to 180 degrees orientation. Use 180. Be sure to declare a digest before calling the function, like this:
    """

    if isinstance(filename, bytes):
        filename_bytes = filename
    else:
        filename_bytes = filename.encode(FS_ENCODING)

    d = Digest()
    ph_image_digest(filename_bytes, sigma, gamma, d, lines)
    return d

# To compare two radial hashes, a peak of cross correlation is determined between two hashes:
# The peak of cross correlation between the two vectors is returned in the pcc parameter.

# int ph_crosscorr(Digest &x, Digest &y, double &pcc, double threshold=0.90);
ph_crosscorr = libphash.ph_crosscorr
ph_crosscorr.restype = ctypes.c_int
ph_crosscorr.err_check = _phash_errcheck
ph_crosscorr.argtypes = [DIGEST_P, DIGEST_P, ctypes.POINTER(ctypes.c_double), ctypes.c_double]


def cross_correlation(digest_1, digest_2, threshold=0.90):
    pcc = ctypes.c_double()
    ph_crosscorr(pointer(digest_1), pointer(digest_2), byref(pcc), threshold)
    return pcc.value

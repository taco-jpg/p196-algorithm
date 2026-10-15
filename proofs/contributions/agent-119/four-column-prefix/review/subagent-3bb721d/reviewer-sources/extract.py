import sys, tarfile, zstandard, os
src, dst = sys.argv[1], sys.argv[2]
with open(src, 'rb') as fh:
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        with tarfile.open(fileobj=reader, mode='r|') as tf:
            for m in tf:
                # refuse absolute paths / traversal
                if m.name.startswith('/') or '..' in m.name.split('/'):
                    print('SKIP suspicious', m.name); continue
                tf.extract(m, dst, filter='tar') if hasattr(tarfile, 'data_filter') else tf.extract(m, dst)
print('done')

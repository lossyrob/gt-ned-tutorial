import re, os
from subprocess import check_output, call

SITE = "ftp://www.pasda.psu.edu/pub/pasda/ned/10meter_quads/"

reNED = r"ned10m_([^\d]+)_(PA|NJ|NY)_.*\.zip"

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def main(old_cwd):
    if not which('gt-tool'):
        print "Must have gt-tool installed or in path!"
        return 1

    if not which('gdalwarp'):
        print "Need to install GDAL in order to reproject tiffs."
        return 2

    # If we're in the expected directory (root of source)
    # go into the data directory to download the data.
    if os.path.join(old_cwd,'data'):
        d = os.path.join(old_cwd,'data','ned')
        if not os.path.isdir(os.path.join(old_cwd,'data','ned')):
            d = os.path.join(old_cwd,'data','ned')
            os.makedirs(d)
        os.chdir(d)

    cmd = "curl " + SITE
    txt = check_output(cmd, shell=True)

    for m in re.finditer(reNED,txt):
        name = m.group(1).replace("_"," ") + ", " + m.group(2)
        fname = m.group(0)

        print "Downloading data for %s..." % name
        cmd = "wget %s%s" % (SITE,fname)
        call(cmd, shell=True)

        print "Unzipping data for %s..." % name
        cmd = "unzip -d tmp %s" % (fname)
        call(cmd, shell=True)

        print "Reprojecting data for %s..." % name
        tif = list(filter(lambda x: x.endswith('.tif'), os.listdir("tmp")))[0]
        wmtif = 'wm_' + tif
        cmd = "gdalwarp -t_srs EPSG:3857 tmp/%s tmp/%s" % (tif, wmtif)
        call(cmd, shell=True)

        print "Converting GeoTIFF to ARG for %s..." % name
        cmd = 'gt-tool geotiff_convert -i tmp/%s -o %s -n "%s" -t double' % \
            (wmtif, wmtif.replace('.tif','.arg'), name)
        call(cmd, shell=True)

        print "Cleaning up temp directory..."
        call("rm -r tmp", shell=True)

        print "Deleting archive file..."
        os.remove(fname)

    os.chdir(old_cwd)
    print "Done!"

if __name__ == "__main__":
    main(os.getcwd())

VERSION="NotForRelease"
PREFIX="WeatherDataServer_Install_Bundle"

if [ $# -eq 1 ]; then
    VERSION="$1"
fi

./make_manifest.sh $VERSION > ./manifest.xml

zip -r "${PREFIX}_version_${VERSION}.zip" ./manifest.xml ../run.py ../requirements.txt ../databrowser ../ccs_dlconfig ../static ../templates ./system







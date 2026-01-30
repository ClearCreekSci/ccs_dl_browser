VERSION="NotForRelease"
PREFIX="DataServer_Install_Bundle"

if [ $# -eq 1 ]; then
    VERSION="$1"
fi

./make_manifest.sh $VERSION > ./manifest.xml

rm -rf ../databrowser/__pycache__
zip -r "${PREFIX}_v${VERSION}.zip" ./settings.cfg ./manifest.xml ../run.py ../requirements.txt ../databrowser ../ccs_dlconfig/config.py ../ccs_dlconfig/manifest.py ../static ../templates ./system







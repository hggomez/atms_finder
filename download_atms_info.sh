wget  http://cdn.buenosaires.gob.ar/datosabiertos/datasets/cajeros-automaticos/cajeros-automaticos.csv
{ echo "id,long,lat,bank,network,address,city,terminals,unseeing,dollars,street,number,street2,district,commune,postal_code,argentinian_postal_code" & grep CABA cajeros-automaticos.csv; } > /tmp/tmp.csv
rm cajeros-automaticos.csv
mv /tmp/tmp.csv atms.csv

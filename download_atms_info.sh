wget  http://cdn.buenosaires.gob.ar/datosabiertos/datasets/cajeros-automaticos/cajeros-automaticos.csv
{ head -n 1 cajeros-automaticos.csv & grep CABA cajeros-automaticos.csv; } > /tmp/tmp.csv
mv /tmp/tmp.csv cajeros-automaticos.csv

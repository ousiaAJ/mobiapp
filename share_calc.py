import csv

def auslesenPreis(klasse, dauer, vers, km):
    if klasse == "XS":
        csvdatei = open("preiseXS.csv")
        csv_reader_object = csv.DictReader(csvdatei, delimiter=";")
    elif klasse == "S":
        csvdatei = open("preiseS.csv")
        csv_reader_object = csv.DictReader(csvdatei, delimiter=";")
    elif klasse == "M":
        csvdatei = open("preiseM.csv")
        csv_reader_object = csv.DictReader(csvdatei, delimiter=";")        
    #if "Tag" in dauer:
    vers = vers
    
    
    for row in csv_reader_object:
        dauer = str(dauer) + " Stunden"
        print(dauer)
        val1 = row.get(dauer)
        kmp = row.get("km")
    if vers == "J":
        val2 = row.get("Versicherung")
    if vers == "N":
        val2 = "0,0"
    val1 = val1.replace(",",".")
    val2 = val2.replace(",",".")
    kmp = kmp.replace(",",".")
    val3 = dauer.split()
    val3 = int(val3[0])
    ergv = val3 * float(val2)
    erg1 = float(val1) + ergv
    erg2 = km * float(kmp)
    ergf = erg1 + erg2
    ergf = round (ergf, 2)
    csvdatei.close()
    return (ergf)
        
#auslesenPreis("M", "3 Tage", "J", 100)
def parseVersion(text):
    updateH = {}
    nList = []
    for i in text.split("\n"):
        if(i == ""):
            updateH[version] = nList
            nList = []
        elif(i[0] == "-"):
            nList.append(i)
        else:
            version = i
    return updateH

parseVersion("""1.0
-1
-2
-3

1.2
-1
-2
-3

1.3
-Program için gerekli sürücülerin otomatik olarak yüklenmesi
-Programdaki hataların çözülmesi
-Sistem optimizasyonları

1.4
-Bazı uyarı, hata mesajlarının eklenmesi

1.5
-Sorunların düzeltilmesi
-Uyarı mesajlarının eklenmesi

1.6
-Ekranlara icon eklenmesi
-Sorunların düzeltilmesi

1.7
-Mesaj atarkenki program hatalarının düzeltilmesi
-Sorunların düzeltilmesi

1.8
-Mesaj Önizlemesi
-Resim,Dosya Ekleme
-Eklenilen dosya ve resimleri önizleyebilme
-Eklenilen dosya ve resimleri sıraya koyabilme

1.8.4
-Programın açılırken verdiği hataların düzeltilmesi
-Mesaj önizlemesindeki hataların çözülmesi
""")
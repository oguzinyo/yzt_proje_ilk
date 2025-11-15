import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

hava_durumu_df= pd.read_csv("munich.csv")
#bunların hepsi tek bir sütun columnlara bölelim
hava_durumu_df[['time', 'precipitation_sum (mm)', 'snowfall_sum (cm)']] = \
    hava_durumu_df['time;precipitation_sum (mm);snowfall_sum (cm)'].str.split(';', expand=True)

#eski column u silelim
hava_durumu_df = hava_durumu_df.drop(columns=['time;precipitation_sum (mm);snowfall_sum (cm)'])

#tip dönüşümlerini yapalım tarihi tarih olarak kaydedelim
#sayılar da string şuan integer a çevirelim

hava_durumu_df['time'] = pd.to_datetime(hava_durumu_df['time'])
hava_durumu_df['precipitation_sum (mm)'] = pd.to_numeric(hava_durumu_df['precipitation_sum (mm)'], errors='coerce')
hava_durumu_df['snowfall_sum (cm)'] = pd.to_numeric(hava_durumu_df['snowfall_sum (cm)'], errors='coerce')

#en fazla yağış alan 10 güne bakalım
#bu günler aykırı hava olayları olarak değerlendirilebilir

fazlayagis_df=hava_durumu_df.nlargest(10,"precipitation_sum (mm)")

# Bar grafiği ve PNG kaydı
fig, ax = plt.subplots(figsize=(10,6))
fazlayagis_df.plot(x="time", y="precipitation_sum (mm)", kind="bar", ax=ax)
plt.title("En Fazla Yağış Alan 10 Gün")
plt.xlabel("Tarih")
plt.ylabel("Yağış (mm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("fazlayagis_df.png")  # PNG olarak kaydet
plt.close()  # Grafiği kapat




#bu da bar grafiği
fazlayagis_df.plot(x="time",y="precipitation_sum (mm)",kind="bar")

#en fazla kar yağışı alan 10 güne bakalım
#bu günler aykırı hava olayları olarak değerlendirilebilir
fazlakar_df= hava_durumu_df.nlargest(10,"snowfall_sum (cm)")

fig, ax = plt.subplots(figsize=(10,6))
fazlakar_df.plot(x="time", y="snowfall_sum (cm)", kind="bar", ax=ax)
plt.title("En Fazla Kar Yağışı Alan 10 Gün")
plt.xlabel("Tarih")
plt.ylabel("Kar (cm)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("fazlakar_df.png")
plt.close()



#bu da bar grafiği
fazlakar_df.plot(x="time",y="snowfall_sum (cm)",kind="bar")


#iklim trenlerini inceleyelim
#bunun için önce index i time olarak ayarlayalım
hava_durumu_df.set_index('time', inplace=True)
hava_durumu_df=hava_durumu_df.dropna()


aylik_toplam_yagis = hava_durumu_df['precipitation_sum (mm)'].resample('ME').sum()
aylik_toplam_kar = hava_durumu_df['snowfall_sum (cm)'].resample('ME').sum()
#burada günlük verileri aylık olarak grupladık
#ve ME kullanarak ay sonu month end olarak ayarladık

aylik_trend_df = pd.DataFrame({
    'precipitation_sum (mm)': aylik_toplam_yagis,
    'snowfall_sum (cm)': aylik_toplam_kar
})
#burada da yeni bi dataframe oluşturduk

# Grafik ve PNG kaydı
fig, ax = plt.subplots(figsize=(12,6))
aylik_toplam_yagis.plot(ax=ax, color='blue', label='Yağış (mm)')
aylik_toplam_kar.plot(ax=ax, color='red', label='Kar (cm)')
plt.title("Aylık Yağış ve Kar Trendleri")
plt.xlabel("Tarih")
plt.ylabel("Miktar")
plt.legend()
plt.tight_layout()
plt.savefig("aylik_trend.png")
plt.close()






aylik_toplam_yagis.plot(x="precipitation_sum (mm)",y="time")

aylik_toplam_kar.plot(x="snowfall_sum (cm)",y="time")


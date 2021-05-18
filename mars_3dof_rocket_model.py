from vpython import *
from math import sin, cos, atan, degrees
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter

# Roket Bilgileri
yakit_mass = 4.349
motor_bos_mass = 7.032 - yakit_mass
roket_mass = 22.037 + motor_bos_mass
yanma_suresi = 4.2
yakit_tuketimi = yakit_mass / yanma_suresi


# Roket Tanımlamalar
R = 0.129 / 2   # roket karakteristik yarıçapı [m]
Aref = pi * R ** 2    # roket karakteristik alanı[m^2]
g= 9.804             #yer çekimi
theta = 85 *pi/180  # fırlatma açısı RADİAN

mach_girdi = [0.1,
0.2,
0.3,
0.4,
0.5,
0.6,
0.7,
0.8
]
CD_girdi = [0.39981,
0.401,
0.4008,
0.3996,
0.39954,
0.3988,
0.39973,
0.39938
]
eng_time = [0.01,
0.036,
0.053,
0.073,
0.089,
0.136,
0.182,
0.262,
0.364,
0.566,
1.387,
1.639,
1.986,
2.198,
2.457,
2.708,
2.831,
2.933,
3.036,
3.109,
3.175,
3.307,
3.45,
3.589,
3.698,
3.814,
3.996,
4.115,
4.201,
4.301]
eng_thrust = [2070.111,
1929.889,
2147.601,
2369.004,
2505.535,
2649.446,
2627.306,
2608.856,
2616.236,
2623.616,
2575.646,
2538.745,
2450.185,
2394.834,
2295.203,
2206.642,
2162.362,
2088.561,
1988.93,
1800.738,
1594.096,
1335.793,
1014.76,
708.487,
601.476,
461.255,
339.483,
202.952,
88.561,
0
]



#Atmosferik Tanımlamalar
Tb = 288.15  # [K] Katmanın temel sıcaklığı
Hb = 0   # [km] OrtalamadenizseviyesininüzerindekiTemelJeopotansiyelRakım
Pb = 101325  # [pa] temel statik basınç
Lb = -0.0065  # [K/km] -->> K/m  KilometreJeopotansiyelRakım BaşınaTemelSıcaklıkAtlama Oranı
g0 = 9.80665  # [ m/s^2]
M = 0.0289644  # [kg/mol] dünya havasının molar kütlesi
R = 8314.32  # [Nm/kmol*K] evrensel gaz sabiti
Rsp = 287.052  # [ J/kg*K ] spesifik gaz sabiti
gama = 1.4
a = 343.2    #ses hızı

mhi = InterpolatedUnivariateSpline(mach_girdi, CD_girdi)
thrust = InterpolatedUnivariateSpline(eng_time, eng_thrust)


#Başlangıç koşulları
ilk_hiz = 0.001
ilk_yol = 0  # roket x ekseni doğrultusunda

ilk_vx = 0.001
ilk_x = 0
ilk_vz = 0.001
ilk_z = 0

Mach = ilk_hiz / a

Drag = 0
Aci = theta #Aci = Beta

zaman = []

aci = []
kutle = []
itki = []
kuvet = []
ivme = []
hiz = []
yol = []

GlobalFx = []
GlobalFz = []
Globalax = []
Globalaz = []
Globalvx = []
Globalvz = []
irtifa = []
menzil = []


CD = []
drag = []

basinc = []
yogunluk = []
sicaklik = []
dinamik_basinc = []

mach = []


baslanngic_irtifasi = 970 #[m]


time = 0
dt = 0.01

while True:

    zaman.append(time)

    #Roket Modeli
    def Itki(t):
        if t <= yanma_suresi:
            return thrust(t)
        else:
            return 0
    def Agirlik(t):
        if t <= yanma_suresi:
            return roket_mass + yakit_mass - (yakit_tuketimi * time)
        else:
            return roket_mass

    kutle.append(Agirlik(time))
    itki.append(Itki(time))

    # Atmosfer Modeli
    Tm = Tb + Lb * (ilk_z + baslanngic_irtifasi - Hb)
    T = Tm
    sicaklik.append(T-272.15)  # Celsius
    #P = Pb * np.exp((-g0 * M * (ilk_H - Hb)) / (R * Tb))  Lb = 0 ise
    P = Pb * (Tb/Tm)**((g0*M)/(R*Lb))
    basinc.append(P)
    ro = P / (Rsp * T)
    yogunluk.append(ro)
    a = np.sqrt(gama*Rsp*T)
    DBasic = 0.5 * ro * ilk_hiz **2
    dinamik_basinc.append(DBasic)

    #Aerodinamik Model
    Drag = DBasic * Aref * mhi(Mach)
    drag.append(Drag)
    CD.append(mhi(Mach))

    #Kinematik Model
    #Body Frame
    Force = Itki(time) - Agirlik(time) * g * sin(Aci) - Drag
    kuvet.append(Force)

    Ivme = Force / Agirlik(time)
    ivme.append(Ivme)

    Hiz = ilk_hiz + Ivme * dt
    hiz.append(Hiz)

    Yol = ilk_yol + ilk_hiz * dt #path
    yol.append(Yol)


    # Launch Point Frame
    ForceX = Itki(time) * cos(Aci) - Drag * cos(Aci)
    GlobalFx.append(ForceX)

    ForceZ = Itki(time) * sin(Aci) - Drag * sin(Aci) - Agirlik(time) * g
    GlobalFz.append(ForceZ)

    IvmeX = ForceX / Agirlik(time)
    Globalax.append(IvmeX)

    IvmeZ = ForceZ / Agirlik(time)
    Globalaz.append(IvmeZ)

    HizX = ilk_vx + IvmeX * dt
    Globalvx.append(HizX)

    HizZ = ilk_vz + IvmeZ * dt
    Globalvz.append(HizZ)

    YolX = ilk_x + ilk_vx * dt
    menzil.append(YolX)

    YolZ = ilk_z + ilk_vz * dt
    irtifa.append(YolZ)


    Mach = ilk_hiz / a
    mach.append(Mach)

    Aci = atan(HizZ/HizX)
    aci.append(180/pi * Aci)


    if 5.9 < Yol < 6.1:
        RampaCikis_Hizi = Hiz


    ilk_hiz = Hiz
    ilk_yol = Yol

    ilk_vx = HizX
    ilk_x = YolX
    ilk_vz = HizZ
    ilk_z = YolZ

    time += dt

    if HizZ <= 0:
        break

plt.plot(zaman, irtifa)
plt.title("İrtifa[m]")
plt.xlabel("Zaman[s]")
plt.grid()
plt.show()


print("Apogee Time   :", time, "s")
print("Maximum Irtifa:",(max(irtifa)), "m")
print("Maximum Menzil:",(max(menzil)), "m")
print("Maximum Hız   :",max(hiz), "m/s")
print("Maximum Mach   :",max(mach), "M")
print("Maximum Ivme  :",max(ivme), "m/s^2")
print("Menzil(Apogee e kadar):",max(menzil), "m")
print("Rampa Çıkış Hızı:", RampaCikis_Hizi,"m/s")
print("Uçuş Boyunca Top. Kütle Değişimi", kutle[0]-kutle[-1],"kg")

output = xlsxwriter.Workbook('mars_output.xlsx')
outsheet = output.add_worksheet(('Fight Data'))

outsheet.write("A1","Zaman[s]")
outsheet.write("B1","irtifa[m]")
outsheet.write("C1","menzil[m]")
outsheet.write("D1","düşey ivme[m/s^2]")
outsheet.write("E1","yatay ivme[m/s^2]")
outsheet.write("F1","düşey hız[m/s]")
outsheet.write("G1","yatay hız[m/s]")
outsheet.write("H1","Mach sayısı")
outsheet.write("I1","Kütle[kg]")
outsheet.write("J1","Açı[deg]")

for t in range(1,len(zaman)):
    outsheet.write(t, 0, zaman[t])
    outsheet.write(t, 1, irtifa[t])
    outsheet.write(t, 2, menzil[t])
    outsheet.write(t, 3, Globalaz[t])
    outsheet.write(t, 4, Globalax[t])
    outsheet.write(t, 5, Globalvz[t])
    outsheet.write(t, 6, Globalvx[t])
    outsheet.write(t, 7, mach[t])
    outsheet.write(t, 8, kutle[t])
    outsheet.write(t, 9, aci[t])

output.close()

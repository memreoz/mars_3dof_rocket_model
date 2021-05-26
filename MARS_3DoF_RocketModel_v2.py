from vpython import *
from math import sin, cos, atan, degrees
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter

# Motor Bilgileri
M2020_yanma_suresi = 4.2  #s
M2020_yakit_mass = 4.349 #[kg]
M2020_yakit_debi = M2020_yakit_mass / M2020_yanma_suresi #[kg/s]
M2020_ISP = 197.6 # s
M2020_CFD_mach = [0.1,
0.2,
0.3,
0.4,
0.5,
0.6,
0.7,
0.8
]
M2020_CFD_CD = [0.39981,
0.401,
0.4008,
0.3996,
0.39954,
0.3988,
0.39973,
0.39938
]
M2020_time = [0.01,
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
M2020_thrust = [2070.111,
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
M2020_dia = 0.129 #[m]

# Veri Seti Tanımlamaları
M2500T_ISP = 209.5 #s
M2500T_time = [0.01,
0.02,
0.03,
0.04,
0.05,
0.06,
0.07,
0.08,
0.09,
0.1,
0.11,
0.12,
0.13,
0.14,
0.15,
0.16,
0.17,
0.18,
0.19,
0.2,
0.21,
0.22,
0.23,
0.24,
0.25,
0.26,
0.27,
0.28,
0.29,
0.3,
0.31,
0.32,
0.33,
0.34,
0.35,
0.36,
0.37,
0.38,
0.39,
0.4,
0.41,
0.42,
0.43,
0.44,
0.45,
0.46,
0.47,
0.48,
0.49,
0.5,
0.51,
0.52,
0.53,
0.54,
0.55,
0.56,
0.57,
0.58,
0.59,
0.6,
0.61,
0.62,
0.63,
0.64,
0.65,
0.66,
0.67,
0.68,
0.69,
0.7,
0.71,
0.72,
0.73,
0.74,
0.75,
0.76,
0.77,
0.78,
0.79,
0.8,
0.81,
0.82,
0.83,
0.84,
0.85,
0.86,
0.87,
0.88,
0.89,
0.9,
0.91,
0.92,
0.93,
0.94,
0.95,
0.96,
0.97,
0.98,
0.99,
1,
1.01,
1.02,
1.03,
1.04,
1.05,
1.06,
1.07,
1.08,
1.09,
1.1,
1.11,
1.12,
1.13,
1.14,
1.15,
1.16,
1.17,
1.18,
1.19,
1.2,
1.21,
1.22,
1.23,
1.24,
1.25,
1.26,
1.27,
1.28,
1.29,
1.3,
1.31,
1.32,
1.33,
1.34,
1.35,
1.36,
1.37,
1.38,
1.39,
1.4,
1.41,
1.42,
1.43,
1.44,
1.45,
1.46,
1.47,
1.48,
1.49,
1.5,
1.51,
1.52,
1.53,
1.54,
1.55,
1.56,
1.57,
1.58,
1.59,
1.6,
1.61,
1.62,
1.63,
1.64,
1.65,
1.66,
1.67,
1.68,
1.69,
1.7,
1.71,
1.72,
1.73,
1.74,
1.75,
1.76,
1.77,
1.78,
1.79,
1.8,
1.81,
1.82,
1.83,
1.84,
1.85,
1.86,
1.87,
1.88,
1.89,
1.9,
1.91,
1.92,
1.93,
1.94,
1.95,
1.96,
1.97,
1.98,
1.99,
2,
2.02,
2.04,
2.05,
2.06,
2.07,
2.08,
2.09,
2.1,
2.11,
2.12,
2.13,
2.14,
2.15,
2.16,
2.17,
2.18,
2.19,
2.2,
2.21,
2.22,
2.23,
2.24,
2.25,
2.26,
2.27,
2.28,
2.29,
2.3,
2.31,
2.32,
2.33,
2.34,
2.35,
2.36,
2.37,
2.38,
2.39,
2.4,
2.41,
2.42,
2.43,
2.44,
2.45,
2.46,
2.47,
2.48,
2.49,
2.5,
2.51,
2.52,
2.53,
2.54,
2.55,
2.56,
2.57,
2.58,
2.59,
2.6,
2.61,
2.62,
2.63,
2.64,
2.65,
2.66,
2.67,
2.68,
2.69,
2.7,
2.71,
2.72,
2.73,
2.74,
2.75,
2.76,
2.77,
2.78,
2.79,
2.8,
2.81,
2.82,
2.83,
2.84,
2.85,
2.86,
2.87,
2.88,
2.89,
2.9,
2.91,
2.92,
2.93,
2.94,
2.95,
2.96,
2.97,
2.98,
2.99,
3,
3.01,
3.02,
3.03,
3.04,
3.05,
3.06,
3.07,
3.08,
3.09,
3.1,
3.11,
3.12,
3.13,
3.14,
3.15,
3.16,
3.17,
3.18,
3.19,
3.2,
3.21,
3.22,
3.23,
3.24,
3.25,
3.26,
3.27,
3.28,
3.29,
3.3,
3.31,
3.32,
3.33,
3.34,
3.35,
3.36,
3.37,
3.38,
3.39,
3.4,
3.41,
3.42,
3.43,
3.44,
3.45,
3.46,
3.47,
3.48,
3.49,
3.5,
3.51,
3.52,
3.53,
3.54,
3.55,
3.56,
3.57,
3.58,
3.59,
3.6,
3.61,
3.62,
3.63,
3.64,
3.65,
3.66,
3.67,
3.68,
3.69,
3.7,
3.71,
3.72,
3.73,
3.74,
3.75,
3.76,
3.77,
3.78,
3.79,
3.8,
3.81,
3.82,
3.83,
3.84,
3.85,
3.86,
3.87,
3.88,
3.89,
3.9,
3.91,
3.92,
3.93,
3.94,
3.95,
3.96,
3.97,
3.98,
3.99,
4,
4.01,
4.03,
4.04,
4.05,
4.07,
4.08,
4.09,
4.1,
4.11,
4.12,
4.13,
4.14,
4.15,
4.16,
4.17,
4.18,
4.19,
4.2,
4.21,
4.22,
4.23,
4.24,
4.25,
4.26,
4.27
]
M2500T_thrust = [2587.18,
2587.18,
2587.18,
2587.18,
2587.18,
2587.18,
2587.18,
2587.18,
2658.012,
2665.702,
2673.391,
2681.081,
2688.771,
2696.461,
2704.151,
2711.841,
2719.53,
2727.22,
2734.91,
2742.6,
2750.29,
2757.98,
2765.669,
2773.359,
2780.522,
2782.944,
2785.367,
2787.789,
2790.211,
2792.633,
2795.055,
2797.477,
2799.899,
2802.322,
2804.744,
2807.166,
2809.588,
2812.01,
2814.432,
2816.855,
2819.277,
2821.264,
2822.598,
2823.932,
2825.266,
2826.6,
2827.934,
2829.268,
2830.603,
2831.937,
2833.271,
2834.605,
2835.939,
2837.273,
2838.607,
2839.941,
2841.276,
2842.61,
2843.208,
2843.491,
2843.773,
2844.056,
2844.339,
2844.622,
2844.904,
2845.187,
2845.47,
2845.753,
2846.035,
2846.318,
2846.601,
2846.884,
2847.166,
2847.449,
2847.732,
2847.946,
2848.154,
2848.361,
2848.568,
2848.775,
2848.982,
2849.19,
2849.397,
2849.604,
2849.811,
2850.018,
2850.226,
2850.433,
2850.64,
2850.847,
2851.054,
2851.262,
2851.474,
2851.687,
2851.899,
2852.111,
2852.323,
2852.535,
2852.747,
2852.959,
2853.171,
2853.383,
2853.595,
2853.807,
2854.019,
2854.231,
2854.443,
2854.655,
2854.988,
2855.402,
2855.816,
2856.229,
2856.643,
2857.057,
2857.47,
2857.884,
2858.298,
2858.711,
2859.125,
2859.539,
2859.953,
2860.366,
2860.78,
2861.194,
2861.607,
2861.519,
2861.304,
2861.09,
2860.876,
2860.661,
2860.447,
2860.233,
2860.019,
2859.804,
2859.59,
2859.376,
2859.161,
2858.947,
2858.733,
2858.519,
2858.304,
2858.09,
2857.668,
2857.247,
2856.825,
2856.403,
2855.982,
2855.56,
2855.138,
2854.717,
2854.295,
2853.873,
2853.451,
2853.03,
2852.608,
2852.186,
2851.765,
2851.343,
2850.936,
2850.551,
2850.166,
2849.781,
2849.395,
2849.01,
2848.625,
2848.24,
2847.855,
2847.47,
2847.085,
2846.7,
2846.315,
2845.929,
2845.544,
2845.159,
2844.774,
2844.129,
2843.31,
2842.49,
2841.671,
2840.852,
2840.033,
2839.214,
2838.395,
2837.576,
2836.757,
2835.938,
2835.119,
2834.3,
2833.481,
2832.662,
2831.843,
2831.024,
2829.607,
2828.041,
2826.476,
2824.91,
2823.344,
2821.778,
2820.212,
2818.646,
2815.514,
2812.383,
2810.817,
2809.251,
2807.685,
2806.119,
2804.476,
2802.132,
2799.788,
2797.444,
2795.1,
2792.756,
2790.412,
2788.068,
2785.724,
2783.38,
2781.036,
2778.692,
2776.348,
2774.004,
2771.66,
2769.316,
2766.972,
2764.154,
2760.863,
2757.572,
2754.281,
2750.99,
2747.699,
2744.408,
2741.117,
2737.826,
2734.535,
2731.244,
2727.953,
2724.662,
2721.371,
2718.079,
2714.788,
2711.497,
2707.916,
2704.211,
2700.506,
2696.8,
2693.095,
2689.389,
2685.684,
2681.979,
2678.273,
2674.568,
2670.863,
2667.157,
2663.452,
2659.747,
2656.041,
2652.336,
2648.631,
2644.934,
2641.238,
2637.542,
2633.846,
2630.151,
2626.455,
2622.759,
2619.063,
2615.368,
2611.672,
2607.976,
2604.28,
2600.584,
2596.889,
2593.193,
2589.497,
2585.729,
2581.794,
2577.858,
2573.922,
2569.986,
2566.051,
2562.115,
2558.179,
2554.244,
2550.308,
2546.372,
2542.436,
2538.501,
2534.565,
2530.629,
2526.694,
2522.758,
2519.047,
2515.561,
2512.074,
2508.588,
2505.102,
2501.615,
2498.129,
2494.643,
2491.156,
2487.67,
2484.184,
2480.697,
2477.211,
2473.725,
2470.239,
2466.752,
2463.266,
2460.437,
2457.89,
2455.343,
2452.796,
2450.249,
2447.702,
2445.155,
2442.608,
2440.061,
2437.514,
2434.967,
2432.42,
2429.873,
2427.326,
2424.779,
2422.232,
2416.796,
2385.359,
2353.922,
2322.485,
2291.048,
2259.611,
2228.174,
2196.736,
2165.299,
2133.862,
2102.425,
2070.988,
2039.551,
2008.114,
1976.677,
1945.239,
1913.802,
1869.062,
1804.365,
1739.669,
1674.973,
1610.277,
1545.58,
1480.884,
1416.188,
1351.492,
1286.795,
1222.099,
1157.403,
1092.707,
1028.01,
963.314,
898.618,
833.922,
789.158,
757.682,
726.207,
694.731,
663.256,
631.78,
600.305,
568.83,
537.354,
505.879,
474.403,
442.928,
411.452,
379.977,
348.501,
317.026,
285.551,
272.458,
261.409,
250.359,
239.31,
228.26,
217.211,
206.161,
195.112,
184.062,
173.013,
161.963,
150.914,
139.864,
128.815,
117.765,
106.716,
97.002,
92.634,
88.266,
83.898,
79.53,
75.162,
70.794,
66.426,
62.058,
53.321,
48.953,
44.585,
35.849,
31.481,
27.113,
23.909,
22.451,
20.993,
19.535,
18.077,
16.62,
15.162,
13.704,
12.246,
10.788,
9.33,
7.872,
6.415,
4.957,
3.499,
2.041,
0.583,
0
]
M2500T_mach = [0.1,
0.2,
0.3,
0.4,
0.5,
0.6,
0.7,
0.8,
0.9,
1
]
M2500T_CD = [0.434,
0.3954,
0.3752,
0.3617,
0.3515,
0.3429,
0.3359,
0.3309,
0.3293,
0.37
]
M2500T_yanma_suresi = 4.27 #s
M2500T_mass = 25-4.659
M2500T_yakit_mass = 4.659 #[kg]
M2500T_yakit_debi = M2500T_yakit_mass/M2500T_yanma_suresi #[kg/s]
M2500T_dia = 0.14 #[m]

eng = int(input("Motor Sec:"))
if eng == 1:
    mach_girdi = M2020_CFD_mach
    CD_girdi =  M2020_CFD_CD
    eng_time = M2020_time
    eng_thrust = M2020_thrust
    yakit_mass = M2020_yakit_mass
    yanma_suresi = M2500T_yanma_suresi
    yakit_debi = M2020_yakit_debi
    dia = M2020_dia
elif eng == 2:
    mach_girdi = M2500T_mach
    CD_girdi = M2500T_CD
    eng_time = M2500T_time
    eng_thrust = M2500T_thrust
    yakit_mass = M2500T_yakit_mass
    yanma_suresi = M2500T_yanma_suresi
    yakit_debi = M2020_yakit_debi
    dia = M2500T_dia

motor_bos_mass = 7.032 - yakit_mass
roket_mass = 22.035 + motor_bos_mass

R = dia / 2   # roket karakteristik yarıçapı [m]
Aref = pi * R ** 2    # roket karakteristik alanı[m^2]
g= 9.804             #yer çekimi
theta = 85 * pi / 180  # fırlatma açısı RADİAN

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
ilk_hiz = 0.5
ilk_yol = 0  # roket x ekseni doğrultusunda

ilk_vx = 0
ilk_x = 0
ilk_vz = 0
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
    itki.append(Itki(time))
    def Mass(t):
        if t <= yanma_suresi:
            return roket_mass + yakit_mass - (yakit_debi * time)
        else:
            return roket_mass
    kutle.append(Mass(time))

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
    Force = Itki(time) - Mass(time) * g * sin(Aci) - Drag
    kuvet.append(Force)

    Ivme = Force / Mass(time)
    ivme.append(Ivme)

    Hiz = ilk_hiz + Ivme * dt
    hiz.append(Hiz)

    Yol = ilk_yol + ilk_hiz * dt #path
    yol.append(Yol)

    # Launch Point Frame
    ForceX = Itki(time) * cos(Aci) - Drag * cos(Aci)
    GlobalFx.append(ForceX)

    ForceZ = Itki(time) * sin(Aci) - Drag * sin(Aci) - Mass(time) * g
    GlobalFz.append(ForceZ)

    IvmeX = ForceX / Mass(time)
    Globalax.append(IvmeX)

    IvmeZ = ForceZ / Mass(time)
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

    if 5.5 < Yol < 6.5:
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

plt.plot(zaman, kutle)
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
print("Rampa Çıkış Hızı:", RampaCikis_Hizi,"m/s")
print("Uçuş Boyunca Top. Kütle Değişimi", kutle[0]-kutle[-1],"kg")

if eng == 1:
    eng_name = "M2020 "
elif eng == 2:
    eng_name = "M2500T "

output = xlsxwriter.Workbook('mars_'+eng_name+'output.xlsx')
outsheet = output.add_worksheet((eng_name+"Simulation Results"))

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
outsheet.write("K1","Hız[m/s]")

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
    outsheet.write(t, 10, hiz[t])
output.close()

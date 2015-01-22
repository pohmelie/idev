import collections
from math import asin, atan, atan2, sin, cos, pi


def plavun(data):

    prm = 57.296
    e0_Nosit = float(data["Проекция угла наклона ε0"])
    e1_Nosit = float(data["Проекция угла наклона ε1"])
    Alfa_celi_Nosit = float(data["Угол цели α (t0)"])
    Beta_celi_Nosit = float(data["Угол цели β (t0)"])
    D_celi_Nosit = float(data["Дистанция до цели (t0)"])
    Uglubl_Nosit = float(data["Углубление МК"])
    fi0_Nosit = float(data["Угол поворота МК (t0)"])
    fi1_Nosit = float(data["Угол поворота МК (t1)"])

    if abs(e0_Nosit) < 0.3:

        if abs(e1_Nosit) < 0.3:

            e = delt = 0

        else:

            delt = 90 if e1_Nosit > 0 else 270
            e = asin(sin(e1_Nosit / prm) / cos((delt + 60) / prm)) * prm

    else:

        aa = sin(e0_Nosit / prm) * cos(60 / prm) - sin(e1_Nosit / prm)
        bb = sin(e0_Nosit / prm) * sin(60 / prm)
        de = atan(aa / bb) * prm
        if e0_Nosit < 0:

            delt = -de + 180

        else:

            delt = -de if de < 0 else -de + 360

        e = asin(sin(e0_Nosit / prm) / cos(delt / prm)) * prm

    lamb = Alfa_celi_Nosit - 50 - delt
    Cx = cos(Beta_celi_Nosit / prm) * cos(lamb / prm) * cos(e / prm) + sin(Beta_celi_Nosit / prm) * sin(e / prm)
    Cy = -cos(Beta_celi_Nosit / prm) * cos(lamb / prm) * sin(e / prm) + sin(Beta_celi_Nosit / prm) * cos(e / prm)
    Cz = -cos(Beta_celi_Nosit / prm) * sin(lamb / prm)
    mu = 0 if Cx == 0 else atan(Cz / Cx) * prm
    Xg_c = D_celi_Nosit * Cx
    Yg_c = D_celi_Nosit * Cy
    Zg_c = D_celi_Nosit * Cz
    H_c = -Yg_c + Uglubl_Nosit
    dH_c = -Yg_c
    Qet_ras_o = asin(Cy) * prm
    if Cx == 0:

        if Cz == 0:

            Psi_ras_o = 0

        elif Cz < 0:

            Psi_ras_o = 90

        else:

            Psi_ras_o = -90

    elif Cx > 0:

        Psi_ras_o = -mu

    elif Cz > 0:

        Psi_ras_o = -mu - 180

    else:

        Psi_ras_o = -mu + 180

    fi00 = 360 - fi0_Nosit
    Ugol_hi = -(delt + fi00)
    chi = cos(Ugol_hi / prm)
    shi = sin(Ugol_hi / prm)
    Xnc = Xg_c * chi - Zg_c * shi
    Ync = Yg_c
    Znc = Xg_c * shi + Zg_c * chi
    mun = 0 if Xnc == 0 else atan(Znc / Xnc) * prm
    if Xnc == 0:

        if Znc == 0:

            Psi_ras = 0

        elif Znc < 0:

            Psi_ras = 90

        else:

            Psi_ras = -90

    elif Xnc > 0:

        Psi_ras = -mun

    elif Znc > 0:

        Psi_ras = -mun - 180

    else:

        Psi_ras = -mun + 180

    Qet_ras = asin(Cy) * prm
    dfi = fi0_Nosit - fi1_Nosit
    delt1 = delt - dfi
    C11 = sin(e / prm)
    C12 = cos(e / prm)
    C13 = 0
    C21 = cos((delt1 + 50) / prm) * cos(e / prm)
    C22 = -cos((delt1 + 50) / prm) * sin(e / prm)
    C23 = sin((delt1 + 50) / prm)
    C31 = sin((delt1 + 50) / prm) * cos(e / prm)
    C32 = -sin((delt1 + 50) / prm) * sin(e / prm)
    C33 = -cos((delt1 + 50) / prm)

    C11 = chi * sin(e / prm)
    C12 = cos(e / prm)
    C13 = shi * sin(e / prm)
    C21 = chi * cos(e / prm) * cos((delt1 + 50) / prm) - shi * sin((delt1 + 50) / prm)
    C22 = -sin(e / prm) * cos((delt1 + 50) / prm)
    C23 = shi * cos(e / prm) * cos((delt1 + 50) / prm) + chi * sin((delt1 + 50) / prm)
    C31 = chi * cos(e / prm) * sin((delt1 + 50) / prm) + shi * cos((delt1 + 50) / prm)
    C32 = -sin(e / prm) * sin((delt1 + 50) / prm)
    C33 = shi * cos(e / prm) * sin((delt1 + 50) / prm) - chi * cos((delt1 + 50) / prm)

    c11 = C11
    c12 = C21
    c13 = C31
    c21 = C12
    c22 = C22
    c23 = C32
    c31 = C13
    c32 = C23
    c33 = C33

    qet_n = asin(c21)
    if abs(c21) < 0.99999:

        psi_n = atan2(-c31, c11)
        gam_n = atan2(-c23, c22)

    else:

        psi_n = 0
        gam_n = atan2(c13, c33)

    Y0 = -Uglubl_Nosit

    return collections.OrderedDict((
        ("ψ₀", psi_n * prm),
        ("θ₀", qet_n * prm),
        ("γ₀", gam_n * prm),
        ("Y₀", Y0),
    ))


if __name__ == "__main__":

    d = {
        "Проекция угла наклона ε0": 2.1,
        "Проекция угла наклона ε1": 2.7,
        "Угол цели α (t0)": 290,
        "Угол цели β (t0)": 10,
        "Дистанция до цели (t0)": 810,
        "Углубление МК": 260,
        "Угол поворота МК (t0)": 290,
        "Угол поворота МК (t1)": 290,
    }
    print(plavun(d))

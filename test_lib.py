import pandas as pd
from math import floor


def E_off_calc(tmp_V, tmp_I, tmp_T):
    # Eoff[mJ]計算
    # 空のデータシリーズの作成
    f = pd.Series([0], index=["VCE[V]"])
    g = pd.Series([0], index=["IC[A]"])
    h = pd.Series([0], index=["Time(sec)"])
    # 空のデータシリーズを先頭と末尾に挿入
    # 各要素の2ステップごとの平均を計算する
    Eoff_data = ((f.append(tmp_V, ignore_index=True) + tmp_V.append(f, ignore_index=True)) / 2) \
                * ((g.append(tmp_I, ignore_index=True) + tmp_I.append(g, ignore_index=True)) / 2) \
                * (tmp_T.append(h, ignore_index=True) - h.append(tmp_T, ignore_index=True)) * 1000
    # 探索方法が違う理由が不明だが、動いている
    Vce_3 = tmp_V[(tmp_V <= (tmp_V.tail(100).mean() * 0.03))].size + 1
    Ic_0 = tmp_I[(tmp_I <= (tmp_I.tail(100).mean() * 0))].head(1) + 1
    E_off_data = Eoff_data[Vce_3:Ic_0.index.values.min()].sum()
    return E_off_data


def E_on_calc(tmp_V, tmp_I, tmp_T):
    # Eon[mJ]計算
    # 空のデータシリーズの作成
    f = pd.Series([0], index=["VCE[V]"])
    g = pd.Series([0], index=["IC[A]"])
    h = pd.Series([0], index=["Time(sec)"])

    Eon_mJ = ((f.append(tmp_V, ignore_index=True) + tmp_V.append(f, ignore_index=True)) / 2) \
             * ((g.append(tmp_I, ignore_index=True) + tmp_I.append(g, ignore_index=True)) / 2) \
             * ((tmp_T.append(h, ignore_index=True) - h.append(tmp_T, ignore_index=True)) * 1000)

    Ic_size = tmp_I[(tmp_I >= round(Ic_calc(tmp_I) * 0.1))]
    Vce_3 = tmp_V[(tmp_V <= tmp_V.head(100).mean() * 0.03)]
    E_on_data = round(Eon_mJ[Ic_size.index.values.min():Vce_3.index.values.min() + 1].sum(), 2)
    return E_on_data


def VceT_calc(tmp_V):
    # VCE計算
    vce_data = floor(tmp_V.tail(100).mean())
    return vce_data


def VceH_calc(tmp_V):
    # Turn ON時のVCE計算
    Vce_H_data = floor(tmp_V.head(100).mean())
    return Vce_H_data


def Ic_calc(tmp_I):
    # IC計算
    Ic_data = floor(tmp_I.tail(100).mean())
    return Ic_data


def Vcep_calc(tmp_V):
    # Vcep計算
    Vce_Max = tmp_V.max()
    return Vce_Max


def Icp_calc(tmp_I):
    # ICp計算
    Icp_data = round(tmp_I.max())
    return Icp_data


def VgeM_calc(tmp_VGE):
    # Vge最大値
    Vge_max = tmp_VGE.max()
    return Vge_max


def Vget_calc(tmp_VGE):
    # Vgeラスト100行の平均値
    Vget_data = floor(tmp_VGE.tail(100).mean())
    return Vget_data


def Tf_calc(tmp_I):
    # tf計算
    Ic_90 = Icp_calc(tmp_I) * 0.9
    Ic_10 = Icp_calc(tmp_I) * 0.1
    tf_data = tmp_I[(tmp_I <= float(Ic_90)) & (tmp_I >= float(Ic_10))]
    return tf_data


def Tr_calc(tmp_I):
    Ic_90 = Ic_calc(tmp_I) * 0.9
    Ic_10 = Ic_calc(tmp_I) * 0.1
    tr_data = tmp_I[(tmp_I <= float(Ic_90)) & (tmp_I >= float(Ic_10))].size
    return tr_data


def dvdt_calc(tmp_V) -> object:
    # dV/dt計算
    Vce_80 = ((tmp_V.tail(100).sum()).mean() * 0.8) / 100
    Vce_20 = ((tmp_V.tail(100).sum()).mean() * 0.2) / 100
    if Vce_80 == 0:
        Vce_80 = round(((tmp_V.head(100).sum()).mean() * 0.8) / 100)
        Vce_20 = round(((tmp_V.head(100).sum()).mean() * 0.2) / 100)
    dvdt_range = tmp_V[(tmp_V >= float(Vce_20)) & (tmp_V <= float(Vce_80))]
    dvdt_data = round((((Vce_80 - Vce_20) / 1000) /
                       ((dvdt_range.index.values.max() - dvdt_range.index.values.min()) * 1E-9 * 1000000)), 2)
    return dvdt_data


def didt_calc(tmp_I) -> object:
    # dV/dt計算
    Ice_90 = ((tmp_I.tail(100).sum()).mean() * 0.9) / 100
    Ice_10 = ((tmp_I.tail(100).sum()).mean() * 0.1) / 100
    didt_range = tmp_I[(tmp_I >= float(Ice_10)) & (tmp_I <= float(Ice_90))]
    didt_data = round((((Ice_90 - Ice_10) / 1000) / (didt_range.size * 1E-9 * 1000000)), 2)
    return didt_data


def td_off_calc(tmp_VGE, tmp_I):
    # td(off)計算
    Ic_90 = Icp_calc(tmp_I) * 0.9
    Vge_90 = tmp_VGE.head(100).mean() * 0.9
    td_off_data = (tmp_I[(tmp_I >= Ic_90)].size
                   - tmp_VGE[(tmp_VGE >= Vge_90)].size) * 1E-9 * 1000000
    return td_off_data


def td_on_calc(tmp_I, tmp_VGE):
    # td(on)計算
    Ic_10 = round(Ic_calc(tmp_I) * 0.1)
    Vge_10 = Vget_calc(tmp_VGE) * 0.1
    td_on_data = round((tmp_I[(tmp_I <= Ic_10)].size
                        - tmp_VGE[(tmp_VGE <= Vge_10)].size) * 1E+9 * 1E-9)
    return td_on_data


if __name__ == '__main__':
    print('実行されない')

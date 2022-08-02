import glob

import pandas as pd
import sandbox
import makechart
import re

import test_lib as tl


class calculatede_library:
    @staticmethod

    @staticmethod
    # ファイル名のソート用
    def result_sort(result):
        result_index = result.set_index('FileName')
        result_sort = result_index.sort_values('BBTNo', na_position='first')
        return result_sort

    @staticmethod
    # ファイル名からBBT番号だけを切り取って新たなデータフレームを作成
    def BBTNo_generate(csv_data):
        comp_pattern = re.compile(r'BBT[\d]+')
        BBTNo_pattern = re.compile(r'[\d]+')
        filename = comp_pattern.search(csv_data)
        BBTNo = BBTNo_pattern.search(filename.group())
        return BBTNo, filename

    def eon_calc(self, e_var):
        fp = glob.glob(e_var + '\\*.csv')
        result = pd.DataFrame({'Eon': ['mJ'], 'td(on)': ['nsec'], 'tr': ['nsec'], 'dV/dt': ['kV/μsec'],
                               'dI/dt': ['kA/μsec'], 'Ic': ['A'], 'Icp': ['A'], 'Vce': ['V']}, index=['FileName'])
        fpc = len(fp)
        print('file数' + str(fpc) + 'を読み込み')
        for csv_data in fp:
            tmp = pd.read_csv(csv_data, names=('VCE[V]', 'IC[A]', 'VGE[V]', 'POW[W]', 'Time(sec)'), header=38)
            tmp_T = tmp['Time(sec)']
            # 装置誤差まるめ（オフセット計算）
            tmp_V = tmp['VCE[V]'] - tmp['VCE[V]'].tail(100).mean()
            tmp_I = tmp['IC[A]'] - tmp['IC[A]'].head(100).mean()
            tmp_VGE = tmp['VGE[V]'] - tmp['VGE[V]'].head(100).mean()
            makechart.make_chart(self, e_var, tmp_V, tmp_I, tmp_VGE, tmp_T)
            BBTNo = self.BBTNo_generate(csv_data)[0]
            filename = self.BBTNo_generate(csv_data)[1]
            result_token1 = pd.DataFrame({'FileName': [filename.group()],
                                          'BBTNo': [BBTNo.group().zfill(3)],
                                          'Eon': [tl.E_on_calc(tmp_V, tmp_I, tmp_T)],
                                          'td(on)': [tl.td_on_calc(tmp_I, tmp_VGE)],
                                          'tr': [tl.Tr_calc(tmp_I)],
                                          'dV/dt': [tl.dvdt_calc(tmp_V)],
                                          'dI/dt': [tl.didt_calc(tmp_I)],
                                          'Ic': [tl.Ic_calc(tmp_I)],
                                          'Icp': [tl.Icp_calc(tmp_I)],
                                          'Vce': [tl.VceH_calc(tmp_V)]})
            result = pd.concat([result, result_token1])
        eon_result = self.result_sort(result)

        return eon_result

    def RBSOA_eoff_calc(self, e_var):
        # プログラム1｜ライブラリの設定
        fp = glob.glob(e_var + '\\*.csv')
        df = pd.DataFrame()
        fpc = len(fp)
        result = pd.DataFrame({'Eon': ['mJ'], 'td(off)': ['μsec'], 'tf': ['nsec'], 'dV/dt': ['kV/μsec'],
                               'Icp': ['A'], 'Vce': ['V'], 'Vcep': ['V']}, index=['unit'])
        print('file数' + str(fpc) + 'を読み込み')

        for csv_data in fp:
            # 基礎データ設定 宣言など
            tmp = pd.read_csv(csv_data, names=('VCE[V]', 'IC[A]', 'VGE[V]', 'POW[W]', 'Time(sec)'), header=39)
            tmp_T = tmp['Time(sec)']
            # 装置誤差まるめ（オフセット計算）
            tmp_V = tmp['VCE[V]'] - tmp['VCE[V]'].head(100).mean()
            tmp_I = tmp['IC[A]'] - tmp['IC[A]'].tail(100).mean()
            tmp_VGE = tmp['VGE[V]'] - tmp['VGE[V]'].tail(100).mean()

            result_token = pd.DataFrame({'Eon': [tl.E_off_calc(tmp_V, tmp_I, tmp_T)],
                                         'td(off)': [tl.td_off_calc(tmp_I, tmp_VGE)],
                                         'tf': [tl.Tf_calc(tmp_I)],
                                         'dV/dt': [tl.dvdt_calc(tmp_V)],
                                         'Icp': [tl.Icp_calc(tmp_I)],
                                         'Vce': [tl.VceT_calc(tmp_V)],
                                         'Vcep': [tl.Vcep_calc(tmp_V)]})
            result = pd.concat([result, result_token])


e_var = sandbox.x
gebgeb = calculatede_library()
print(gebgeb.eon_calc(e_var))

# Excelへ書き込み
# with pd.ExcelWriter(e_var + '\\sliced_data.xlsx') as wr:
#     df.to_excel(wr, sheet_name='Data')


#
# if __name__ == '__main__':
#     print('実行されない')

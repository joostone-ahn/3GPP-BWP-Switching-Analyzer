import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui
import time_calc

CourierNewFont = QtGui.QFont()
CourierNewFont.setFamily("Courier New")

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        bwp = ''

        self.open_btn = QPushButton("Open")
        self.open_btn.setFixedWidth(300)
        self.open_btn.setCheckable(False)
        self.open_btn.clicked.connect(self.load_msg)

        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.te.setFixedHeight(150)
        self.te.setFixedWidth(300)
        self.te.setFont(CourierNewFont)

        self.Exe_btn = QPushButton("Execute")
        self.Exe_btn.setFixedWidth(300)
        self.Exe_btn.setCheckable(False)
        self.Exe_btn.clicked.connect(self.extract)

        self.rst = QTextBrowser()
        self.rst.setAcceptRichText(False)
        self.rst.setFixedHeight(100)
        self.rst.setFixedWidth(300)


        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("<Opt.1> Directly paste input."))
        vbox.addWidget(self.te)
        vbox.addWidget(self.Exe_btn)
        vbox.addWidget(QLabel())
        vbox.addWidget(QLabel("<Opt.2> Open text file(*.txt) including input."))
        vbox.addWidget(self.open_btn)
        vbox.addWidget(QLabel())
        vbox.addWidget(self.rst)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('BWP Ind Time')
        self.show()

    @pyqtSlot()
    def load_msg(self):
        fname = QFileDialog.getOpenFileName(self,'Load file','',"Text files(*.txt)")
        opened_file = '> File : ' + fname[0]
        if fname[0]:
            f = open(fname[0],'rt',encoding='UTF8') #https://m.blog.naver.com/yejoon3117/221058408177
            with f:
                try:
                    msg_all = f.readlines()
                except:
                    print("read fail")
                for n in range(len(msg_all)):
                    msg_all[n] = msg_all[n].replace('\n', '')
                # for n in msg_all:
                #     print(n)
                self.te.clear()
                self.calc(msg_all)

    @pyqtSlot()
    def extract(self):
        bwp_str = self.te.toPlainText()
        bwp = bwp_str.split('\n')
        self.calc(bwp)


    def calc(self,bwp):
        time_list = []
        bwp_ind_list = []
        for n in bwp:
            if n != '':
                if 'TIME' not in n :
                    if 'BWP' not in n :
                        if n.split('\t')[1]:
                            time_list.append(n.split('\t')[0])
                            bwp_ind_list.append(n.split('\t')[1])

        for n in range(len(time_list)):
            if ' ' in time_list[n]:
                time_list[n] = time_list[n].split(' ')[1]

        # print(time_list)
        # print(bwp_ind_list)

        bwp_start = []
        bwp_id = []
        bwp_id_prev = 0

        for n in range(len(bwp_ind_list)):
            if bwp_id_prev != int(bwp_ind_list[n]):
                bwp_id_prev = int(bwp_ind_list[n])
                bwp_start.append(n)
                bwp_id.append(int(bwp_ind_list[n]))
            if n == len(bwp_ind_list)-1:
                bwp_start.append(n)

        # print(bwp_id)
        # print(bwp_start)

        bwp1_time = []
        bwp2_time = []
        for n in range(len(bwp_id)):
            if bwp_id[n] == 1:
                a = time_calc.time_abs(time_list[bwp_start[n]])
                b = time_calc.time_abs(time_list[bwp_start[n+1]])
                c = time_calc.time_diff(a,b)
                bwp1_time.append(c)
            elif bwp_id[n] == 2:
                a = time_calc.time_abs(time_list[bwp_start[n]])
                b = time_calc.time_abs(time_list[bwp_start[n+1]])
                c = time_calc.time_diff(a,b)
                bwp2_time.append(c)

        # print(bwp1_time)
        # print(bwp2_time)

        rst_dsp = ''
        bwp1_sum = 0
        for n in bwp1_time:
            bwp1_sum += time_calc.time_abs(n)
            bwp1_sum = round(bwp1_sum,3)
        # print(bwp1_sum)

        bwp2_sum = 0
        for n in bwp2_time:
            bwp2_sum += time_calc.time_abs(n)
            bwp2_sum = round(bwp2_sum,3)
        # print(bwp2_sum)

        a = time_calc.time_abs(time_list[0])
        b = time_calc.time_abs(time_list[len(time_list)-1])
        c = time_calc.time_diff(a,b)
        d = len(bwp_id)-1

        rst_dsp = 'BWP Switching Count : ' + str(d) + '\n'
        rst_dsp += '-' * 38 + '\n'
        rst_dsp += 'Total : ' + c +'\n'
        rst_dsp += 'BWP#1 : ' + time_calc.time_ext(bwp1_sum)
        rst_dsp += ' (' + str(round(100*bwp1_sum/(bwp1_sum+bwp2_sum),1)) +'%)\n'
        rst_dsp += 'BWP#2 : ' + time_calc.time_ext(bwp2_sum)
        rst_dsp += ' (' + str(round(100*bwp2_sum/(bwp1_sum+bwp2_sum),1)) +'%)'

        # print(rst_dsp)

        self.rst.setText(rst_dsp)
        self.rst.setFont(CourierNewFont)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
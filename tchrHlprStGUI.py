from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import socket

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.title = 'Teacher Helper'
        self.setWindowTitle(self.title)


        self.studentNum = 0

        self.studentNames = []
        self.studentAddresses = []
        self.studentAges = []
        #self.studentInfo = {}

        #self.studentIPs = []
        self.studentCheckboxes = []
        self.studentButtons = []
        self.launchMinecraftPSButtons = []
        self.launchMinecraftPRButtons = []
        self.closeMinecraftButtons = []
        #self.studentLockStates = []
        self.studentLayouts = []
        self.studentLabelsIcons = []
        self.studentLabels = []
        self.layoutV = QVBoxLayout()

        mainCheckbox = QCheckBox('Всі учні')
        mainCheckbox.setFont(QFont('SansSerif', 10))

        mainCheckbox.setChecked(True)
        mainCheckbox.stateChanged.connect(self.checkEverybody)

        self.lockAllButton = QPushButton('')
        self.lockAllButton.setCheckable(True)
        self.lockAllButton.setChecked(False)
        self.lockAllButton.toggled.connect(self.lockEveryChecked)
        self.lockAllButton.setIcon(QIcon('unlocked.png'))
        self.lockAllButton.setIconSize(QSize(100,30))

        self.launchMinecraftPSForAllButton = QPushButton('')
        self.launchMinecraftPSForAllButton.setChecked(False)
        self.launchMinecraftPSForAllButton.pressed.connect(self.launchMinecraftPSEveryChecked)
        self.launchMinecraftPSForAllButton.setIcon(QIcon('minecraft.ico'))
        self.launchMinecraftPSForAllButton.setIconSize(QSize(30,30))

        self.launchMinecraftPRForAllButton = QPushButton('')
        self.launchMinecraftPRForAllButton.setChecked(False)
        self.launchMinecraftPRForAllButton.pressed.connect(self.launchMinecraftPREveryChecked)
        self.launchMinecraftPRForAllButton.setIcon(QIcon('agent_g.ico'))
        self.launchMinecraftPRForAllButton.setIconSize(QSize(30,30))

        self.closeMinecraftForAllButton = QPushButton('')
        self.closeMinecraftForAllButton.setChecked(False)
        self.closeMinecraftForAllButton.pressed.connect(self.closeMinecraftEveryChecked)
        self.closeMinecraftForAllButton.setIcon(QIcon('closeMine.ico'))
        self.closeMinecraftForAllButton.setIconSize(QSize(30,30))

        topLayout = QHBoxLayout()
        topLayout.addWidget(mainCheckbox)
        topLayout.addWidget(self.lockAllButton)
        topLayout.addWidget(self.launchMinecraftPSForAllButton)
        topLayout.addWidget(self.launchMinecraftPRForAllButton)
        topLayout.addWidget(self.closeMinecraftForAllButton)
        topLayout.addStretch(1)

        self.layoutV.addLayout(topLayout)
        splitterLayout = QHBoxLayout()
        sepLine = QFrame()
        sepLine.setFrameShape(QFrame.HLine)
        splitterLayout.addWidget(sepLine)
        self.layoutV.addLayout(splitterLayout)



        #file = open('studentsList.txt')
        #for line in file:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(("", 37020))
        self.client.settimeout(False)

        #file.close()
        #self.screenLocked = False
        self.counter = 0
        #self.teachermsg = ''
        #self.createTickBoxsGroup()
        #layoutStudent = QHBoxLayout()
        #self.setMinimumSize(QSize(480, 80)) 
        #layout = QGridLayout()
        #self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        #self.useStylePaletteCheckBox.setChecked(True)
 
        #self.l = QLabel("Start")
        #label = QLabel(self)
        #pixmap = QPixmap('keep.png')
        #label.setPixmap(pixmap)
        #label.setAlignment(Qt.AlignCenter)
        #layout.addWidget(label)
        #self.showFullScreen() 


        #b = QPushButton("DANGER!")
        #b.pressed.connect(self.oh_no)

        #layout.addWidget(self.l)
        #layout.addWidget(b)

        w = QWidget()
        w.setLayout(self.layoutV)

        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        #self.IPlistenerThreadpool = QThreadPool()
        #self.IPlistenerThreadpool.setMaxThreadCount(1)


        self.timer1 = QTimer()
        self.timer1.setInterval(3000)
        self.timer1.timeout.connect(self.btn_state_timer)
        self.timer1.start()

        self.timer2 = QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.listen_IP_timer)
        self.timer2.start()

        self.timer3 = QTimer()
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.olden_students)
        self.timer3.start()

        #self.UDPthreadpool = QThreadPool()
        #self.UDPthreadpool.setMaxThreadCount(1)
        #tcpListener = Worker(self.listenTCP)
        #tcpListener.signals.result.connect(self.do_what_teacher_said)
        #tcpListener.signals.finished.connect(self.listen_again)
        ##tcpListener.signals.progress.connect(self.)
        #self.threadpool.start(tcpListener)
#
        #self.hide()


    #def createTickBoxsGroup(self):
    #    self.tickBoxsGroup = QGroupBox("Group 1")
    def launchMinecraftPSEveryChecked(self):
        print("launched minecraft education on all machines")
        for i, cb in enumerate(self.studentCheckboxes):
            if cb.isChecked():
                self.launchMinecraftPSButtons[i].click()

    def launchMinecraftPREveryChecked(self):
        print("launched minecraft programmig on all machines")
        for i, cb in enumerate(self.studentCheckboxes):
            if cb.isChecked():
                self.launchMinecraftPRButtons[i].click()

    def closeMinecraftEveryChecked(self):
        print("closed minecraft on all machines")
        for i, cb in enumerate(self.studentCheckboxes):
            if cb.isChecked():
                self.closeMinecraftButtons[i].click()



    def make_lockStudent(self, studentIndex):
        def lockStudent():
            if self.studentButtons[studentIndex].isChecked():
                self.studentButtons[studentIndex].setIcon(QIcon('locked.png'))
                tcpTeacher = Worker(self.lockMachine, studentIndex)
                self.threadpool.start(tcpTeacher)
                #tcpTeacher.signals.result.connect()
                #tcpListener = Worker(self.listenTCP)
                #tcpListener.signals.result.connect(self.do_what_teacher_said)
                #tcpListener.signals.finished.connect(self.listen_again)
                ##tcpListener.signals.progress.connect(self.)
                #self.threadpool.start(tcpListener)
                print("student number {} was locked".format(studentIndex+1))
            elif not self.studentButtons[studentIndex].isChecked():
                self.studentButtons[studentIndex].setIcon(QIcon('unlocked.png'))
                tcpTeacher = Worker(self.unlockMachine, studentIndex)
                self.threadpool.start(tcpTeacher)
                #tcpListener = Worker(self.listenTCP)
                #tcpListener.signals.result.connect(self.do_what_teacher_said)
                #tcpListener.signals.finished.connect(self.listen_again)
                ##tcpListener.signals.progress.connect(self.)
                #self.threadpool.start(tcpListener)
                print("student number {} was unlocked".format(studentIndex+1))
        return lockStudent

    def make_launchMinecraftPS(self, studentIndex):
        def launchMinecraftPS():
            self.sendMsgToSt(studentIndex, "launchPS")
            #print(f"Minecraft launch is not implemented yet for student number {studentIndex}")
        return launchMinecraftPS

    def make_launchMinecraftPR(self, studentIndex):
        def launchMinecraftPR():
            self.sendMsgToSt(studentIndex, "launchPR")
            #print(f"Minecraft launch is not implemented yet for student number {studentIndex}")
        return launchMinecraftPR

    def make_closeMinecraft(self, studentIndex):
        def closeMinecraft():
            self.sendMsgToSt(studentIndex, "closeMine")
            #print(f"Minecraft launch is not implemented yet for student number {studentIndex}")
        return closeMinecraft

    def lockMachine(self, studentIndex):
        self.sendMsgToSt(studentIndex, "l")
        #print("Info from thread: student {} locked".format(studentIndex+1))


    def unlockMachine(self, studentIndex):
        self.sendMsgToSt(studentIndex, "u")
        #print("Info from thread: student {} unlocked".format(studentIndex+1))

    def sendMsgToSt(self, studentIndex, msg):
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        #while True:
        MESSAGE = msg

        #for ipAddr in TCP_IP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect((self.studentAddresses[studentIndex], TCP_PORT))
        except:
            print('connect timeout')
            return
        try:
            s.send(MESSAGE.encode())
        except:
            print("Failed to send msg")
        try:
            data = s.recv(BUFFER_SIZE)
        except:
            print('recv timeout')
            return
        s.close()
        print (f"received data from student {studentIndex+1}:", data.decode())

        #if msg == "l":
        #    self.studentLockStates[studentIndex] = True
        #elif msg == "u":
        #    self.studentLockStates[studentIndex] = False

    def olden_students(self):
        for i in range(len(self.studentAges)):
            self.studentAges[i] += 1
            if self.studentAges[i] >= 30:
                self.studentButtons[i].setChecked(False)


    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def listenIP(self):
        receivedNewInfo = False
        try:
            print("Listening IP")
            data, addr = self.client.recvfrom(1024)
            if data:
                print(f"received data{data.decode()}")
                name, IP = data.decode().split(",")
                print(name)
                print(IP)
                receivedNewInfo = True
                #data = ""
        except:
            receivedNewInfo = False

        if receivedNewInfo:
            self.addStudent(name, IP)
        #print("received message: %s"%data)
        #print("test")

    def listen_IP_timer(self):
        print("Listening IP")
        self.listenIP()


    def btn_state_timer(self):
        #studentListener = Worker(self.listenIP)
        #self.threadpool.start(studentListener)
        #studentListener = Worker(self.listenIP)
        #self.IPlistenerThreadpool.start(studentListener)
        #data, addr = self.client.recvfrom(1024)
        #print("received message: %s"%data)
        #self.counter += 1
        #if self.counter > 10:
        print("sent lock command to those which button state is locked...")
        #self.counter = 0

        for i, btn in enumerate(self.studentButtons):
            if self.studentCheckboxes[i].isChecked(): 
                if btn.isChecked():
                    self.lockMachine(i)
                else:
                    self.unlockMachine(i)
                    #self.studentButtons[i].setChecked(state)
            #for btn in self.studentButtons:
            #    if btn.isChecked():

            #self.do_what_teacher_said('u')
        #self.l.setText("Counter: %d" % self.counter)


    def checkEverybody(self, state):
        for cb in self.studentCheckboxes:
            cb.setChecked(state)

    def lockEveryChecked(self, state):
        #self.lockAllButton.setChecked(state)
        if self.lockAllButton.isChecked():
            self.lockAllButton.setIcon(QIcon('locked.png'))
            self.lockAllButton.setText('')
        else:
            self.lockAllButton.setIcon(QIcon('unlocked.png'))
            self.lockAllButton.setText('')
        for i, cb in enumerate(self.studentCheckboxes):
            if cb.isChecked():
                self.studentButtons[i].setChecked(state)
        #print("locked all")

    def addStudent(self, name, IP):
        print("adding student")
        if (name in self.studentNames):
            studentIndex = self.studentNames.index(name)
            self.studentAddresses[studentIndex] = IP
            self.studentAges[studentIndex] = 0
            print(f"student with name: {name} already exists")
        else:
            self.studentNum += 1
            self.studentAddresses.append(IP)
            self.studentNames.append(name)
            self.studentAges.append(0)
            #print("Added name and address")
            self.studentCheckboxes.append(QCheckBox())
            self.studentCheckboxes[-1].setChecked(True)
            self.studentLabels.append(QLabel(name))
            self.studentLabels[-1].setFont(QFont('SansSerif', 10))
            #print("Added layout")
            #self.studentLabels[-1]
            self.studentButtons.append(QPushButton(''))
            #self.studentButtons[-1].setMaximumSize(QSize(32,32))
            self.studentButtons[-1].setCheckable(True)
            self.studentButtons[-1].setChecked(False)
            self.studentButtons[-1].toggled.connect(self.make_lockStudent(self.studentNum-1))
            self.studentButtons[-1].setIcon(QIcon('unlocked.png'))
            self.studentButtons[-1].setIconSize(QSize(100,30))
            #self.studentLockStates.append(False)
            #studentLayout = QHBoxLayout()

            self.launchMinecraftPSButtons.append(QPushButton(''))
            self.launchMinecraftPSButtons[-1].setChecked(False)
            self.launchMinecraftPSButtons[-1].pressed.connect(self.make_launchMinecraftPS(self.studentNum-1))
            self.launchMinecraftPSButtons[-1].setIcon(QIcon('minecraft.ico'))
            self.launchMinecraftPSButtons[-1].setIconSize(QSize(30,30))
            self.launchMinecraftPSButtons[-1].hide()
            '''trying to remmove buttton with hide. If it doesn't help you can test visibility or
             transperency method and then if still doesn't work just use regular function....It should be even easier!!!
            '''
            #other things to improve are in phone notes...Minecraft bug rememmber. Maybe use win32 to setforeground window or something like it... 
            self.launchMinecraftPRButtons.append(QPushButton(''))
            self.launchMinecraftPRButtons[-1].setChecked(False)
            self.launchMinecraftPRButtons[-1].pressed.connect(self.make_launchMinecraftPR(self.studentNum-1))
            self.launchMinecraftPRButtons[-1].setIcon(QIcon('agent_g.ico'))
            self.launchMinecraftPRButtons[-1].setIconSize(QSize(30,30))
            self.launchMinecraftPRButtons[-1].hide()

            self.closeMinecraftButtons.append(QPushButton(''))
            self.closeMinecraftButtons[-1].setChecked(False)
            self.closeMinecraftButtons[-1].pressed.connect(self.make_closeMinecraft(self.studentNum-1))
            self.closeMinecraftButtons[-1].setIcon(QIcon('closeMine.ico'))
            self.closeMinecraftButtons[-1].setIconSize(QSize(30,30))
            self.closeMinecraftButtons[-1].hide()


            self.studentLayouts.append(QHBoxLayout())
            self.studentLayouts[-1].addWidget(self.studentCheckboxes[-1])
            #self.studentLayouts[-1].addWidget(self.studentLabelsIcons[-1])
            self.studentLayouts[-1].addWidget(self.studentLabels[-1])
            self.studentLayouts[-1].addWidget(self.studentButtons[-1])
            self.studentLayouts[-1].addWidget(self.launchMinecraftPSButtons[-1])

            self.studentLayouts[-1].addWidget(self.launchMinecraftPRButtons[-1])
            self.studentLayouts[-1].addWidget(self.closeMinecraftButtons[-1])
            self.studentLayouts[-1].addStretch(1)
            self.layoutV.addLayout(self.studentLayouts[-1])

        #def listenTCP(self, progress_callback):
        #    TCP_PORT = 5005
        #    BUFFER_SIZE = 20  # Normally 1024, but we want fast response
    #
        #    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    #timeoutTime = 6
        #    #s.settimeout(timeoutTime)
        #    s.bind(('', TCP_PORT)) #TCP_IPs
        #    s.listen(1)
        #    try: 
        #        conn, addr = s.accept()
        #    except:
        #        return "Accept error"
        #    print ('Connection address:', addr)
        #    while 1:
        #        data = conn.recv(BUFFER_SIZE)
        #        if not data: 
        #            break
        #        print ("received data:", data.decode())
        #        teachermsg = data.decode()
        #        conn.send(data)  # echo                
        #    conn.close()
        #    return teachermsg

        #def listen_again(self) :
        #    tcpListener = Worker(self.listenTCP)
        #    tcpListener.signals.result.connect(self.do_what_teacher_said)
        #    tcpListener.signals.finished.connect(self.listen_again)
        #    #tcpListener.signals.progress.connect(self.)
        #    self.threadpool.start(tcpListener)


app = QApplication([])
window = MainWindow()
app.exec_()

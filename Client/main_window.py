#!/usr/bin/env python3.10
# This Python file uses the following encoding: utf-8
import sys
import time

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, \
                            QMdiArea, QWidget, QLineEdit, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QFile, QDir, QSize
from PyQt5.QtGui import QPixmap, QPalette, QImage, QBrush

from Source.client_socket import ClientSocket
from Source.stack_of_widgets import StackOfWidgets

from Source.initial_widget import InitialWidget
from Source.authentification_widget import AuthentificationWidget
from Source.registration_widget import RegistrationWidget
from Source.account_info_widget import AccountInfoWidget
from Source.user_menu import UserMenu
from Source.consultant_menu import ConsultationMenu
from Source.consultation_chat import ConsultationChat
from Source.broker_menu import BrokerMenu
from Source.company_widget import CompanyWidget
from Source.service_widget import ServiceWidget
from Source.plot_choice import PlotChoice
from Source.histogram import Histogram
from Source.linear_plot import LinearPlot
from Source.report_widget import ReportWidget
from Source.broker_client import BrokerClient
from fpdf import FPDF

class MainWindow(QMainWindow):
    def __init__(self, client_socket):
        super(MainWindow, self).__init__()
        uic.loadUi('Form/main_window_form.ui', self)

        self.client_socket = client_socket
        self.stack_of_widgets = StackOfWidgets()

        self.client_socket.onReadyRead.connect(self.handleRespond)
        self.chat_wnd = None
        self.chat = None

    #---------------CREATION WIDGETS BELOW------------------------------------------
        self.init_wdg = InitialWidget()
        self.auth_wdg = AuthentificationWidget()
        self.regi_wdg = RegistrationWidget()

    #--------------SIGNAL-SLOT WIDGETS CONNECTIONS BELOW----------------------------
        self.init_wdg.startButtonClicked.connect(
            self.slotInitStartButtonClicked
        )
        self.init_wdg.close.connect(
            self.childClosed
        )
        self.auth_wdg.authentificationButtonClicked.connect(
            self.slotAuthentificationButtonClicked
        )
        self.auth_wdg.registrationButtonClicked.connect(
            self.slotRegistrationButtonClicked
        )
        self.auth_wdg.close.connect(
            self.childClosed
        )
        self.regi_wdg.createButtonClicked.connect(
            self.slotCreateAccountButtonClicked
        )
        self.regi_wdg.backButtonClicked.connect(
            self.slotBackFromRegistrationButtonClicked
        )
        self.regi_wdg.close.connect(
            self.childClosed
        )
    #------------SIGNAL-SLOT MAINWINDOW MENUBAR CONNECTIONS BELOW-------------------
        self.accInfo.triggered.connect(self.slotAccInfoButtonClicked)
        self.quitAccount.triggered.connect(self.slotQuitAccountClicked)

    #----------------------------INIT ACTIONS---------------------------------------
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)
        self.setWindowTitle('')
        self.stack_of_widgets.push(self.init_wdg)
        self.sourcePalette = self.palette()

    #------------------------INITIAL WIDGET SLOTS BELOW---------------------------------
    def slotInitStartButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)
    #----------------AUTHENTIFICATION WIDGET SLOTS BELOW--------------------------------
    def slotAuthentificationButtonClicked(self):
        self.client_socket.sendToServer('SIGN IN ACCOUNT~!#$~login:' + \
            self.auth_wdg.login + '~!#$~password:' + self.auth_wdg.passw
        )

    def slotRegistrationButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.regi_wdg)
    #---------------REGISTRATION WIDGET SLOTS BELOW-------------------------------------
    def slotCreateAccountButtonClicked(self):
        self.client_socket.sendToServer('REGISTRATION ACCOUNT~!#$~login:' + \
            self.regi_wdg.login + '~!#$~password:' + self.regi_wdg.passw
        )

    def slotBackFromRegistrationButtonClicked(self):
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)
    #-----------------MAINWINDOW MENUBAR SLOTS BELOW------------------------------------
    def slotAccInfoButtonClicked(self):
        self.info_wdg = AccountInfoWidget()
        self.info_wdg.saveButtonClicked.connect(
            self.slotSaveAccountInfoButtonClicked
        )
        self.info_wdg.deleteAccountButtonClicked.connect(
            self.slotDeleteAccountButtonClicked
        )
        self.info_wdg.uploadThemeButtonClicked.connect(
            self.slotUploadThemeButtonClicked
        )
        self.info_wdg.deleteThemeButtonClicked.connect(
            self.slotDeleteThemeButtonClicked
        )
        self.client_socket.sendToServer('GET ACCOUNT INFO~!#$~login:' + \
            self.auth_wdg.login
        )

        wnd = self.mdiArea.addSubWindow(self.info_wdg)
        wnd.setWindowTitle('Личная информация')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotQuitAccountClicked(self):
        if self.mdiArea.activeSubWindow() == self.chat:
            self.client_socket.sendToServer("FINISH CHAT~!#$~" + \
                self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion
            )
        self.auth_wdg.clearLines()
        self.stack_of_widgets.pop()
        self.stack_of_widgets.push(self.auth_wdg)
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

    #--------------INFO WINDGET SLOTS BELOW--------------------------------------------
    def slotUploadThemeButtonClicked(self):
        login = self.auth_wdg.loginLineEdit.text()
        filename = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            QDir.homePath()
        )
        profilesPath = QDir.currentPath() + '/Profiles/'

        profilesDir = QDir(profilesPath)
        if not QDir(profilesPath + login).exists():
            profilesDir.mkdir(login)

        if QFile(profilesPath + login + '/background.jpg').exists():
            QFile.remove(profilesPath + login + '/background.jpg')
        QFile.copy(filename[0], profilesPath + login + '/background.jpg')

        self.setStyleSheet("");
        originalImage = QImage(profilesPath + login + '/background.jpg')
        scaledImage = originalImage.scaled(
            QSize(self.frameGeometry().width(), self.frameGeometry().height())
        )
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaledImage))
        self.setPalette(palette)

    def slotDeleteThemeButtonClicked(self):
        login = self.auth_wdg.loginLineEdit.text()
        profilesPath = QDir.currentPath() + '/Profiles/'
        if QFile(profilesPath + login + '/background.jpg').exists():
            QFile.remove(profilesPath + login + '/background.jpg')
            self.setStyleSheet("background-color: rgb(153, 193, 241);");

    def slotSaveAccountInfoButtonClicked(self):
        self.client_socket.sendToServer('REDO ACCOUNT INFO~!#$~login:' + \
            self.info_wdg.login + '~!#$~password:' + self.info_wdg.passw + \
            '~!#$~mob_num:' + self.info_wdg.mobnum + '~!#$~email:' + self.info_wdg.email
        )

    def slotDeleteAccountButtonClicked(self):
        if self.auth_wdg.passw == self.info_wdg.passw_:
            profilesPath = QDir.currentPath() + '/Profiles/'
            currentDir = QDir(profilesPath + self.auth_wdg.login)
            currentDir.removeRecursively()
            self.client_socket.sendToServer('DELETE ACCOUNT~!#$~login:' + \
                self.auth_wdg.login
            )
        else:
            QMessageBox.about(self, "Уведомление", "Неверный пароль")


    #----------------------------------------MAINWINDOW SLOTS----------------------------------
    def closeEvent(self, event):
        if self.chat_wnd:
            self.client_socket.sendToServer("FINISH CHAT~!#$~" + \
                self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion
            )
        elif self.auth_wdg.rolename == 'USER':
                self.client_socket.sendToServer("DELETE BASKET~!#$~login:" + \
                self.auth_wdg.login + "~!#$~name:" + \
                self.auth_wdg.login)
        self.client_socket.sendToServer('EXIT')

    def resizeEvent(self, event):
        login = self.auth_wdg.loginLineEdit.text()
        profilesPath = QDir.currentPath() + '/Profiles/'
        if QFile(profilesPath + login + '/background.jpg').exists():
            palette = QPalette()
            originalImage = QImage(profilesPath + login + '/background.jpg')
            scaledImage = originalImage.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, transformMode = Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Window, QBrush(scaledImage))
            self.setPalette(palette)

    #-----------------MAINWINDOW FUNCTION BELOW------------------------------------------------
    def childClosed(self):
        if self.chat_wnd:
            self.client_socket.sendToServer("FINISH CHAT~!#$~" + \
                self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion
            )
        elif self.auth_wdg.rolename == 'USER':
                self.client_socket.sendToServer("DELETE BASKET~!#$~login:" + \
                self.auth_wdg.login + "~!#$~name:" + \
                self.auth_wdg.login)
        self.client_socket.sendToServer('EXIT')


    def slotCreateConsultationClicked(self):
        self.chat_wnd = ConsultationChat()
        self.chat_wnd.sendMessage.connect(lambda: self.client_socket.sendToServer("MESSAGE~!#$~" + \
                self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion + "~!#$~" + self.chat_wnd.message
            )
        )
        self.chat_wnd.finishChat.connect(
            self.slotFinishChatClicked
        )
        self.chat_wnd.setParticipants(self.auth_wdg.login, self.cons_wdg.currentUser)
        self.client_socket.sendToServer("START CHAT~!#$~" + self.auth_wdg.login + "~!#$~" + self.cons_wdg.currentUser)
        self.client_socket.sendToServer("DELETE BASKET~!#$~login:" + \
            self.chat_wnd.companion + "~!#$~name:" + \
            self.chat_wnd.companion
        )
        self.chat = self.mdiArea.addSubWindow(self.chat_wnd)
        self.chat.setWindowTitle('Чат')
        self.chat.setWindowFlags(QtCore.Qt.FramelessWindowHint);
        self.chat.showMaximized()

    def slotFinishChatClicked(self):
        self.chat.close()
        self.client_socket.sendToServer("FINISH CHAT~!#$~" + \
            self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion
        )

    def slotCompanyClicked(self):
        self.comp_wdg = CompanyWidget()
        self.comp_wdg.addButtonClicked.connect(lambda: self.client_socket.sendToServer('ADD COMPANY~!#$~company_name:' + \
                self.comp_wdg.selected_company
            )
        )
        self.comp_wdg.changeButtonClicked.connect(lambda: self.client_socket.sendToServer('CHANGE COMPANY~!#$~old_name:' + \
                self.comp_wdg.selected_company + '~!#$~company_name:' + \
                self.comp_wdg.new_name
            )
        )
        self.comp_wdg.deleteButtonClicked.connect(lambda: self.client_socket.sendToServer('DELETE COMPANY~!#$~company_name:' + \
                self.comp_wdg.selected_company
            )
        )
        self.comp_wdg.itemDoubleClicked.connect(
            self.slotItemDoubleClicked
        )
        self.client_socket.sendToServer('GET COMPANY')
        wnd = self.mdiArea.addSubWindow(self.comp_wdg)
        wnd.setWindowTitle('Работа с компаниями')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotItemDoubleClicked(self):
        self.serv_wdg = ServiceWidget()
        self.serv_wdg.addButtonClicked.connect(lambda: self.client_socket.sendToServer('ADD SERVICE~!#$~service_name:' + \
            self.serv_wdg.service + '~!#$~price:' + self.serv_wdg.price + '~!#$~company_name:' + self.comp_wdg.selected_company
            )
        )
        self.serv_wdg.changeButtonClicked.connect(lambda: self.client_socket.sendToServer('CHANGE SERVICE~!#$~service_name:' + \
            self.serv_wdg.service + '~!#$~price:' + self.serv_wdg.price + '~!#$~company_name:' + self.comp_wdg.selected_company
            )
        )
        self.serv_wdg.deleteButtonClicked.connect(lambda: self.client_socket.sendToServer('DELETE SERVICE~!#$~service_name:' + \
            self.serv_wdg.service + '~!#$~company_name:' + self.comp_wdg.selected_company
            )
        )
        self.client_socket.sendToServer('GET SERVICE~!#$~company_name:' + self.comp_wdg.selected_company)
        wnd = self.mdiArea.addSubWindow(self.serv_wdg)
        wnd.setWindowTitle('Работа с услугами')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def uploadTheme(self):
        login = self.auth_wdg.loginLineEdit.text()
        profilesPath = QDir.currentPath() + '/Profiles/'
        if QFile(profilesPath + login + '/background.jpg').exists():
            self.setStyleSheet("");
            originalImage = QImage(profilesPath + login + '/background.jpg')
            scaledImage = originalImage.scaled(
                QSize(self.frameGeometry().width(), self.frameGeometry().height())
            )
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(scaledImage))
            self.setPalette(palette)
        else:
            self.setStyleSheet("background-color: rgb(153, 193, 241);");

    def slotPlotClicked(self):
        self.plot_choice = PlotChoice()
        self.plot_choice.histogramClicked.connect(self.slotHistogramClicked)
        self.plot_choice.linearClicked.connect(self.slotLinearClicked)
        wnd = self.mdiArea.addSubWindow(self.plot_choice)
        wnd.setWindowTitle('Графики')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotHistogramClicked(self):
        self.client_socket.sendToServer('GET DATA FOR HISTOGRAM')

    def slotLinearClicked(self):
        self.client_socket.sendToServer('GET SERVICES ONLY')


    def slotReportClicked(self):
        self.report_wid = ReportWidget()
        self.report_wid.txtButtonClicked.connect(lambda: self.client_socket.sendToServer('GET PRICE HISTORY'))
        self.report_wid.pdfButtonClicked.connect(lambda: self.client_socket.sendToServer('GET PRICE HISTORY'))
        wnd = self.mdiArea.addSubWindow(self.report_wid)
        wnd.setWindowTitle('Графики')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotOrderClicked(self):
        self.brcl_wgd = BrokerClient()
        self.brcl_wgd.orderClicked.connect(self.slotBrokerClientOrderClicked)
        self.client_socket.sendToServer("GET ORDERS~!#$~type:SERVICE")
        wnd = self.mdiArea.addSubWindow(self.brcl_wgd)
        wnd.setWindowTitle('Заказы')
        wnd.setWindowFlags(QtCore.Qt.Dialog);
        wnd.showMaximized()

    def slotBrokerClientOrderClicked(self):
        self.client_socket.sendToServer("DELETE BASKET~!#$~login:" + \
            self.brcl_wgd.login + "~!#$~name:" + \
            self.brcl_wgd.order
        )

    def handleRespond(self):
        respond = self.client_socket.get_data()
        respond_list = respond.split('~!#$~')
        command, args = "", []


        match len(respond_list):
            case 1: command = respond_list[0]
            case _: command, *args = respond_list

        if command == 'REGISTRATION SUCCESSFUL':
            self.regi_wdg.clearLines()
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self.auth_wdg)
            QMessageBox.about(self, "Уведомление", "Регистрация успешна")
        elif command == 'REGISTRATION FAILED':
            self.regi_wdg.setError('Ошибка регистрации')
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args[0] == 'USER':
            self.auth_wdg.rolename = args[0]
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
            self.user_wdg = UserMenu()
            self.user_wdg.close.connect(
                self.childClosed
            )
            self.user_wdg.consultationButtonClicked.connect(
                lambda: self.client_socket.sendToServer("ADD BASKET~!#$~login:" + \
                    self.auth_wdg.login + "~!#$~name:" + \
                    self.auth_wdg.login + "~!#$~type:CONSULTATION"
                )
            )
            self.user_wdg.orderButtonClicked.connect(lambda: self.client_socket.sendToServer("ADD BASKET~!#$~login:" + \
                self.auth_wdg.login + "~!#$~name:" + self.user_wdg.currentService + "~!#$~type:SERVICE"
                )
            )
            self.client_socket.sendToServer("GET AVG PRICE AND SERVICE")
            wnd = self.mdiArea.addSubWindow(self.user_wdg)
            wnd.setWindowTitle('Меню')
            wnd.setWindowFlags(QtCore.Qt.FramelessWindowHint);
            wnd.showMaximized()
            self.uploadTheme()
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args[0] == 'CONSULTANT':
            self.auth_wdg.rolename = args[0]
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
            self.cons_wdg = ConsultationMenu()
            self.cons_wdg.close.connect(
                self.childClosed
            )
            self.cons_wdg.cancelConsultation.connect(
                lambda: self.client_socket.sendToServer("DELETE BASKET~!#$~login:" + \
                    self.cons_wdg.currentUser + "~!#$~name:" + \
                    self.cons_wdg.currentUser
                )
            )
            self.cons_wdg.createConsultation.connect(
                self.slotCreateConsultationClicked
            )
            self.client_socket.sendToServer("GET BASKET~!#$~type:CONSULTATION")
            self.cons_wdg.showRequests.setEnabled(False)
            wnd = self.mdiArea.addSubWindow(self.cons_wdg)
            wnd.setWindowTitle('Меню')
            wnd.setWindowFlags(QtCore.Qt.FramelessWindowHint);
            wnd.showMaximized()
            self.uploadTheme()
        elif command == 'AUTHENTIFICATION SUCCESSFUL' and args[0] == 'BROKER':
            self.auth_wdg.rolename = args[0]
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self)
            self.brok_wdg = BrokerMenu()
            self.brok_wdg.close.connect(
                self.childClosed
            )
            self.brok_wdg.companyClicked.connect(
                self.slotCompanyClicked
            )
            self.brok_wdg.plotClicked.connect(
                self.slotPlotClicked
            )
            self.brok_wdg.reportClicked.connect(
                self.slotReportClicked
            )
            self.brok_wdg.orderClicked.connect(
                self.slotOrderClicked
            )
            wnd = self.mdiArea.addSubWindow(self.brok_wdg)
            wnd.setWindowTitle('Меню')
            wnd.setWindowFlags(QtCore.Qt.FramelessWindowHint);
            wnd.showMaximized()
            self.uploadTheme()
        elif command == 'AUTHENTIFICATION FAILED':
            self.auth_wdg.setError(args[0])
        elif command == 'REDO ACC INFO SUCCESS':
            QMessageBox.about(self, "Уведомление", "Данные изменены успешно")
            self.info_wdg.setError('')
        elif command == 'REDO ACC INFO FAILED':
            self.info_wdg.setError('Ошибка. Некорректные данные')
        elif command == 'DELETING SUCCESSFUL':
            QMessageBox.about(self, "Уведомление", "Аккаунт удален")
            self.auth_wdg.clearLines()
            self.stack_of_widgets.pop()
            self.stack_of_widgets.push(self.auth_wdg)
        elif command == 'DELETING FAILED':
            QMessageBox.about(self, "Уведомление", "Ошибка удаления аккаунта")
        elif command == "GET INFORMATION SUCCESS":
            self.info_wdg.setInfo(*args)
        elif command == "GETDATA FAILED":
            self.info_wdg.setError("Ошибка при соединении с сервером")
        elif command == "GET BASKET SUCCESS" and self.auth_wdg.rolename == 'CONSULTANT':
            if args:
                self.cons_wdg.setConsultation(args)
            else:
                self.cons_wdg.clearList()
        elif command == "GET BASKET SUCCES" and self.auth_wdg.rolename == 'BROKER':
            pass
        elif command == "GET BASKET FAILED" and self.auth_wdg.rolename == 'CONSULTANT':
            self.cons_wdg.setError('Ошибка при соединении с сервером')
        elif command == "GET BASKET FAILED" and self.auth_wdg.rolename == 'BROKER':
            pass
        elif command == 'REQUEST AGAIN' and self.auth_wdg.rolename == 'CONSULTANT':
            self.client_socket.sendToServer("GET BASKET~!#$~type:CONSULTATION")
        elif command == "REQUEST AGAIN" and self.auth_wdg.rolename == 'BROKER':
            self.client_socket.sendToServer("GET ORDERS~!#$~type:SERVICE")
        elif command == "DELETE BASKET FAILED" and self.auth_wdg.rolename == "CONSULTANT":
            pass
        elif command == "START CHAT" and self.auth_wdg.login == args[1]:
            companion, login = args
            self.chat_wnd = ConsultationChat()
            self.chat_wnd.sendMessage.connect(lambda: self.client_socket.sendToServer("MESSAGE~!#$~" + \
                    self.chat_wnd.login + "~!#$~" + self.chat_wnd.companion + "~!#$~" + self.chat_wnd.message
                )
            )
            self.chat_wnd.finishChat.connect(
                self.slotFinishChatClicked
            )
            self.chat_wnd.setParticipants(login, companion)
            self.chat = self.mdiArea.addSubWindow(self.chat_wnd)
            self.chat.setWindowTitle('Чат')
            self.chat.setWindowFlags(QtCore.Qt.FramelessWindowHint);
            self.chat.showMaximized()
        elif command == "MESSAGE" and self.auth_wdg.login == args[1]:
            if self.auth_wdg.rolename == 'USER':
                companion = 'Консультант'
            else:
                companion = 'Клиент'
            self.chat_wnd.setMessage(companion, args[2])
        elif command == "FINISH CHAT" and self.auth_wdg.login == args[1]:
            if self.chat_wnd:
                self.chat.close()
                self.chat_wnd = None
        elif command == "GET COMPANY SUCCESS" and self.auth_wdg.rolename == 'BROKER':
            self.comp_wdg.clearError()
            self.comp_wdg.setCompanies(args)
        elif command == "GET COMPANY FAILED" and self.auth_wdg.rolename == 'BROKER':
            self.comp_wdg.setError('Ошибка при соединении с сервером')
        elif command == 'DELETE COMPANY FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.comp_wdg.setError('Ошибка при соединении с сервером')
        elif command == 'ADD COMPANY FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.comp_wdg.setError('Ошибка! Такая компания уже существует')
        elif command == 'CHANGE COMPANY FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.comp_wdg.setError('Ошибка! Новое имя компании уже существует')
        elif command == 'REQUEST COMPANIES' and self.auth_wdg.rolename == 'BROKER':
            self.client_socket.sendToServer('GET COMPANY')
        elif command == "GET SERVICE SUCCESS" and self.auth_wdg.rolename == 'BROKER':
            self.serv_wdg.clearError()
            self.serv_wdg.setServices(args)
        elif command == "GET SERVICE FAILED" and self.auth_wdg.rolename == 'BROKER':
            self.serv_wdg.setError('Ошибка при соединении с сервером')
        elif command == 'DELETE SERVICE FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.serv_wdg.setError('Ошибка при соединении с сервером')
        elif command == 'ADD SERVICE FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.serv_wdg.setError('Ошибка! Такая услуга уже существует')
        elif command == 'CHANGE SERVICE FAILED' and self.auth_wdg.rolename == 'BROKER':
            self.serv_wdg.setError('Ошибка! Новое имя услуги уже существует')
        elif command == 'REQUEST SERVICES' and self.auth_wdg.rolename == 'BROKER':
            self.client_socket.sendToServer('GET SERVICE~!#$~company_name:' + self.comp_wdg.selected_company)
        elif command == "CREATE LINEAR" and self.auth_wdg.rolename == 'BROKER':
            companies, prices = [], []
            for x in args:
                com, pr = x.split(':')
                companies.append(com)
                prices.append(float(pr))
            self.linear.createLinearPlot(companies, prices)
        elif command == 'GET SERVICE ONLY SUCCESS' and self.auth_wdg.rolename == 'BROKER':
            self.linear = LinearPlot()
            self.linear.setServices(args)
            self.linear.selOption.connect(lambda: self.client_socket.sendToServer('CREATE LINEAR~!#$~service_name:' + self.linear.currName()))
            wnd = self.mdiArea.addSubWindow(self.linear)
            wnd.setWindowTitle('Линейный график')
            wnd.setWindowFlags(QtCore.Qt.Dialog);
            wnd.showMaximized()
            self.client_socket.sendToServer('CREATE LINEAR~!#$~service_name:' + self.linear.currName())
        elif command == 'CREATE HISTOGRAM' and self.auth_wdg.rolename == 'BROKER':
            companies_prices, std_list = [], []
            for x in args:
                std, com_pr = x.split(':')
                companies_prices.append(com_pr)
                std_list.append(std)
            self.hist.createHistogram(companies_prices, std_list)
        elif command == 'GET DATA FOR HISTOGRAM SUCCESS' and self.auth_wdg.rolename == 'BROKER':
            self.hist = Histogram()
            self.hist.setServices(args)
            self.hist.selOption.connect(lambda: self.client_socket.sendToServer('CREATE HISTOGRAM~!#$~service_name:' + self.hist.currName()))
            wnd = self.mdiArea.addSubWindow(self.hist)
            wnd.setWindowTitle('Работа с компаниями')
            wnd.setWindowFlags(QtCore.Qt.Dialog);
            wnd.showMaximized()
        elif command == 'GET PRICE HISTORY SUCCESS' and self.auth_wdg.rolename == 'BROKER':
            if self.report_wid.format:
                file = open(self.report_wid.filename + '.txt', 'w')
                for x in args:
                    file.write(x + '\n')
                file.close()
            else:
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font('DejaVu', '', 'font/DejaVuSansCondensed.ttf', uni=True)
                pdf.set_font('DejaVu', '', 14)
                for x in args:
                    pdf.cell(200, 10, txt=x, ln=1, align="C")
                pdf.output(self.report_wid.filename + '.pdf')
        elif command == "GET AVG PRICE AND SERVICE SUCCESS" and self.auth_wdg.rolename == "USER":
            avgs, services = [], []
            for x in args:
                price, service = x.split(':')
                avgs.append(price)
                services.append(service)
            data = dict(zip(services, avgs))
            self.user_wdg.setServices(data)
        elif command == "GET ORDERS SUCCESS" and self.auth_wdg.rolename == "BROKER":
            self.brcl_wgd.setData(args)



if __name__ == "__main__":
    app = QApplication([])
    client_socket = ClientSocket('localhost', 6606)
    main_window = MainWindow(client_socket)
    sys.exit(app.exec_())

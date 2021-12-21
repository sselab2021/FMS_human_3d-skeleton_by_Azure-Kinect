#-------------------------------------------------
#
# Project created by QtCreator 2021-05-10T14:57:05
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = FMS_data_acquisition_sideLow
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

INCLUDEPATH += \
            ./../3rdparty/AzureKinectSDK/include \
            ./../3rdparty/opencv/include

LIBS += \
    $$PWD/../3rdparty/AzureKinectSDK/windows-desktop/amd64/release/lib/k4a.lib \
    $$PWD/../3rdparty/AzureKinectSDK/windows-desktop/amd64/release/lib/k4arecord.lib \
    $$PWD/../3rdparty/opencv/x64/vc15/lib/opencv_world3410d.lib

SOURCES += \
        main.cpp \
        mainwindow.cpp

HEADERS += \
        mainwindow.h

FORMS += \
    mainwindow.ui

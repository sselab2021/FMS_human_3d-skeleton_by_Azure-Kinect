#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <k4a/k4a.h>
#include <opencv2/opencv.hpp>
#include <QDebug>

using namespace std;

class QImage;
class QPushButton;

static QImage cvMat_to_QImage(const cv::Mat &mat) {
    switch (mat.type())
    {
    // 8-bit, 4 channel
    case CV_8UC4:
    {
        QImage image(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB32);
        return image;
    }
    // 8-bit, 3 channel
    case CV_8UC3:
    {
        QImage image(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB888);
        return image.rgbSwapped();
    }
    // 8-bit, 1 channel
    case CV_8UC1:
    {
        static QVector<QRgb>  sColorTable;
        // only create our color table once
        if (sColorTable.isEmpty())
        {
            for (int i = 0; i < 256; ++i)
                sColorTable.push_back(qRgb(i, i, i));
        }
        QImage image(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_Indexed8);
        image.setColorTable(sColorTable);
        return image;
    }
    default:
        qDebug("Image format is not supported: depth=%d and %d channels\n", mat.depth(), mat.channels());
        break;
    }
    return QImage();
}

static QPixmap cvMatToQPixmap(const cv::Mat &inMat)
{
    return QPixmap::fromImage(cvMat_to_QImage(inMat));
}

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_warmUpBtn_clicked();
    void on_startBtn_clicked();
    void on_endBtn_clicked();
    void on_choosePathBtn_clicked();

    void on_cameraCalibration_clicked();
    void slotButtonClicked();

private:
    Ui::MainWindow *ui;

    // FMS movements array.
    string fmsAactionsArr[15] = { "m01_Deep squat(floor)", "m02_Deep squat(board)",
                                  "m03_Hurdle step(L)", "m04_Hurdle step(R)",
                                  "m05_In-line lunge(L)", "m06_In-line lunge(R)",
                                  "m07_Shoulder mobility(L)", "m08_Shoulder mobility(R)",
                                  "m09_Active straight raise(L)", "m10_Active straight raise(R)",
                                  "m11_Trunk stability push-up",
                                  "m12_Rotary stability(Ipsilateral-L)", "m13_Rotary stability(Ipsilateral-R)",
                                  "m14_Rotary stability(Contralateral-L)", "m15_Rotary stability(Contralateral-R)"};

    QList<QPushButton*> userBtnList;
    QPushButton *userBtn;
    int userNumber = 70;

    QList<QPushButton*> fmsActionBtnList;
    QPushButton *fmsActionBtn;
    int fmsActionNumber = 15;

    string cameraCalibrationPath;

    QString chosenUserNumber;
    QString chosenActionNumber;

    QString diskName;
    string mkvName;

    k4a_device_t device;
    k4a_device_configuration_t config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
    k4a_calibration_t sensorCalibration;

    int stopFlag = 0;
};

#endif // MAINWINDOW_H

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iomanip>
#include <io.h>
#include <QDir>
#include <QFileDialog>
#include <qtextcodec.h>
#include <direct.h>     //mkdir
#include <k4arecord/record.h>

// call k4a_device_close on every failed CHECK
#define CHECK(x, device)                                 \
{                                                        \
    auto retval = (x);                                   \
    if (retval)                                          \
    {                                                    \
        k4a_device_close(device);                        \
    }                                                    \
}

// Get current system time
string getTime() {
    time_t tt = time(NULL);
    struct tm* stm = localtime(&tt);

    char tmp[32];
    sprintf(tmp, "%04d%02d%02d%02d%02d%02d",
            1900 + stm->tm_year, 1 + stm->tm_mon, stm->tm_mday,
            stm->tm_hour, stm->tm_min, stm->tm_sec);
    return tmp;
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->diskNameLabel->setText("D:\\");
    ui->diskNameLabel->setStyleSheet("color:red");
    diskName = "D:\\";

    ui->userNumLabel->setStyleSheet("color:red");
    ui->actionNameLabel->setStyleSheet("color:red");

    // Dynamically creating the buttons of user numbers
    int userBtnRows = userNumber / 10;
    for (int row = 0; row < userBtnRows; row++)
    {
        for (int col = 0; col < 10; col++)
        {
            int totalUserBtnNumber = row * 10 + col;
            userBtn = new QPushButton(this);
            // position of button
            userBtn->setGeometry((17 + (93 * col)), (536 + (62 * row)), 88, 42);
            // the object name of button
            userBtn->setObjectName("userBtnPush" + QString::number(totalUserBtnNumber));
            // the text of button
            userBtn->setText(QString::number(totalUserBtnNumber + 1));

            userBtnList.append(userBtn);
            connect(userBtnList.at(totalUserBtnNumber), SIGNAL(clicked()), this, SLOT(slotButtonClicked()));
        }
    }

    // Dynamically creating the buttons of FMS
    for (int i = 0; i < fmsActionNumber; i++)
    {
        fmsActionBtn = new QPushButton(this);
        fmsActionBtn->setGeometry(1030, (268 + 42 * i), 320, 32);
        fmsActionBtn->setObjectName("fmsActionBtnPush" + QString::number(i));
        QString qstr2 = QString::fromStdString(fmsAactionsArr[i]);
        fmsActionBtn->setText(qstr2);
        fmsActionBtnList.append(fmsActionBtn);
        connect(fmsActionBtnList.at(i), SIGNAL(clicked()), this, SLOT(slotButtonClicked()));
    }
}

MainWindow::~MainWindow()
{
    qDeleteAll(userBtnList);
    qDeleteAll(fmsActionBtnList);
    userBtnList.clear();
    fmsActionBtnList.clear();

    delete ui;
}

// warm-up button
void MainWindow::on_warmUpBtn_clicked()
{
    stopFlag = 0;
    // open device
    device = NULL;
    k4a_device_open(0, &device);

    // camera configuration
    config.camera_fps = K4A_FRAMES_PER_SECOND_30;
    config.color_format = K4A_IMAGE_FORMAT_COLOR_MJPG;
    config.color_resolution = K4A_COLOR_RESOLUTION_1080P;
    config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
    config.wired_sync_mode = K4A_WIRED_SYNC_MODE_STANDALONE;	// the mode of single device
//    config.wired_sync_mode = K4A_WIRED_SYNC_MODE_MASTER;		// the sync-mode of mutli-device, the device is master.
//    config.wired_sync_mode = K4A_WIRED_SYNC_MODE_SUBORDINATE; // the sync-mode of mutli-device, the device is subordinate.
    config.synchronized_images_only = true;
    // Desired delay between the capture of the color image and the capture of the depth image.
    config.depth_delay_off_color_usec = 160;

    //-------------------------------------------------Create storage path of file-----------------------------------
    string PATH = diskName.toStdString() + "kinect_data\\" + cameraCalibrationPath + "\\";
    if (_access(PATH.c_str(), 0) == -1)
    {
        mkdir(PATH.c_str());
    }
    string YMDHMS_timestamp = getTime();
    string chosenUserNum = "front_" + chosenUserNumber.toStdString();		// Modify string according to camera position. front_, side_
    string chosenActionNum = chosenActionNumber.toStdString();

    // the path is different for camera calibration and the video of subjects.
    if (cameraCalibrationPath == "")
    {
        // the path of videos of test by subjects.
        string mkvPath = PATH + chosenUserNum + "\\";
        if (_access(mkvPath.c_str(), 0) == -1)
        {
            mkdir(mkvPath.c_str());
        }
        mkvName = mkvPath + chosenUserNum + "_" + chosenActionNum + "_" + YMDHMS_timestamp + ".mkv";
    }
    else
    {
        // the path of the videos of camera calibration.
        string mkvPath = PATH + "\\";
        if (_access(mkvPath.c_str(), 0) == -1)
        {
            mkdir(mkvPath.c_str());
        }
        mkvName = mkvPath + "front_" + YMDHMS_timestamp + ".mkv";
    }

    cameraCalibrationPath = "";
    ui->curStatus->setText("OK");
}

// Starting record
void MainWindow::on_startBtn_clicked()
{
    k4a_capture_t capture;
    // Image calibration
    k4a_device_get_calibration(device, config.depth_mode, config.color_resolution, &sensorCalibration);
    k4a_device_start_cameras(device, &config);

    // Creating the file of saving MKV
    k4a_record_t recording;
    k4a_record_create(mkvName.c_str(), device, config, &recording);

    // k4a_record_write_header()——Writes the recording header and metadata to file.
    CHECK(k4a_record_write_header(recording), device);

    int32_t timeout_sec_for_first_capture = 60;
    if (config.wired_sync_mode == K4A_WIRED_SYNC_MODE_SUBORDINATE)
    {
        timeout_sec_for_first_capture = 360;
    }
    clock_t first_capture_start = clock();
    k4a_wait_result_t result = K4A_WAIT_RESULT_TIMEOUT;

    while ((clock() - first_capture_start) < (CLOCKS_PER_SEC * timeout_sec_for_first_capture))
    {
        result = k4a_device_get_capture(device, &capture, 100);
        if (result == K4A_WAIT_RESULT_SUCCEEDED)
        {
            k4a_capture_release(capture);
            break;
        }
        else if (result == K4A_WAIT_RESULT_FAILED)
        {
            k4a_device_close(device);
        }
    }

    while (stopFlag == 0) {
        k4a_wait_result_t get_capture_result = k4a_device_get_capture(device, &capture, K4A_WAIT_INFINITE);

        if (get_capture_result == K4A_WAIT_RESULT_SUCCEEDED)
        {
            // k4a_record_write_capture()——Writes a camera capture to file.
            CHECK(k4a_record_write_capture(recording, capture), device);

            k4a_image_t color_image = k4a_capture_get_color_image(capture);

            //rgb
            int nSize = k4a_image_get_size(color_image);
            cv::Mat jpegImg(1, nSize, CV_8UC1, (void *)k4a_image_get_buffer(color_image));
            cv::Mat cv_rgbImage_with_alpha = cv::imdecode(jpegImg, cv::IMREAD_COLOR);

            k4a_image_release(color_image);

            // show
            cv::resize(cv_rgbImage_with_alpha, cv_rgbImage_with_alpha, cv::Size(900, 506));
            QPixmap image_rgb = cvMatToQPixmap(cv_rgbImage_with_alpha);

            ui->display->clear();
            ui->display->setPixmap(image_rgb);
            ui->display->show();

            k4a_capture_release(capture);
            QCoreApplication::processEvents();
        }
    }
    k4a_device_stop_cameras(device);
    // Flushes all pending recording data to disk
    CHECK(k4a_record_flush(recording), device);
    // Closes a recording handle.
    k4a_record_close(recording);

    k4a_device_close(device);
}

void MainWindow::on_endBtn_clicked()
{
    stopFlag = 1;
    ui->display->clear();
    ui->curStatus->clear();
}

void MainWindow::on_choosePathBtn_clicked()
{
//    QDir dir;
    diskName = QFileDialog::getExistingDirectory(this, tr("Open Directory"), "D:/",
                                                 QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);
    diskName = diskName.left(3); // the root path of the disk is selected
    diskName.replace("/", "\\");
    ui->diskNameLabel->setText(diskName);
}

void MainWindow::on_cameraCalibration_clicked()
{
    cameraCalibrationPath = "cameraCalibration";
}

void MainWindow::slotButtonClicked()
{
    QPushButton *btn = qobject_cast<QPushButton*>(sender());
    QString chosen_btn_text = btn->text();
    int textLength = chosen_btn_text.length();
    if (textLength < 3)
    {	// subjectsID
        ui->userNumLabel->setText(chosen_btn_text);
        int flag = chosen_btn_text.toInt();
        char tmp[3];
        sprintf(tmp, "%03d", flag);
        chosenUserNumber = tmp;
    }
    else
    {	// movementID
        ui->actionNameLabel->setText(chosen_btn_text);
        chosenActionNumber = chosen_btn_text.left(3);
    }
}

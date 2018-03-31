#include "ptf_csv.h"
#include "ui_ptf_csv.h"
#include "QFileDialog"
#include "QJsonValue"
#include "QDebug"
#include "QJsonDocument"
#include "QJsonObject"
#include "QString"
#include "QJsonArray"
#include "QDateTime"
#include "QTextStream"

PTF_CSV::PTF_CSV(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::PTF_CSV)
{
    ui->setupUi(this);
}

PTF_CSV::~PTF_CSV()
{
    delete ui;
}

void PTF_CSV::on_pushButton_3_clicked()
{
    QString s = QFileDialog::getOpenFileName(this,"选择JSON文件进行读取","/","C++ files(*.json)");
    ui->lineEdit->setText(s);
}

void PTF_CSV::on_pushButton_clicked()
{
    QString fileinfo = ui->lineEdit->text();

    QString val;
    QFile file;

    file.setFileName(fileinfo);
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    val = file.readAll();
    file.close();

    QJsonDocument d = QJsonDocument::fromJson(val.toUtf8());
    QJsonObject rootObject = d.object();
    QJsonValue hashJsonValue = rootObject.value(QString("hash"));
    QJsonValue dataJsonValue = rootObject.value(QString("data"));

    QJsonObject dataObject = dataJsonValue.toObject();
    QJsonArray testsList = dataObject["tests"].toArray();

    QString totalNumber =  QString("%1").arg(testsList.count());
    ui->textEdit->append("总测试项数量：" + totalNumber);


    QDateTime current_date_time =QDateTime::currentDateTime();
    QString current_date =current_date_time.toString("yyyy_MM_dd_hh_mm_ss_zzz");
    QString homePath = QDir::homePath();

    QFile result;
    result.setFileName(homePath + "/Downloads/" + current_date + ".csv");
    result.open(QIODevice::WriteOnly);

    result.write("ITEM; CODE; INFO; MESSAGE \n");


    for(int i=0; i < testsList.count(); i++)
    {
        QJsonObject eachTestItem = testsList[i].toObject();
        qWarning() << eachTestItem["description"];

        QString testItem = eachTestItem["category"].toString();
        QString testCode = QString("%1").arg(eachTestItem["key"].toDouble());
        QString testName = eachTestItem["name"].toString();
        QString testInfo = eachTestItem["description"].toString();

        ui->textEdit->append("--------->>");
        ui->textEdit->append(testItem);
        ui->textEdit->append(testCode);
        ui->textEdit->append(testName);
        ui->textEdit->append(testInfo);

        QString eachRow = testItem + ";" + testCode + ";" + testName + ";" + testInfo + "\n";
        QTextStream stream(&result);
        stream << eachRow;
    }
    result.close();

    QString resultName = homePath + "/Downloads/" + current_date + ".csv";
    ui->textEdit->append("结果路径如下:");
    ui->textEdit->append(resultName);
}

void PTF_CSV::on_pushButton_2_clicked()
{
    system("open ~/Downloads/");
}

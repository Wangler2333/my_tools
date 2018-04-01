#ifndef PTF_CSV_H
#define PTF_CSV_H

#include <QMainWindow>

namespace Ui {
class PTF_CSV;
}

class PTF_CSV : public QMainWindow
{
    Q_OBJECT

public:
    explicit PTF_CSV(QWidget *parent = 0);
    ~PTF_CSV();

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::PTF_CSV *ui;
};

#endif // PTF_CSV_H

#include "ptf_csv.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    PTF_CSV w;
    w.show();

    return a.exec();
}

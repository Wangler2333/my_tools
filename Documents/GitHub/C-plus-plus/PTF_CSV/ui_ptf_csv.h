/********************************************************************************
** Form generated from reading UI file 'ptf_csv.ui'
**
** Created by: Qt User Interface Compiler version 5.10.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PTF_CSV_H
#define UI_PTF_CSV_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_PTF_CSV
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QPushButton *pushButton_3;
    QLineEdit *lineEdit;
    QPushButton *pushButton_2;
    QTextEdit *textEdit;
    QPushButton *pushButton;
    QMenuBar *menuBar;

    void setupUi(QMainWindow *PTF_CSV)
    {
        if (PTF_CSV->objectName().isEmpty())
            PTF_CSV->setObjectName(QStringLiteral("PTF_CSV"));
        PTF_CSV->resize(521, 212);
        centralWidget = new QWidget(PTF_CSV);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        pushButton_3 = new QPushButton(centralWidget);
        pushButton_3->setObjectName(QStringLiteral("pushButton_3"));

        gridLayout->addWidget(pushButton_3, 0, 1, 1, 1);

        lineEdit = new QLineEdit(centralWidget);
        lineEdit->setObjectName(QStringLiteral("lineEdit"));

        gridLayout->addWidget(lineEdit, 0, 0, 1, 1);

        pushButton_2 = new QPushButton(centralWidget);
        pushButton_2->setObjectName(QStringLiteral("pushButton_2"));
        pushButton_2->setMinimumSize(QSize(80, 60));

        gridLayout->addWidget(pushButton_2, 2, 1, 1, 1);

        textEdit = new QTextEdit(centralWidget);
        textEdit->setObjectName(QStringLiteral("textEdit"));
        textEdit->setReadOnly(true);

        gridLayout->addWidget(textEdit, 1, 0, 2, 1);

        pushButton = new QPushButton(centralWidget);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setMinimumSize(QSize(80, 60));

        gridLayout->addWidget(pushButton, 1, 1, 1, 1);

        PTF_CSV->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(PTF_CSV);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 521, 22));
        PTF_CSV->setMenuBar(menuBar);

        retranslateUi(PTF_CSV);
        QObject::connect(pushButton, SIGNAL(clicked()), textEdit, SLOT(clear()));

        QMetaObject::connectSlotsByName(PTF_CSV);
    } // setupUi

    void retranslateUi(QMainWindow *PTF_CSV)
    {
        PTF_CSV->setWindowTitle(QApplication::translate("PTF_CSV", "PTF_CSV", nullptr));
        pushButton_3->setText(QApplication::translate("PTF_CSV", "...", nullptr));
        pushButton_2->setText(QApplication::translate("PTF_CSV", "OPEN", nullptr));
        pushButton->setText(QApplication::translate("PTF_CSV", "START", nullptr));
    } // retranslateUi

};

namespace Ui {
    class PTF_CSV: public Ui_PTF_CSV {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PTF_CSV_H

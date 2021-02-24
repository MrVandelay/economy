/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the demonstration applications of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "spreadsheet.h"

#include <QApplication>
#include <QLayout>
#include <string>
#include <vector>
#include <stdio.h>

#include <Python.h>


wchar_t* convertToCharPtr(std::string str)
{
    std::vector<wchar_t> chars(str.begin(), str.end());

    chars.push_back('\0');
    return &chars[0];


}

void createCsvFile()
{
    int argc1;
        wchar_t* argv1[4];

        argc1 = 4;
        wchar_t str1[] = L"Reader.py";
        wchar_t str2[] = L"-o";
        wchar_t str3[] = L"-r";
        wchar_t str4[] = L"freja.csv";

        argv1[0] = str1;
        argv1[1] = str2;
        argv1[2] = str3;
        argv1[3] = str4;

        const char filename[] = "Reader.py";
        FILE* fp;
        printf("1111");
        Py_SetProgramName(argv1[0]);
        Py_Initialize();
        PySys_SetArgv(argc1, argv1);

        fp = _Py_fopen(filename, "r");
        PyRun_SimpleFile(fp, filename);

        Py_Finalize();
 printf("ffff");
sleep(10);
}









int main(int argc, char **argv)
{

    createCsvFile();
    printf("ffff");
    return 0;
    Q_INIT_RESOURCE(spreadsheet);
#ifdef Q_OS_ANDROID
    QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif


    QApplication app(argc, argv);
    SpreadSheet sheet(10, 6);
   // sheet.setWindowIcon(QPixmap(":/images/interview.png"));
    sheet.show();
    sheet.layout()->setSizeConstraint(QLayout::SetFixedSize);

    return app.exec();
}



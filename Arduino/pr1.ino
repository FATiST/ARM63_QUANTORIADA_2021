#include <Encoder.h>
#include "ServoSmooth.h"
int _AvlDFU0 = 0;
bool En_102238583_1;
bool Rst_102238583_1;
long Data_102238583_1;
Encoder myEnc_102238583_1(4, 46);
bool En_124616490_1;
int NewAng_124616490_1;
ServoSmooth servo_124616490_1; // создали объект
long servoTimer_124616490_1;
boolean ServoState_124616490_1;
bool En_161166447_1;
int NewAng_161166447_1;
int Speede_161166447_1;
ServoSmooth servo_161166447_1; // создали объект
long servoTimer_161166447_1;
boolean ServoState_161166447_1;
bool En_161166447_2;
int NewAng_161166447_2;
int Speede_161166447_2;
ServoSmooth servo_161166447_2; // создали объект
long servoTimer_161166447_2;
boolean ServoState_161166447_2;
bool En_161166447_3;
int NewAng_161166447_3;
int Speede_161166447_3;
ServoSmooth servo_161166447_3; // создали объект
long servoTimer_161166447_3;
boolean ServoState_161166447_3;
struct _poligonInexes
{
    int minIndex;
    int maxIndex;
}
;
int _Poligon_InArray_1[5] = {0, 10, 40, 80, 360};
int _Poligon_OutArray_1[5] = {50, 70, 90, 130, 150};
int _Poligon_InArray_3[3] = {0, 60, 360};
int _Poligon_OutArray_3[3] = {50, 80, 120};
String _gtv2;
bool _gtv1 = 0;
int _gtv8 = 10;
int _gtv3 = 100;
int _gtv5 = 50;
int _gtv4 = 90;
int _gtv14 = 90;
int _gtv15 = 90;
bool _gtv6 = 1;
int _gtv7 = 0;
bool _gtv9 = 0;
int _gtv10 = 100;
bool _gtv11 = 0;
bool _gtv12 = 0;
int _gtv13 = 0;
int _gtv16;
bool _changeNumber1_Out = 0;
int _changeNumber1_OLV;
bool _changeNumber4_Out = 0;
int _changeNumber4_OLV;
int _convertStringToNamberOutput_3 = 0;
int _convertStringToNamberOutput_6 = 0;
String _GSFS4 = "0";
int _convertStringToNamberOutput_2 = 0;
bool _tim5I = 0;
bool _tim5O = 0;
unsigned long _tim5P = 0UL;
int _FSFS7IO = 0;
bool _FSFS7CO = 0;
String _GSFS5 = "0";
byte _BitsToByte2_Out = 0;
String _RVFU2Data;
bool _RVFU2Reset = 1;
int _convertStringToNamberOutput_5 = 0;
String _GSFS1 = "0";
String _GSFS7 = "0";
int _FSFS1IO = 0;
bool _FSFS1CO = 0;
bool _tim3I = 0;
bool _tim3O = 0;
unsigned long _tim3P = 0UL;
bool _tim1I = 0;
bool _tim1O = 0;
unsigned long _tim1P = 0UL;
int _FSFS6IO = 0;
bool _FSFS6CO = 0;
int _FSFS3IO = 0;
bool _FSFS3CO = 0;
float _strFunabs1 = 0.00;
bool _tim2I = 0;
bool _tim2O = 0;
unsigned long _tim2P = 0UL;
bool _tim4I = 0;
bool _tim4O = 0;
unsigned long _tim4P = 0UL;
int _convertStringToNamberOutput_9 = 0;
int _convertStringToNamberOutput_7 = 0;
bool _trgrt2 = 0;
bool _trgrt2I = 0;
int _FSFS2IO = 0;
bool _FSFS2CO = 0;
unsigned long _stou1 = 0UL;
String _GSFS6 = "0";
String _GSFS3 = "0";
int _convertStringToNamberOutput_11 = 0;
String _GSFS2 = "0";
bool _changeNumber2_Out = 0;
int _changeNumber2_OLV;
float _strFunabs3 = 0.00;
bool _trgrt3 = 0;
bool _trgrt3I = 0;
int _FSFS4IO = 0;
bool _FSFS4CO = 0;
bool _changeNumber3_Out = 0;
int _changeNumber3_OLV;
bool FTrig_2_Out = 0;
bool FTrig_2_OldStat = 0;
int _FSFS5IO = 0;
bool _FSFS5CO = 0;
bool _tempVariable_bool;
String _tempVariable_String;
int _tempVariable_int;
void setup()
{
    pinMode(17, OUTPUT);
    digitalWrite(17, 1);
    pinMode(2, OUTPUT);
    digitalWrite(2, 0);
    pinMode(8, OUTPUT);
    digitalWrite(8, 0);
    Serial.begin(115200, SERIAL_8N1);
    _stou1 = millis();
    servo_124616490_1.attach(35, 80); // пин и  стартовый угол градусов
    servo_124616490_1.smoothStart(); // "плавно" движемся к нему
    servo_124616490_1.setSpeed(80);
    servo_124616490_1.setAccel(0.5);
    servo_161166447_1.attach(37, 90); // пин и  стартовый угол градусов
    servo_161166447_1.smoothStart(); // "плавно" движемся к нему
    servo_161166447_1.setSpeed(Speede_161166447_1);
    servo_161166447_1.setAccel(0.2);
    servo_161166447_2.attach(36, 90); // пин и  стартовый угол градусов
    servo_161166447_2.smoothStart(); // "плавно" движемся к нему
    servo_161166447_2.setSpeed(Speede_161166447_2);
    servo_161166447_2.setAccel(0.2);
    servo_161166447_3.attach(A5, 90); // пин и  стартовый угол градусов
    servo_161166447_3.smoothStart(); // "плавно" движемся к нему
    servo_161166447_3.setSpeed(Speede_161166447_3);
    servo_161166447_3.setAccel(0.2);
}
void loop()
{
    if (_AvlDFU0)
    {
        _AvlDFU0=0;
    }
     else
    {
        if (Serial.available()) 
        {
            _AvlDFU0=1;
            _readByteFromUART((Serial.read()),0);
        }
    }
    //Плата:1
    digitalWrite(17, 1);
    if (_gtv1)
    {
        if(!_RVFU2Reset)
        {
            _RVFU2Data = String("");
            _RVFU2Reset =1;
        }
    }
     else 
    {
        _RVFU2Reset =0;
    }
    if(_AvlDFU0) 
    {
        _tim4O = 1;
        _tim4I = 1;
    }
     else 
    {
         if(_tim4I) 
        {
            _tim4I = 0;
            _tim4P = millis();
        }
         else 
        {
             if (_tim4O) 
            {
                if (_isTimer(_tim4P, 20)) _tim4O = 0;
            }
        }
    }
    FTrig_2_Out = 0;
    if ((!(_tim4O))&&(FTrig_2_OldStat))
    {
        FTrig_2_Out = 1;
    }
    FTrig_2_OldStat = _tim4O;
    _gtv1 = FTrig_2_Out;
    _gtv2 = _RVFU2Data;
    //Плата:2
    if (_gtv1 == 1) 
    {
        _FSFS6IO = ((_gtv2).indexOf(String("A")));
        _FSFS6CO = _FSFS6IO >-1 ;
        _GSFS6 = (_gtv2).substring(((_FSFS6IO)+(1)));
        _tempVariable_String = _GSFS6;
        _convertStringToNamberOutput_3 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS6CO) 
        {
            _gtv8 = _convertStringToNamberOutput_3;
        }
        _FSFS7IO = ((_gtv2).indexOf(String("B")));
        _FSFS7CO = _FSFS7IO >-1 ;
        _GSFS7 = (_gtv2).substring(((_FSFS7IO)+(1)));
        _tempVariable_String = _GSFS7;
        _convertStringToNamberOutput_11 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS7CO) 
        {
            _gtv3 = _convertStringToNamberOutput_11;
        }
        _FSFS2IO = ((_gtv2).indexOf(String("C")));
        _FSFS2CO = _FSFS2IO >-1 ;
        _GSFS2 = (_gtv2).substring(((_FSFS2IO)+(1)));
        _tempVariable_String = _GSFS2;
        _convertStringToNamberOutput_5 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS2CO) 
        {
            _gtv5 = _convertStringToNamberOutput_5;
        }
        _FSFS4IO = ((_gtv2).indexOf(String("D")));
        _FSFS4CO = _FSFS4IO >-1 ;
        _GSFS4 = (_gtv2).substring(((_FSFS4IO)+(1)));
        _tempVariable_String = _GSFS4;
        _convertStringToNamberOutput_7 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS4CO) 
        {
            _gtv4 = _convertStringToNamberOutput_7;
        }
        _FSFS3IO = ((_gtv2).indexOf(String("E")));
        _FSFS3CO = _FSFS3IO >-1 ;
        _GSFS3 = (_gtv2).substring(((_FSFS3IO)+(1)));
        _tempVariable_String = _GSFS3;
        _convertStringToNamberOutput_6 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS3CO) 
        {
            _gtv14 = _convertStringToNamberOutput_6;
        }
        _FSFS5IO = ((_gtv2).indexOf(String("F")));
        _FSFS5CO = _FSFS5IO >-1 ;
        _GSFS5 = (_gtv2).substring(((_FSFS5IO)+(1)));
        _tempVariable_String = _GSFS5;
        _convertStringToNamberOutput_9 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS5CO) 
        {
            _gtv15 = _convertStringToNamberOutput_9;
        }
        _FSFS1IO = ((_gtv2).indexOf(String("S")));
        _FSFS1CO = _FSFS1IO >-1 ;
        _GSFS1 = (_gtv2).substring(((_FSFS1IO)+(1)));
        _tempVariable_String = _GSFS1;
        _convertStringToNamberOutput_2 = strtol(_tempVariable_String.c_str(),NULL,10);
        if (_FSFS1CO) 
        {
            _gtv16 = _convertStringToNamberOutput_2;
        }
    }
    //Плата:3
    if (1) 
    {
         if (_trgrt2I) 
        {
             _trgrt2 = 0;
        }
         else 
        {
            _trgrt2 = 1;
            _trgrt2I = 1;
        }
    }
     else 
    {
        _trgrt2 = 0;
        _trgrt2I = 0;
    }
    ;
    if (((_trgrt2) || (0))) 
    {
         if (_trgrt3I) 
        {
             _trgrt3 = 0;
        }
         else 
        {
            _trgrt3 = 1;
            _trgrt3I = 1;
        }
    }
     else 
    {
        _trgrt3 = 0;
        _trgrt3I = 0;
    }
    ;
    En_102238583_1 = 1;
    Rst_102238583_1 = _trgrt3;
    if(En_102238583_1) 
    {
        Data_102238583_1 = myEnc_102238583_1.read();
        if (Rst_102238583_1) 
        {
            myEnc_102238583_1.write(0);
        }
    }
    _gtv7 = (Data_102238583_1)/(13.3);
    //Плата:4
    _strFunabs3 = abs((_gtv7)-(_gtv13));
    _strFunabs1 = abs((_gtv8)-(_gtv7));
    analogWrite(12, (constrain(((_poligon((_strFunabs1), _Poligon_InArray_1, _Poligon_OutArray_1, 5))), (110), ((_poligon((_strFunabs3), _Poligon_InArray_3, _Poligon_OutArray_3, 3))))));
    _gtv10 = (constrain(((_poligon((_strFunabs1), _Poligon_InArray_1, _Poligon_OutArray_1, 5))), (110), ((_poligon((_strFunabs3), _Poligon_InArray_3, _Poligon_OutArray_3, 3)))));
    _gtv11 = (_gtv8) > (_gtv7);
    digitalWrite(8, (_gtv8) > (_gtv7));
    _gtv12 = ((!((_gtv8) > (_gtv7))) && ((_gtv7) != (_gtv8)));
    digitalWrite(2, ((!((_gtv8) > (_gtv7))) && ((_gtv7) != (_gtv8))));
    if (!((_gtv7) != (_gtv8))) 
    {
        _gtv13 = _gtv7;
    }
    _gtv9 = (_gtv7) != (_gtv8);
    //Плата:5
    if (_changeNumber1_Out) 
    {
        _changeNumber1_Out = 0;
    }
     else 
    {
        _tempVariable_int = (map((_gtv14), (0), (180), (129), (0)));
        if (_tempVariable_int != _changeNumber1_OLV) 
        {
            _changeNumber1_OLV = _tempVariable_int;
            _changeNumber1_Out = 1;
        }
    }
    if(_changeNumber1_Out) 
    {
        _tim2O = 1;
        _tim2I = 1;
    }
     else 
    {
         if(_tim2I) 
        {
            _tim2I = 0;
            _tim2P = millis();
        }
         else 
        {
             if (_tim2O) 
            {
                if (_isTimer(_tim2P, 3000)) _tim2O = 0;
            }
        }
    }
    En_124616490_1 = ((_gtv6) && (_tim2O));
    NewAng_124616490_1 = (map((_gtv14), (0), (180), (129), (0)));
    ServoState_124616490_1 = servo_124616490_1.tick(); // здесь происходит движение серво по встроенному таймеру!
    if(En_124616490_1)
    {
        if (millis() - servoTimer_124616490_1 >= 20) 
        {
            servoTimer_124616490_1 = millis();
            servo_124616490_1.start();
            servo_124616490_1.setTargetDeg(NewAng_124616490_1);
        }
    }
    else
    {
        servo_124616490_1.stop();
    }
    if (_changeNumber3_Out) 
    {
        _changeNumber3_Out = 0;
    }
     else 
    {
        _tempVariable_int = (map((_gtv4), (0), (180), (129), (0)));
        if (_tempVariable_int != _changeNumber3_OLV) 
        {
            _changeNumber3_OLV = _tempVariable_int;
            _changeNumber3_Out = 1;
        }
    }
    if(_changeNumber3_Out) 
    {
        _tim3O = 1;
        _tim3I = 1;
    }
     else 
    {
         if(_tim3I) 
        {
            _tim3I = 0;
            _tim3P = millis();
        }
         else 
        {
             if (_tim3O) 
            {
                if (_isTimer(_tim3P, 3000)) _tim3O = 0;
            }
        }
    }
    En_161166447_3 = ((_gtv6) && (_tim3O));
    NewAng_161166447_3 = _gtv4;
    Speede_161166447_3 = _gtv16;
    ServoState_161166447_3 = servo_161166447_3.tick(); // здесь происходит движение серво по встроенному таймеру!
    servo_161166447_3.setSpeed(Speede_161166447_3);
    if(En_161166447_3)
    {
        if (millis() - servoTimer_161166447_3 >= 20) 
        {
            servoTimer_161166447_3 = millis();
            servo_161166447_3.start();
            servo_161166447_3.setTargetDeg(NewAng_161166447_3);
        }
    }
    else
    {
        servo_161166447_3.stop();
    }
    if (_changeNumber4_Out) 
    {
        _changeNumber4_Out = 0;
    }
     else 
    {
        _tempVariable_int = _gtv5;
        if (_tempVariable_int != _changeNumber4_OLV) 
        {
            _changeNumber4_OLV = _tempVariable_int;
            _changeNumber4_Out = 1;
        }
    }
    if(_changeNumber4_Out) 
    {
        _tim1O = 1;
        _tim1I = 1;
    }
     else 
    {
         if(_tim1I) 
        {
            _tim1I = 0;
            _tim1P = millis();
        }
         else 
        {
             if (_tim1O) 
            {
                if (_isTimer(_tim1P, 3000)) _tim1O = 0;
            }
        }
    }
    En_161166447_2 = ((_gtv6) && (_tim1O));
    NewAng_161166447_2 = _gtv5;
    Speede_161166447_2 = _gtv16;
    ServoState_161166447_2 = servo_161166447_2.tick(); // здесь происходит движение серво по встроенному таймеру!
    servo_161166447_2.setSpeed(Speede_161166447_2);
    if(En_161166447_2)
    {
        if (millis() - servoTimer_161166447_2 >= 20) 
        {
            servoTimer_161166447_2 = millis();
            servo_161166447_2.start();
            servo_161166447_2.setTargetDeg(NewAng_161166447_2);
        }
    }
    else
    {
        servo_161166447_2.stop();
    }
    if (_changeNumber2_Out) 
    {
        _changeNumber2_Out = 0;
    }
     else 
    {
        _tempVariable_int = _gtv3;
        if (_tempVariable_int != _changeNumber2_OLV) 
        {
            _changeNumber2_OLV = _tempVariable_int;
            _changeNumber2_Out = 1;
        }
    }
    if(_changeNumber2_Out) 
    {
        _tim5O = 1;
        _tim5I = 1;
    }
     else 
    {
         if(_tim5I) 
        {
            _tim5I = 0;
            _tim5P = millis();
        }
         else 
        {
             if (_tim5O) 
            {
                if (_isTimer(_tim5P, 3000)) _tim5O = 0;
            }
        }
    }
    En_161166447_1 = ((_gtv6) && (_tim5O));
    NewAng_161166447_1 = _gtv3;
    Speede_161166447_1 = _gtv16;
    ServoState_161166447_1 = servo_161166447_1.tick(); // здесь происходит движение серво по встроенному таймеру!
    servo_161166447_1.setSpeed(Speede_161166447_1);
    if(En_161166447_1)
    {
        if (millis() - servoTimer_161166447_1 >= 20) 
        {
            servoTimer_161166447_1 = millis();
            servo_161166447_1.start();
            servo_161166447_1.setTargetDeg(NewAng_161166447_1);
        }
    }
    else
    {
        servo_161166447_1.stop();
    }
    //Плата:6
    _tempVariable_bool = _gtv11;
    bitWrite(_BitsToByte2_Out, 0, _tempVariable_bool);
    _tempVariable_bool = _gtv12;
    bitWrite(_BitsToByte2_Out, 1, _tempVariable_bool);
    _tempVariable_bool = _gtv6;
    bitWrite(_BitsToByte2_Out, 2, _tempVariable_bool);
    _tempVariable_bool = 0;
    bitWrite(_BitsToByte2_Out, 3, _tempVariable_bool);
    _tempVariable_bool = 1;
    bitWrite(_BitsToByte2_Out, 4, _tempVariable_bool);
    _tempVariable_bool = 0;
    bitWrite(_BitsToByte2_Out, 5, _tempVariable_bool);
    _tempVariable_bool = 0;
    bitWrite(_BitsToByte2_Out, 6, _tempVariable_bool);
    _tempVariable_bool = 0;
    bitWrite(_BitsToByte2_Out, 7, _tempVariable_bool);
    if (1)
    {
         if (_isTimer(_stou1, 1000)) 
        {
            Serial.println((((String(_gtv8, DEC))) + (String("  ")) + ((String(_gtv7, DEC))) + (String("  ")) + ((String(_gtv10, DEC))) + (String("  ")) + ((String(_BitsToByte2_Out, BIN)))));
            _stou1 = millis();
        }
    }
     else 
    {
        _stou1 = millis();
    }
}
bool _isTimer(unsigned long startTime, unsigned long period)
{
    unsigned long currentTime;
    currentTime = millis();
    if (currentTime>= startTime) 
    {
        return (currentTime>=(startTime + period));
    }
     else 
    {
        return (currentTime >=(4294967295-startTime+period));
    }
}
void _readByteFromUART(byte data,int port)
{
    if (port==0)
    {
        _RVFU2Data += char(data);
    }
}
int _poligon(int value, int intArray[], int outArray[], int arraySize)
{
    struct  _poligonInexes indexes;
    indexes = _getPoligonIndexes(value, intArray, arraySize);
    return map(value, intArray[indexes.minIndex], intArray[indexes.maxIndex], outArray[indexes.minIndex], outArray[indexes.maxIndex]);
}
struct  _poligonInexes _getPoligonIndexes(int value, int array[], int arraySize)
{
    struct  _poligonInexes result;
    int i;
    result.minIndex = 0;
    result.maxIndex = 0;
    for (i = 0; i < arraySize; i++) 
    {
        if (array [result.minIndex] > array[i]) 
        {
            result.minIndex = i;
        }
        if (array [result.maxIndex] < array[i]) 
        {
            result.maxIndex = i;
        }
    }
    for (i = 0; i < arraySize; i++)
    {
        if ((array [i] >= value) && (array [result.maxIndex] > array[i])) 
        {
            result.maxIndex = i;
        }
    }
    if (result.maxIndex==0)
    {
        result.minIndex = 0;
        result.maxIndex=1;
    }
     else 
    {
         result.minIndex = result.maxIndex -1;
    }
    return result;
    return result;
}

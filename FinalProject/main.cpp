#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"

Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
BBCar car(pin5, pin6, servo_ticker);

// BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D1,D0); //tx,rx
BufferedSerial Xbee(A1,A0); //tx,rx

Thread thread_uart;
Thread thread_Xbee;

void func_uart();
void func_Xbee();

int main() {

    thread_uart.start(&func_uart);
    thread_Xbee.start(&func_Xbee);

    return 0;
}

void func_uart(){
    char buf[256], outbuf[256];
    FILE *devin = fdopen(&uart, "r");
    FILE *devout = fdopen(&uart, "w");
    uart.set_baud(9600);

    while (1) {
        memset(buf, 0, 256);
        for( int i = 0; ; i++ ) {
            char recv = fgetc(devin);
            // printf("%c", recv);     // test only 
            if(recv == '\n') {
                printf("\r\n");
                break;
            }
            buf[i] = fputc(recv, devout);
        }
        // printf ("\n");              // test only 
        RPC::call(buf, outbuf);
    }
}

void func_Xbee(){
    char buf[256], outbuf[256];
    FILE *devin = fdopen(&Xbee, "r");
    FILE *devout = fdopen(&Xbee, "w");
    uart.set_baud(9600);

    while (1) {
        memset(buf, 0, 256);
        for( int i = 0; ; i++ ) {
            char recv = fgetc(devin);
            // printf ("\n");              // test only 
            if(recv == '\n') {
                printf("\r\n");
                break;
            }
            buf[i] = fputc(recv, devout);
        }
        // printf ("\n");                  // test only 
        RPC::call(buf, outbuf);
    }
}
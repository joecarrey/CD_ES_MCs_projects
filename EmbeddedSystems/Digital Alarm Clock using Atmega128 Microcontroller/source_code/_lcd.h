#include <avr/io.h>
#include "_main.h"

#define LCD_WDATA PORTA
#define LCD_WINST PORTA
#define LCD_CTRL PORTG
#define LCD_RS 2
#define LCD_RW 1
#define LCD_EN 0

#define RIGHT 1
#define LEFT 0

void portInit()
{
	DDRA = 0xff; // portA is output
	DDRG = 0x0f; // lower 4 bits = output
}

// WRITE TO DATA REGISTER
void LCD_Data(char ch)
{
	LCD_WDATA = ch;
	LCD_CTRL |= (1<<LCD_RS); // rs = 1 (Data Reg)
	LCD_CTRL &= ~(1<<LCD_RW); // rw = 0 (write data)
	LCD_CTRL |= (1<<LCD_EN); // en = 1 (enable)
	_delay_us(2);
	LCD_CTRL &= ~(1<<LCD_EN); // en = 0 (disable)
	_delay_us(42);
}

// WRITE TO CONTROL REGISTER
void LCD_Cmd(char ch)
{
	LCD_WINST = ch;
	LCD_CTRL &= ~(1<<LCD_RS); // rs = 0 (Inst Reg)
	LCD_CTRL &= ~(1<<LCD_RW); // rw = 0 (write data)
	LCD_CTRL |= (1<<LCD_EN); // en = 1 (enable)
	_delay_us(2);
	LCD_CTRL &= ~(1<<LCD_EN); // en = 0 (disable)
	_delay_us(42);
}

void LCD_Clear()
{
	LCD_Cmd(0x01);
}

void Cursor_Blink(){
	LCD_Cmd(0x0f); // display on, cursor on, blink
	LCD_Clear();
}

void Cursor_NoBlink(){
	LCD_Cmd(0x0c); // display on, cursor on, blink
	LCD_Clear();
}

void LCD_Init()
{
	portInit();
	LCD_Cmd(0x38); //ddram 2 lines, 5*7 font, 8 bit
	LCD_Cmd(0x0f); // display on, cursor on, blink
	LCD_Cmd(0x06); // shift cursor right
	LCD_Clear();
}

void LCD_Print(char *str)
{
	while (*str != 0)
	{
		LCD_Data(*str);
		str++;
	}
}

// X - horizontal | Y - vertical
void LCD_Pos(unsigned char x, unsigned char y)
{
	LCD_Cmd(0x80 | (x + y * 0x40));
}

// put position and print (joined)
void LCD_PosPrint(unsigned char x, unsigned char y, char *str){
	LCD_Pos(x, y);
	LCD_Print(str);
}

void Cursor_Home(){
	LCD_Cmd(0x02);
}

void LCD_Shift(char p){
	if(p == RIGHT)
	LCD_Cmd(0x1f);
	else if(p == LEFT)
	LCD_Cmd(0x18);
}

void Cursor_Shift(char p){
	if(p == RIGHT)
	LCD_Cmd(0x14);
	else
	LCD_Cmd(0x10);
}
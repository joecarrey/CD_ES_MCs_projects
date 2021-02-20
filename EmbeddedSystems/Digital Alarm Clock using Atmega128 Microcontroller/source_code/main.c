/*
* Team: Project 42
* Project: Digital Alarm CLock
*/

#include "_main.h"
#include "_lcd.h"

#define CTCnum 59 // CTC number ~ 60

// CONSTs
const int MONTHS[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
const char WEEKDAYS[7][4] = {"Mon", "Tue", "Wed", "Thu", "Fri" , "Sat", "Sun"};

// DATE + TIME VALUES
int year = 2020, month = 11, day = 30, maxDayValue, leapYear; // for Date
int fullHour, hour, minute, second, msecond; // for Clock
int stopwatchHour, stopwatchMinute, stopwatchSecond, stopwatchMsec; // for Stopwatch
int alarmHour, alarmMinute;  // for Alarm
int inputNum; // for switch inputing values

// CHARs
unsigned char tCNT, blinks, blinksDelay;
char date[16], time[16], stopwatch[16], alarm[16], weekday[4];
char midday[3] = "AM", aMidday[3] = "AM";
char xPos, switchKey, targetIndex;

// FLAGs
int isPM, isAlarmPM;
char stopwatch_ON, alarm_ON, isRinging, clockIsSet;
char inMain, inStopwatch, inAlarm, inClock = 1;
char OFF = 0xff;


// *********************************************************************
// *************************  FUNCTIONS  *******************************
// *********************************************************************
void Init_Timer0(){
	TCCR0 = 0x0f;	// CTC mode, Prescale 1024
	TIMSK = 0x02;	// Output compare interrupt enable
	OCR0 = 1;		// count 0 to 1
	sei();			// Enable global interrupts
}

void Init_Ports(){
	// Switch inputs - all work
	PORTD = 0xff; DDRD = 0x00;
	// LED outputs - turn off
	PORTB = 0xff; DDRB = 0xff;
	// LCD outputs
	PORTA = 0x00; DDRA = 0xff;
}

void Init_Devices(){
	Init_Ports();
	LCD_Init();
}

// used for switch inputs when setting Clock or Alarm
void switchController(){
	switch(switchKey)
	{
		case 0xfe: // 1st - decrease number
		inputNum = -1;
		break;
		
		case 0xfd: // 2nd - increase number
		inputNum = +1;
		break;

		case 0xfb: // 3rd - go prev
		inputNum = 0;
		if(targetIndex!=0) targetIndex--; //min 0 value
		break;
		
		case 0xf7: // 4th - go next
		inputNum = 0;
		if(targetIndex!=11) targetIndex++; //max 10 value
		break;
		
		case 0x7f: // last - exit to main
		if(clockIsSet) mainMenu();
		break;
	}
}

// *********************************************************************
// **************************** CLOCK **********************************
// *********************************************************************

// change values of Date & Time on input (Decrease or Increase)
void changeValue(int* target, int mod)
{
	// mod = # of possible values
	// mod = 60 -> result range[0~59]
	// mod = 2 -> result range[0~1]
	// mod = N -> result range[1~N]
	int zero = (mod == 60) ? -1 : 0;
	int result = (mod == 2) ? 0 : mod;
	*target += inputNum;
	*target %= mod;
	*target = (*target == zero) ? ((mod == 60) ? 59 : result) : abs(*target);
}

// change the 24-hours -> result range [0~23]
void fullHourChange(int n){
	fullHour += n;
	fullHour %= 24;
	fullHour = (fullHour == -1) ? 23 : fullHour;
	
	//update the Midday regarding to 24-hours
	isPM = (fullHour > 11) ? 1 : 0;
	strcpy(midday, (isPM) ? "PM" : "AM");
}

// knowing year, month, day -> get Week day
int getWeekday(int y, int m, int d)
{
	static int t[] = {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4};
	y -= m < 3;
	return ((y + y/4 - y/100 + y/400 + t[m-1] + d - 1) % 7);
}

// get max day of the given month
void getMaxDayValue()
{
	maxDayValue = MONTHS[month - 1];
	if(month == 2)
	maxDayValue = (leapYear == 1) ? 29 : 28;
}

// time in 12-hour method
void printTime(){
	sprintf(time, "%s %02d:%02d:%02d", midday, hour, minute, second);
	LCD_PosPrint(0, 1, time);
	LCD_Pos(xPos, 1);
}

void printDate(){
	sprintf(date, "%04d %02d/%02d %s", year, day, month, weekday);
	LCD_PosPrint(0, 0, date);
	LCD_Pos(xPos, 0);
}

// update and get the Date (maxDayValue and Weekday)
void getDate()
{
	// whether given year is leap or not
	leapYear = (((year % 4 == 0) && (year % 100!= 0)) || (year % 400 == 0)) ? 1 : 0;
	getMaxDayValue();
	int index = getWeekday(year, month, day);
	strcpy(weekday, WEEKDAYS[index]);
	if (inClock) printDate();
}

// CLOCK Screen
void goClock(){
	inStopwatch = inAlarm = inMain = 0;
	inClock = 1;
	Cursor_NoBlink();
	getDate();
	printTime();
}

void setClock()
{
	Cursor_Blink();
	getDate();
	clockIsSet = switchKey = targetIndex = 0;
	LCD_Pos(3,0);
	
	// indexes ->
	//0 = year | 1 = month | 2 = day | 3 = hour | 4 = min | 5 = sec
	while(targetIndex < 6)
	{
		switchKey = 0xff & PIND; // all inputs work
		switchController();
		
		// if Input Pressed
		if(switchKey != 0xff)
		{
			// allow only 1 press in 200ms
			_delay_ms(200);
			
			// change DATE
			if (targetIndex == 0){
				xPos = 3;
				year += inputNum;
				getDate();
			}
			else if(targetIndex == 1)
			{
				xPos = 9;
				changeValue(&month, 12);
				getDate();
			}
			else if(targetIndex == 2){
				xPos = 6;
				changeValue(&day, maxDayValue);
				getDate();
			}
			
			// change TIME
			else if(targetIndex == 3){
				xPos = 4;
				changeValue(&hour, 12);
				fullHourChange(inputNum);
				
			}
			else if(targetIndex == 4){
				xPos = 7;
				changeValue(&minute, 60);
			}
			else if(targetIndex == 5){
				xPos = 10;
				changeValue(&second, 60);
			}
			
			// print the DATE & TIME on LCD
			
			if(targetIndex > 2) printTime();
			else printDate();
		}
	}
	
	clockIsSet = 1;
	//goClock();
}

// *********************************************************************
// **************************** STOPWATCH *****************************
// *********************************************************************

void printStopwatch()
{
	sprintf(stopwatch, "%02d:%02d:%02d:%02d", stopwatchHour, stopwatchMinute, stopwatchSecond, stopwatchMsec);
	LCD_PosPrint(0, 1, stopwatch);
	
	switchKey = 0xff & PIND;
	switch(switchKey)
	{
		case 0xfe: // 1st switch - START/PAUSE
		stopwatch_ON = !stopwatch_ON; // clicker
		LCD_PosPrint(0, 0, stopwatch_ON ? "1-Pause" : "1-Start");
		break;
		case 0xfd: // 2nd switch - STOP
		LCD_PosPrint(0, 0, "1-Start");
		stopwatch_ON = 0;
		stopwatchHour = stopwatchMinute = stopwatchSecond = stopwatchMsec = 0;
		break;
		case 0x7f: // last switch - EXIT
		mainMenu();
		break;
	}
}

// STOPWACH Screen
void goStopwatch()
{
	inClock = inAlarm = inMain = 0;
	inStopwatch = 1;
	Cursor_NoBlink();
	LCD_PosPrint(0, 0, "1-Start   2-Stop");
	printStopwatch();
}

// *********************************************************************
// **************************** ALARM **********************************
// *********************************************************************

void printAlarm(){
	sprintf(alarm, "%s %02d:%02d", aMidday, alarmHour, alarmMinute);
	LCD_PosPrint(0,1,alarm);
	LCD_Pos(xPos, 1);
}

void setAlarm(){
	
	switchKey = 0xff & PIND;
	switchController();
	
	if(switchKey != 0xff)
	{
		// allow only 1 press in 200ms
		_delay_ms(200);
		if(targetIndex > 3) targetIndex = 3;
		// change TIME
		if(targetIndex == 0){
			xPos = 0;
			changeValue(&isAlarmPM, 2);
			strcpy(aMidday, isAlarmPM ? "PM" : "AM");
		}
		else if(targetIndex == 1){
			xPos = 4;
			changeValue(&alarmHour, 12);
		}
		else if(targetIndex == 2){
			xPos = 7;
			changeValue(&alarmMinute, 60);
			LCD_Clear();
			LCD_PosPrint(0, 0,"Want to Set?");
		}
		// alarm is set
		else if(targetIndex == 3){
			LCD_PosPrint(0, 0, "Alarm is Set:");
			alarm_ON = 1;
		}
		
		// dont show alarm if last switch pressed
		if(switchKey!= 0x7f) printAlarm();
	}
}

// ALARM screen
void goAlarm()
{
	inStopwatch = inClock = inMain = 0;
	inAlarm = 1;
	Cursor_Blink();
	LCD_PosPrint(xPos, 0, alarm_ON ? "Alarm is Set:" : "Alarm isn't Set:");
	printAlarm();
	
	if(!alarm_ON){
		strcpy(aMidday, midday);
		isAlarmPM = isPM;
		alarmHour = hour;
		alarmMinute = minute;
	}
}

void Led_Alarm()
{
	// alarming flag
	isRinging = (blinks < 11 && strcmp(aMidday,midday) == 0
	&& alarmHour == hour && alarmMinute == minute) ? 1 : 0;

	// turn of led
	if (!isRinging) PORTB = 0xff;
	// blink every 2 sec
	else if(blinksDelay > 1){
		blinks++;
		OFF = ~OFF;
		PORTB = OFF;
		blinksDelay = 0;
	}
}

// *********************************************************************
// ********************** ISR for timer0 CTC mode **********************
// *********************************************************************

// TOV0 = (1/(14.7456Mhz) * 1024(prescale)) * 100 (CTC) = 6.945s
// 6.945s * 144 = 1 sec
// in our case -> CTC = 60 , multiplier = 100
ISR(TIMER0_COMP_vect)
{
	tCNT++;
	if(tCNT == CTCnum){
		tCNT = 0;
		msecond++;
		
		// reset milliseconds and update seconds
		if(msecond == 99){
			second++;
			msecond = 0;
			if(isRinging) blinksDelay++;
		}
		// reset seconds and update minutes
		if(second == 60){
			minute++;
			second=0;
		}
		// reset minutes and update both 12 and 24 hours
		if(minute == 60){
			hour++;
			fullHour++;
			minute=0;
			//reset 12-hours
			if(hour == 13) hour = 1;
		}
		// update midday values
		if(fullHour == 12)
		fullHourChange(0);
		// reset 24-hours w/ #-blinks and update days and middays
		if(fullHour == 24){
			fullHourChange(0);
			LCD_Clear();
			day++;
			getDate();
			blinks = 0;
		}
		// reset days and update months
		if(day > maxDayValue){
			month++;
			day = 1;
		}
		// reset months and update year
		if (month>12)
		{
			year++;
			month = 1;
		}
		
		// =====================================
		// WHERE I AM - Places
		// =====================================
		if(inMain){
			switchKey = 0xff & PIND;
			if(switchKey == 0xfe) goClock(); //1st switch
			if(switchKey == 0xfd) goAlarm(); //2nd switch
			if(switchKey == 0xfb) goStopwatch(); //3st switch
		}
		else if(inStopwatch) printStopwatch();
		else if(inClock) printTime();
		else if(inAlarm) setAlarm();
		
		// if pressed -> allow only 1 press in 200ms
		if(switchKey != 0xff) _delay_ms(200);
		
		// =====   If Flags ON =======
		if(alarm_ON) Led_Alarm();
		if(stopwatch_ON)
		{
			stopwatchMsec = msecond + 1;
			// update seconds
			if(stopwatchMsec == 99)
			stopwatchSecond++;
			// reset seconds and update minutes
			if (stopwatchSecond == 60){
				stopwatchMinute++;
				stopwatchSecond = 0;
			}
			// reset minutes and update hours
			if (stopwatchMinute == 60){
				stopwatchHour++;
				stopwatchMinute = 0;
			}
		}
		
		// ============ for cases when SETTING Clock =============
		switchKey = 0xff & PIND;
		// to GO to MainMenu if last Switch Pressed and Clock is Set
		if(switchKey == 0x7f && clockIsSet) mainMenu();
		// press 7th switch to RESET CLOCK while ONLY in Clock Screen and it is Set
		else if(inClock && switchKey == 0xbf && clockIsSet) setClock();
	}
}


// ***********************************************************
// ********************* WELCOME + MENU **********************
// ***********************************************************

void mainMenu()
{
	targetIndex = xPos = 0;
	inStopwatch = inClock = inAlarm = 0;
	inMain = 1;
	Cursor_NoBlink();
	LCD_PosPrint(xPos, 0, "1-Clock  2-Alarm");
	LCD_PosPrint(xPos, 1, "  3-Stopwatch   ");
}

void Welcome()
{
	char TEXT[16][16] = {
		"    WELCOME    ",
		"Press for Next ",
		"We use switches",
		"1 2 3 4 and 7 8",
		"Inside Clock:  ",
		"1 2 3 4     7 8",
		"  Go Back - 8  ",
		"Reset Clock - 7",
		"Update num: 1 2",
		"3-prev   4-next",
		"Inside Alarm:  ",
		"1 2 3 4       8",
		"In Stopwatch:  ",
		"1-start 2-stop ",
		"First SET DATE ",
		"-------------->"
	};
	
	for(int i = 0; i < 16; i++)
	{
		switchKey = 0xff;
		LCD_PosPrint(0, 0, TEXT[i]);
		LCD_PosPrint(0, 1, TEXT[++i]);
		while(switchKey == 0xff) switchKey = 0xff & PIND;
		_delay_ms(200);
	}
}

// ***************************************************************
// **************************** MAIN *****************************
// ***************************************************************

int main(void)
{
	// set all them to ZERO
	fullHour = hour = minute = second = msecond = stopwatchHour = stopwatchMinute
	= stopwatchSecond = stopwatchMsec = alarmHour
	= alarmMinute = inputNum = tCNT = blinks = blinksDelay
	= xPos = targetIndex = isPM = isAlarmPM
	= stopwatch_ON = alarm_ON = isRinging = inMain
	= inStopwatch = inAlarm = clockIsSet = 0;
	
	Init_Devices();
	Welcome();
	Cursor_Blink();
	setClock();
	mainMenu();
	Init_Timer0();
	
	while (1);
}


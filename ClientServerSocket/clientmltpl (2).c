#include <stdio.h>
#include <string.h> //strlen
#include <stdlib.h>
#include <errno.h>
#include <unistd.h> //close
#include <arpa/inet.h> //close
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h> //FD_SET, FD_ISSET, FD_ZERO macros
#define TRUE 1
#define FALSE 0
#define PORT 8888
int main(int argc, char const *argv[])
{
struct sockaddr_in address;
int sock = 0, valread;
struct sockaddr_in serv_addr;
char *hello = "Hello from client";
char buffer[1024] = {0}, cchat[1024];
char *bye = "bye";
printf("CREATING CLIENT SOCKET .....\n");
if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
{
printf("\n Socket creation error \n");
return -1;
}
printf("DEFINING SOCKET FAMILY, ADDRESS & PORT .....\n");
memset(&serv_addr, '0', sizeof(serv_addr));
serv_addr.sin_family = AF_INET;
serv_addr.sin_port = htons(PORT);
// Convert IPv4 and IPv6 addresses from text to binary form
if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
{
printf("\nInvalid address/ Address not supported \n");
return -1;
}
printf("CLIENT CONNECTING ON PORT 8888 TO COMMUNICATE WITH SERVER..\n");
if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
{
printf("\nConnection Failed \n");
return -1;
}
send(sock , hello , strlen(hello) , 0 );
printf("Hello message sent\n");
valread = read( sock , buffer, 1024);
printf("%s\n",buffer );
printf(" Ready for Chat....\n");
memset(buffer, 0, sizeof(buffer));
valread = read( sock , buffer, 1024);
printf("%s\n",buffer );
while(1)
{
memset(buffer, 0, sizeof(buffer));
memset(cchat, 0, sizeof(cchat));
printf("CLIENT : ");
fgets (cchat, sizeof(cchat), stdin);
send(sock , cchat , strlen(cchat) , 0 );
cchat[strlen(cchat)] = '\0';
if(strncmp(cchat, bye, strlen(bye))==0)
break;
valread = read( sock , buffer, 1024);
printf("%s\n",buffer );

/*
memset(cchat, 0, sizeof(cchat));
printf("CLIENT : ");
fgets (cchat, sizeof(cchat), stdin);
send(sock , cchat , strlen(cchat) , 0 );
cchat[strlen(cchat)] = '\0';
if(strncmp(cchat, bye, strlen(bye))==0)
break;
memset(buffer, 0, sizeof(buffer));
valread = read( sock , buffer, 1024);
printf("%s\n",buffer );
*/
}
return 0;
}

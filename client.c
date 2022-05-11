#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h> 

#include "Message.h"

#define IP_ADDR "127.0.0.1"

int main(int argc, char *argv[])
{
    int sockfd = 0, n = 0;
    char recvBuff[1024];
    struct sockaddr_in serv_addr; 

    memset(recvBuff, '0',sizeof(recvBuff));
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Error : Could not create socket \n");
        return 1;
    } 

    memset(&serv_addr, '0', sizeof(serv_addr)); 

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000); 

    if(inet_pton(AF_INET, IP_ADDR, &serv_addr.sin_addr)<=0)
    {
        printf("\n inet_pton error occured\n");
        return 1;
    } 

    if( connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
       printf("\n Error : Connect Failed \n");
       return 1;
    } 
    Message* received_test_struct = malloc(sizeof(Message));
    while ( (n = read(sockfd, received_test_struct, sizeof(Message))) > 0)
    {
       /* recvBuff[n] = 0;
        if(fputs(recvBuff, stdout) == EOF)
        {
            printf("\n Error : Fputs error\n");
        }*/
        
        printf("{ X = %f Y = %f M = %s }\n", received_test_struct->x, received_test_struct->y, received_test_struct->message);
        
       
        /*
        if(read(sockfd, received_test_struct, sizeof(Message)) < 0){
            printf("read struct < 0");
        }
        else{
            printf("%f %f %s\n", received_test_struct->x, received_test_struct->y, received_test_struct->message);
        }
        */
        
    } 
    free(received_test_struct);
    if(n < 0)
    {
        printf("\n Read error \n");
    }

    return 0;
}
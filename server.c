#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/syscall.h>
#include "Message.h"

char* commands[] = 
{
	"status",
	"pingcrc"
};

void* connection_handler(void *socket_desc) {
	
	/* Get the socket descriptor */
	int sock = * (int *)socket_desc;
	int read_size;
	char *message , client_message[2000];
	pid_t clientTid = syscall(SYS_gettid);
	 
	printf("\n ----- NEW CLIENT OPENED ID: %d ----- \n", clientTid);
	memset(client_message, 0, 2000);
	// free(test_struct_message);
	Message* received_test_struct = malloc(sizeof(Message));
	ping_crc* ping_struct = malloc(sizeof(ping_crc));

	do {

		/* Read command part */
		/* Exisiting commands:
			-> status
			-> pingcrc
			->
		*/

		read_size = recv(sock , client_message , 20 , 0);

		client_message[read_size] = '\0';
		printf("\n[ %d -> %s ]\n", read_size, client_message);

		if(strcmp(client_message, commands[0]) == 0)
		{
			printf("Waiting for message\n");
			read_size = recv(sock, received_test_struct, sizeof(Message), 0);
			printf("{ %f %f %s \t}", received_test_struct->x, received_test_struct->y, received_test_struct->message);
			/* Send the message back to client */
			//write(sock, received_test_struct, sizeof(Message));
		}
		//printf("%s \n%s", client_message, commands[1]);
		if(strcmp(client_message, commands[1]) == 0)
		{
			read_size = recv(sock, ping_struct, sizeof(ping_crc), 0);
			/* Send the message back to client */
			printf("pingcrc {%d}", ping_struct->ping);
			write(sock, ping_struct, sizeof(ping_crc));
		}
		
		/* Clear the message buffer */
		memset(client_message, 0, 2000);

	} while(read_size > 0); /* Wait for empty line */
	free(received_test_struct);
	
	fprintf(stderr, "Client disconnected\n"); 
	
	close(sock);
	pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
	int listenfd = 0, connfd = 0;
	struct sockaddr_in serv_addr; 
	
	pthread_t thread_id;
	listenfd = socket(AF_INET, SOCK_STREAM, 0);
	memset(&serv_addr, '0', sizeof(serv_addr));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(5000); 

	bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)); 

	listen(listenfd, 10); 

	for (;;) {
		connfd = accept(listenfd, (struct sockaddr*)NULL, NULL);
		fprintf(stderr, "\nConnection accepted\n"); 
		pthread_create(&thread_id, NULL, connection_handler , (void *) &connfd);
	}
}

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include "Message.h"


void* connection_handler(void *socket_desc) {
	
	/* Get the socket descriptor */
	int sock = * (int *)socket_desc;
	int read_size;
	char *message , client_message[2000];
	 
	printf("\n ----- NEW CLIENT OPENED ----- \n");
	//write(sock , message , strlen(message));

	/* Send test struct */
	// Message* test_struct_message = malloc(sizeof(Message));
	// test_struct_message->x = 1.0;
	// test_struct_message->y = 2.0;
	// strcpy(test_struct_message->message, "Sent");
	// write(sock, test_struct_message, sizeof(Message));
	
	// /* Send modified test struct */
	// strcpy(test_struct_message->message, "Sent sdfgs dfg");
	// write(sock, test_struct_message, sizeof(Message));
	
	// /* Send modified test struct 2 */
	// strcpy(test_struct_message->message, "Sen asdfasd dsaf asdf asdf asdf t");
	// write(sock, test_struct_message, sizeof(Message));
	// memset(test_struct_message, 0, sizeof(Message));

	// free(test_struct_message);
	Message* received_test_struct = malloc(sizeof(Message));
	do {
		//read_size = recv(sock , client_message , 2000 , 0);
		
		/* To dodałem */
		printf("Waiting for message\n");
		read_size = recv(sock, received_test_struct, sizeof(Message), 0);
		printf("Message read\n");
		printf("{ %f %f %s }", received_test_struct->x, received_test_struct->y, received_test_struct->message);
		printf("\n");
		for (int i =0; i <10;i++)
		printf("%c", received_test_struct->message[i]);

		printf("\n");
		/* --------- */ 
		client_message[read_size] = '\0';
		
		/* Send the message back to client */
		//write(sock , client_message , strlen(client_message));
		
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
		fprintf(stderr, "Connection accepted\n"); 
		pthread_create(&thread_id, NULL, connection_handler , (void *) &connfd);
	}
}

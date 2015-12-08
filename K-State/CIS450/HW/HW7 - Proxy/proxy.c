/*
Andy Gregoire
David Parker
Proxy Lab (HW7)

Unfinished
*/

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "csapp.h"

//Prototypes
void *thread(void *vargp);
void proxy_handler(int fd);
void parse_uri(char *uri, char *hostname, char *path, int *port);
struct hostent *gethostbyname_ts(char *hostname);
void cleanup(char *buf,char *buf2, char * method, char *request, char *uri, char *hostname, char *path);

// Thread lock 
pthread_rwlock_t lock;

//Mutex 
static sem_t mutex;

int main(int argc, char **argv)
{
	int listenfd, port;
	int *cfd;
	socklen_t clientlen = sizeof(struct sockaddr_in);
	struct sockaddr_in clientaddr;
	pthread_t tid;
	pthread_rwlock_init(&lock, 0);
	Sem_init(&mutex,0,1);

	/* Check command line args */
	if (argc != 2) 
	{
		fprintf(stderr, "usage: %s <port>\n", argv[0]);
		exit(1);
	}
	port = atoi(argv[1]);

	/* Ingore SIGPIPE */
	signal(SIGPIPE, SIG_IGN);
	listenfd = open_listenfd(port);

	while (1) 
	{
		cfd = malloc(sizeof(int));
		if(cfd == NULL)
			continue;
		*cfd = accept(listenfd, (SA *)&clientaddr, &clientlen);

		/* Create thread and let thread handle functions */
		if((*cfd > 0))
			Pthread_create(&tid, NULL, thread, cfd);
	}
	Free(cfd);
}

// Detachs new thread from main
void *thread(void *vargp)
{
	int connfd = *((int *) vargp);
	pthread_detach(pthread_self());
	Free(vargp);
	proxy_handler(connfd);
	close(connfd);
	return NULL;
}

// handle one request
void proxy_handler(int clientfd)
{
	int serverfd, port, contentLength, contentSize = 0,count = 0;
	char *buf = calloc(MAXLINE,1), *buf2 = calloc(MAXLINE,1),
	*method = calloc(MAXLINE,1), *uri = calloc(MAXLINE,1),
	*request = calloc(MAXLINE,1), *hostname = calloc(MAXLINE,1),
	*path = calloc(MAXLINE,1);
	char* content = NULL;
	rio_t server_rio;
	rio_t client_rio;

	// Read request line and headers
	rio_readinitb(&client_rio, clientfd);
	while(rio_readlineb(&client_rio, buf, MAXLINE) && strcmp(buf, "\r\n"))
	{
		//gets method and uri if first line
		if(count == 0)
		{
			sscanf(buf, "%s %s", method, uri);
			//parse_uri
			parse_uri(uri, hostname, path, &port);
			sprintf(buf, "%s %s HTTP/1.0\r\n", method, path);
			strcat(request, buf);
			count++;
		}
	}
	strcat(request, "\r\n");
	//GET
	if (strcasecmp(method, "GET")) 
	{
		cleanup(buf,buf2,method,request,uri,hostname,path);
		return;
	}	
	if((serverfd = open_clientfd(hostname, port)) == -1)
	{
		printf("Open Serverdf failed.\n");	
		cleanup(buf,buf2,method,request,uri,hostname,path);
		return;
	}
	rio_readinitb(&server_rio, serverfd); // serverfd 

	// Write request object via serverfd
	if(rio_writen(serverfd, request, strlen(request)) < 0)
	{
		printf("Write request failed\n");
		close(serverfd);
		cleanup(buf,buf2,method,request,uri,hostname,path);
		return;
	}

	// Read response from Server
	while((contentLength = rio_readnb(&server_rio, buf2, MAXLINE)) > 0){
		rio_writen(clientfd, buf2, contentLength);
		if((content = realloc(content, contentSize + contentLength*sizeof(char))) == NULL)
		{
			printf("Realloc failed\n");
			close(serverfd);
			cleanup(buf,buf2,method,request,uri,hostname,path);
			return;
		}
		memcpy(content + contentSize, buf2, contentLength);
		contentSize = contentSize + contentLength;
	}	

	// close connection to server
	if(rio_writen(serverfd, "close header\r\n", 15) < 0)
	{
		printf("Failed to write close request to server\n");
		close(serverfd);
		cleanup(buf,buf2,method,request,uri,hostname,path);
		return;
	}
	close(serverfd);
	cleanup(buf,buf2,method,request,uri,hostname,path);
	return;
}

//frees allocated objectes 
void cleanup(char *buf,char *buf2, char * method, char *request, char *uri, char *hostname, char *path)
{
	free(buf);
	free(buf2);
	free(method);
	free(request);
	free(uri);
	free(hostname);
	free(path);
}

/*
parse_uri - Uses function strpbrk to break up URI and extract the
port and path. strpbrk returns a pointer to the start of the
position of the string that contains the key. In this case, temp
will hold the last portion of the URI: ":[PORT]/path". Default case
of port is 80.
*/
void parse_uri(char *uri, char *hostname, char *path, int *port)
{	
	char *temp;
	*port = 0;
	strcpy(path, "/");
	if((temp = strpbrk(strpbrk(uri, ":") + 1, ":")))
	{
		sscanf(temp, "%d %s", port, path);
		sscanf(uri, "http://%[^:]s", hostname);
	} 
	else 
	{
		sscanf(uri, "http://%[^/]s/", hostname);
		sscanf(uri, "http://%*[^/]%s", path);
	}
	if((*port) == 0)
		*port = 80;
}

/*
Altered from csapp.c
Threadsafe
*/
struct hostent *gethostbyname_ts(char *hostname)
{
	struct hostent *hP, *hP2;
	  
	if((hP2 = malloc(sizeof(struct hostent))) == NULL)
		return NULL;

	P(&mutex);
	hP = gethostbyname(hostname);
	if(hP)
		*hP2 = *hP;	
	else 
		hP2 = NULL;
	V(&mutex);
	return hP2;
}

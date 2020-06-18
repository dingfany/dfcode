
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>

#include <sys/epoll.h>
#include <sys/inotify.h>

#include <dirent.h>
#include <string.h>
#include <limits.h>

#define EVENT_SIZE  ( sizeof (struct inotify_event) )
#define BUF_LEN     ( 1024 * ( EVENT_SIZE + 16 ) )

int g_fd = 0;

int readFileList(char *basePath)
{
    DIR *dir;
    struct dirent *ptr;
    char base[PATH_MAX];

    if ((dir = opendir(basePath)) == NULL)
    {
        perror("Open dir error...");
        exit(1);
    }

    while ((ptr = readdir(dir)) != NULL)
    {
        if (strcmp(ptr->d_name, ".") == 0 || strcmp(ptr->d_name, "..") == 0) ///current dir OR parrent dir
            continue;
        else if (ptr->d_type == 8)   ///file
            ;
        else if (ptr->d_type == 10)   ///link file
            ;
        else if (ptr->d_type == 4)   ///dir
        {
            memset(base, '\0', sizeof(base));
            strcpy(base, basePath);
            strcat(base, "/");
            strcat(base, ptr->d_name);
            printf("in dir %s\n", base);
			
            if(inotify_add_watch(g_fd, base, IN_MODIFY | IN_CREATE | IN_DELETE)<0)
			{
				perror("inotify_add_watch fail");
				//?return ?
			}
			
			//recursive
            readFileList(base);
        }
    }
    closedir(dir);
    return 1;
}

int main(int argc, char *argv[])
{
    int i, epfd, nfds;
    int wd;
    int length;

    char buffer[BUF_LEN];
    struct epoll_event ev, events[20];
    epfd = epoll_create(256);

    g_fd = inotify_init();
    
	if((wd = inotify_add_watch(g_fd, argv[1], IN_MODIFY | IN_CREATE | IN_DELETE))<0)
	{
		perror("inotify_add_watch fail");
		return -1;
	}
	
    readFileList(argv[1]);

    ev.data.fd = g_fd;
    ev.events = EPOLLIN | EPOLLET;

    epoll_ctl(epfd, EPOLL_CTL_ADD, g_fd, &ev);

    for (;;)
    {
        nfds = epoll_wait(epfd, events, 20, 500);

        for (i = 0; i < nfds; ++i)
        {
            if (events[i].data.fd == g_fd)

            {
                length = read(g_fd, buffer, BUF_LEN);

                if (length < 0)
                {
                    perror("read");
                }

                while (i < length)
                {
                    struct inotify_event *event =
                        (struct inotify_event *) &buffer[i];
                    if (event->len)
                    {
                        if (event->mask & IN_CREATE)
                        {
                            if (event->mask & IN_ISDIR)
                            {
                                printf("The directory %s was created.\n",
                                       event->name);
                            }
                            else
                            {
                                printf("The file %s was created.\n",
                                       event->name);
                            }
                        }
                        else if (event->mask & IN_DELETE)
                        {
                            if (event->mask & IN_ISDIR)
                            {
                                printf("The directory %s was deleted.\n",
                                       event->name);
                            }
                            else
                            {
                                printf("The file %s was deleted.\n",
                                       event->name);
                            }
                        }
                        else if (event->mask & IN_MODIFY)
                        {
                            if (event->mask & IN_ISDIR)
                            {
                                printf("The directory %s was modified.\n",
                                       event->name);
                            }
                            else
                            {
                                printf("The file %s was modified.\n",
                                       event->name);
                            }
                        }
                    }
                    i += EVENT_SIZE + event->len;
                }

            }


        }

    }



    return 0;
}





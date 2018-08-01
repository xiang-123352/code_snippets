#include <stdio.h>
#include <event.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <sys/inotify.h>

static void displayInotifyEvent(struct inotify_event *i)
{
  printf("    wd =%2d; ", i->wd);
  if (i->cookie > 0)
    printf("cookie =%4d; ", i->cookie);
  printf("mask = ");
  if (i->mask & IN_ACCESS)
    printf("IN_ACCESS ");
  if (i->mask & IN_ATTRIB)
    printf("IN_ATTRIB ");
  if (i->mask & IN_CLOSE_NOWRITE)
    printf("IN_CLOSE_NOWRITE ");
  if (i->mask & IN_CLOSE_WRITE)
    printf("IN_CLOSE_WRITE ");
  if (i->mask & IN_CREATE)
    printf("IN_CREATE ");
  if (i->mask & IN_DELETE)
    printf("IN_DELETE ");
  if (i->mask & IN_DELETE_SELF)
    printf("IN_DELETE_SELF ");
  if (i->mask & IN_IGNORED)
    printf("IN_IGNORED ");
  if (i->mask & IN_ISDIR)
    printf("IN_ISDIR ");
  if (i->mask & IN_MODIFY)
    printf("IN_MODIFY ");
  if (i->mask & IN_MOVE_SELF)
    printf("IN_MOVE_SELF ");
  if (i->mask & IN_MOVED_FROM)
    printf("IN_MOVED_FROM ");
  if (i->mask & IN_MOVED_TO)
    printf("IN_MOVED_TO ");
  if (i->mask & IN_OPEN)
    printf("IN_OPEN ");
  if (i->mask & IN_Q_OVERFLOW)
    printf("IN_Q_OVERFLOW ");
  if (i->mask & IN_UNMOUNT)
    printf("IN_UNMOUNT ");
  printf("\n");

  if (i->len > 0)
    printf("        name = %s\n", i->name);
}

#define BUF_LEN (10 * (sizeof(struct inotify_event) + NAME_MAX + 1))

static void readcb(struct bufferevent* bev, void* args)
{
  char buf[BUF_LEN];
  size_t numRead = bufferevent_read(bev, buf, BUF_LEN);
  char *p;
  for (p = buf; p < buf + numRead; ) {
    struct inotify_event *event = (struct inotify_event*) p;
    displayInotifyEvent(event);
    p += sizeof(struct inotify_event) + event->len;
  }
}

int main(int argc, char **argv)
{
  int inotifyFd, wd, j;
  if (argc < 2 || strcmp(argv[1], "--help") == 0) {
    fprintf(stderr, "%s pathname...\n", argv[0]);
    return 1;
  }
  inotifyFd = inotify_init();
  if (inotifyFd == -1) {
    fprintf(stderr, "inotify_init");
    return 1;
  }
  for (j = 1; j < argc; j++) {
    wd = inotify_add_watch(inotifyFd, argv[j], IN_ALL_EVENTS);
    if (wd == -1) {
      fprintf(stderr, "inotify_add_watch");
      return 1;
    }
    printf("Watching %s using wd %d\n", argv[j], wd);
  }
  struct event_base* event_base = event_base_new();
  struct bufferevent *tmp = bufferevent_socket_new(event_base, inotifyFd, 0);
  bufferevent_setcb(tmp, readcb, NULL, NULL, NULL);
  bufferevent_enable(tmp, EV_READ);
  event_base_dispatch(event_base);
  return 0;
}
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
/* Lean 4.19.0 queries its own executable using /proc/<PID>/exe.
   Use the host-supported /proc/self/exe alias only for that exact path. */
ssize_t readlink(const char *path, char *buf, size_t size) {
  static ssize_t (*original)(const char *, char *, size_t) = NULL;
  if (!original) original = dlsym(RTLD_NEXT, "readlink");
  char own_path[64];
  snprintf(own_path, sizeof own_path, "/proc/%ld/exe", (long)getpid());
  if (strcmp(path, own_path) == 0) path = "/proc/self/exe";
  return original(path, buf, size);
}

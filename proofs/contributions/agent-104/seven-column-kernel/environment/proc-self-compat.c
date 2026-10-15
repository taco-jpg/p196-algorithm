#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

/* Lean 4.19 queries its own executable via /proc/<pid>/exe.  This host
 * exposes the equivalent /proc/self/exe but denies numeric /proc paths.
 * Translate only the current process's exact executable symlink query.
 * Leave all other readlink requests and every returned byte unchanged. */
ssize_t readlink(const char *path, char *buffer, size_t capacity) {
    typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
    readlink_fn original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (original == NULL) {
        errno = ENOSYS;
        return -1;
    }
    char own_executable[64];
    snprintf(own_executable, sizeof own_executable, "/proc/%ld/exe", (long)getpid());
    if (strcmp(path, own_executable) == 0) {
        path = "/proc/self/exe";
    }
    return original(path, buffer, capacity);
}

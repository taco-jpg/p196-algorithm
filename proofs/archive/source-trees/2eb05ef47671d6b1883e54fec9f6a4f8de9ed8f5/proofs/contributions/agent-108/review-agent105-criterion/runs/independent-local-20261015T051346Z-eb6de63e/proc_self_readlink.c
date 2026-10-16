/*
 * Lean 4.19.0 compatibility adapter for a PID namespace whose /proc mount
 * belongs to an ancestor namespace. No Lean code or proof data is changed.
 * Only readlink("/proc/<getpid()>/exe", ...) is redirected to the equivalent
 * self-reference readlink("/proc/self/exe", ...). All other calls are delegated.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

typedef ssize_t (*readlink_fn)(const char *, char *, size_t);

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    readlink_fn next_readlink = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (next_readlink == NULL) {
        errno = ENOSYS;
        return -1;
    }
    char current_exe[64];
    int n = snprintf(current_exe, sizeof(current_exe), "/proc/%ld/exe",
                     (long)getpid());
    if (n > 0 && (size_t)n < sizeof(current_exe)
        && strcmp(path, current_exe) == 0) {
        return next_readlink("/proc/self/exe", buf, bufsiz);
    }
    return next_readlink(path, buf, bufsiz);
}
